# Feature Specification: Multiplayer Final Kill Cam

**Feature Branch**: `004-multiplayer-kill-cam`

**Created**: 2026-08-15

**Status**: Draft

**Input**: The "Future multiplayer TODO" in the root [README.md](../../README.md), which sketches a per-tick position and rotation buffer for the last 10 seconds of a match.

## User Scenarios & Testing *(mandatory)*

Call of Duty's final kill cam: when a match ends, everyone watches the last kill replayed from the
killer's point of view before the scoreboard comes up. The README sketches the recording half (a
200-tick ring buffer of every player's position and rotation) and stops there.

### User Story 1 - Everyone sees the final kill replayed (Priority: P1)

A Team Deathmatch match ends on a headshot. Instead of cutting straight to the scoreboard, every
player watches the last few seconds from the killer's eyes, then the scoreboard appears.

**Why this priority**: It is the feature. The buffer, the playback and the presentation only have
value together, so there is no smaller shippable slice.

**Independent Test**: Play a short FFA to the score limit, and confirm every player, winner and loser
alike, watches the same replay from the same viewpoint before the scoreboard.

**Acceptance Scenarios**:

1. **Given** a match ends on a kill, **When** the end sequence starts, **Then** every player is moved into the replay and sees it from the final killer's viewpoint.
2. **Given** a replay is playing, **When** it reaches the moment of the kill, **Then** the killed player's death is visible from that viewpoint.
3. **Given** a replay finishes, **When** it ends, **Then** every player returns to normal spectate and the scoreboard appears.
4. **Given** a match ends on the timer rather than a kill, **When** the end sequence starts, **Then** it skips the replay cleanly rather than showing an empty one.

---

### User Story 2 - The recording costs nothing for most of the match (Priority: P1)

A match runs for ten minutes with twelve players and the kill cam adds no measurable tick cost until
the last ten seconds.

**Why this priority**: A naive implementation records every player every tick for the whole match. On
a busy server that is the most expensive thing in the pack, for a feature used once. The recording
must be bounded by design, not by hope.

**Independent Test**: Measure MSPT with F3+L during mid-match play with the feature enabled and
disabled; the difference must be indistinguishable.

**Acceptance Scenarios**:

1. **Given** a match with more than half its time left, **When** the tick runs, **Then** no kill cam recording work happens at all.
2. **Given** the last 10 seconds of a match, **When** the tick runs, **Then** exactly one sample per player per tick is appended and the buffer never exceeds 200 entries per player.
3. **Given** a match that ends early on a score limit rather than the timer, **When** it ends, **Then** whatever was recorded is used and a short replay plays rather than none.

---

### User Story 3 - Replays survive an imperfect recording (Priority: P2)

A player who joined 3 seconds before the end, or who disconnected mid-replay, does not break the
sequence for everyone else.

**Why this priority**: The sequence runs at the most visible moment in the match and is watched by
every player at once. A failure here is a failure everybody sees.

**Independent Test**: Have a player disconnect during the replay and confirm it continues for the rest.

**Acceptance Scenarios**:

1. **Given** the final killer disconnected before the match ended, **When** the end sequence starts, **Then** it skips the replay and goes to the scoreboard.
2. **Given** a viewer disconnects mid-replay, **When** they are gone, **Then** the replay continues for everyone else and no entity is orphaned.
3. **Given** a buffer shorter than the full 10 seconds, **When** it plays, **Then** it plays what exists rather than stalling on missing samples.

### Edge Cases

- A match ending on the timer with no kill in the buffer window has nothing to replay.
- The final kill may be a suicide, an out-of-bounds death or a trap, none of which have a killer viewpoint.
- Search and Destroy ends per round, not only per match. Whether it gets a per-round kill cam is a design decision, not an implementation detail.
- The world moves on during the replay: objectives, bomb sites and other players are in their post-match state, not their state at recording time. Only positions and rotations are recorded, not the world.
- A player killed by an explosion may have a killer who was never near them, which reads oddly from that viewpoint.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Recording MUST only run in the final 10 seconds (200 ticks) of a match.
- **FR-002**: Recording MUST append one `[x, y, z, yaw, pitch]` sample per in-game player per tick to `storage mgs:kill_cam players.<username>`.
- **FR-003**: Each player's buffer MUST be capped at 200 entries, dropping the oldest.
- **FR-004**: The end sequence MUST identify the final kill: its killer, its victim and its tick index in the buffer.
- **FR-005**: Playback MUST move every player to a camera driven from the killer's recorded samples, and MUST restore them afterwards.
- **FR-006**: Playback MUST be skipped, going straight to the scoreboard, when there is no valid final kill or the killer is gone.
- **FR-007**: The buffer MUST be cleared on match start and match stop, so a stale one can never replay.
- **FR-008**: Recording MUST NOT run in Missions or Zombies.
- **FR-009**: The replay MUST have a visible in-game presentation (a title or overlay naming the killer and the victim) so it reads as a kill cam and not as a camera glitch.

### Key Entities

- **Sample**: One player's `[x, y, z, yaw, pitch]` at one tick.
- **Player buffer**: An ordered list of up to 200 samples, keyed by username under `storage mgs:kill_cam players`.
- **Final kill record**: Killer, victim and the buffer index at which the kill happened. Written by the death path, read by the end sequence.

Layout from the original sketch:

```text
storage mgs:kill_cam players set value {
  Stoupy51:[[x,y,z,yaw,pitch],[x,y,z,yaw,pitch],...],
  username_2:[...]
}
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: MSPT during mid-match play is indistinguishable with the feature on and off, measured with F3+L on a full lobby.
- **SC-002**: In the final 10 seconds, recording cost stays flat per player and the storage never grows past 200 entries each.
- **SC-003**: A match ending on a kill shows a replay to every player, and the scoreboard follows it.
- **SC-004**: A match ending with no valid final kill goes straight to the scoreboard with no visible hitch.
- **SC-005**: No kill cam entity or camera mount survives the end of the sequence, checked with `/kill @e[tag=mgs.gm_entity]` finding nothing left over.

## Assumptions

- Only positions and rotations are recorded. The world, other entities and projectiles are not, so the replay is an approximation and is accepted as one.
- 200 ticks at 20 tps is the whole budget. No compression, no sub-sampling in the first version.
- The camera is an entity the viewers ride, the same pattern the zombies downed camera already uses in `src/functional/zombies/player/revive/`.
- Search and Destroy gets one kill cam at match end, not one per round, unless play testing says otherwise.
- Usernames are the buffer key, as in the original sketch. If name changes turn out to matter, the key becomes the UUID.
