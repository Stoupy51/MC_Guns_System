---

description: "Task list for fire modes faithful to the original"
---

# Tasks: Fire Modes Faithful to the Original

**Input**: [spec.md](spec.md), [plan.md](plan.md)

**Tests**: No automated tests. Every phase closes on range checks, per constitution principle V.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 mode sets, US2 SPAS-12 pump and semi, US3 burst rhythm

---

## Phase 1: Foundational

- [X] T001 Add `FireMode` (frozen dataclass), `AUTO`, `SEMI`, `PUMP`, `FireMode.stats(*modes)` and `FireMode.pap(*modes)` in `src/config/stats/fire_modes.py`
- [X] T002 Replace `BURST`, `CAN_AUTO` and `CAN_BURST` with `FIRE_MODES` in `src/config/stats/keys.py`, `STATS_FIELDS` included, and rewrite the `FIRE_MODE` docstring
- [X] T003 Declare every gun and grenade through `**FireMode.stats(...)` with the FR-002 mode sets; the RPG-7 Pack-a-Punch goes through `FireMode.pap(AUTO)`
- [X] T004 Write `storage mgs:data fire_modes.<base_weapon>` at load from `Mem.definitions`, and migrate a held item without `fire_modes`: list from the table, `fire_mode` to its first entry, the three old keys removed, written back to the item (FR-007, FR-008)

## Phase 2: User Story 1 - Each gun offers its original modes (P1)

- [X] T005 [US1] Rotate `fire_modes` on drop, copy `fire_mode` from the new first entry, skip single-mode weapons, and play `mgs:common/fireselect` (FR-001, FR-009)
- [X] T006 [US1] Read the burst length from `fire_modes[0].burst` in click handling and burst bookkeeping (FR-011)
- [X] T007 [US1] Build the actionbar indicator from the list in a fixed `P S B A` order (FR-010)

## Phase 3: User Story 2 - The SPAS-12 pumps or fires semi-automatically (P1)

- [X] T008 [US2] Treat `pump` as a single tap; take the shot cooldown from `fire_modes[0].cooldown`, or `pap_cooldown` on a Pack-a-Punched gun (FR-003, FR-004)
- [X] T009 [US2] Tag the pump from `fire_mode:"pump"`, eject the shell with the pump sound, and skip the shell on the shot in pump mode (FR-003)
- [X] T010 [US2] Read the crouched accuracy from `fire_modes[0].accuracy_sneak` when present (FR-004)
- [X] T011 [US2] Play `fire_modes[0].fire_sound` and `pap_fire_sound` to the shooter only; other players keep the weapon's sounds (FR-004, FR-005)

## Phase 4: User Story 3 - Burst rhythm (P2)

- [X] T012 [US3] Space burst rounds by `fire_modes[0].burst_spacing` (the weapon's cooldown when absent) and add `burst_pause` after the last round (FR-006)

## Phase 5: Verification

- [X] T013 Build, `verify.py check --diff` limited to the intended functions and item data, `verify.py lint` on the touched files
- [ ] T014 In game: drop each gun of `_give_all` and compare its cycle with FR-002 (SC-001, SC-002)
- [ ] T015 In game: SPAS-12 ten shots per mode, pump and shell timing, crouched spread, both semi clips, PaP semi (SC-003, SC-005)
- [ ] T016 In game: an AK-47 left in burst and a SPAS-12 from before the update, held once, follow the new lists (SC-004)
- [ ] T017 In game: M16A4 and FAMAS bursts, counting ticks between rounds and before the next burst

---

## Dependencies & Execution Order

- T001 and T002 before T003; T003 before every functional task
- T004 before any in-game test with a pre-existing item
- Phases 2 to 4 touch different functions and can land in any order after Phase 1

## Notes

- `fire_mode` keeps naming the current mode; only `fire_modes` is new
- Old keys are deleted from the definitions and from migrated items in the same change
