# Implementation Plan: XP Advancements

**Branch**: `007-xp-advancements` | **Date**: 2026-08-15 | **Spec**: [spec.md](spec.md)

## Summary

One MGS tab in the Advancement screen, rooting into three branches (Multiplayer, Missions, Zombies),
holding 16 chains and 3 event challenges, each paying XP into the progression system that already exists.

Two observations carry the design:

**Vanilla does the evaluation.** A threshold tier is a `minecraft:tick` criterion with a
`minecraft:entity_scores` condition on the counter. It unlocks the instant the score qualifies, with no
command, no polling function and no `advancement grant`. That deletes an entire layer a command-driven
version would need (a next-threshold companion score per stat, an unlock ladder per chain, an admin
resync after every retune) and drops the per-event cost to the single command that moves the counter.
Retuning becomes self-healing: lower a threshold, reload, and everyone who already qualifies unlocks on
the next tick, including players who were offline.

**The award functions are the funnel.** Every XP award already passes through a generated
`progression/{side}/award_{key}` running as the earning player, so lifetime counters are fed from inside
those functions without touching one of the thirty-odd award sites scattered across gamemodes, machines,
traps and barricades. Fifteen of the 31 award functions gain exactly one line.

`advancement grant` survives only for the three challenges a score genuinely cannot express (finish
without dying, reach round 20 alone). Those use `minecraft:impossible` and one guarded command at the
site that already detects the moment.

The decision that cannot be got wrong: advancement ids are **unversioned**. An advancement is state in
the player's world, so a `v<version>` segment would wipe every unlock on every pack update, and vanilla
would then re-evaluate the fresh ids against the counters and pay the whole catalog out again. Reward
functions stay versioned like every other function.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction and advancement JSON through StewBeet

**Primary Dependencies**: beet + StewBeet (`Advancement`, `set_json_encoder`, `write_versioned_function`,
`write_load_file`, `write_tag`)

**Storage**: 14 new `dummy` scoreboard objectives, 2 existing objectives read directly (`mgs.mp.xp_level`,
`mgs.zb.xp_level`), plus vanilla per-player advancement state under `mgs:challenges/`

**Testing**: In-game, per Constitution V. Counters are plain scoreboards, so every threshold is reachable
with one `/scoreboard` command instead of by playing to it. See [quickstart.md](quickstart.md)

**Target Platform**: Minecraft Java 26.2 (`beet.yml`), with the JSON shapes checked against the game
source bundled in `minecraft_source_code/`

**Project Type**: Minecraft datapack generated from a Python build pipeline

**Performance Goals**: One command per award event, on 15 of 31 award functions. Zero new pack functions
running per tick, zero new entity selectors, zero NBT reads

**Constraints**: No unlock lost to a pack update; no admin step after a retune; the tab count stays at one

**Scale/Scope**: 60 advancement files, 16 chains, 3 event challenges, one new package of roughly seven
modules, three small edits to existing progression files and three one-line inserts at event sites

## Constitution Check

*GATE: passed, before and after Phase 1 design.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | Every advancement JSON is emitted by the generator from the catalog. Nothing under `build/` is authored, and no advancement is committed as a source file. |
| II. Data-driven definitions | The feature is `Branch` / `Stat` / `Chain` / `Tier` / `EventChallenge` dataclasses in one catalog, written as explicit keyword-argument constructor calls, one per row. Thresholds, payouts, titles, icons and frames are values. The tree, the criteria, the reward functions, the counter lines and the objective declarations are one parameterised implementation over that table. |
| III. Typed, linted, readable | New package under `progression/advancements/`, split by feature so no file approaches 300 lines. Everything public, tabs for indent, `@staticmethod` helpers grouped in classes, pyright strict and `ruff check src --fix`. |
| IV. Runtime cost is a design constraint | Budgeted and stated below, including the part that is not free. |
| V. In-game verification | [quickstart.md](quickstart.md) is the check list, and it covers the two properties the design rests on: that a version bump preserves unlocks, and that a retune self-heals with no command run. |

### What this costs, stated rather than implied

Constitution IV asks for the cost of any feature that adds per-tick work, and this one does, just not on
the pack's side.

- **Pack side**: one `scoreboard players` command inside 15 of the 31 generated award functions, plus
  three small hooks that run once per mission victory and once per Zombies round. No new function runs
  per tick. This is strictly cheaper than the command-driven alternative, which needed a second
  comparison per award event on top of the same counter line.
- **Vanilla side**: a `tick` criterion is real per-player, per-tick work on the server thread. It is a
  hash lookup and an integer compare in native code, not a command dispatch, and vanilla unregisters a
  criterion as soon as it completes, so the cost decays to zero as a player finishes the tree. Worst case
  is a brand new player with 56 live criteria, which is still orders of magnitude below one `@e` scan.
- **Objectives**: 14 new dummy objectives. They cost nothing per tick and live in `level.dat` forever.
  They sit under a fresh `mgs.adv.` prefix so they are recognisable and never caught by a per-match wipe.
  The two `level` chains read `mgs.*.xp_level` directly instead of mirroring it, which is 2 objectives and
  2 hooks that do not exist.

### Deliberate deviation worth recording

`Curve.write_award_functions` gains a parameter. It takes a generic "extra lines per award key" dict, not
an advancements concept, so `curve.py` keeps knowing nothing about challenges and the dependency stays
one-way. The alternative was importing the catalog into `curve.py`, which would have made the progression
package circular.

## Project Structure

### Documentation (this feature)

```text
specs/007-xp-advancements/
├── spec.md
├── plan.md              # This file
├── research.md          # Phase 0: twelve decisions, schema checked against the bundled game source
├── data-model.md        # Phase 1: dataclasses, invariants, the full catalog
├── quickstart.md        # Phase 1: the in-game validation run
├── contracts/
│   └── interfaces.md    # Phase 1: stable ids, JSON shapes, objectives, extension point
└── tasks.md             # Phase 2 output (/speckit-tasks, NOT created here)
```

### Source Code (repository root)

```text
src/functional/progression/
├── __init__.py                      # Wire in: objectives, generate_advancements()
├── awards.py                        # One `challenge` row per XP pool, scaled=True
├── curve.py                         # write_award_functions gains the per-award extra-lines dict
└── advancements/                    # New package
    ├── __init__.py                  # generate_advancements(), Advancements.stat_lines / .grant
    ├── model.py                     # Branch, StatKind, Stat, Tier, Chain, EventChallenge
    ├── catalog/
    │   ├── __init__.py              # BRANCHES, CHAINS, EVENTS, lookups, invariant asserts
    │   ├── multiplayer.py           # 5 chains, 1 event, 18 advancements
    │   ├── missions.py              # 2 chains, 1 event, 7 advancements
    │   └── zombies.py               # 9 chains, 1 event, 31 advancements
    ├── tree.py                      # The advancement JSON: root, branch roots, criteria, parenting
    ├── rewards.py                   # Per-tier reward function, the message, the on_challenge_unlock signal
    └── hooks.py                     # The three non-award feeds: on_round_end, missions/victory, on_game_end
```

**Structure Decision**: A new package under `progression/`, not a new top-level system. Challenges are a
view onto progression state and pay progression XP, so they belong with the curve and the awards rather
than beside them. The catalog is a subpackage because 56 explicit constructor calls plus their notes will
not fit in one file under the 300-line rule, and splitting it by branch is the grouping that matches how
it is read and retuned.

## Implementation Order

Phased so each phase leaves the pack in a working state, and so the assumption everything rests on gets
proven in phase 3 rather than at the end.

1. **Model and catalog.** `model.py` plus `catalog/`, with the invariant asserts. Nothing is generated
   yet, so a build failure here is a pure data error and easy to read.
2. **The tree.** `tree.py`: the root, the three branch roots, every tier's criteria and parenting, with
   no counters and no payouts. Objectives are declared so the criteria reference something real. This
   alone delivers User Story 2 and is testable by opening the Advancement screen: the tab exists, the
   branches hang off it, and nothing unlocks because every counter is zero.
3. **One chain end to end.** The counter line inside `award_kill`, the reward function, the message, the
   signal. Zombies `kills` is the right one: it is the `COUNT_SCORE` case, so the hardest shape gets
   proven first rather than last. This is where the design is confirmed or sent back, because it is the
   first time a criterion actually fires. Delivers User Story 1.
4. **The remaining chains.** Pure table work once step 3 is generic, plus `hooks.py` for `best_round` and
   the two Missions counters, and the `level` chains which need no feed at all.
5. **The event challenges.** `Advancements.grant` and the three one-line inserts. Delivers User Story 3.
6. **Retune pass.** Change a threshold, rebuild, reload, confirm nothing was run by hand. Delivers User
   Story 4, and is the check that no admin function quietly became necessary.
7. **README.** The root feature matrix, and the `zombies/README.md` inbox line this feature came from,
   which stops being an inbox item here.

## Risks

| Risk | Handling |
|---|---|
| `conditions.player` shape wrong for this version | It is `Optional<Holder<LootItemCondition>>`, a single inline condition or a predicate reference, not the pre-1.20 list. Taken from [PlayerTrigger.java:28](../../minecraft_source_code/net/minecraft/advancements/triggers/PlayerTrigger.java#L28); phase 2 fails loudly and immediately if it is wrong, which is why the tree lands before any counter does |
| 56 tick criteria per new player costs more than expected | Measured in phase 3 with F3+L before the catalog is complete, so the answer arrives while the catalog is still cheap to shrink |
| A future per-match wipe clears `mgs.adv.*` | The wipes clear by explicit objective name today. The `mgs.adv.` prefix and the contract in [interfaces.md](contracts/interfaces.md) are what keep it that way |
| An operator revoke re-pays a challenge | Accepted and documented. It is the same re-evaluation that makes retuning self-healing, and fighting it would mean reintroducing the paid-state scores the design just removed |
| Titles not picked up by the lang plugin | `auto.lang_file` walks `ctx.data.all()`, which includes advancements. Verified in the quickstart by reading the generated `en_us.json` |

## Complexity Tracking

No constitutional violations to justify. The costs worth stating are already above: 14 new objectives, one
new parameter on `Curve.write_award_functions`, and per-tick criteria evaluation on the vanilla side. All
three were weighed against the command-driven alternative, which was worse on every axis the constitution
cares about: more generated functions, more per-event commands, more persistent state that can desync, and
an admin step after every retune.
