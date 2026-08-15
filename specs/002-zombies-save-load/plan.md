# Implementation Plan: Zombies Save and Load

**Branch**: `002-zombies-save-load` | **Date**: 2026-08-15 | **Spec**: [spec.md](spec.md)

## Summary

Serialize a between-rounds zombies run into a compound in `mgs:zombies_saves`, and restore it by
running the normal `zombies/start` first and replaying the saved state on top.

The architectural bet: restore is replay, never reconstruction. Doors reopen by calling their own open
function, power turns on through `power/turn_on`, inventories go through the existing
`restore_inventory`. Nothing writes a block or a tag that a subsystem owns. That is what keeps a
half-correct restore from corrupting a map.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction through StewBeet

**Primary Dependencies**: beet + StewBeet (`stewbeet>=3.6.2`), Bookshelf (`bs.id` for UUID matching), `register_dialog` for both UIs

**Storage**: Minecraft storages. `mgs:zombies_saves` for the slots, `mgs:zombies` for live game state, `mgs:temp` for the restore handoff

**Testing**: In-game only, one verification pass per subsystem. This is the reason the feature was deferred, so the task list is organized around it

**Target Platform**: Minecraft Java 26.2, singleplayer and multiplayer

**Project Type**: Minecraft datapack generated from a Python build pipeline

**Performance Goals**: Save and load are one-shot operations, not per-tick. A save may take several ticks; a load may run over the existing start sequence. Neither adds tick cost to normal play

**Constraints**: Between rounds only. No live entity may need serializing. Restore must be idempotent enough that a failed load leaves no half-started game

**Scale/Scope**: New package `src/functional/zombies/save/`, plus hooks in the admin menu, the setup dialog, and `zombies/round_complete`

## Constitution Check

*GATE: passed.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | The save schema and every capture/replay function are generated from `src/functional/zombies/save/`. |
| II. Data-driven definitions | The capture list is one table of `SavedScore` dataclass rows (objective, storage key), consumed by both capture and restore. Writing capture and restore as two hand-maintained command lists is exactly how they drift apart. |
| III. Typed, linted, readable | New package grouped by feature (capture, restore, ui, schema), not by kind. |
| IV. Runtime cost is a design constraint | Zero per-tick cost. The only recurring work is the availability check on the admin menu, which is a score compare. |
| V. In-game verification | Phase 3 is a per-subsystem verification matrix, and the feature is not done until every row passes. |

## Project Structure

### Documentation (this feature)

```text
specs/002-zombies-save-load/
├── spec.md
├── plan.md              # This file
└── tasks.md
```

### Source Code (repository root)

```text
src/functional/zombies/
├── save/                       # New package
│   ├── __init__.py             # generate_zombies_save(): entry point, wired from zombies/__init__.py
│   ├── schema.py               # SavedScore rows + the slot layout constants, shared by capture and restore
│   ├── capture.py              # zombies/save/capture: game meta, per-player, map state
│   ├── restore.py              # zombies/save/load: start-then-replay, per-subsystem replay functions
│   ├── slots.py                # slot read/write/delete against mgs:zombies_saves
│   └── ui.py                   # save dialog (admin menu) + load list (setup dialog)
├── game/round/completion.py    # Hook: open the save window in the between-rounds gap
├── menus.py                    # Hook: the admin-menu entry and the setup-dialog slot list
├── objects/doors.py            # Read: door group ids and each group's open function
├── objects/power.py            # Read: #zb_power, replay via power/turn_on
├── machines/pap/               # Read: the PaP unlock flag
├── machines/mystery_box/       # Read: box position, uses, moved
├── objects/barricades/         # Read: per-barricade repair state
├── machines/perks/definitions.py   # Read: PERK_DEFINITIONS drives the perk capture table
└── player/inventory/           # Reuse: zombies/inventory/restore_inventory
```

**Structure Decision**: A dedicated `save/` package rather than a `save_state()` bolted onto each
subsystem. The capture and the replay for one subsystem belong next to each other, and every
subsystem's contribution is a few lines; scattering them makes the schema impossible to review as a
whole. The one thing `save/` does not own is how a door opens or how power turns on: it calls those.

## Complexity Tracking

| Accepted cost | Why | Alternative rejected because |
|---|---|---|
| `save/` reaches into many subsystems to read state | The schema has to be reviewable as one artifact, and it is read-only against each subsystem. | Per-subsystem `save`/`load` hooks spread one schema across a dozen files and guarantee capture and restore drift. |
| Between-rounds-only restricts when players can save | It removes the entire class of live-entity serialization. | Mid-round saving means serializing zombies, projectiles, power-ups, downed bodies and trap timers, which is where the corruption risk lives. |
