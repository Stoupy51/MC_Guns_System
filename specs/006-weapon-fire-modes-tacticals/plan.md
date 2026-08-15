# Implementation Plan: Fire Sound Variants and Tactical Grenade Slotting

**Branch**: `006-weapon-fire-modes-tacticals` | **Date**: 2026-08-15 | **Spec**: [spec.md](spec.md)

## Summary

Move smoke and flash out of `LETHAL_GRENADE_IDS` and onto the `"tactical": True` path the monkey bomb
already uses, then handle the `mgs.zb.lethal_type` enum renumbering that falls out of it.

Separately, replace the "prefer `fire_alt` whenever it exists" branch in the fire sound dispatch with a
real condition, after deciding what `fire_alt` means. Only the SPAS-12 defines it, and the SPAS-12's
declared `FIRE_MODE` is `semi` with no second mode in the data, so the TODO's premise needs checking
before it is implemented.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction through StewBeet

**Primary Dependencies**: beet + StewBeet

**Storage**: `storage mgs:gun all.sounds` for the fire dispatch. `mgs.zb.lethal_type` per-player score for the slot enum

**Testing**: In-game. A zombies game for User Story 1, a range for User Story 2

**Target Platform**: Minecraft Java 26.2

**Project Type**: Minecraft datapack generated from a Python build pipeline

**Performance Goals**: Neither change adds per-tick work. The fire dispatch gains at most one condition per shot

**Constraints**: The enum renumbering must not leave a live game with empty slots

**Scale/Scope**: Two touched areas, roughly 40 lines between them

## Constitution Check

*GATE: passed.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | Both changes are in the generating code and its data tables. |
| II. Data-driven definitions | The whole point of User Story 1: `"tactical": True` is already the data flag that routes a grenade, and smoke and flash should carry it instead of being special-cased. `LETHAL_GRENADE_IDS` becomes a list of actual lethals. |
| III. Typed, linted, readable | No new modules. The lethal-type enum gets a docstring stating that its indices are positional and load-bearing. |
| IV. Runtime cost is a design constraint | One condition per shot, no scans. |
| V. In-game verification | Every task closes on a check in a live zombies game or on the range. |

## Project Structure

### Documentation (this feature)

```text
specs/006-weapon-fire-modes-tacticals/
├── spec.md
├── plan.md              # This file
└── tasks.md
```

### Source Code (repository root)

```text
src/config/stats/weapons/grenades.py             # SMOKE and FLASH gain "tactical": True; LETHAL_GRENADE_IDS shrinks
src/functional/zombies/player/inventory/
├── grenades.py                                  # give_lethal_type, record_lethal_type, the refill paths
└── loadout.py                                   # Starting loadout, lethal_type reset
src/functional/zombies/objects/wallbuys/
├── purchase.py                                  # Records the bought grenade type
└── give.py                                      # Routes the bought grenade to its slot
src/functional/weapon/firing/sound.py            # sound/main: the fire vs fire_alt branch
src/config/stats/weapons/shotguns.py             # SPAS12: the only weapon defining fire_alt
```

**Structure Decision**: No restructuring. Both changes fit inside existing modules, and neither is
close to the 300-line threshold.

## Complexity Tracking

No violations. One risk is called out rather than tracked as a violation: the `lethal_type` enum is
positional, so shrinking the list renumbers live per-player scores. That is why FR-004 exists, and why
the plan does the enum work before the slot routing rather than after.
