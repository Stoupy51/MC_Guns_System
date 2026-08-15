---

description: "Task list for the multiplayer final kill cam"
---

# Tasks: Multiplayer Final Kill Cam

**Input**: [spec.md](spec.md), [plan.md](plan.md)

**Tests**: No automated tests. Every task closes on a played match or an F3+L reading.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 replay, US2 recording cost, US3 robustness

---

## Phase 1: Setup

- [ ] T001 Create `src/functional/multiplayer/kill_cam/` with `__init__.py` exposing `generate_kill_cam()`, and wire it from `src/functional/multiplayer/__init__.py`
- [ ] T002 Define `RECORD_TICKS`, `BUFFER_MAX`, `PLAYBACK_SPEED` and the `mgs:kill_cam` storage paths in `kill_cam/shared.py`, each with a one-line docstring under it

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The buffer and its lifecycle. Nothing can replay until something records, and nothing may record outside the window.

- [ ] T003 Clear `storage mgs:kill_cam` on match start in `src/functional/multiplayer/game/start.py` and on match stop in `game/stop.py`, so a stale buffer can never replay (FR-007)
- [ ] T004 Add the recording gate in `src/functional/multiplayer/game/tick.py`: a single score compare against the match timer that only passes in the final `RECORD_TICKS`
- [ ] T005 Verify the gate is inert before the sampler exists: play a full match and confirm nothing is written to `mgs:kill_cam` until the last 10 seconds

**Checkpoint**: The window opens and closes correctly and costs one failed compare per tick.

---

## Phase 3: User Story 2 - The recording costs nothing for most of the match (Priority: P1)

**Goal**: A bounded, cheap recorder.

Ordered before the replay on purpose. If the recorder cannot be made cheap, the feature does not ship, and finding that out after building playback wastes the playback.

- [ ] T006 [US2] Implement the per-tick sampler in `kill_cam/record.py`: append `[x, y, z, yaw, pitch]` for each in-game player to `mgs:kill_cam players.<username>`
- [ ] T007 [US2] Trim each buffer to `BUFFER_MAX` entries by dropping the oldest, so the storage cannot grow past 200 per player (FR-003)
- [ ] T008 [US2] Verify the storage shape with `/data get storage mgs:kill_cam players` at the end of a match: one key per player, at most 200 entries each
- [ ] T009 [US2] Measure MSPT with F3+L on a full lobby, mid-match and in the last 10 seconds, with the feature on and off (SC-001, SC-002)
- [ ] T010 [US2] Confirm nothing records in Missions or Zombies (FR-008)

**Checkpoint**: The recording half is proven cheap and correct. Playback can be built on it.

---

## Phase 4: User Story 1 - Everyone sees the final kill replayed (Priority: P1) MVP

**Goal**: The sequence plays at match end and hands off to the scoreboard.

**Independent Test**: Play a short FFA to the score limit and watch the replay as every player.

- [ ] T011 [US1] Write the final kill record (killer, victim, buffer index) from `src/functional/multiplayer/game/death.py` on every kill, so the last one written is the final kill (FR-004)
- [ ] T012 [US1] Implement the replay camera in `kill_cam/replay.py`: an `item_display` with `teleport_duration:1` that viewers ride, following the pattern already proven by the zombies downed camera in `src/functional/zombies/player/revive/down.py`
- [ ] T013 [US1] Implement per-tick playback: step through the killer's samples, teleporting the camera to each recorded position and rotation
- [ ] T014 [US1] Move every player into the replay at match end and restore them to normal spectate afterwards (FR-005)
- [ ] T015 [US1] Sequence it into `src/functional/multiplayer/game/stop.py` before the scoreboard, and hand off to the scoreboard when it ends
- [ ] T016 [US1] Add the presentation in `kill_cam/present.py`: a title naming the killer and the victim, so it reads as a kill cam rather than a camera glitch (FR-009)
- [ ] T017 [US1] Clean up the camera entity and every mount at the end of the sequence, and verify nothing tagged `mgs.gm_entity` survives (SC-005)
- [ ] T018 [US1] Verify the replay across gamemodes: FFA, Team Deathmatch, Domination and Hardpoint

**Checkpoint**: The feature works on a clean match. This is the MVP.

---

## Phase 5: User Story 3 - Replays survive an imperfect recording (Priority: P2)

**Goal**: The most-watched moment in the match never breaks.

- [ ] T019 [US3] Skip the replay and go straight to the scoreboard when there is no final kill record, when the match ended on the timer, or when the killer's buffer is empty (FR-006)
- [ ] T020 [US3] Skip cleanly when the killer disconnected before the end
- [ ] T021 [US3] Handle a viewer disconnecting mid-replay: the sequence continues for everyone else and leaves no orphan entity
- [ ] T022 [US3] Handle a short buffer (a player who joined seconds before the end) by playing what exists rather than stalling
- [ ] T023 [US3] Decide and implement the Search and Destroy behavior: one kill cam at match end, or one per round. Write the decision into `kill_cam/shared.py` next to the constants
- [ ] T024 [US3] Handle killer-less deaths (suicide, out of bounds, trap) by skipping the replay

---

## Phase 6: Polish

- [ ] T025 Tune `PLAYBACK_SPEED` and the replay length so the sequence lands rather than dragging
- [ ] T026 Delete the "Future multiplayer TODO" sketch from the root `README.md` and add the kill cam to the multiplayer feature list
- [ ] T027 `ruff check src --fix` and a clean `beet build`

---

## Dependencies & Execution Order

- **Phase 2** blocks everything
- **Phase 3 (US2)** before **Phase 4 (US1)**: there is nothing to replay until there is a buffer, and the cost question decides whether the feature is viable at all
- T011 can be written alongside Phase 3; it touches a different file
- **Phase 5 (US3)** depends on Phase 4
- T023 is a design decision and should be made early, even though it is implemented late

---

## Implementation Strategy

Prove the recorder is free before building the replay. That ordering is the whole risk management for
this feature: everything else is straightforward work on a pattern the codebase already uses.

Ship Phases 1 to 4 as the MVP, then harden with Phase 5 before it goes anywhere near a busy server.

## Notes

- The camera pattern already exists; read `src/functional/zombies/player/revive/down.py` before writing T012
- Buffers are keyed by username per the original sketch. Switch to UUID only if name changes prove to matter
- Commit per phase; the recorder and the replay are independently reviewable
