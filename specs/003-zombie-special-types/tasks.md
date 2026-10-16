---

description: "Task list for zombie special types"
---

# Tasks: Zombie Special Types

**Input**: [spec.md](spec.md), [plan.md](plan.md)

**Tests**: No automated tests. Each type closes on a round-jump check in game; the aura also closes on an F3+L measurement.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 fast and tank, US2 armed, US3 aura

---

## Phase 1: Setup

- [ ] T001 Move `src/functional/zombies/game/round/enemies.py` into the `src/functional/zombies/enemies/types/` package from plan.md, moving code only, and confirm `uv run python scripts/verify.py check` is empty before adding anything

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The type table and the spawn roll. Every type after this is a table row plus one module.

- [X] T002 Define a `ZombieType` dataclass (in `game/round/enemies.py` until T001 moves it to `src/functional/zombies/enemies/types/table.py`) with one explicit keyword-argument constructor call per type: id, distinguishing tag, speed factor, health factor, first round, spawn weight
- [ ] T003 Extract the BO health curve into `types/curve.py` (`calc_zombie_hp`, `apply_zombie_hp`, `apply_dog_hp`) and have every type call it instead of restating it
- [X] T004 Replace the hardcoded `data modify storage {ns}:temp _zpos.type set value "normal"` in `src/functional/zombies/game/round/spawning.py` with a weighted roll generated from the `types.py` table
- [X] T005 Gate the roll on the Zonweeb variant, so the Vanilla variant always rolls `normal` (FR-001), and skip it entirely on dog rounds (FR-009)
- [ ] T006 Verify the gate before any type exists: a Zonweeb game and a Vanilla game both still spawn only normal zombies, and nothing regressed

**Checkpoint**: The dispatch is live and provably inert. Types can be added one at a time.

---

## Phase 3: User Story 1 - The horde stops being one enemy repeated (Priority: P1) MVP

**Goal**: Fast and tank zombies spawn in Zonweeb waves and feel different to fight.

**Independent Test**: Zonweeb game, `/scoreboard players set #zb_round mgs.data 20`, watch a wave.

- [X] T007 [US1] Keep `types/normal` as the single reference: special types run it, then scale its speed and health by their table percentages
- [X] T008 [P] [US1] Implement `types/fast` in `types/fast.py`: speed above the round's normal value, health below it, and a distinguishing tag
- [X] T009 [P] [US1] Implement `types/tank` in `types/tank.py`: health well above the round's normal value, speed below it, and a distinguishing tag
- [X] T010 [US1] Make sure the fast type and the round-15 10% walker roll cannot combine into a fast zombie slower than a normal one
- [ ] T011 [US1] Verify tank health stays under the 2048 cap in `curve.py` at rounds 40, 50 and 80
- [X] T012 [P] [US1] Give fast and tank a visual difference (scale, equipment or a subtle glow) so they read from across a room
- [ ] T013 [US1] Verify the escort taxi speed derivation still matches at both ends: force a fast zombie and a tank zombie into an escort and confirm each taxi moves at its passenger's speed
- [ ] T014 [US1] Verify kills, points, power-up rolls, nukes, traps, barricades and round completion all treat both types as ordinary zombies
- [X] T015 [US1] Delete the fast and tank TODO comments

**Checkpoint**: Waves are varied. This alone is worth shipping.

---

## Phase 4: User Story 2 - A zombie that shoots back (Priority: P2)

**Goal**: An armed zombie that attacks at range and drops ammo.

- [X] T016 [US2] Implement `types/armed` base stats in `types/armed.py` and give it a visibly armed look
- [X] T017 [US2] Implement the ranged attack tick: line of sight check, cooldown, damage application, and a firing cue the player can hear and locate
- [X] T018 [US2] Gate the attack tick on armed zombies being alive, the same count-gated pattern the escort system uses, so it costs nothing when none are out
- [X] T019 [US2] Hook the guaranteed ammo power-up into `src/functional/zombies/rewards/powerups/drops.py` on armed-zombie death, bypassing the random roll
  Built on the Missions gun AI (`mob/default/on_new`, `mob/tick`, gated by `#armed_mob_count`); the Max Ammo drops from `on_zombie_dying` through `max_ammo_at_self`, shared with the last hound.
- [ ] T020 [US2] Verify the drop fires on every death path: shot, trap, nuke, and the round-end cleanup
- [X] T021 [US2] Delete the armed TODO comment

---

## Phase 5: User Story 3 - A zombie worth killing first (Priority: P3)

**Goal**: An aura zombie that makes nearby zombies tougher, and dies first because of it.

- [X] T022 [US3] Add the `aura` row to `types/table.py` with a hard cap of one alive at a time (FR-010)
- [X] T023 [US3] Implement `types/aura` in `types/aura.py`: base stats plus an unmistakable look, since the whole mechanic depends on players spotting it
- [X] T024 [US3] Implement the aura tick on an interval (roughly every 10 ticks), applying resistance to zombies in radius through an attribute modifier or a short effect that lapses on its own
  The tick runs once a second with a 2 s Resistance II, so it lapses on its own within 2 s of the aura zombie's death.
- [ ] T025 [US3] Make the resistance lift when the aura zombie dies, whether it lapses naturally or is cleared explicitly, and verify it on a nuke that kills the whole wave at once
- [ ] T026 [US3] Measure the aura tick with F3+L against a full horde, before and after, and confirm no measurable MSPT change (SC-005)
- [ ] T027 [US3] Verify a zombie inside the aura takes measurably more shots to kill than the same zombie outside it

---

## Phase 6: Polish

- [ ] T028 Tune the weight table across rounds 10, 20, 40 and 60 so waves stay varied without any one type dominating
- [X] T029 Add the special types to the root `README.md` zombies feature list
- [X] T030 `uv run python scripts/verify.py lint` and `uv run python scripts/verify.py validate` pass

---

## Dependencies & Execution Order

- **Phase 2** blocks every type. Nothing can spawn until the dispatch exists
- T007 blocks T008 and T009: they scale against the reference it establishes
- **Phase 3, 4 and 5** are independent of each other once Phase 2 is done, and are ordered by cost
- T028 depends on all shipped types existing

### Parallel Opportunities

- T008 and T009 are separate modules with no shared state
- T012 is asset and presentation work that can run alongside the stat work

---

## Implementation Strategy

Ship Phase 3 and stop if the budget runs out. Fast and tank deliver most of the felt variety for a
fraction of the cost, and neither adds a tick function.

Armed and aura are each a self-contained addition on a proven dispatch. Neither blocks the other.

## Notes

- One type per commit
- Never restate the round ladder from `types/normal` in another type. It is one table now
- Every new type carries `mgs.zombie_round`, or half the game stops counting it
