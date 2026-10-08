# Feature Specification: Fire Modes Faithful to the Original

**Feature Branch**: `008-original-fire-modes`

**Created**: 2026-10-08

**Status**: Draft

**Input**: An audit of every weapon in the original MGS (`based_of/datapack/data/mgs/function/guns/*` and `core/init/weapon_stat.mcfunction`) against `src/config/stats/weapons/*.py`, started from the SPAS-12's unused `fire_alt` clip (feature 006).

## User Scenarios & Testing *(mandatory)*

The pack already has a fire selector: dropping a gun cycles `auto`, `semi` and `burst`, narrowed by what the gun supports, and the actionbar shows the current mode.
What it selects between is wrong for most guns. The original stored a per-gun `burst` number that was never a burst mode: it was how many shots each detected click queued, so that holding the trigger gave continuous automatic fire.
The port read that number as a burst length, so fifteen automatic guns gained a 2 to 4 round burst they never had, the M16A4 gained an automatic mode it never had, the M249 gained semi and burst, and the SPAS-12 lost its semi-automatic mode.

### User Story 1 - Each gun offers the modes it originally had (Priority: P1)

A player drops an AK-47 to change its fire mode and cycles between automatic and semi-automatic only. An M16A4 cycles between a three-round burst and semi-automatic. A FAMAS cycles through all three. An M249 has nothing to cycle.

**Why this priority**: It is the visible bug. Fifteen guns expose a fake burst mode, and two guns expose modes their real counterpart and the original pack never had.

**Independent Test**: Give every gun with `/function mgs:_give_all`, drop each one repeatedly and read the actionbar mode indicator. The cycle matches the table in FR-002 for every gun.

**Acceptance Scenarios**:

1. **Given** an AK-47, **When** the player drops it repeatedly, **Then** the mode alternates between automatic and semi-automatic and never shows burst.
2. **Given** an M16A4, **When** the player drops it repeatedly, **Then** the mode alternates between three-round burst and semi-automatic and never shows automatic.
3. **Given** a FAMAS, **When** the player drops it repeatedly, **Then** the mode cycles automatic, burst, semi-automatic.
4. **Given** an M249, **When** the player drops it, **Then** the mode stays automatic.
5. **Given** a pistol, sniper rifle, pump shotgun other than the SPAS-12, or launcher, **When** the player drops it, **Then** nothing changes, as today.

---

### User Story 2 - The SPAS-12 switches between pump-action and semi-automatic (Priority: P1)

A player drops a SPAS-12 to switch it to semi-automatic. It now fires faster, with no pump between shots, ejects the shell as it fires, holds its spread when crouched, and sounds different to the shooter. Switching back restores the pump-action behaviour.

**Why this priority**: It is the one gun whose second mode is missing entirely, and its semi-automatic clips already ship unused.

**Independent Test**: Fire a SPAS-12 in each mode on the range. Pump-action: one shot every 16 ticks, the pump sound and the shell halfway through. Semi-automatic: one shot every 9 ticks, no pump, the shell out on the shot.

**Acceptance Scenarios**:

1. **Given** a SPAS-12 in pump-action, **When** it fires, **Then** the shooter hears `fire`, the pump plays and the shell ejects halfway through the cooldown, and the next shot is possible 16 ticks after it.
2. **Given** a SPAS-12 in semi-automatic, **When** it fires, **Then** the shooter hears `fire_semi`, no pump plays, the shell ejects on the shot, and the next shot is possible 9 ticks after it.
3. **Given** a crouching player, **When** they fire the SPAS-12, **Then** the spread is 190 in pump-action and 230 in semi-automatic.
4. **Given** a Pack-a-Punched SPAS-12 in semi-automatic, **When** it fires, **Then** the shooter hears `pap_fire_semi`.
5. **Given** any SPAS-12 mode, **When** another player hears the shot, **Then** they hear `fire` (or `pap_fire`), as in the original.

---

### User Story 3 - Burst fire keeps its own rhythm (Priority: P2)

The M16A4 fires its three rounds two ticks apart and the FAMAS on three consecutive ticks, and both then pause three ticks before the next burst.

**Why this priority**: The burst mode works today; only its timing differs from the original. Feel, not function.

**Independent Test**: Fire one burst from each gun and count ticks between shots and before the next burst is allowed.

**Acceptance Scenarios**:

1. **Given** an M16A4 in burst, **When** the player clicks once, **Then** three rounds fire two ticks apart and the next burst is possible three ticks after the third.
2. **Given** a FAMAS in burst, **When** the player clicks once, **Then** three rounds fire on consecutive ticks and the next burst is possible three ticks after the third.

### Edge Cases

- Every weapon item carries its stats, its supported modes and its current mode in its own data. Items already in players' worlds still say `can_burst` and may sit in `burst` mode.
- A gun whose stored current mode is no longer supported (an AK-47 left in burst) must not fire in that mode, and must not get stuck unable to fire.
- Switching mode mid-burst or mid-pump must not leave a shot queued or the pump sound playing in the new mode.
- A semi-automatic SPAS-12 switched to pump-action right after a shot must not skip the pump of the next shot or fire before the pump cooldown.
- Pack-a-Punch overrides (`PAP_STATS`) change cooldown and capacity; per-mode values must compose with them rather than replace them.
- Zombies wallbuys and the Mystery Box give fresh items, multiplayer loadouts give fresh items, and the map editor stores weapon ids only, so only items already held in a world carry stale mode data.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each gun MUST declare the exact list of fire modes it supports, in cycle order, and its default mode is the first one.
- **FR-002**: The supported modes MUST match the original pack:

  | Gun | Modes, default first |
  |---|---|
  | ak47, fnfal, aug, m4a1, g3a3, scar17, glock18, vz61, mp5, mac10, mp7, ppsh41, sten, rpk | auto, semi |
  | m16a4 | burst (3), semi |
  | famas | auto, burst (3), semi |
  | m249 | auto |
  | spas12 | pump, semi |
  | Every other gun | its single current mode |

- **FR-003**: `pump` MUST be a fire mode for single taps, where the pump sound and the shell ejection happen together halfway through the cooldown. The M500 and M590 already pump there; their shell moves from the shot to the pump. The original timed the SPAS-12 pump and shell 6 and 10 ticks after the shot; the halfway point is the port's existing rule for every pump gun.
- **FR-004**: A mode MUST be able to override, for its gun: the cooldown, the crouched accuracy, the shooter's fire sound, the Pack-a-Punch fire sound, and when the shell ejects.
- **FR-005**: Another player MUST always hear the gun's base `fire` (or `pap_fire`) sound, whatever the mode.
- **FR-006**: A burst MUST be able to declare the delay between its shots separately from the cooldown that follows it (M16A4: 2 then 3, FAMAS: 1 then 3).
- **FR-007**: A held item whose current mode is no longer supported MUST resolve to its gun's default mode the next time it is fired or switched, without any player action.
- **FR-008**: A held item whose supported-mode data predates this feature MUST follow its gun's current mode list.
- **FR-009**: Changing mode MUST play the original fire-select click (`common/fireselect`) to the shooter.
- **FR-010**: The actionbar mode indicator MUST show `pump` distinctly from `semi`.
- **FR-011**: The per-gun `burst` value that only fed automatic fire MUST NOT exist as a burst length on guns without a burst mode.

### Key Entities

- **Fire mode**: one of `auto`, `semi`, `burst`, `pump`.
- **Mode set**: a gun's ordered list of fire modes; its first entry is the default.
- **Mode override**: values a mode replaces on its gun (cooldown, crouched accuracy, shooter sounds, shell ejection timing, burst shot spacing).
- **Weapon item**: an item carrying its gun's stats, supported modes and current mode, which may predate this feature.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For all 31 guns, the cycle seen in game matches FR-002, verified gun by gun from `_give_all`.
- **SC-002**: No gun outside the M16A4 and the FAMAS can be put in burst.
- **SC-003**: A SPAS-12 fires at 16-tick intervals in pump-action and 9-tick intervals in semi-automatic, measured over ten shots each.
- **SC-004**: An AK-47 item saved in burst mode before the update fires automatically after the update, with no player action besides firing.
- **SC-005**: Both `fire_semi` and `pap_fire_semi` play in game; no SPAS-12 clip is dead audio.

## Assumptions

- Changing mode stays on dropping the gun (Q). The original used a double tap on Q because a single tap reloaded; here reloading has its own input, so a single drop is enough.
- The guns' other stats are out of scope. The audit also found the Sten (base, walk, sprint and jump spread, switch time, kick) and the M500 (base, crouched, sprint and jump spread, switch time, kick) differing from the original; they are treated as deliberate rebalancing until stated otherwise.
- The ray gun is new to this pack and keeps its single automatic mode.
- Snipers, the M500 and the M590 keep their current behaviour; giving the M500 and M590 an explicit `pump` mode must not change how they fire.
