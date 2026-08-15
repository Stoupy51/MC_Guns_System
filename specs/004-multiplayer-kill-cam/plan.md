# Implementation Plan: Multiplayer Final Kill Cam

**Branch**: `004-multiplayer-kill-cam` | **Date**: 2026-08-15 | **Spec**: [spec.md](spec.md)

## Summary

Record a 200-tick ring buffer of every player's position and rotation during the final 10 seconds of a
match, then replay the last kill from the killer's viewpoint before the scoreboard.

The design constraint that shapes everything: recording must be invisible in the tick profile until it
starts. It is gated on a single score compare against the match timer, so for 95% of a match the whole
feature is one `execute if score` that fails.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction through StewBeet

**Primary Dependencies**: beet + StewBeet. The camera-mount pattern is already proven in `src/functional/zombies/player/revive/` (`downed_cam`, an `item_display` with `teleport_duration:1` that the player rides)

**Storage**: `storage mgs:kill_cam` for the buffers and the final kill record. Cleared on match start and stop

**Testing**: In-game. F3+L for SC-001, short FFA matches for the sequence itself

**Target Platform**: Minecraft Java 26.2, multiplayer

**Project Type**: Minecraft datapack generated from a Python build pipeline

**Performance Goals**: Zero measurable cost outside the final 10 seconds. Inside it, one storage append per in-game player per tick

**Constraints**: Only positions and rotations are recorded. The replayed world is the post-match world. 200 ticks is the entire budget

**Scale/Scope**: New package `src/functional/multiplayer/kill_cam/`, plus hooks in `game/tick.py`, `game/death.py`, `game/stop.py` and `game/start.py`

## Constitution Check

*GATE: passed.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | The recorder, the replay and the presentation are all generated from `kill_cam/`. |
| II. Data-driven definitions | Buffer size, record window and playback speed are named constants with docstrings, not numbers repeated across three files. |
| III. Typed, linted, readable | New package grouped by feature: record, replay, presentation. |
| IV. Runtime cost is a design constraint | This is the principle the whole design is built around. The recorder is behind one score compare, and User Story 2 exists purely to make that a testable requirement rather than an intention. |
| V. In-game verification | Every task closes on a played match or an F3+L reading. |

## Project Structure

### Documentation (this feature)

```text
specs/004-multiplayer-kill-cam/
├── spec.md
├── plan.md              # This file
└── tasks.md
```

### Source Code (repository root)

```text
src/functional/multiplayer/
├── kill_cam/                   # New package
│   ├── __init__.py             # generate_kill_cam(): entry point, wired from multiplayer/__init__.py
│   ├── shared.py               # RECORD_TICKS, BUFFER_MAX, PLAYBACK_SPEED and the storage paths
│   ├── record.py               # The gated per-tick sampler and the ring-buffer trim
│   ├── replay.py               # Camera entity, per-tick playback from the killer's samples, cleanup
│   └── present.py              # Titles and overlay naming killer and victim
├── game/tick.py                # Hook: the gate that turns recording on in the last 10 seconds
├── game/death.py               # Hook: write the final kill record (killer, victim, buffer index)
├── game/start.py               # Hook: clear the buffers
└── game/stop.py                # Hook: run the sequence before the scoreboard, then clear the buffers
```

**Structure Decision**: A dedicated package rather than functions spread across `game/`. Recording,
playback and presentation are three halves of one mechanism that only make sense together, and none of
them belongs to the match lifecycle modules they hook into. The lifecycle files get one line each.

## Complexity Tracking

| Accepted cost | Why | Alternative rejected because |
|---|---|---|
| The replay shows the post-match world, not the recorded one | Only positions and rotations are recorded. | Recording the world state is not feasible in a datapack and is far beyond what a kill cam needs. |
| A per-tick storage append per player during the window | It is the recording. | Sub-sampling to every other tick halves the cost but visibly stutters the camera, which defeats the feature. |
