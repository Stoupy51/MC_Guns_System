# Feature Specification: Zombies Save and Load

**Feature Branch**: `002-zombies-save-load`

**Created**: 2026-08-15

**Status**: Draft

**Input**: [src/functional/zombies/README.md](../../src/functional/zombies/README.md) §11, "Zombies - save a game and load it later [NOT IMPLEMENTED - specced only]".

## User Scenarios & Testing *(mandatory)*

Black Ops "Save & Quit": freeze a run to a slot, come back another day, carry on from the same round
with the same points, perks, guns and map state.

This was left unbuilt deliberately. It is the only backlog item that has to serialize every subsystem
at once, and a half-correct restore silently corrupts a map: doors that look shut but are pathable, a
mystery box that cannot be bought, perks nobody owns. It needs an in-game verification pass per
subsystem, which is what the task list below is built around.

### User Story 1 - Save a run between rounds (Priority: P1)

A solo player finishes round 17, opens the admin menu during the gap before round 18, picks a slot,
names it, and the game ends cleanly with the run stored.

**Why this priority**: Without a save there is nothing to load. It is also the half that can be
verified on its own by inspecting the storage compound, with no restore logic written yet.

**Independent Test**: Save at round 17, then `/data get storage mgs:zombies_saves slots[0]` and check
every field in the layout below is populated and matches what was on screen.

**Acceptance Scenarios**:

1. **Given** the 5s gap after `round_complete`, **When** the player opens the admin menu, **Then** a "Save & Quit" entry is available.
2. **Given** a round is in progress, **When** the player opens the admin menu, **Then** the "Save & Quit" entry is present but disabled, with a reason.
3. **Given** a save completes, **When** it finishes, **Then** the game stops the way a normal stop does, with no orphan entities left behind.
4. **Given** an occupied slot is picked, **When** the player confirms the overwrite, **Then** the old save is replaced and not merged.

---

### User Story 2 - Load a saved run (Priority: P1)

The same player comes back the next day, picks the slot from the setup dialog, and lands in round 18
on the same map with their points, perks, guns and every door they had opened.

**Why this priority**: The other half of the same feature. P1 with User Story 1 because neither is
worth shipping alone.

**Independent Test**: Save at round 17, stop the server, restart it, load the slot, and compare the
sidebar, the perk row, the inventory and the map against a screenshot taken before the save.

**Acceptance Scenarios**:

1. **Given** a saved slot, **When** the player loads it, **Then** the round counter, points, kills and downs match the saved values.
2. **Given** a saved slot where power was on, **When** it loads, **Then** power is on and every system it gates is live.
3. **Given** a saved slot with doors opened, **When** it loads, **Then** those doors are open, their blocks are gone, and the spawn points each door group unlocks are tagged unlocked.
4. **Given** a saved slot with a Pack-a-Punched weapon, **When** it loads, **Then** the weapon keeps its PaP level, camo, ammo counts and slot tags.
5. **Given** a saved slot, **When** it loads, **Then** the mystery box is at its saved position with its saved use count.

---

### User Story 3 - Load a co-op run with a different roster (Priority: P2)

A 3-player run is saved. Two of the three come back. The run loads with those two restored and the
third parked rather than blocking the load.

**Why this priority**: Co-op is where the feature is most wanted, but a solo save-load loop has to work
first. Blocking the load on a missing player would make the feature useless in practice.

**Independent Test**: Save a 2-player run, load it with only one of them online, and confirm the
present player is fully restored and the absent one does not break anything.

**Acceptance Scenarios**:

1. **Given** a saved player is offline, **When** the slot loads, **Then** they are skipped or parked in spectator and the game starts normally.
2. **Given** a player joins who was not in the save, **When** they join, **Then** they are treated as a fresh joiner rather than inheriting someone else's state.

### Edge Cases

- Saving mid-round would require serializing live zombies, thrown grenades, active power-ups, downed bodies and in-flight traps. The between-rounds constraint removes all of it and must not be relaxed.
- The saved map may have been edited between save and load. Element ids can no longer exist.
- A saved weapon may reference a weapon id that has since been renamed or removed from the item database.
- The save is a storage compound in the world save, so copying the world copies the saves and deleting the world deletes them.
- A player restored with Juggernog needs `max_health` base 40 applied before their health is filled, or the fill clamps to 20.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Saving MUST only be possible between rounds, in the 5s gap after `round_complete`.
- **FR-002**: A save MUST be a single compound appended to `slots[]` in a dedicated `mgs:zombies_saves` storage. No files, no external state.
- **FR-003**: A save MUST capture game meta: map id, variant, round, and state, from `storage mgs:zombies game`.
- **FR-004**: A save MUST capture per-player scores: `mgs.zb.points`, `kills`, `downs`, `passive`, `ability`, `qr_uses`, `dw_uses`, `lethal_type`, every `mgs.zb.perk.<id>` from `PERK_DEFINITIONS`, the matching `mgs.perk.<id>` tags, and `max_health`.
- **FR-005**: A save MUST capture each player's whole `Inventory` NBT, since guns carry PaP level, camo, ammo and slot tags in `custom_data`.
- **FR-006**: A save MUST capture map progress: `#zb_power`, the Pack-a-Punch unlock, opened door group ids, the `mgs.spawn_unlocked` tags those groups grant, mystery box position and use count, and barricade repair state.
- **FR-007**: Loading MUST run the normal `zombies/start` on the saved map and variant first, so every subsystem initializes the way it always does, and only then replay the saved state on top.
- **FR-008**: Loading MUST replay opened doors by calling each door's own open function rather than by editing blocks directly.
- **FR-009**: Loading MUST reuse the existing `zombies/inventory/restore_inventory`, which already takes a copied `Inventory` list in `mgs:temp _restore.items`.
- **FR-010**: Loading MUST skip or park in spectator any saved player who is not online.
- **FR-011**: The save UI MUST be an admin-menu button opening a slot picker dialog, following the `zombies/admin/powerups` pattern.
- **FR-012**: The load UI MUST be a slot list on the setup dialog, next to "Select Map".
- **FR-013**: A load MUST fail loudly and change nothing if the saved map id no longer exists.

### Key Entities

- **Save slot**: One entry in `mgs:zombies_saves slots[]`. Name, map id, variant, round, `saved_at` gametime, a player list and a map-state compound.
- **Saved player**: UUID, name, every per-player score, perk ownership, `max_health`, and an `Inventory` NBT list.
- **Map state**: Power flag, Pack-a-Punch unlock flag, opened door group ids, unlocked spawn group ids, mystery box position/uses/moved, and per-player wallbuy purchases.

Suggested layout, kept from the original spec:

```text
{ name:"Saturday run", map:"<map id>", variant:"vanilla|zonweeb", round:17, saved_at:<gametime>,
  players:[ {uuid:[I;..], name:"Stoupy51", points:.., kills:.., downs:.., lethal_type:.., ability:..,
             passive:.., qr_uses:.., dw_uses:.., max_health:.., perks:{juggernog:1,..},
             inventory:[<player Inventory NBT>]} ],
  map_state:{ power:0|1, pap_unlocked:0|1, doors:[<group ids opened>], spawns:[<unlocked group ids>],
              box:{pos:[..], uses:.., moved:0|1}, wallbuys:[<bought ids per player>] } }
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A solo run saved at round 17 and loaded after a full server restart resumes at round 18 with identical points, kills, downs, perks, weapons and ammo.
- **SC-002**: Every door that was open before the save is open after the load, and every spawn point it unlocked still spawns zombies.
- **SC-003**: A Pack-a-Punched, camo'd weapon survives the round trip with its PaP level, camo, magazine contents and slot tags intact.
- **SC-004**: Loading a 3-player save with 2 players online starts a working 2-player game.
- **SC-005**: No save can be taken while a round is live, verified by trying during a round and during a dog round.

## Assumptions

- Storages persist in the world save, so a slot is a compound and never a file.
- Between-rounds-only is a hard design constraint, not a first-iteration simplification.
- The existing `restore_inventory` path, built for Who's Who and Tombstone, is correct and reusable as-is.
- Slot count is small and fixed (for example 5). No pagination is needed in the picker.
- Cross-version loading is out of scope. A save taken on one pack version may refuse to load on another.
- `src/functional/zombies/README.md` names pre-restructure modules (`perks.py`, `round.py`, `power.py`). The current paths are the packages under `src/functional/zombies/`; the README needs updating alongside this work.
