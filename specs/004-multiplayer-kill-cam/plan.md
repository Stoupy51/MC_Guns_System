# Implementation Plan: Multiplayer Final Kill Cam

**Branch**: `004-multiplayer-kill-cam` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

## Summary

Record a bounded window of every match player's motion near the end of a match, log the kills in it,
and replay the final killer's chain as a puppet show: one mannequin per player, one spectated camera at
the killer's eyes.

Two decisions shape everything. The window is gated on match point, not on the timer alone, because
most matches end on the score limit. And a sample never reads player NBT: a marker is teleported to the
player and read instead, which is what makes 12 players x 20 samples a second affordable.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction through StewBeet

**Primary Dependencies**: beet + StewBeet, Bookshelf (`bs.id` for player ids, `bs.position` for marker-based position and rotation reads)

**Storage**: `storage mgs:kill_cam` with `frames`, `kills` and `roster` (spec Key Entities). Cleared on match start, stop and window close

**Testing**: In game: short FFA and TDM matches, F3+L for SC-001 and SC-002

**Target Platform**: Minecraft Java at the version pinned in `beet.yml`, multiplayer

**Performance Goals**: Zero cost outside the window. Inside: one frame append per tick, built without macros or player NBT reads

**Constraints**: No world rewind. Held items are snapshotted at window open. Multiplayer only

**Scale/Scope**: New package `src/functional/multiplayer/kill_cam/`, hooks in `game/tick.py`, `game/death.py`, `game/start.py`, `game/stop.py` and the three win paths (`team_wins`, `ffa/player_wins`, `game_draw`)

## Design

### Recording

- `#kc_window` is recomputed once per second from the team scores, the FFA top score and `#mp_timer`. The per-tick recorder is behind `execute if score #kc_window matches 1`.
- Per player: `tp` a shared marker to the player with their rotation, read `Pos` and `Rotation` from the marker into a sample compound, set the flag bits from scores (`fired` from the weapon cooldown changing this tick, `sneak` and `sprint` from predicates).
- Samples are appended to `kill_cam:temp frame.s`, then the frame is appended to `frames`. When `frames[0].t` is older than `RECORD_TICKS`, `frames[0]` is removed. One removal per tick keeps the cost flat.
- On window open, and on a late join while open, the player's roster entry is written: name, `bs.id`, team, mainhand and armor items.

### Kill log

- The multiplayer `on_kill` path, already run as the killer with the victim tagged, appends `{t, killer, victim}` while the window is open.
- The final chain is computed at match end by walking `kills` backwards (spec FR-005). The result is `chain_start`, `chain_end` and the chain length.

### Playback

- The three win paths call `kill_cam/start` before announcing results. When the chain is empty, `kill_cam/start` returns at once and the results come as today.
- Viewers: every `mp.in_game` player is tagged `mgs.kc_viewer`, saved position and gamemode go to scores and storage, gamemode spectator, `spectate` the camera.
- A playback cursor walks `frames` from `chain_start - PRE_ROLL` to `chain_end + POST_ROLL`, one frame per tick. Each frame: teleport each mannequin to its sample (summoned on first appearance with `teleport_duration` set for smoothing), set its pose from the flags, teleport the camera to the killer's sample at eye height, play fire effects, kill the mannequins of victims whose kill tick is reached.
- Titles: "KILLCAM", the killer's name, the chain length.
- End: kill every `mgs.kill_cam` entity, restore viewers, clear storage, continue to the results.

## Constitution Check

*GATE: passed.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | Recorder, chain logic and playback are generated from `kill_cam/`. |
| II. Data-driven definitions | Every tunable is a constant in `kill_cam/shared.py` with a docstring (FR-013). |
| III. Typed, linted, readable | One package grouped by feature: record, chain, playback, present. |
| IV. Runtime cost is a design constraint | The window gate, the marker read and the single-frame trim exist for US2. |
| V. In-game verification | Every phase closes on a played match or an F3+L reading. |

## Project Structure

```text
src/functional/multiplayer/kill_cam/
    __init__.py      # generate_kill_cam(), wired from multiplayer/__init__.py
    shared.py        # tunables and storage paths
    record.py        # window gate, per-tick sampler, roster snapshot, trim
    chain.py         # kill log append and final chain resolution
    playback.py      # viewers, mannequins, camera, cursor, cleanup
    present.py       # titles and sounds
```

## Complexity Tracking

| Accepted cost | Why | Alternative rejected because |
|---|---|---|
| Mannequins for every player in the window | Victims must die on screen and teammates must be visible. | A camera-only replay shows a floating view and nobody dying. |
| Held items frozen at window open | Tracking item changes per tick means reading player NBT. | The rare weapon swap mid-chain is not worth that cost. |
| No world rewind | Blocks, grenades and objectives are out of reach of a datapack recorder. | Accepted by Call of Duty players as part of how a kill cam looks. |
