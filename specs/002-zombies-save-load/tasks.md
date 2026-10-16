---

description: "Task list for zombies suspend, resume, save and load"
---

# Tasks: Zombies Suspend, Resume, Save and Load

**Input**: [spec.md](spec.md), [plan.md](plan.md)

**Tests**: No automated tests. Each task closes on a quit and reopen, a server restart or a dump comparison.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 suspend and resume, US2 save and load, US3 roster

---

## Phase 1: User Story 1 - A run survives disconnects and restarts (Priority: P1)

- [ ] T001 [US1] Reproduce the bug: solo run at round 3, quit and reopen, confirm `zombies/game_over` fires on the first ticks
- [X] T002 [US1] Suspend instead of ending when no roster player is online, in `game/lifecycle/tick.py` (FR-001)
- [X] T003 [US1] Write `zombies/suspend` on top of `zombies/freeze_on`, with the "PAUSED" display (FR-002)
- [X] T004 [US1] Audit every run timer against `#zb_freeze` (round, spawn, power-ups, box move, traps, perks, abilities, bleed-out, Dying Wish, Who's Who, Tombstone) and gate the ones that still tick (FR-002)
- [X] T005 [US1] Add `mgs.zb.rejoins` (`custom:leave_game`) and `zombies/rejoin` restoring team, gamemode, sidebar, attributes and post effects (FR-003)
- [X] T006 [US1] Resume after a 5 s countdown once a roster player is online, cancelled if they leave again (FR-004)
- [X] T007 [US1] Clear stale players: `mgs.zb.in_game=1` with no run in progress (FR-005)
- [X] T008 [US1] Admin menu: Pause, Resume and End for a suspended run (FR-006)
- [ ] T009 [US1] Verify solo quit and reopen mid-round and between rounds (SC-001)
- [ ] T010 [US1] Verify a co-op restart, one player leaving and coming back, and a downed player leaving (SC-002, US1/AC3, US1/AC4)
- [X] T011 [US1] Verify a player offline when the run ended comes back clean (SC-003)

**Checkpoint**: Shippable alone. It fixes the lost runs.

---

## Phase 2: User Story 2 - Save a run between rounds (Priority: P2)

- [ ] T012 [US2] Create `src/functional/zombies/save/` with `generate_zombies_save()`
- [ ] T013 [US2] Write the `SavedScore` and `SavedMapScore` tables in `save/schema.py` from the existing objectives (FR-009)
- [ ] T014 [US2] Write the slot storage: 5 slots, overwrite with confirmation, delete (FR-013)
- [ ] T015 [US2] Capture game meta and per-player state, inventories included (FR-008)
- [ ] T016 [US2] Capture the map state by iterating element entities (FR-008)
- [ ] T017 [US2] Gate "Save & Quit" on the between-rounds gap, then stop normally (FR-007)
- [ ] T018 [US2] Verify a save by dumping the slot and comparing with the live state (SC-004, first half)
- [ ] T019 [US2] Add the silent entry points: door open, power on, Pack-a-Punch unlock, box placement, Der Wunderfizz placement (FR-010)
- [ ] T020 [US2] Write the load: refuse unknown format and missing map, `zombies/start`, then replay on `preload_complete` (FR-010, FR-012)
- [ ] T021 [US2] Restore players by UUID through `bs.id` and `restore_inventory`
- [ ] T022 [US2] Rebuild every restored weapon from its current definition (FR-011)
- [ ] T023 [US2] Skip and report map elements missing from the current map (US2/AC6)
- [ ] T024 [US2] UI: Save & Quit in the admin menu, slot list on the setup dialog (FR-014)
- [ ] T025 [US2] Verify the full round trip at round 17 across another game (SC-004)
- [ ] T026 [US2] Verify a PaP camo weapon across a pack version bump (SC-005)
- [ ] T027 [US2] Verify no save during a round or a dog round (SC-006)

---

## Phase 3: User Story 3 - Load with a different roster (Priority: P3)

- [ ] T028 [US3] Keep offline saved players in `pending_players` and restore them on join (FR-015)
- [ ] T029 [US3] Verify a 3-player save loaded with 2, the third joining later, and a newcomer joining fresh

---

## Phase 4: Polish

- [ ] T030 Add suspend and save to the root `README.md` zombies feature list
- [ ] T031 `uv run python scripts/verify.py lint` and `uv run python scripts/verify.py validate` pass
