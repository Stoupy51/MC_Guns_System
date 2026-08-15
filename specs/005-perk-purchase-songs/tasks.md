---

description: "Task list for perk purchase songs"
---

# Tasks: Perk Purchase Songs

**Input**: [spec.md](spec.md), [plan.md](plan.md)

**Tests**: No automated tests. The test is buying every perk and listening.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 the 10 staged clips, US2 the 4 missing ones
- **[HUMAN]**: Needs a person, not a build

---

## Phase 1: Setup

- [ ] T001 Rename `assets/zombies_perk_songs/jungernog.ogg` to `juggernog.ogg` (FR-002)
- [ ] T002 Confirm the perk ids the files must match, from `PERK_DEFINITIONS` in `src/functional/zombies/machines/perks/definitions.py`: `juggernog`, `speed_cola`, `double_tap`, `quick_revive`, `mule_kick`, `stamin_up`, `phd_flopper`, `deadshot`, `timeslip`, `electric_cherry`, `tombstone`, `whos_who`, `dying_wish`, `widows_wine`

---

## Phase 2: User Story 1 - Buying a perk plays its jingle (Priority: P1) MVP

**Goal**: The 10 staged clips play on purchase.

**Independent Test**: Buy each of the 10 and confirm each plays its own jingle.

- [ ] T003 [US1] Move the 10 clips to `assets/sounds/zombies/perks/<perk_id>.ogg`, renaming each staged filename to its perk id (`doubletap` becomes `double_tap`, `mulekick` becomes `mule_kick`, `phdflopper` becomes `phd_flopper`, `quickrevive` becomes `quick_revive`, `speedcola` becomes `speed_cola`, `staminup` becomes `stamin_up`, `whoswho` becomes `whos_who`)
- [ ] T004 [US1] Delete the now-empty `assets/zombies_perk_songs/` directory
- [ ] T005 [US1] Build and confirm all 10 register as `mgs:zombies/perks/<perk_id>`, testing one with `/playsound mgs:zombies/perks/juggernog`
- [ ] T006 [US1] Add a `has_song: bool = False` field to `PerkDef` in `definitions.py`, with a one-line docstring under it, and set it on the 10 perks that now have a clip (FR-004)
- [ ] T007 [US1] Emit the `playsound` from the generated `zombies/perks/apply/<perk_id>` in `apply.py`, only when `has_song` is set, matching the volume, pitch and audience conventions of `pu_snd` in `src/functional/zombies/rewards/powerups/types.py` (FR-003, FR-006)
- [ ] T008 [US1] Decide positional at the machine versus private to the buyer, and write the reason into the comment above the generated line
- [ ] T009 [US1] Buy all 14 perks in one game: the 10 play their own jingle, the 4 without clips are silent with a clean client log (SC-001, SC-002)
- [ ] T010 [US1] Buy two perks at nearby machines simultaneously and confirm the result is not obviously broken

**Checkpoint**: 10 of 14 perks have their jingle. Shippable as-is.

---

## Phase 3: Non-purchase grants (Priority: P1)

**Goal**: Settle FR-007 rather than letting the behavior fall out of the code by accident.

- [ ] T011 Decide whether the jingle plays when a perk is granted without a purchase: the random-perk power-up, Wunderfizz, and the Who's Who and Tombstone restores
- [ ] T012 Implement that decision. A restore can regrant five perks in one tick, so if restores are excluded, exclude them explicitly rather than relying on `apply` not being called
- [ ] T013 Verify a Tombstone recovery of a full perk loadout produces the intended result (SC-004)

---

## Phase 4: User Story 2 - The remaining four clips exist (Priority: P2)

**Goal**: All 14 perks have a jingle.

Explicitly last, per the original backlog note. Blocked on a human, not on code.

- [ ] T014 [HUMAN] [US2] Source the final-seconds cuts for `electric_cherry`, `widows_wine`, `timeslip` and `dying_wish`
- [ ] T015 [US2] Drop them into `assets/sounds/zombies/perks/` and set `has_song` on those four rows. No other code change should be needed (SC-003)
- [ ] T016 [US2] Buy all four and confirm each plays

---

## Phase 5: Polish

- [ ] T017 Delete §7 from `src/functional/zombies/README.md`
- [ ] T018 `ruff check src --fix` and a clean `beet build`

---

## Dependencies & Execution Order

- T001 and T002 before anything else
- T003 before T005, T005 before T007
- Phase 3 depends on Phase 2 and should not be deferred: it is where the surprising behavior lives
- Phase 4 is blocked on T014, which is a human task with no schedule

---

## Implementation Strategy

Phase 2 plus Phase 3 is the whole feature for practical purposes. Phase 4 is four files dropped into a
directory whenever someone gets around to finding them.

## Notes

- The staged filenames do not match the perk ids. T003 is a rename, not a copy
- If a clip turns out to be the wrong cut, that is an asset problem, not a code problem
