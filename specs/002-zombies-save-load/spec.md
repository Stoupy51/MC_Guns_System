# Feature Specification: Zombies Suspend, Resume, Save and Load

**Feature Branch**: `002-zombies-save-load`

**Created**: 2026-08-15, rewritten 2026-10-16

**Status**: Draft

**Input**: A zombies run must survive a server restart, and a run must be storable to come back to it later.

## Context

A zombies run dies today as soon as no player of the run is online. `zombies/game_tick` counts living
players with `@a[scores={mgs.zb.in_game=1,...}]`, and `@a` only sees online players. When the last
player disconnects, or when a server restarts with a run in progress, the count is 0 for two ticks and
`zombies/game_over` ends the run. Its cleanup only resets online players, so players who were offline
keep `mgs.zb.in_game=1`, their points and their zombies inventory, and come back into a lobby with stale
run state.

Most of a run already persists by itself: the map elements (doors, barricades, perk machines, traps,
boxes, Pack-a-Punch) are entities whose scores live in the world, players keep their inventory, and
the round state is in scores and `storage mgs:zombies`. So the cheapest way to keep a run is to stop
killing it. Taking a run out of the world, to free the server for another map or mode, is the
expensive part, and the second half of this spec.

### User Story 1 - A run survives disconnects and restarts (Priority: P1)

Three players are at round 22. The server restarts for an update. When they reconnect, the run is
paused where it was, and it resumes when they are back.

**Why this priority**: It fixes a loss of progress that happens today, and every later story builds on it.

**Independent Test**: Solo run, round 5, quit the world mid-round, reopen it: the run is paused on
round 5 with the same zombies, points and inventory, and resumes after the countdown.

**Acceptance Scenarios**:

1. **Given** a run in progress, **When** every roster player is offline, **Then** the run is suspended, not ended: zombies get NoAI and every run timer stops.
2. **Given** a suspended run, **When** a roster player connects, **Then** they are put back in the run (team, gamemode, post effects, sidebar) and a 5 s countdown resumes it.
3. **Given** a co-op run where one player disconnects, **When** the others are still online, **Then** the run continues and the absent player is no longer counted as alive or downed.
4. **Given** that absent player reconnects, **When** the run is still going, **Then** they rejoin with the inventory, points and perks they left with, at a spawn point.
5. **Given** a run that ended while a roster player was offline, **When** that player connects, **Then** their zombies state is cleared (in_game, points, perks, zombies inventory) and they land in the lobby.
6. **Given** a run in progress, **When** an operator presses Pause in the admin menu, **Then** the run is suspended exactly as in AC1 until an operator resumes it.

---

### User Story 2 - Save a run between rounds and free the server (Priority: P2)

A group stops at round 30 on Kino and wants to play multiplayer tonight. Between two rounds, the host
picks "Save & Quit", names the slot "Kino r30", and the run ends with nothing left on the map. A week
later they load the slot and start round 31 with the same points, perks, guns and opened doors.

**Why this priority**: Only one zombies run can exist on a server at a time, and the other modes share
the world. Suspension keeps the run but blocks the server; a slot frees it.

**Independent Test**: Save at round 17, start and finish another zombies map, load the slot: round 18
starts with the round 17 state, compared field by field with a dump taken before saving.

**Acceptance Scenarios**:

1. **Given** the gap after `round_complete`, **When** the host opens the admin menu, **Then** "Save & Quit" is available; during a round it is shown disabled with the reason.
2. **Given** a save, **When** it completes, **Then** the slot holds everything in FR-008, and the run stops as a normal stop does.
3. **Given** a slot, **When** it is loaded, **Then** the map starts through the normal `zombies/start` and the saved state is replayed on top, silently: no door announces, no sounds, no point charges.
4. **Given** a slot saved on an older pack version, **When** it is loaded, **Then** every weapon is rebuilt from the current item definition, keeping its Pack-a-Punch level, camo, magazine and reserve ammo.
5. **Given** the saved map no longer exists, **When** the slot is loaded, **Then** the load fails with a message and nothing changes.
6. **Given** a map element of the save no longer exists in the map, **When** the slot is loaded, **Then** that element is skipped and listed in a warning to the host.

---

### User Story 3 - Load with a different roster (Priority: P3)

A 3-player save is loaded with 2 of them online. The third connects an hour later and gets their own
state back.

**Acceptance Scenarios**:

1. **Given** a saved player is offline at load, **When** the run starts, **Then** their saved state is kept aside and the run starts without them.
2. **Given** that player connects during the loaded run, **When** they join, **Then** they get their saved state, not a fresh joiner's.
3. **Given** a player who was not in the save joins, **When** they join, **Then** they join as a fresh late joiner.

### Edge Cases

- A player disconnects while downed. On reconnect they are downed with the bleed-out time they had left, since suspension stopped it. In solo, Quick Revive rules apply as if they never left.
- The server stops during the 5 s gap between rounds. The next round starts after the resume countdown.
- A Who's Who clone or a Tombstone is out when the run is suspended. Both are entities and persist; their timers stop with the rest.
- A power-up on the ground at save time is lost. Saving is between rounds, when few are left, and the cost is accepted.
- Zombies alive at suspension stay where they are, NoAI. Saving needs an empty map, which the between-rounds rule gives.
- A player renamed their account between save and load. Players are matched by UUID, not name.
- The world is copied: slots and suspended runs are copied with it, since both live in the world.

## Requirements *(mandatory)*

### Functional Requirements

**Suspend and resume**

- **FR-001**: The game-over check MUST count only online roster players, and MUST suspend the run instead of ending it when none is online.
- **FR-002**: Suspension MUST reuse the operator freeze (`zombies/freeze_world`), MUST stop every run timer (round, spawn, power-up, box move, trap, perk, ability, bleed-out, Dying Wish, the 5 s gap between rounds), and MUST be shown as "PAUSED" to the roster.
- **FR-003**: A roster player connecting MUST be detected with a `custom:leave_game` counter. Team, gamemode, scores, inventory and attributes persist in the player data, post effects are reset by `player/fx_after_rejoin`, and a player connecting during a freeze is frozen too.
- **FR-004**: Resuming MUST follow a 5 s countdown, cancelled if every roster player leaves again.
- **FR-005**: A connecting player whose run ended while they were away MUST get the same cleanup as a player online at stop (`zombies/reset_player`). Their `mgs.zb.run` differs from `#zb_run`, or no run is in progress.
- **FR-006**: Operators MUST be able to pause, resume and end a suspended run from the admin menu.

**Save and load**

- **FR-007**: Saving MUST only be possible in the gap after `round_complete`, and MUST end the run through the normal stop afterwards.
- **FR-008**: A slot MUST capture: format version, pack version, map id, variant, round, `saved_at`; per player (by UUID) every `mgs.zb.*` score of the schema table, perk tags and paid perks, `max_health`, the `Inventory`, the Tombstone and Who's Who inventories; and the map state: power, Pack-a-Punch state, opened doors and partial door payments, unlocked spawn groups, barricade boards, mystery box position, uses, moved flag and `#mb_dry_ray_gun`, Der Wunderfizz position, partial perk payments, trap cooldowns, and the dog round schedule (`#zb_dog_mod`).
- **FR-009**: The captured scores MUST come from one schema table of dataclass rows used by both capture and restore.
- **FR-010**: Loading MUST run `zombies/start` on the saved map and variant first, then replay the state through silent variants of the subsystems' own functions (door open, power on, Pack-a-Punch unlock, box placement), never by writing their blocks or tags directly.
- **FR-011**: Loading MUST rebuild every weapon item from the current definition, carrying over Pack-a-Punch level, camo, magazine contents and reserve ammo.
- **FR-012**: Loading MUST refuse a missing map, skip and report missing elements, and refuse a format version it does not know.
- **FR-013**: Slots MUST be a fixed list of 5 in `storage mgs:zombies_saves`, each overwritable after confirmation and deletable.
- **FR-014**: The save UI MUST be in the admin menu, the load UI a slot list on the setup dialog.

**Roster**

- **FR-015**: A saved player offline at load MUST keep their saved state in the run's pending list until they join or the run ends.

### Key Entities

- **Roster**: Players with `mgs.zb.in_game=1`, online or not. Their scores persist offline; online-ness is read with `@a`.
- **Run id**: `#zb_run`, incremented at each start, copied to `mgs.zb.run` of the roster and of late joiners, zeroed by `zombies/reset_player`.
- **Suspension**: `#zb_freeze` at 2, where 1 is the operator freeze. `game.state` stays `"active"`, so joins and admin actions keep working.
- **Save slot**: One entry of `mgs:zombies_saves slots[]`.
- **Schema row**: `SavedScore(objective, key)` for per-player scores, `SavedMapScore(tag, objective, key)` for map element scores.

```text
{ format:1, pack:"5.1.0", name:"Kino r30", map:"kino", variant:"zonweeb", round:30, saved_at:<gametime>,
  players:[ {uuid:[I;..], name:"Stoupy51", scores:{points:.., kills:.., ...}, perks:[..], max_health:..,
             inventory:[..], tombstone:[..], whos_who:[..]} ],
  map:{ power:1b, pap:{..}, doors:[{id:.., open:1b, paid:..}], spawns:[..], barricades:[{id:.., boards:..}],
        box:{pos:[..], uses:.., moved:1b, dry_ray_gun:..}, wunderfizz:{pos:[..]}, perks:[{id:.., paid:..}],
        traps:[{id:.., cd:..}], dog_mod:.. } }
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A solo run quit and reopened mid-round resumes on the same round with the same zombies, points, perks and inventory.
- **SC-002**: A co-op run survives a server restart, and resumes when the first player is back.
- **SC-003**: A player who left while their run ended comes back to a clean lobby state.
- **SC-004**: A run saved at round 17 and loaded after another full zombies game starts round 18 with every FR-008 field equal to the pre-save dump.
- **SC-005**: A Pack-a-Punched, camo'd weapon saved on one pack version loads on the next with its level, camo and ammo.
- **SC-006**: No save can be taken during a round or a dog round.

## Assumptions

- US1 needs no new state: suspension is a value of the existing freeze score.
- Five slots are enough; no paging in the picker.
- Saves are per world. Moving a save between worlds is out of scope.
- The between-rounds rule is permanent: mid-round saving would mean serializing live zombies, grenades, power-ups and downed players.
