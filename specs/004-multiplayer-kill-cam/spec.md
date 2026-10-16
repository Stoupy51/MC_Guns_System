# Feature Specification: Multiplayer Final Kill Cam

**Feature Branch**: `004-multiplayer-kill-cam`

**Created**: 2026-08-15, rewritten 2026-10-16

**Status**: Draft

**Input**: Call of Duty's final kill cam, including the killer's whole kill streak when the match ends on one.

## User Scenarios & Testing *(mandatory)*

When a match ends on a kill, every player of the match watches the end of it again from the final
killer's eyes before the results. If the killer chained several kills into the winning one, the replay
starts at the first kill of the chain and shows all of them: a 4-kill run ending the match is the
moment the feature exists for.

The replay is a puppet show, not a recording of the world. Every player of the match is redrawn as a
`minecraft:mannequin` wearing their skin, driven by recorded positions, rotations and actions. The camera
is a display entity every viewer spectates, driven by the killer's recorded eye position and rotation.

### User Story 1 - The final kill chain is replayed (Priority: P1)

A Team Deathmatch is at 29-27, score limit 30. A red player kills three blue players in eight seconds,
the last one ending the match. Everyone in the match sees "KILLCAM" and watches those eight seconds from
the red player's eyes: the three victims move as they did, the shots are heard, each victim falls when
hit. Then the results come up.

**Why this priority**: It is the feature. Recording, puppets, camera and presentation have no value apart.

**Independent Test**: Two players, FFA, score limit 3. One gets 3 kills within a few seconds. Both watch
a replay that starts shortly before the first kill and ends shortly after the third.

**Acceptance Scenarios**:

1. **Given** a match ends on a kill, **When** the end sequence starts, **Then** every match player is put in the replay and sees it from the final killer's eyes.
2. **Given** the final killer made several kills in a chain (FR-005), **When** the replay plays, **Then** it starts `PRE_ROLL` before the first kill of the chain and every kill of the chain is shown.
3. **Given** a victim is killed in the replay, **When** the kill tick is reached, **Then** that victim's mannequin dies on screen with the vanilla death animation.
4. **Given** the killer fired during the replayed window, **When** each fire tick is reached, **Then** the weapon's fire sound plays at the camera and a muzzle particle shows in front of it.
5. **Given** the replay ends, **When** `POST_ROLL` after the final kill has played, **Then** every mannequin and the camera are gone, viewers get their gamemode and position back, and the normal results follow.

---

### User Story 2 - Recording is cheap and bounded (Priority: P1)

A 12-player match runs for ten minutes and the kill cam costs nothing measurable until the match gets
close to its end.

**Why this priority**: Recording every player every tick for a whole match is the most expensive thing
the pack could do, for a feature used once per match.

**Independent Test**: F3+L in the middle of a match, then in the recording window. Mid-match costs nothing; in the window, the cost stays flat per player.

**Acceptance Scenarios**:

1. **Given** no team or player is within `MATCH_POINT_KILLS` of the score limit and more than `RECORD_TICKS` remain on the timer, **When** the tick runs, **Then** no recording work happens.
2. **Given** the recording window is open (FR-002), **When** the tick runs, **Then** exactly one frame is appended, holding one sample per match player, and frames older than `RECORD_TICKS` are dropped.
3. **Given** the window opened and then closed again (a team lost its lead), **When** it closes, **Then** recording stops and the buffer is cleared.
4. **Given** a sample, **When** it is taken, **Then** it reads no player NBT: position and rotation come through a marker (Bookshelf `bs.position`), flags from scores and predicates.

---

### User Story 3 - The replay survives an imperfect match (Priority: P2)

Players join late, leave mid-replay, or the match ends in a way that has no killer viewpoint.

**Why this priority**: The sequence plays at the most visible moment of the match, in front of everyone.

**Acceptance Scenarios**:

1. **Given** the final killer disconnected after the kill, **When** the end sequence starts, **Then** the replay still plays from their recorded samples.
2. **Given** a viewer disconnects mid-replay, **When** they rejoin, **Then** they are restored like any player rejoining after a match, and the replay continued for the others.
3. **Given** a player joined after the window opened, **When** the replay plays, **Then** their mannequin appears from their first sample on and is absent before it.
4. **Given** the match ends on the timer, a suicide, a fall, out-of-bounds or a bomb, **When** the end sequence starts, **Then** there is no replay and the results come immediately (FR-010).

### Edge Cases

- The final kill is an explosive kill (grenade, RPG). The killer may not be looking at the victim. The replay still shows the killer's view; that is what Call of Duty does.
- A chain kill happened before the window opened. The chain is cut at the first kill that is still in the buffer.
- Search and Destroy and Demolition end per round. Only the match-ending round gets a kill cam.
- Domination and Hardpoint end on points, not kills. They get a kill cam only when the last kill of the match happened within `RECORD_TICKS` of the end, recorded under the timer and points gates.
- The world keeps its post-match state: bomb sites, dropped items and destroyed blocks are not rewound.
- Two mannequins can overlap a viewer camera if the killer stood inside a doorway with a teammate. Accepted.
- The killer is a mannequin too. It is hidden during the replay, since the camera sits in its head.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The kill cam MUST only run in multiplayer matches, never in Missions or Zombies, and only match players MUST see it.
- **FR-002**: The recording window MUST open while any team (team modes) or player (FFA) is within `MATCH_POINT_KILLS` of the score limit, or while at most `RECORD_TICKS` remain on the match timer, and MUST stay closed otherwise.
- **FR-003**: While open, recording MUST append one frame per tick to a single list, each frame holding the tick and one sample per match player: player id, position, yaw, pitch, and flags (fired, sneaking, sprinting, dead).
- **FR-004**: The buffer MUST hold at most `RECORD_TICKS` frames, MUST be keyed by absolute tick rather than list index, and MUST be cleared at match start, match stop and when the window closes.
- **FR-005**: Every multiplayer kill MUST be logged with its tick, killer id and victim id while the window is open. The final kill chain is the run of the final killer's kills, walking back from the final kill, where each kill is at most `CHAIN_GAP` ticks after the previous one, capped at `MAX_CHAIN` kills and at the buffer start.
- **FR-006**: Playback MUST cover from `PRE_ROLL` before the first chain kill to `POST_ROLL` after the final kill, at recorded speed.
- **FR-007**: Playback MUST spawn one mannequin per player present in the replayed frames, with that player's profile, held item and armor as snapshotted when the window opened, and MUST drive them from their samples with smooth interpolation.
- **FR-008**: Playback MUST drive a camera entity from the killer's samples at eye height, and every viewer MUST spectate it for the whole replay.
- **FR-009**: The fired flag MUST play the killer's weapon fire sound and a muzzle particle at the camera; each chain kill MUST kill its victim's mannequin on its tick.
- **FR-010**: The replay MUST be skipped when the final kill has no player killer or the kill log is empty.
- **FR-011**: The replay MUST show "KILLCAM", the killer's name and the chain length (for example "x4") on screen.
- **FR-012**: No mannequin, camera or replay marker MUST survive the sequence, including when it is interrupted by `/function mgs:multiplayer/stop`.
- **FR-013**: Every tunable (`RECORD_TICKS`, `MATCH_POINT_KILLS`, `CHAIN_GAP`, `MAX_CHAIN`, `PRE_ROLL`, `POST_ROLL`) MUST be a named constant with a docstring.

### Key Entities

- **Frame**: `{t:<tick>, s:[<sample>, ...]}`, one per recorded tick.
- **Sample**: `{id:<mp player id>, p:[x, y, z], r:[yaw, pitch], f:<flag bits>}`.
- **Kill log entry**: `{t:<tick>, killer:<id>, victim:<id>}`.
- **Roster snapshot**: per player id, the name, profile, team, mainhand and armor at window open. Written when the window opens and when a player joins while it is open.

```text
storage mgs:kill_cam {
  frames:[{t:12034, s:[{id:3, p:[...], r:[...], f:1}, ...]}, ...],
  kills:[{t:12010, killer:3, victim:7}, ...],
  roster:[{id:3, name:"Stoupy51", team:1, mainhand:{...}, armor:[...]}, ...]
}
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Mid-match MSPT is the same with the feature on and off on a 12-player match (F3+L).
- **SC-002**: In the recording window, the added cost stays under 1 ms per tick with 12 players.
- **SC-003**: A 4-kill chain ending a match is replayed whole, every victim dying on screen at its kill.
- **SC-004**: A match ending without a player kill goes to the results with no visible delay.
- **SC-005**: After the sequence, `/execute if entity @e[tag=mgs.kill_cam]` finds nothing.

## Assumptions

- Defaults: `RECORD_TICKS` 300 (15 s), `MATCH_POINT_KILLS` 5, `CHAIN_GAP` 80 (4 s), `MAX_CHAIN` 6, `PRE_ROLL` 40, `POST_ROLL` 30. Tuned in play.
- Only players are puppeted. Zombies, mission enemies, projectiles, grenades and block changes are not replayed.
- Held items change during the window are not tracked; the snapshot at window open is used. A weapon swap mid-chain shows the old weapon.
- The camera uses `/spectate` on an `item_display` with `teleport_duration`, the pattern of the zombies downed camera, so the client interpolates between samples.
- The sample id is the Bookshelf `bs.id` score the player menus already use. Usernames are not keys.
