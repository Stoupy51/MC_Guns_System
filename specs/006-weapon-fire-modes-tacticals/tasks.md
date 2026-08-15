---

description: "Task list for fire sound variants and tactical grenade slotting"
---

# Tasks: Fire Sound Variants and Tactical Grenade Slotting

**Input**: [spec.md](spec.md), [plan.md](plan.md)

**Tests**: No automated tests. User Story 1 closes in a live zombies game, User Story 2 on the range.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 tactical slotting, US2 fire sound variants

The two stories are independent. Either can ship alone.

---

## Phase 1: User Story 1 - Smoke and flash go in the tactical slot (Priority: P1) MVP

**Goal**: Buying smoke or flash no longer costs the player their lethal grenade.

**Independent Test**: Buy smoke from a wallbuy, then let a round end. Frags are still in the lethal slot and smoke is in the tactical slot.

### Handle the enum before moving anything

- [ ] T001 [US1] Document in `src/config/stats/weapons/grenades.py` that `LETHAL_GRENADE_IDS` order defines the `mgs.zb.lethal_type` enum from 0, so its indices are load-bearing and reordering it renumbers live player scores
- [ ] T002 [US1] Make an out-of-range `lethal_type` fall back to the default lethal in `src/functional/zombies/player/inventory/grenades.py`, so a player carrying the old index 2 or 3 gets frags rather than an empty slot (FR-004)
- [ ] T003 [US1] Verify the fallback with the current list: set `mgs.zb.lethal_type` to 9 by hand, end a round, and confirm the slot refills with frags

### Move smoke and flash

- [ ] T004 [US1] Add `"tactical": True` to the smoke and flash grenade definitions in `grenades.py`, matching the monkey bomb, so the camo pipeline skips them and the inventory routes them to the tactical slot
- [ ] T005 [US1] Remove `smoke_grenade` and `flash_grenade` from `LETHAL_GRENADE_IDS` and delete the TODO comment on that line (FR-002, FR-009)
- [ ] T006 [US1] Extend the wallbuy purchase path in `src/functional/zombies/objects/wallbuys/` to record a tactical purchase the way it records a lethal, so a bought tactical survives a refill (FR-005)
- [ ] T007 [US1] Make every refill path fill the lethal and tactical slots independently: round-end replenish, Max Ammo, item recovery, and the starting loadout in `player/inventory/loadout.py` (FR-003)
- [ ] T008 [US1] Confirm the Widow's Wine web-grenade override still forces webs into the lethal slot for its owners on every refill path (FR-006)

### Verify

- [ ] T009 [US1] Buy smoke, then let a round end: smoke in tactical, frags in lethal (SC-001)
- [ ] T010 [US1] Buy a monkey bomb while holding smoke and confirm the tactical duplicate check behaves sensibly rather than silently replacing it
- [ ] T011 [US1] Trigger a Max Ammo and confirm both slots refill
- [ ] T012 [US1] Go down and recover, and confirm both slots come back correctly
- [ ] T013 [US1] Play a full game with no empty lethal or tactical slot at any point (SC-002)

**Checkpoint**: The slot bug is fixed. Shippable on its own.

---

## Phase 2: User Story 2 - A weapon's alternate fire sound plays for the right fire mode (Priority: P2)

**Goal**: Both SPAS-12 fire clips are live audio under a documented condition.

**Independent Test**: Fire the SPAS-12 in each condition on the range and hear the difference.

### Decide what `fire_alt` means before implementing the TODO

- [ ] T014 [US2] Listen to `assets/sounds/spas12/fire.ogg` and `fire_alt.ogg` and establish what actually differs between them
- [ ] T015 [US2] Check whether the SPAS-12 has a second fire mode at all. Its declared `FIRE_MODE` in `src/config/stats/weapons/shotguns.py` is `semi`, so the TODO's "mode check" may be describing a mode that was never implemented
- [ ] T016 [US2] Write the decision into a comment above the dispatch: either a real fire-mode check, an alternating variation on successive shots, or a distance or acoustics condition. If the answer is that `fire_alt` was a spare, delete the sound and the branch instead

### Implement

- [ ] T017 [US2] Replace the unconditional `if data ... fire_alt` branch in `src/functional/weapon/firing/sound.py` with the chosen condition, and delete the TODO comment (FR-007, FR-009)
- [ ] T018 [US2] Confirm `pap_fire` still wins over both when the weapon is Pack-a-Punched (FR-008)
- [ ] T019 [US2] Confirm every weapon that defines only `fire` is unchanged, since all but one are in that category
- [ ] T020 [US2] Fire the SPAS-12 under both conditions and confirm neither clip is dead audio (SC-003)

---

## Phase 3: Polish

- [ ] T021 Update the root `README.md` weapon framework list if the tactical slot description changed
- [ ] T022 `ruff check src --fix` and a clean `beet build`

---

## Dependencies & Execution Order

- T001 to T003 before T004 to T007. The enum fallback has to exist before the list shrinks, or the first player to load with an old score gets an empty slot
- T014 to T016 before T017. Implementing a "mode check" for a weapon with one mode produces a branch that never fires
- Phase 1 and Phase 2 are fully independent

---

## Implementation Strategy

Phase 1 alone is worth shipping and is the half with real gameplay impact.

Phase 2 may end in "delete the sound" rather than "add a check". That is a valid outcome and closes the
TODO just as well; T016 exists to make that a legitimate answer rather than a failure.

## Notes

- Both TODOs get deleted, not updated (FR-009)
- Commit the two stories separately; they share no files
