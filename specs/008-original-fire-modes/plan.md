# Implementation Plan: Fire Modes Faithful to the Original

**Branch**: `008-original-fire-modes` | **Date**: 2026-10-08 | **Spec**: [spec.md](spec.md)

## Summary

Replace the `can_auto` / `can_burst` / `burst` triple with one ordered list of fire modes per weapon, `fire_modes`, stored in the item like every other stat.
The list rotates on each drop, so its first entry is always the current mode and the mode's own values are read from `fire_modes[0]` without a macro.
A mode carries only what it changes: cooldown (and its Pack-a-Punch value), crouched accuracy, the shooter's fire sounds, burst length, burst spacing and the pause after a burst.
Items already in worlds have no `fire_modes`; the first tick they are held, they get their weapon's list from a table written at load, and lose the three old keys.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction through StewBeet

**Primary Dependencies**: beet + StewBeet

**Storage**: item `custom_data.mgs.stats.fire_modes` (list of compounds) next to the existing `fire_mode`; `storage mgs:data fire_modes.<base_weapon>` written at load for the migration

**Testing**: In game, with `/function mgs:_give_all` and the range

**Target Platform**: Minecraft Java, at the version pinned in `beet.yml`

**Project Type**: Minecraft datapack generated from a Python build pipeline

**Performance Goals**: No new per-tick work on an up-to-date item: one `unless data` on the held gun. A shot reads at most three more NBT paths (mode cooldown, PaP cooldown, mode sound)

**Constraints**: `fire_mode` stays the current mode's name, so its readers (click handling, burst bookkeeping, the `on_fire_mode_change` signal) keep working; `mgs.*` item data is frozen, so old items are migrated rather than abandoned

**Scale/Scope**: 31 guns, 4 grenades, one migration path

## Constitution Check

*GATE: passed.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | Modes are declared in the weapon tables; the migration table is generated from the same definitions. |
| II. Data-driven definitions | A frozen `FireMode` dataclass, shared constants (`AUTO`, `SEMI`, `PUMP`) and one constructor call per special mode. The selector, the HUD and the migration read the list, never a per-gun branch. |
| III. Typed, linted, readable | Three keys and their branches are replaced, not kept beside the new list. |
| IV. Runtime cost is a design constraint | The migration check is one NBT test per tick on the held gun; mode values are read only when a shot happens. |
| V. In-game verification | Every task list phase ends with range checks per gun family. |

## Project Structure

### Documentation (this feature)

```text
specs/008-original-fire-modes/
├── spec.md
├── plan.md              # This file
└── tasks.md
```

### Source Code (repository root)

```text
src/config/stats/fire_modes.py                   # FireMode dataclass, AUTO/SEMI/PUMP, FireMode.stats() and FireMode.pap()
src/config/stats/keys.py                         # FIRE_MODES replaces BURST, CAN_AUTO, CAN_BURST
src/config/stats/weapons/*.py                    # **FireMode.stats(...) in every gun and grenade
src/functional/weapon/ammo/switch.py             # Rotation on drop, fireselect click, migration of old items, load-time table
src/functional/weapon/firing/raycast/clicks.py   # pump as a single tap, mode cooldown, burst length, spacing and pause
src/functional/weapon/common.py                  # Burst bookkeeping reads fire_modes[0].burst
src/functional/weapon/firing/raycast/accuracy.py # Mode crouched accuracy
src/functional/weapon/firing/sound.py            # Mode fire sounds for the shooter only
src/functional/weapon/firing/casing.py           # No shell on the shot in pump mode
src/functional/weapon/ammo/magazine/core.py      # The pump tag follows the pump mode, not the pump sound
src/functional/weapon/hud/actionbar.py           # [P | S | B | A] from the list
```

**Structure Decision**: No new package. The dataclass sits with the other stat definitions, and each consumer reads `fire_modes[0]` where it already reads the stat it overrides.

## Complexity Tracking

| Accepted cost | Why | Alternative rejected because |
|---|---|---|
| `fire_mode` duplicates `fire_modes[0].name` | Its readers, including a public signal, keep working untouched. | Dropping it renames a frozen item key and every reader at once. |
| Old RPG-7 items keep their old `pap_stats` (fire_mode auto, can_auto) | The migration rewrites `stats` only; a later Pack-a-Punch on such an item gives auto fire with a one-entry list, so the HUD shows S while it fires automatically. | Rewriting `pap_stats` in the migration needs a second table for one weapon. |
