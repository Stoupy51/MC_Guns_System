# Feature Specification: Zombie Special Types

**Feature Branch**: `003-zombie-special-types`

**Created**: 2026-08-15

**Status**: Draft

**Input**: The three stub type functions in [src/functional/zombies/game/round/enemies.py](../../src/functional/zombies/game/round/enemies.py) and the aura-zombie idea in [src/functional/zombies/README.md](../../src/functional/zombies/README.md) §10.

## User Scenarios & Testing *(mandatory)*

The type dispatch already exists. `zombies/types/armed`, `types/fast` and `types/tank` are macro
functions that carry a TODO and fall straight through to `types/normal`, and
`zombies/do_spawn_zombie` hardcodes `_zpos.type` to `"normal"`, so nothing ever reaches them. The
scaffolding is done; the types are not.

The comment in `do_spawn_zombie` is the governing constraint: special types are Zonweeb-variant only.
The Vanilla variant must keep spawning nothing but normal zombies.

### User Story 1 - The horde stops being one enemy repeated (Priority: P1)

A Zonweeb player past the early rounds meets zombies that are not all the same: some outrun them, some
soak a magazine, and they have to change how they play rather than kite the same wall of identical mobs.

**Why this priority**: It is the whole point of the feature, and `fast` and `tank` need no new
mechanics at all. They are health and speed variations on a curve that already exists.

**Independent Test**: Start a Zonweeb game, `/scoreboard players set #zb_round mgs.data 20`, and watch
a wave spawn with a visible mix of speeds and durability.

**Acceptance Scenarios**:

1. **Given** a Zonweeb game past the introduction round, **When** a wave spawns, **Then** it contains a mix of normal, fast and tank zombies in a controlled ratio.
2. **Given** a Vanilla game at any round, **When** a wave spawns, **Then** every zombie is a normal zombie.
3. **Given** a fast zombie, **When** it is engaged, **Then** it is visibly quicker than a normal zombie of that round and dies faster.
4. **Given** a tank zombie, **When** it is engaged, **Then** it is visibly slower and takes far more damage to kill.
5. **Given** any special type, **When** it dies, **Then** kills, points, power-up rolls, nukes, traps and round completion all treat it exactly like a normal zombie.

---

### User Story 2 - A zombie that shoots back (Priority: P2)

An armed zombie fires at the player from range and drops an ammo power-up when killed, so the player
has a reason to prioritize it over the ones already chewing on them.

**Why this priority**: It needs a genuinely new behavior (a ranged attack goal) rather than a stat
curve, which makes it the most expensive of the four and the one most likely to need redesign.

**Independent Test**: Spawn one armed zombie in an open room, stand at range, and confirm it deals
damage from distance and drops ammo on death.

**Acceptance Scenarios**:

1. **Given** an armed zombie with line of sight, **When** the player is out of melee range, **Then** it attacks at range on a cooldown rather than closing to melee only.
2. **Given** an armed zombie, **When** it dies, **Then** an ammo power-up drops at its position regardless of the normal random power-up roll.
3. **Given** an armed zombie, **When** the player looks at the horde, **Then** it is visually distinguishable before it starts shooting.

---

### User Story 3 - A zombie worth killing first (Priority: P3)

An aura zombie grants damage resistance to zombies near it. Players learn to shoot it first, which
turns a wave into a target-priority problem instead of a spray.

**Why this priority**: The most interesting of the four, and the only one that changes how a wave is
fought rather than how an individual zombie feels. It is P3 because it depends on the type machinery
that User Story 1 proves out, and because a per-tick aura is the one piece here with a real cost.

**Independent Test**: Spawn an aura zombie plus a few normals, shoot a normal inside the aura and one
outside, and compare shots to kill.

**Acceptance Scenarios**:

1. **Given** an aura zombie, **When** zombies are within its radius, **Then** they take measurably less damage than the same zombie outside it.
2. **Given** an aura zombie, **When** it dies, **Then** the resistance lifts from every zombie that was in its radius.
3. **Given** an aura zombie, **When** the player looks at the horde, **Then** it stands out clearly enough to prioritize.
4. **Given** any round, **When** a wave spawns, **Then** at most one aura zombie is alive per wave.

### Edge Cases

- The escort taxi derives its speed from the zombie's base `movement_speed`, so a fast or tank zombie changes how its own escort moves. The relationship must stay correct at both ends of the range.
- A tank zombie's health goes through the same BO curve and the same 2/15 conversion, which is already capped at 2048 to stay Minecraft-safe. A tank multiplier must not push past that cap or every high-round tank silently becomes a normal-health zombie.
- The 10% walker roll at round 15+ already varies speed inside `types/normal`. A fast type on top of it must not produce a "fast walker" that is slower than a normal zombie.
- The aura's per-tick scan is the one real performance risk in this feature. It runs while the aura zombie is alive, in the middle of a horde.
- Special types must be excluded from dog rounds, which spawn from the special spawn markers.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Special types MUST only spawn in the Zonweeb variant. The Vanilla variant MUST spawn only `normal`.
- **FR-002**: Type selection MUST happen in `zombies/do_spawn_zombie`, which currently hardcodes `_zpos.type` to `"normal"`, and MUST be driven by round-gated weights rather than by copy-pasted round checks.
- **FR-003**: `types/fast` MUST raise base `movement_speed` above the round's normal value and lower the health the BO curve produced.
- **FR-004**: `types/tank` MUST raise health well above the round's normal value and lower base `movement_speed`, without exceeding the 2048 health cap in `calc_zombie_hp`.
- **FR-005**: `types/armed` MUST attack at range on a cooldown and MUST drop a guaranteed ammo power-up on death.
- **FR-006**: A new `types/aura` MUST apply damage resistance to zombies within a radius, refreshed on a tick interval rather than every tick.
- **FR-007**: Every special type MUST carry `mgs.zombie_round`, so alive counts, round completion, traps, barricades, nukes and the stuck rescue apply with no extra wiring, exactly as dogs do.
- **FR-008**: Every special type MUST be visually distinguishable from a normal zombie before it acts.
- **FR-009**: Special types MUST NOT spawn during dog rounds.
- **FR-010**: At most one aura zombie MUST be alive at a time.
- **FR-011**: The TODO comments in `enemies.py` MUST be removed as each type lands, not left beside a working implementation.

### Key Entities

- **Zombie type**: A macro function under `zombies/types/` taking `{level:"1".."4"}`, responsible for health, speed, damage and any tag the rest of the system reads. Types are dispatched by name from `do_spawn_zombie`.
- **Type weight table**: Round-gated spawn weights per type, the single place that decides what a wave is made of.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A Zonweeb wave at round 20 contains at least three distinct types, verifiable by counting entities with each type tag.
- **SC-002**: A Vanilla wave at any round contains only normal zombies.
- **SC-003**: A fast zombie's effective speed and a tank zombie's health differ from the round's normal values by a documented, deliberate factor at rounds 1, 10, 20 and 40.
- **SC-004**: Tank health never exceeds the 2048 cap, checked at round 50 and beyond.
- **SC-005**: The aura's per-tick cost does not measurably move MSPT with a full horde on screen, measured with F3+L before and after.
- **SC-006**: `enemies.py` contains no TODO comments for any shipped type.

## Assumptions

- The four types stay Zonweeb-only. Bringing them to Vanilla is a separate decision, not a follow-up.
- Fast and tank need no new AI, only attribute values on the existing curve.
- The armed zombie's ranged attack is achievable with existing datapack tools (a periodic raycast or projectile from the zombie) rather than needing a vanilla AI goal, which a datapack cannot add.
- The aura grants resistance through an attribute modifier or a brief effect, applied on an interval, not a per-tick reapplication.
- Special spawn markers stay reserved for dog rounds and future minibosses. Special types spawn from ordinary zombie spawns.
