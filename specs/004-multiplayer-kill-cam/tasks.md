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

- [ ] T001 Create `src/functional/multiplayer/kill_cam/` with `generate_kill_cam()`, wired from `src/functional/multiplayer/__init__.py`
- [ ] T002 Define the tunables of spec FR-013 and the `mgs:kill_cam` paths in `kill_cam/shared.py`
- [ ] T003 Clear `mgs:kill_cam` and kill `mgs.kill_cam` entities in `game/start.py` and `game/stop.py` (FR-004, FR-012)

---

## Phase 2: User Story 2 - Recording is cheap and bounded (Priority: P1)

- [ ] T004 [US2] Write the window gate in `record.py`, recomputed once a second from `#red`/`#blue`, the FFA top `mp.kills` and `#mp_timer`, and clear the buffer when it closes (FR-002, US2/AC3)
- [ ] T005 [US2] Write the per-player sampler through a marker and `bs.position`, with the fired, sneak, sprint and dead flags (FR-003, US2/AC4)
- [ ] T006 [US2] Append one frame per tick and trim `frames[0]` once older than `RECORD_TICKS` (FR-004)
- [ ] T007 [US2] Write the roster snapshot on window open and on a late join while open
- [ ] T008 [US2] Verify in game: nothing written mid-match, frames appear at match point, the list never exceeds `RECORD_TICKS` entries
- [ ] T009 [US2] F3+L with 2 players and as many as available: mid-match unchanged (SC-001), window cost per player (SC-002)

---

## Phase 3: User Story 1 - The final kill chain is replayed (Priority: P1)

- [ ] T010 [US1] Append `{t, killer, victim}` from the multiplayer `on_kill` path while the window is open, in `chain.py` (FR-005)
- [ ] T011 [US1] Resolve the final chain at match end: walk back through `kills` with `CHAIN_GAP` and `MAX_CHAIN`, cut at the buffer start (FR-005)
- [ ] T012 [US1] Call `kill_cam/start` from `team_wins`, `ffa/player_wins` and `game_draw` before the results, returning at once when there is no chain (FR-010)
- [ ] T013 [US1] Put viewers in spectator on the camera and save their position and gamemode, in `playback.py` (FR-008)
- [ ] T014 [US1] Spawn mannequins from the roster on each player's first replayed sample, hide the killer's, and drive them from their samples (FR-007)
- [ ] T015 [US1] Drive the camera from the killer's samples at eye height (FR-008)
- [ ] T016 [US1] Play the fire sound and muzzle particle on fired flags, and kill each victim's mannequin on its kill tick (FR-009)
- [ ] T017 [US1] Show "KILLCAM", the killer and the chain length in `present.py` (FR-011)
- [ ] T018 [US1] Clean up and restore viewers, then continue to the results (US1/AC5, FR-012)
- [ ] T019 [US1] Verify a 1-kill and a 4-kill ending in FFA and in TDM (SC-003)

---

## Phase 4: User Story 3 - The replay survives an imperfect match (Priority: P2)

- [ ] T020 [US3] Verify a final killer who disconnects right after the kill still gets replayed (US3/AC1)
- [ ] T021 [US3] Verify a viewer leaving mid-replay rejoins restored, and the others are unaffected (US3/AC2)
- [ ] T022 [US3] Verify a late joiner's mannequin appears from their first sample (US3/AC3)
- [ ] T023 [US3] Verify the skips: timer end, suicide, fall, out of bounds, bomb (US3/AC4, SC-004)
- [ ] T024 [US3] Verify S&D and Demolition get a kill cam only on the match-ending round, Domination and Hardpoint only with a kill in the window
- [ ] T025 [US3] Verify `/function mgs:multiplayer/stop` mid-replay leaves nothing behind (SC-005)

---

## Phase 5: Polish

- [ ] T026 Tune the defaults of spec Assumptions in play
- [ ] T027 Add the kill cam to the root `README.md` multiplayer feature list
- [ ] T028 `uv run python scripts/verify.py lint` and `uv run python scripts/verify.py validate` pass
