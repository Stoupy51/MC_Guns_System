---

description: "Task list for zombies save and load"
---

# Tasks: Zombies Save and Load

**Input**: [spec.md](spec.md), [plan.md](plan.md)

**Tests**: No automated tests. Constitution principle V: each subsystem gets a named in-game round-trip check, and the feature is not done until the Phase 6 matrix passes in full.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 save, US2 load, US3 co-op roster

---

## Phase 1: Setup

- [ ] T001 Create `src/functional/zombies/save/` with `__init__.py` exposing `generate_zombies_save()`, and wire it from `src/functional/zombies/__init__.py`
- [ ] T002 Add the `mgs:zombies_saves` storage and initialize `slots` to `[]` on load in `src/functional/zombies/save/slots.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The schema and the slot primitives both halves depend on. Writing capture before the schema is how capture and restore drift.

- [ ] T003 Define the slot layout constants and a `SavedScore` dataclass table in `src/functional/zombies/save/schema.py`: one row per objective with its storage key, covering `points`, `kills`, `downs`, `passive`, `ability`, `qr_uses`, `dw_uses`, `lethal_type`
- [ ] T004 Extend `schema.py` to derive the perk rows from `PERK_DEFINITIONS` in `src/functional/zombies/machines/perks/definitions.py`, so a new perk is captured without touching this feature
- [ ] T005 Implement slot read, write, overwrite and delete in `src/functional/zombies/save/slots.py`, keyed by index, with a fixed slot count
- [ ] T006 Add the between-rounds availability score, set in `src/functional/zombies/game/round/completion.py` for the 5s gap and cleared when the next round starts

**Checkpoint**: A slot can be written and read back by hand with `/data`.

---

## Phase 3: User Story 1 - Save a run between rounds (Priority: P1) MVP half

**Goal**: A run becomes a slot compound that survives a server restart.

**Independent Test**: Save at round 17, then `/data get storage mgs:zombies_saves slots[0]` and check every field against the screen.

### Capture

- [ ] T007 [US1] Capture game meta in `src/functional/zombies/save/capture.py`: map id, variant, round and state from `storage mgs:zombies game`
- [ ] T008 [US1] Capture per-player scores by iterating the `schema.py` table, one entry per in-game player, with UUID and name
- [ ] T009 [US1] Capture per-player `max_health` (Juggernog sets base 40, so the raw attribute is not enough on its own)
- [ ] T010 [US1] Capture each player's whole `Inventory` NBT into their save entry
- [ ] T011 [P] [US1] Capture power state from `#zb_power` and the Pack-a-Punch unlock flag
- [ ] T012 [P] [US1] Capture opened door group ids from `src/functional/zombies/objects/doors.py` and the `mgs.spawn_unlocked` groups they granted
- [ ] T013 [P] [US1] Capture mystery box position, use count and moved flag
- [ ] T014 [P] [US1] Capture per-player wallbuy purchases and barricade repair state
- [ ] T015 [US1] Assemble the slot compound and write it through `slots.py`, then run the normal game stop

### Save UI

- [ ] T016 [US1] Add the "Save & Quit" admin-menu entry in `src/functional/zombies/save/ui.py`, gated on the T006 availability score, disabled with a reason during a round
- [ ] T017 [US1] Build the slot picker dialog following the `zombies/admin/powerups` `register_dialog` pattern, with a name field and an overwrite confirmation on an occupied slot

**Checkpoint**: Runs can be saved. Nothing can load them yet, which is fine.

---

## Phase 4: User Story 2 - Load a saved run (Priority: P1) MVP half

**Goal**: A slot becomes a live game identical to the one that was saved.

**Independent Test**: Save at round 17, restart the server, load, and diff against a pre-save screenshot.

### Load flow

- [ ] T018 [US2] Implement the load entry in `src/functional/zombies/save/restore.py`: validate the saved map id still exists and abort loudly, changing nothing, if it does not
- [ ] T019 [US2] Run the normal `zombies/start` on the saved map and variant first, so every subsystem initializes the way it always does
- [ ] T020 [US2] Replay game meta: set `game.round` and the round counter so the next round is the saved round plus one

### Replay, never reconstruct

- [ ] T021 [US2] Replay power by calling `power/turn_on` when saved, not by setting `#zb_power` directly
- [ ] T022 [US2] Replay each opened door by calling that door's own open function, so the block removal, the linked group and the spawn unlock all happen the way they normally do
- [ ] T023 [US2] Replay the Pack-a-Punch unlock through its own unlock path
- [ ] T024 [P] [US2] Replay mystery box position, uses and moved flag
- [ ] T025 [P] [US2] Replay barricade repair state and per-player wallbuy purchases

### Per-player restore

- [ ] T026 [US2] Match saved players to online players by UUID and restore every score from the `schema.py` table
- [ ] T027 [US2] Restore perks: set each `mgs.zb.perk.<id>` score, add the matching `mgs.perk.<id>` tag, and run each perk's `commands` so its attributes and special scores are applied rather than only its bookkeeping
- [ ] T028 [US2] Apply `max_health` before filling health, or a Juggernog player's fill clamps to 20
- [ ] T029 [US2] Restore the inventory through the existing `zombies/inventory/restore_inventory`, feeding the saved list into `mgs:temp _restore.items`
- [ ] T030 [US2] Refresh the perk display items and the info paper so the restored state is visible immediately

### Load UI

- [ ] T031 [US2] Add the saved-slot list to the setup dialog next to "Select Map" in `src/functional/zombies/save/ui.py`, showing name, map, round and saved date
- [ ] T032 [US2] Add slot deletion from the same list

**Checkpoint**: The solo save-load loop works end to end. This is the shippable MVP.

---

## Phase 5: User Story 3 - Load a co-op run with a different roster (Priority: P2)

**Goal**: A load never blocks on a missing player.

- [ ] T033 [US3] Skip or park in spectator any saved player who is not online, and log which ones were skipped
- [ ] T034 [US3] Treat a player who joins and is not in the save as a normal fresh joiner, with no inherited state
- [ ] T035 [US3] Verify Quick Revive solo pricing recomputes correctly for the loaded roster rather than the saved one

---

## Phase 6: Per-subsystem verification matrix

**Purpose**: This is the phase the whole feature was deferred for. Every row is an in-game round trip: set the state, save, restart, load, verify.

- [ ] T036 Round and spawn pacing: the loaded round spawns the right count at the right cadence
- [ ] T037 Points, kills, downs and the sidebar all match
- [ ] T038 Perks: every perk's effect is live, not just its icon. Juggernog HP, Speed Cola reload, Stamin-Up move speed, PhD fall immunity
- [ ] T039 Quick Revive specifically: `qr_uses` restores and the machine blocks or allows rebuy accordingly
- [ ] T040 Inventory: PaP level, camo, magazine contents, reserve ammo, slot tags, and the lethal/tactical slots
- [ ] T041 Doors: open doors are open, pathable, and their spawn groups are unlocked. Closed doors are still buyable
- [ ] T042 Power: every power-gated system (traps, perk machines, the Pack-a-Punch) behaves as it did
- [ ] T043 Mystery box: correct position, use count, and the next roll costs the right thing
- [ ] T044 Barricades: repaired boards are repaired, broken ones are broken, and zombies path through them correctly
- [ ] T045 Traps: cooldowns are clean rather than mid-cycle
- [ ] T046 Map editor round trip: save, edit the map, then confirm a load against the edited map fails safely rather than half-applying

---

## Phase 7: Polish

- [ ] T047 Update `src/functional/zombies/README.md`: delete §11 and fix the pre-restructure module names it still uses (`perks.py`, `round.py`, `power.py`)
- [ ] T048 Add save and load to the root `README.md` zombies feature list
- [ ] T049 `ruff check src --fix` and a clean `beet build`

---

## Dependencies & Execution Order

- **Phase 2** blocks everything. The schema is the contract both halves read
- **Phase 3 (US1)** and **Phase 4 (US2)** are sequential in practice: there is nothing to load until something saves
- Within Phase 3, T011 to T014 are independent captures and can be written in parallel
- Within Phase 4, replay order matters: start, then power, then doors, then per-player. A door replayed before start has nothing to open
- **Phase 6** depends on Phases 3 and 4 and gates the release

---

## Implementation Strategy

Solo first, all the way through Phase 6. Co-op (User Story 3) is a small addition on top of a proven
loop, and debugging a broken restore with three players is far harder than with one.

Do not ship after Phase 4. A save-load that passes a smoke test and fails Phase 6 is worse than no
feature: it silently corrupts a run people care about.

## Notes

- Restore is replay. Any task that writes a block or a tag a subsystem owns is doing it wrong
- Commit per subsystem captured or replayed
- The `saved_at` gametime is for display only; nothing keys off it
