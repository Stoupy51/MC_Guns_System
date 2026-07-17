---
name: datapack-optimization
description: Exhaustive Minecraft datapack performance guide — cost model, selector rules, NBT avoidance, execute/function structure, early returns, scheduling, advancements-as-events, load balancing, macros, entity choices, client-side costs (particles/sounds), and profiling with F3+L / Misode's report analyzer. Use when asked to optimize a datapack, reduce MSPT/tick lag, audit hot paths, review mcfunction code for performance, or explain why a command is slow. Generic and self-contained — exportable to any project by copying this folder.
---

# Minecraft Datapack Optimization

Two levers, in priority order:

1. **Run fewer commands per tick** — gate subsystems, schedule slower loops, return early, load-balance.
2. **Make each command cheaper** — selector hygiene, NBT avoidance, cheap-before-expensive ordering.

Everything below serves one of those two. Always think in terms of **hot paths**: code reachable
from `minecraft:tick`, self-rescheduling loops, per-entity dispatches, per-hit/per-shot callbacks,
ticking advancements/enchantments. A 10× improvement on a function that runs once per game start is
worthless; a 5% improvement on a function that runs 200×/tick is gold.

The budget: **50 ms per tick = 20 TPS**. MSPT (not TPS) is the number that matters — TPS is capped
at 20, MSPT is not. On shared servers or multi-system packs, your realistic budget is a small slice
of that (1–5 ms), because you are not the only thing running.

---

## 1. Profiling — measure before and after, always

- **F3 + L** (singleplayer): records a 10-second profile, drops a `.zip` in `debug/`. Drag it into
  **Misode's Report Analyzer** (https://misode.github.io/report/). Open the command tab to see
  per-function sub-trees.
- **Alt + F3**: live MSPT graph. Good for spotting spikes vs. flat load.
- **`/profile`** on servers (less detailed than F3+L).
- In the report, look at: **% of parent**, **% of total tick**, **ms**, and the **count** column.
  Absolute ms is hardware-dependent — reason in *relative* terms. One command at 80% of a subtree is
  your target. A huge count means a function is fanning out or looping far more than intended.
- Profile in realistic conditions (entity counts, player counts). An empty test world hides
  selector-scan costs that scale with the live entity list.
- Re-profile after each change. Optimizations have overhead; verify the graph actually improved
  (see §8 "When not to load balance").

---

## 2. Cost model — what is expensive and what is not

Cheap (use freely, even in hot paths):

| Operation | Notes |
|---|---|
| `scoreboard players set/add/operation` on fake players or `@s` | The cheapest state primitive in the game |
| `execute if score` | Cheapest condition — put it **first** |
| `tag @s add/remove`, `tag=` selector argument | Tags are the cheap entity-membership primitive |
| `@e[type=x,...]` | `type` with a concrete id is index-backed (class check) |
| `distance=`, `dx/dy/dz`, `limit=`, coordinates | Negligible; great pre-filters on large sets |
| `execute if block` / `if blocks` (small volume) | Cheap |
| `function` call | Small constant overhead; pays for itself past ~2–3 commands sharing a condition |
| `return` / `return run` / `return fail` | Free control flow — use aggressively |
| `if data storage` (existence/shallow match) | Storage checks are far cheaper than entity NBT |

Expensive (justify every use on a hot path):

| Operation | Why | Preferred alternative |
|---|---|---|
| **Player NBT reads/writes** (`data get entity @s`, `nbt=` on players, `SelectedItem`, `Inventory`) | Serializes the full player NBT tree per check — the single worst common offender | `execute if items entity @s <slot> <item>`, predicates, scoreboard criteria |
| `nbt=` selector argument (any entity) | Serializes each candidate's NBT then string-matches | Filter by `type`/`tag` first; tag-once pattern (§5); predicate |
| `clear @s item[component~{...}] N` / component-filtered `clear` | Scans + deep-matches the whole inventory; known multi-ms offender | `execute if items` to gate, then plain `clear`, or `item replace` on a known slot |
| `data modify entity` (esp. players — often blocked — and mobs) | Marks the entity dirty, forces re-save; on selectors it fans out | Work in `storage`, write back once; or components via `item replace`/`item modify` |
| Unbounded `@e` (no `type=`) | Walks the entire entity list | Always add positive `type=`; use `@a` for players |
| `sort=nearest/furthest/random` (`@p` implies nearest) | Extra distance sort over all matches | `sort=arbitrary` (default) + `limit=1` when "any one" is fine; `@n` only when you truly need nearest |
| `name=`, `advancements=` selector args | String/NBT-parser backed | Tags, scores |
| **Macro functions** (`$...` lines, `function ... with`) | Every call re-parses each macro line with the new arguments — no caching | Score-based branch trees for small domains; keep macros out of per-entity per-tick paths |
| Ticking advancements (`minecraft:tick` criterion) and ticking enchantment effects | More overhead than the equivalent tick-function line | Plain tick/schedule function |
| `execute store` into entity NBT | Entity NBT write, same as `data modify entity` | Store into a score or storage |

Selector argument order **matters**: arguments are evaluated left-to-right (with the exception that
a concrete `type=` is always hoisted first by the game). Put cheap filters before expensive ones:

```mcfunction
# BAD — deep-matches NBT of every entity, then checks the tag
kill @e[nbt={Busy:1b},tag=booth.target]
# GOOD — set narrowed by type+tag before the NBT match runs
kill @e[type=marker,tag=booth.target,nbt={Busy:1b}]
```

Canonical order: `type` → `tag` → `scores` → `distance`/`dx dy dz` → `gamemode`/`level` →
`name` → `advancements` → `predicate` → `nbt`.

Selector cheat-sheet: `@a` beats `@e[type=player]` (and also matches dead players, which `@e`
cannot); `@s` is free — never write `execute as @s`; `@p`/`@n` pay a distance sort — use
`@a[limit=1]` / `@e[type=x,limit=1]` when *any* match will do (e.g. existence checks, kills of a
uniquely-tagged entity).

---

## 3. Cheap check before expensive check

The single most repeatable win. Reorder `execute` so score/storage gates run before entity scans,
and entity scans before NBT:

```mcfunction
# BAD — scans all markers every tick even when the system is off
execute as @e[type=marker,tag=sys.node] if score #enabled sys matches 1 run function sys:node_tick
# GOOD — one score check short-circuits the whole scan
execute if score #enabled sys matches 1 as @e[type=marker,tag=sys.node] run function sys:node_tick
```

Apply the same idea at every scale:
- **Subsystem gates**: one `if score #game_active` / `if data storage ns:game {state:"active"}` at the
  top of a subsystem's tick entry point turns the whole subtree off for free.
- **Per-entity gates**: inside a dispatched function, check `@s` scores/tags before touching NBT.
- **Population gates**: maintain a counter (`#armed_count`) when entities are created/destroyed and
  gate the scan behind `if score #armed_count matches 1..` — zero scans while the population is empty.

`as @e[scores={x=1..}]` vs `as @e if score @s x matches 1..`: measured difference is negligible.
Choose whichever lets you order the *rest* of the arguments better; don't micro-optimize this.

**Beware selector-on-selector fan-out** — `execute` sub-commands multiply:

```mcfunction
# N markers × M armor stands = N*M executions of `say hi` AND of the @e scan itself
execute as @e[type=marker] at @e[type=armor_stand] run say hi
```

If you see two selectors on one `execute` line, ask whether the cross-product is intended. It
almost never is.

---

## 4. Early returns and branch structure

`return`, `return run`, `return fail` (1.20.2+) are free and transform hot-path cost:

```mcfunction
# BAD — every line's condition is evaluated even after one matched
execute if score @s st matches 1 run function a
execute if score @s st matches 2 run function b
execute if score @s st matches 3 run function c
# GOOD — first match exits; average evaluations halved
execute if score @s st matches 1 run return run function a
execute if score @s st matches 2 run return run function b
execute if score @s st matches 3 run return run function c
```

- **Guard clauses first**: open hot functions with the cheapest disqualifiers —
  `execute unless score ... run return 0` — so the common "nothing to do" case costs 1–2 score checks.
- **Implicit else**: `if X run A` + `unless X run B` evaluates X twice. Rewrite as
  `if X run return run A` then unconditional `B`. This matters enormously when X is an `@e` scan.
- **Reuse answers instead of re-asking**: if a command already tells you whether it did something,
  capture that with `execute store success/result score` rather than re-scanning:

```mcfunction
# BAD — the second line re-scans all entities to ask "did line 1 tag anything?"
tag @e[type=marker,tag=spawn,tag=!used] add candidate
execute unless entity @e[type=marker,tag=candidate] run <fallback>
# GOOD — line 1 already knew the answer
execute store success score #found ns.data run tag @e[type=marker,tag=spawn,tag=!used] add candidate
execute if score #found ns.data matches 0 run <fallback>
```

- **Large integer dispatch** (ids, 100+ cases): use a binary search tree of functions
  (`if score ... matches 0..127 run function tree/lo`, halving each level) — O(log n) score checks
  instead of n. For *small* domains a flat `return run` chain is simpler and fine.

---

## 5. Avoiding NBT

### Items — never touch player inventory NBT directly
Modern replacements, in order of preference:

```mcfunction
# held-item check
execute if items entity @s weapon.mainhand minecraft:stick run ...
# component / custom-data match
execute if items entity @s weapon.mainhand *[custom_data~{mypack:{gun:true}}] run ...
# whole-inventory check
execute if items entity @s container.* *[custom_data~{mypack:{key:1b}}] run ...
# move/copy without touching NBT
item replace entity @s hotbar.0 from entity @n[type=item_display,tag=x,distance=..3] contents
```

`if items` walks only the requested slots and matches components natively — no full-player
serialization. Predicates (`minecraft:entity_properties` → `equipment`) are equally good and can be
embedded in selectors. The expensive `clear @s x[component~{...}] 1` should be gated:
`execute if items entity @s container.* <spec> run clear ...` — or avoided via `item replace` when
the slot is known.

### Item entities — predicate instead of nbt
```mcfunction
# BAD
execute as @e[type=item,nbt={Item:{id:"minecraft:stick"}}] run ...
# GOOD
execute as @e[type=item,predicate=mypack:is_stick] run ...
```

### The tag-once pattern — convert repeated NBT checks into one check + a tag
For entities whose NBT-derived classification is stable, check NBT **once per entity lifetime**,
then select by tag forever after:

```mcfunction
# tick — only unclassified entities ever face the NBT check
execute as @e[type=item,tag=!seen] run function mypack:classify
execute as @e[type=item,tag=custom] at @s run particle ...
# classify (as @s):
tag @s add seen
execute if data entity @s Item.components."minecraft:custom_data".mypack run tag @s add custom
```

### Storage over entity NBT
`data` on **storage** doesn't dirty an entity and is markedly cheaper. Pattern: copy the blob you
need into storage once, do all reads/edits there, write back once (or never, if storage *is* the
source of truth). Prefer storage as the primary home for system state; keep scoreboards for anything
numeric or condition-checked.

### Scoreboard criteria over scanning
`deathCount`, `minecraft.custom:minecraft.jump`, `minecraft.killed:...`, `minecraft.used:...` etc.
update automatically at zero datapack cost. Checking `if score @s deaths matches 1..` beats any
death-detection scan. Reset after consuming.

---

## 6. Function structure

`function` keeps full context, so it converts *n* evaluations of a selector/condition into one:

```mcfunction
# BAD — 4 identical scans
execute as @e[type=item,tag=a,nbt={x:1b}] run cmd1
execute as @e[type=item,tag=a,nbt={x:1b}] run cmd2
...
# GOOD — 1 scan, context preserved for the whole body
execute as @e[type=item,tag=a,nbt={x:1b}] run function mypack:item_work
```

Threshold: for 1–2 trivial commands behind a *cheap* condition, the function-call overhead can
exceed the saving — inline those. For expensive conditions or 3+ commands, always extract.

More structure rules:
- Repeating the same selector many times in one function is a smell — dispatch once.
- Minimize context changes: `at @s` re-anchors position; only add it when the body uses position.
- **Macros**: every invocation re-parses the macro lines with the new arguments. Fine for rare
  events (UI clicks, setup); wrong for per-entity per-tick work. When the argument domain is small,
  replace with a score-branch (`if score` chain / tree) or pre-generated per-value functions.
- `schedule function` for anything that doesn't need 20 Hz (see §7); use `append` deliberately —
  default `replace` silently cancels a pending schedule of the same function.

---

## 7. Run code only when needed

### Tick function discipline
`minecraft:tick` entries should be a short list of gated dispatchers, nothing else. Most datapack
lag is tick functions doing per-tick work that has no per-tick requirement.

### Schedule loops — slower cadences
```mcfunction
# load.mcfunction
function mypack:loop_2t
# loop_2t.mcfunction
<work>
schedule function mypack:loop_2t 2t
```
Splitting work across cadences (1t for movement-critical, 2t–5t for AI, 10t–20t for displays and
cleanup) routinely halves total command load. Display/scoreboard-UI values tolerate a full second
of staleness. Caveat: naive scheduling causes **spikes** (all work lands on the same tick) — if the
per-run cost is high, load-balance instead (§8).

### Advancements as events
Advancement triggers (`player_killed_entity`, `inventory_changed`, `player_hurt_entity`,
`consume_item`, `placed_block`, ...) run their reward function **only when the event happens**, as
the player, replacing polling entirely:

```json
{ "criteria": { "req": { "trigger": "minecraft:player_killed_entity",
    "conditions": { "entity": { "type": "minecraft:zombie" } } } },
  "rewards": { "function": "mypack:on_zombie_kill" } }
```
```mcfunction
# on_zombie_kill — @s = the player
<work>
advancement revoke @s only mypack:on_zombie_kill_trigger
```
Exception: the `minecraft:tick` criterion is **not** an optimization — it's a slower tick function.
Same for ticking enchantment effects: prefer plain functions.

### Event-driven beats polled — generally
`trigger` objectives for player-initiated actions, `deathCount` for deaths, interaction entities'
`#bs.interaction`-style right-click callbacks (or vanilla `interaction` + advancement) for clicks —
each replaces a per-tick per-player scan with code that runs on demand.

---

## 8. Load balancing — flatten spikes

When one operation over N entities is too heavy for a single tick even at a slow cadence, split the
population into K groups and process one group per tick (each entity still gets serviced every K
ticks, but the graph is flat instead of spiky):

```mcfunction
# tick
execute as @e[type=zombie,tag=sys.mob,tag=!sys.grouped] run function sys:assign_group
scoreboard players add .cur sys.lb 1
scoreboard players operation .cur sys.lb %= .count sys.lb
execute if score .cur sys.lb matches 0 as @e[type=zombie,tag=sys.g0] run function sys:heavy_check
execute if score .cur sys.lb matches 1 as @e[type=zombie,tag=sys.g1] run function sys:heavy_check
...
# assign_group — round-robin a group tag onto @s, then tag @s add sys.grouped
```

Use **tags**, not scores, for group membership (cheaper to select; per-entity scores on despawning
entities are also historically bug-prone). Other shapes of the same idea: process a bounded number
of queue entries per tick; split large block-volume edits into slices across ticks; interleave two
2t schedules doing different halves.

**When not to**: the grouping machinery is overhead. If the balanced version's *max* MSPT isn't
lower than the unbalanced one, revert it. And avoid randomness (`if predicate <random 20%>`) as a
load-balancer — the average is right but the variance produces random spikes and uncontrollable
per-entity intervals.

---

## 9. Entities: choose and count them carefully

- **`marker`** for logic points: no ticking, no rendering, no collisions — near-zero cost. Prefer it
  over armor stands and AECs for any invisible logic entity.
- **Display entities** (`item_display`/`block_display`/`text_display`) for visuals: no AI/physics.
  Still entities — they inflate every `@e` scan, so always give them a `type=`-selectable role tag.
- Kill temp/helper entities the same tick you spawn them; leaked helpers permanently grow the
  entity list that every unindexed scan walks.
- Item entities with big custom components are heavy to scan — set `PickupDelay`/`Age` and clean up.
- Every summon has a per-tick baseline cost; the cheapest entity is the one you didn't spawn
  (raycast with `positioned ^ ^ ^0.5` recursion or a library instead of projectile entities, when
  feasible).

---

## 10. Client-facing costs (server → client spam)

- **`particle` needs a viewer filter**: end with `@a[distance=..48]` (or a relevant tag). Unfiltered
  particles are sent to everyone, and with many emitters this measurably costs both server send time
  and client FPS. Use `force` sparingly (it bypasses the client's particle-reduction setting).
- **`playsound` needs targets**: `playsound ... @a[distance=..24]`, never bare/`@a` for local
  effects.
- `tellraw @a` with per-player `selector`/`score` components re-resolves per recipient — fine for
  events, not for per-tick HUDs (use `title`/actionbar/scoreboard displays at a slow cadence, or
  1.20.3+ `scoreboard ... display name/numberformat` styling).

---

## 11. Review checklist

Auditing a pack (or your own diff), in order:

1. **Map hot paths**: `tick.json` → every reachable function; all `schedule` loops; per-entity
   dispatches; event callbacks that fire per-hit/per-shot. Rank by frequency × population.
2. **Gates**: does every subsystem tick start with a cheap score/storage gate? Population counters
   before scans?
3. **Selectors**: positive `type=` on every `@e`/`@n`; argument order cheap→expensive; no stray
   `sort`/`@p` where `limit=1` suffices; no selector-on-selector cross products.
4. **NBT**: zero `nbt=` on players; `if items`/predicates for item checks; component-`clear` gated
   or replaced; repeated entity-NBT checks converted to tag-once; state living in storage/scores.
5. **Control flow**: guard clauses + `return` at the top; `return run` chains instead of full
   if-lists; if/unless pairs collapsed; `store success` reuse instead of re-scans; repeated
   selectors folded into one `function` dispatch.
6. **Cadence**: anything in tick that tolerates 2t–20t moved to schedule loops; polling replaced by
   advancements/`trigger`/criteria where an event exists.
7. **Spikes**: heavy periodic jobs load-balanced (or consciously not, with a measurement).
8. **Entities**: markers for logic, role tags on displays, no leaked helpers.
9. **Client**: particles/playsound/tellraw filtered.
10. **Measure**: F3+L before/after; compare max MSPT and the offending subtree's share, not just
    averages. Keep the change only if the profile agrees.

Correctness outranks all of this: repeated scans are sometimes intentional because membership
changes mid-function (tags added, entities killed/summoned between two checks). Before merging or
caching a scan, verify nothing in between mutates the relevant set — if uncertain, report the
opportunity instead of rewriting.
