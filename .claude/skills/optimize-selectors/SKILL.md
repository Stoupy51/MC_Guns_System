---
name: optimize-selectors
description: Performance-audit this Minecraft datapack to reduce expensive entity-selector evaluations (@e, if/unless entity, @e[tag=/nbt=/scores=/distance=]). Use when asked to optimize selectors, speed up tick lag, review hot paths, or replace global entity scans with success-based flow / shared dispatch helpers. Covers the StewBeet/beet Python→mcfunction layout, the cost model, the safe refactor catalog, correctness rules, and how to verify with `beet build`.
---

# Selector Optimization Review

Goal: cut the number of **entity-selector evaluations per tick** while preserving behavior exactly.
`@e[...]`, `if entity @e`, `unless entity @e`, `@e[nbt=]`, `@e[scores=]`, `@e[distance=]`, and
`@e[predicate=]` are **full, unindexed scans** of the live entity list. `@e[type=x]` is type-indexed
and comparatively cheap. A scan on a tick path that iterates a 50–256 zombie horde, or runs once per
bullet hit, dwarfs one that runs rarely.

## How this project is built

- Gameplay logic is **Python** under [src/functional/](../../../src/functional/) that *emits* mcfunction
  strings via `write_versioned_function("path", "...")`, `write_tick_file(...)`, `write_load_file(...)`,
  and the `GameMode` helpers `self.func("path", ...)` / `self.tick(...)` / `self.load(...)`.
- `{ns}` = `mgs` (project id), `{version}` from `beet.yml`. Functions live at
  `mgs:v{version}/<path>`. The objective is `{ns}.data`; scratch holders are fake players like
  `#zb_alive {ns}.data`.
- `based_of/` is the **external gun mod** this is built on — do not optimize it; focus on `src/`.
- Build with `beet build` (output under `build/datapack/data/mgs/function/...`). A successful run
  ends with `Done!`.

## Tick hot paths (audit these first, in order)

1. `minecraft:tick` → emitted in [src/functional/main.py](../../../src/functional/main.py):
   `execute as @e[type=player,sort=random] at @s run function .../player/tick`.
2. Mob AI: [src/functional/mob_ai.py](../../../src/functional/mob_ai.py) tick — already gated behind
   `if score #armed_mob_count {ns}.data matches 1..` before `as @e[tag={ns}.armed]`.
3. Zombies: `zombies/game_tick` (gated `if data storage {ns}:zombies game{state:"active"}`) in
   [src/functional/zombies/game.py](../../../src/functional/zombies/game.py) and
   [round.py](../../../src/functional/zombies/round.py). The hottest population is `@e[tag={ns}.zombie_round]`.
4. Multiplayer: `multiplayer/game_tick` in [src/functional/multiplayer/game.py](../../../src/functional/multiplayer/game.py).
5. Missions: `missions/game_tick` in [src/functional/missions/game.py](../../../src/functional/missions/game.py).

A `game_tick` is often **assembled from several `self.func("<mode>/game_tick", ...)` calls** that append
sections (e.g. zombies appends kill-points and death-watch/horde). When reasoning about whether a score
is "fresh," remember the main body runs first and appended sections run after.

## Refactor catalog (each entry: when → how → why-correct)

### 1. Success-based flow — the highest-yield pattern
Look for `(if|unless) entity @e[...]` whose ONLY job is to answer *"did the previous command find/tag
anything?"* The previous command already produced that answer.

- **Single command** (no `as @a` loop): capture it directly.
  ```mcfunction
  # before
  tag @e[tag=spawn_point,...,!spawn_used] add spawn_candidate
  execute unless entity @e[tag=spawn_candidate] run tag @e[...] add spawn_candidate
  # after
  execute store success score #has_candidate {ns}.data run tag @e[tag=spawn_point,...,!spawn_used] add spawn_candidate
  execute if score #has_candidate {ns}.data matches 0 run tag @e[...] add spawn_candidate
  ```
  `store success` of `tag add` = 1 iff ≥1 entity was **newly** tagged; `store result` = the count newly
  tagged. Valid because the temp tag is cleared each call, so "an entity has the tag" ⟺ "this call tagged it."

- **`execute as @a[...] run tag @e[...]` loop**: `store` keeps only the *last* iteration, so you can't
  aggregate on the execute line. Dispatch a **per-player subfunction** that ORs each player's local
  result into a global score:
  ```mcfunction
  scoreboard players set #found {ns}.data 0
  execute as @a[...] at @s run function {ns}:v{version}/.../tag_pass   # subfunction below
  execute if score #found {ns}.data matches 0 ... run <fallback>
  # tag_pass:
  execute store result score #hit {ns}.data run tag @e[...] add X
  scoreboard players operation #found {ns}.data += #hit {ns}.data
  ```
  This is the legitimate reason to create a subfunction — it makes the success value survive the loop.

- **Post-filter emptiness** (a removal pass runs between the tag and the check): initial success isn't
  enough. `store result` the initial count, then **decrement the counter inside the removal loop's
  subfunction** (1:1 with each removal), and gate on `if score #count matches 0`. See
  `multiplayer/uncontest_spawn`.

- **`execute as @r[...,limit=1]`** runs at most once: `store success` works, but **initialize the score
  to 0 first** — if the selector matches nobody the body never runs and `store` never writes.

### 2. Reuse a value already computed this tick instead of rescanning
If `game_tick` already counted/located a population, downstream functions should read that score, not
rescan. Example: `refresh_sidebar` was doing `store result ... if entity @e[tag=zombie_round]` on every
bullet hit and kill; it now reuses `#zb_alive` that `game_tick` recomputes once per tick. Guard the
non-tick callers (prep/start) by seeding the score themselves. Display-only values tolerate ≤1 tick of
staleness — exploit that.

### 3. Replace a redundant existence check with the cached count
`if entity @e[tag=X]` immediately after `store result #n ... if entity @e[tag=X]` (same population, no
membership change between) → `if score #n matches 1..`.

### 4. Merge duplicate scans over one population into a single dispatch
Several `execute as @e[tag=X] ...` / `if entity @e[tag=X]` over the *same* set in one tick → one
`as @e[tag=X] at @s run function tick_X` that does all per-entity work (and accumulates the count via a
per-entity `scoreboard add`). Watch gating differences (some lines run every N ticks or only under a flag).

### 5. Common-parent consolidation
`@e[tag=melee]`, `@e[tag=ranged]`, `@e[tag=boss]` over disjoint sets → tag them all `enemy`, iterate
`@e[tag=enemy]` once, branch inside. Only when it reduces total scan work without ballooning command count.

### 6. Shared helper when a selection pattern repeats — **mcfunction first**
If the same multi-line selection logic appears in 2+ places (e.g. the zombies 32→64→any-unlocked
spawn-proximity tagger used by both round spawning and stuck rescue), extract ONE mcfunction
(`zombies/tag_spawns_near_players`) and have callers `function` it. Reach for a **Python helper only if
mcfunction can't express the reuse** (e.g. it needs to vary structurally per call site). Design shared
helpers so callers never need their own scan — e.g. leave a `#..._found` score set such that
`#found == 0 ⟺ the output tag is empty` (use `store success` on the fallback so it reflects every branch).

### 7. Early-exit with `return run` instead of a complementary condition
When code does `if <cond> run A` then `unless <cond> run B` (or otherwise re-tests the same thing to
pick the "else" branch), and `<cond>` is an expensive `if entity @e[...]`/score test, collapse it: run
the first branch with `return run` so it exits the function, and let B fall through as the implicit else.
```mcfunction
# before — evaluates the @e scan twice (if + unless)
execute if entity @e[tag=nuked] run schedule function .../nuke_loop 1t
execute unless entity @e[tag=nuked] run tag @a[tag=nuke_activator] remove nuke_activator
# after — one scan, `return run` makes the cleanup line the else
execute if entity @e[tag=nuked] run return run schedule function .../nuke_loop 1t
tag @a[tag=nuke_activator] remove nuke_activator
```
This drops the second condition evaluation entirely (here a full entity scan) and needs no scratch
score. It only works when the first branch is the last thing that should happen on that path — i.e.
returning early is safe because nothing after it must still run in the "true" case. Combine with the
success-flow rewrites above (e.g. `... run return run` on a `store`-gated branch) wherever the "true"
case ends the function.

### 8. Fold a dynamic id/score match into the selector with a `predicate`
When code selects a population by tag and then filters to the ONE entity whose score matches a dynamic
value — `as @e[tag=X] if score @s <obj> = #ref <data>` — repeated many times for the same entity, build
a `minecraft:entity_scores` predicate that compares the entity's own score against the reference score
(via a `minecraft:score` provider with a `minecraft:fixed` fake-player target), and put it in the
selector: `@e[tag=X,predicate=ns:.../id_match]`. The id test is then evaluated inline during selection,
in one pass, and the selector can be used directly with `@n[...]`/`@e[...]` anywhere.
```python
# Python (StewBeet): reference = the fake player #my_id on objective ns.data
id_ref = {"type": "minecraft:score", "target": {"type": "minecraft:fixed", "name": "#my_id"}, "score": f"{ns}.data"}
Mem.ctx.data[ns].predicates[f"v{version}/.../id_match"] = set_json_encoder(Predicate({
    "condition": "minecraft:entity_scores", "entity": "this",
    "scores": {f"{ns}.<obj>": {"min": id_ref, "max": id_ref}},
}), max_level=-1)
```
```mcfunction
# before (per command):  as @e[tag=X] if score @s ns.<obj> = #my_id ns.data run ...
# after:                 as @e[tag=X,predicate=ns:.../id_match] run ...
```
Set `#my_id` before the selector runs (the predicate reads it at evaluation time). Existing examples:
`zombies/traps/turret_id_match` and `zombies/revive/downed_id_match`. This pairs naturally with #4/#6:
once the match is a predicate, `tag` the one entity once and dispatch all its work via a single
`execute as @e[tag=X,predicate=P] ... run function` instead of re-selecting it per command.

## Correctness rules (false optimizations are worse than missed ones)

Repeated selectors are sometimes intentional because membership changes mid-execution. Before merging or
removing a scan, verify nothing between the two points changes the relevant set:
- tags added/removed, scores changed, team/dimension changes;
- entities summoned/killed/teleported (a `bounds_kill`/rescue between two player checks can change who
  matches — this blocks naive merging of the two `multiplayer/game_tick` player passes unless re-guarded);
- temp-tag cleanliness: success-based rewrites assume the temp tag is empty on entry — confirm every
  caller clears it after consuming it, and don't add a clearing scan to a hot path to "be safe."
If correctness is uncertain, report the opportunity + risk and do **not** rewrite.

## Workflow

1. `grep` the functional source for `@e\[`, `if entity @e`, `unless entity @e`, and per-tick `as @a`/`as @e`.
2. Trace tick reachability; rank by (population size × frequency).
3. Apply the catalog above, hottest first.
4. For each change, be ready to state: original, # of selector evals, on a tick path?, optimized form,
   why behavior is unchanged, benefit (High/Medium/Low).
5. Verify:
   - `python -c "import ast; ast.parse(open(PATH, encoding='utf-8').read())"` on each edited file
     (these sources are UTF-8 with emoji — always pass `encoding='utf-8'`).
   - `beet build` ends with `Done!`.
   - Spot-check the emitted `build/datapack/data/mgs/function/.../*.mcfunction`.

## Already done (don't redo; extend the pattern)
Success-flow applied to `zombies/spawn_zombie`, `zombies/pick_spawn`, `missions/pick_spawn`,
`zombies/revive/respawn_near_player`, `zombies/on_stuck_zombie`, `multiplayer/pick_spawn`;
`refresh_sidebar`/glow reuse `#zb_alive`; shared helper `zombies/tag_spawns_near_players`.
