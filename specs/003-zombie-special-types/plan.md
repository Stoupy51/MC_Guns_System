# Implementation Plan: Zombie Special Types

**Branch**: `003-zombie-special-types` | **Date**: 2026-08-15 | **Spec**: [spec.md](spec.md)

## Summary

Fill in the three stub type functions in `enemies.py`, add a fourth (`aura`), and replace the
hardcoded `_zpos.type = "normal"` in `do_spawn_zombie` with a round-gated weight table that only fires
in the Zonweeb variant.

The cheap half (fast, tank) is pure attribute work on a curve that already exists. The expensive half
(armed, aura) needs new per-entity behavior and is where the tick budget goes.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction through StewBeet

**Primary Dependencies**: beet + StewBeet, Bookshelf (`bs.raycast` if the armed zombie shoots by raycast), the existing power-up drop path in `src/functional/zombies/rewards/powerups/`

**Storage**: `mgs:temp _zpos` carries `type` and `level` into `summon_zombie_at`. No new storage needed

**Testing**: In-game. `/scoreboard players set #zb_round mgs.data <n>` to jump rounds, F3+L for the aura's tick cost

**Target Platform**: Minecraft Java 26.2

**Project Type**: Minecraft datapack generated from a Python build pipeline

**Performance Goals**: Fast and tank add zero tick cost. The aura adds one radius scan per aura zombie per interval, and there is at most one alive. The armed zombie adds one line-of-sight check per armed zombie per cooldown

**Constraints**: Zonweeb variant only. Health must stay under the 2048 cap in `calc_zombie_hp`. Types must not spawn in dog rounds

**Scale/Scope**: `enemies.py` grows past the 300-line guidance and becomes a package. Plus the weight table in `spawning.py`

## Constitution Check

*GATE: passed, with one structural change required.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | All type functions stay generated. |
| II. Data-driven definitions | The types become a `ZombieType` dataclass table (id, display tag, speed factor, health factor, round gate, weight), and the weight table is the single place a wave's composition is decided. Copy-pasting the round-check ladder from `types/normal` per type is exactly what this rule forbids. |
| III. Typed, linted, readable | `enemies.py` is already 150 lines for two types. Four more makes it a package, grouped by feature. |
| IV. Runtime cost is a design constraint | The aura is the only per-tick addition, capped at one instance, on an interval rather than every tick, and SC-005 makes the budget explicit. |
| V. In-game verification | Each type's task ends in a round-jump check; the aura's ends in an F3+L measurement. |

## Project Structure

### Documentation (this feature)

```text
specs/003-zombie-special-types/
├── spec.md
├── plan.md              # This file
└── tasks.md
```

### Source Code (repository root)

```text
src/functional/zombies/game/round/
├── enemies.py                  # Today: normal, dog, and three fall-through stubs
└── enemies/                    # After: one module per type plus the shared curve
    ├── __init__.py             # write_enemy_types(): dispatch, unchanged entry point
    ├── curve.py                # calc_zombie_hp, apply_zombie_hp, apply_dog_hp, the shared BO curve
    ├── types.py                # ZombieType dataclass rows: factors, round gates, spawn weights
    ├── normal.py               # types/normal, the reference the others scale from
    ├── dog.py                  # types/dog
    ├── fast.py                 # types/fast
    ├── tank.py                 # types/tank
    ├── armed.py                # types/armed plus its ranged attack tick and guaranteed ammo drop
    └── aura.py                 # types/aura plus its radius resistance tick

src/functional/zombies/game/round/spawning.py    # do_spawn_zombie: weight roll replaces the hardcoded "normal"
src/functional/zombies/rewards/powerups/drops.py # Armed zombie's guaranteed ammo drop hooks in here
```

**Structure Decision**: `enemies.py` becomes `enemies/`, one module per type, with the BO health curve
extracted to `curve.py` since every type calls it. The alternative, one 600-line `enemies.py`, breaks
the 300-line rule and buries the interesting per-type logic in a wall of attribute commands.

## Complexity Tracking

| Accepted cost | Why | Alternative rejected because |
|---|---|---|
| The aura runs a radius scan while alive | It is the only way an aura can work, and it is capped at one instance on an interval. | A per-zombie "am I near an aura" check inverts the scan onto every zombie in the horde, which is strictly worse. |
| The armed zombie needs bespoke ranged logic | A datapack cannot add a vanilla AI goal, so the behavior has to be driven from a tick function. | Reusing the normal melee zombie makes it an armed zombie in name only. |
