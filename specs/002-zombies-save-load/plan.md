# Implementation Plan: Zombies Suspend, Resume, Save and Load

**Branch**: `002-zombies-save-load` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

## Summary

Two halves with very different costs. Suspend and resume keeps the run in the world: the game-over
check stops counting offline players as dead, an empty server suspends the run on top of the operator
freeze, and a connection counter brings players back. Save and load takes the run out of the world into
a slot, and puts it back by starting the map normally and replaying the saved state through silent
variants of each subsystem's own functions.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction through StewBeet

**Primary Dependencies**: beet + StewBeet, Bookshelf (`bs.id` for UUID matching), `register_dialog` for the admin and setup dialogs

**Storage**: `mgs:zombies game.state` gains `"suspended"`. `mgs:zombies_saves slots[]` for slots, `mgs:zombies pending_players[]` for US3

**Testing**: In game, singleplayer quit and reopen for US1, a dedicated server restart for co-op, a field-by-field dump comparison for US2

**Target Platform**: Minecraft Java at the version pinned in `beet.yml`, singleplayer and multiplayer

**Performance Goals**: US1 adds one `custom:leave_game` check per player per tick. Save and load are one-shot

**Constraints**: Between rounds only for saves. Restore never writes a block or tag a subsystem owns

**Scale/Scope**: US1 touches `game/lifecycle/tick.py`, `game/lifecycle/over.py`, `game/lifecycle/join.py` and `menus.py`. US2 and US3 add the package `src/functional/zombies/save/`

## Design

### Suspend and resume (US1)

- `game/lifecycle/tick.py`: before the alive count, `execute unless entity @a[scores={mgs.zb.in_game=1}] run return run function zombies/suspend`. The alive count itself is unchanged, since `@a` already excludes offline players: what changes is that zero online players suspends instead of ending.
- `zombies/suspend`: state `"suspended"`, `zombies/freeze_on` without its operator message, and a check that every timer listed in FR-002 is gated on `#zb_freeze`. The audit of those timers is task T004; any timer that ticks during the operator freeze today is a bug for both features.
- Connection: `mgs.zb.rejoins` (`custom:leave_game`), checked in `player/tick`. On a non-zero value: when the run is active or suspended and the player is in the roster, `zombies/rejoin` restores team, gamemode, sidebar, attributes and post effects (`player/fx_after_rejoin`); when no run exists, `zombies/clear_stale_player` (FR-005).
- A suspended run starts the resume countdown as soon as a roster player is online.

### Save (US2)

- `save/schema.py`: the `SavedScore` and `SavedMapScore` tables, generated from the per-player objectives and the map element objectives (`zb.door.*`, `zb.perk.*`, `zb.trap.*`, `zb.barricade.*`, `zb.pap.*`). Capture and restore both iterate these tables (FR-009).
- `save/capture.py`: game meta, then per player (UUID, scores, perks, `max_health`, `Inventory`, Tombstone and Who's Who storages), then map state by iterating the element entities by tag and id.
- After capture, the normal `zombies/stop`.

### Load (US2, US3)

- `save/restore.py`: refuse unknown format or missing map, run `zombies/start` with the saved map and variant, wait for `zombies/preload_complete`, then replay.
- Silent replay: each subsystem gets a `silent` entry point next to its normal one (door open without announce, sound or charge; power on without the broadcast; box placement without the move animation). The normal function calls the silent one and adds the feedback, so there is one implementation.
- Players: matched by UUID through `bs.id`; online ones get their scores, perks and inventory through `zombies/inventory/restore_inventory`; offline ones go to `pending_players`.
- Weapons: each gun in a restored inventory is regenerated from `mgs:i/<id>` and its dynamic fields are copied over (FR-011), the same fields the 008 fire-mode migration already carries.
- `game.round` is set to the saved round and the next round starts after the usual gap.

## Constitution Check

*GATE: passed.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | Schema, capture, restore and UI are generated from `zombies/save/`. |
| II. Data-driven definitions | One schema table drives capture and restore. |
| III. Typed, linted, readable | US1 stays inside the lifecycle files it fixes; US2 and US3 get their own package. |
| IV. Runtime cost is a design constraint | One counter check per player per tick for US1; save and load are one-shot. |
| V. In-game verification | Each story closes on a quit, a restart or a dump comparison. |

## Project Structure

```text
src/functional/zombies/
    game/lifecycle/tick.py     # suspend instead of game over, resume countdown
    game/lifecycle/over.py     # stale player cleanup
    game/lifecycle/join.py     # rejoin restore
    menus.py                   # Pause, Resume, Save & Quit, slot list
    save/
        __init__.py            # generate_zombies_save()
        schema.py              # SavedScore and SavedMapScore tables
        capture.py
        restore.py
        slots.py
```

## Complexity Tracking

| Accepted cost | Why | Alternative rejected because |
|---|---|---|
| A silent entry point per subsystem | Replaying through the normal functions would announce and charge every door again. | Writing blocks and tags directly is how a restore corrupts a map. |
| Weapons rebuilt on load | Item stats are frozen in `custom_data`, so a save from an older version would keep old stats forever. | Refusing cross-version loads makes every pack update delete the saves. |
