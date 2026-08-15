# Feature Specification: Fire Sound Variants and Tactical Grenade Slotting

**Feature Branch**: `006-weapon-fire-modes-tacticals`

**Created**: 2026-08-15

**Status**: Draft

**Input**: Two long-standing `# TODO` comments: [src/functional/weapon/firing/sound.py:82](../../src/functional/weapon/firing/sound.py) and [src/config/stats/weapons/grenades.py:100](../../src/config/stats/weapons/grenades.py).

## User Scenarios & Testing *(mandatory)*

Two small, unrelated gaps that have sat in the tree long enough to be worth closing together. Both are
bugs dressed as TODOs: in each case the data says one thing and the code does another.

### User Story 1 - Smoke and flash go in the tactical slot (Priority: P1)

A zombies player buys a smoke grenade and it lands in the tactical slot alongside the monkey bomb,
leaving the lethal slot for the grenade that actually kills things. Right now buying smoke costs them
their frags.

**Why this priority**: It is a real gameplay loss, not a polish item. Smoke and flash are listed in
`LETHAL_GRENADE_IDS`, so they occupy hotbar.7 and overwrite the player's lethal on every refill path:
round-end replenish, Max Ammo, and item recovery. A player who bought smoke can no longer carry frags.

**Independent Test**: In zombies, buy a smoke grenade from a wallbuy and confirm it goes to the
tactical slot and the lethal slot still holds frags after the next round-end replenish.

**Acceptance Scenarios**:

1. **Given** a player with frags, **When** they buy a smoke grenade, **Then** the smoke goes to the tactical slot and the frags stay in the lethal slot.
2. **Given** a player holding smoke and a monkey bomb, **When** they buy one of them again, **Then** the duplicate check behaves the way it does for two lethals, rather than silently replacing the other tactical.
3. **Given** a round ends, **When** grenades replenish, **Then** the lethal slot refills with the player's recorded lethal type and the tactical slot refills with their tactical.
4. **Given** a Max Ammo drops, **When** it resolves, **Then** both slots refill correctly.
5. **Given** a player's `mgs.zb.lethal_type` was set to smoke or flash under the old enum, **When** they play after the change, **Then** they get a valid lethal rather than an empty slot.

---

### User Story 2 - A weapon's alternate fire sound plays for the right fire mode (Priority: P2)

The SPAS-12 sounds different when it is fired in its alternate mode, which is why it ships two fire
clips.

**Why this priority**: Audio polish affecting exactly one weapon, versus a slot bug affecting a whole
mode. Real, but not urgent.

**Independent Test**: Fire the SPAS-12 in each fire mode and confirm the two clips are distinguishable
and that each mode consistently plays its own.

**Acceptance Scenarios**:

1. **Given** a weapon that defines both `fire` and `fire_alt`, **When** it is fired in its primary mode, **Then** `fire` plays.
2. **Given** the same weapon, **When** it is fired in its alternate mode, **Then** `fire_alt` plays.
3. **Given** a weapon that defines only `fire`, **When** it is fired, **Then** `fire` plays, exactly as today.
4. **Given** a Pack-a-Punched weapon with a `pap_fire` sound, **When** it is fired, **Then** `pap_fire` still wins over both, as it does today.

### Edge Cases

- `LETHAL_GRENADE_IDS` order defines the `mgs.zb.lethal_type` enum, indexed from 0. Removing two entries renumbers it, so any saved or in-flight score referencing index 2 or 3 becomes invalid.
- Wallbuys record the lethal type by matching the bought weapon id against that list. Removing entries changes which purchases record a type at all.
- The Widow's Wine web grenade already overrides the lethal slot for its owners regardless of the recorded type, so it must keep doing so.
- `fire_alt` is currently defined by exactly one weapon, the SPAS-12. There is no second data point for what "alternate mode" means, and the fix must not assume more than the data supports.
- The SPAS-12's declared `FIRE_MODE` is `semi`. If it has no second mode in the data, the fix is to decide what `fire_alt` actually means before writing a mode check.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Smoke and flash grenades MUST be tactical, routed to the tactical slot the way the monkey bomb is via its `"tactical": True` flag.
- **FR-002**: `LETHAL_GRENADE_IDS` MUST contain only grenades that belong in the lethal slot.
- **FR-003**: Every refill path (round-end replenish, Max Ammo, item recovery, starting loadout) MUST fill the lethal and tactical slots independently.
- **FR-004**: The `mgs.zb.lethal_type` enum renumbering MUST be handled so an out-of-range value resolves to the default lethal rather than an empty slot.
- **FR-005**: Wallbuys MUST record a tactical purchase the way they record a lethal one, so a tactical also survives a refill.
- **FR-006**: The Widow's Wine web-grenade override MUST keep applying to the lethal slot for its owners.
- **FR-007**: The fire sound dispatch MUST select between `fire` and `fire_alt` by a documented condition rather than always preferring `fire_alt` when it exists.
- **FR-008**: `pap_fire` MUST keep taking priority over both when the weapon is Pack-a-Punched.
- **FR-009**: Both TODO comments MUST be deleted, not updated.

### Key Entities

- **Lethal slot**: hotbar.7. One grenade type per player, tracked by `mgs.zb.lethal_type`.
- **Tactical slot**: hotbar.6. Currently monkey-bomb only, identified by `"tactical": True` on the grenade definition.
- **Fire sound set**: Per weapon, some subset of `fire`, `fire_alt`, `pap_fire`, resolved at fire time from `storage mgs:gun all.sounds`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A zombies player can hold frags and smoke at the same time, and both survive a round-end replenish and a Max Ammo.
- **SC-002**: No player ends a round with an empty lethal or tactical slot as a result of the enum renumbering.
- **SC-003**: The SPAS-12's `fire` and `fire_alt` clips both play in game, each under a documented condition. Neither is dead audio.
- **SC-004**: Neither TODO comment remains in the tree.

## Assumptions

- The tactical slot can hold more than one type, exactly as the lethal slot does today. If it cannot, User Story 1 grows a per-player tactical-type score mirroring `lethal_type`.
- Nobody depends on smoke or flash being lethal. They deal no meaningful damage.
- `fire_alt` was authored for a real audible difference on the SPAS-12 rather than as a spare.
- No save data outside the current game references the lethal-type enum, so the renumbering only needs to survive a live game (until feature 002 ships, at which point saves reference it too).
