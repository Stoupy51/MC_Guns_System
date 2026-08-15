# Feature Specification: XP Advancements

**Feature Branch**: `007-xp-advancements`

**Created**: 2026-08-15

**Status**: Draft

**Input**: User description: "Advancements for the XP System (reward xp too): should be well designed"

## Context

The pack already has a full cosmetic leveling system (`src/functional/progression/`): two independent
levels (Multiplayer and Zombies), a linear curve, the vanilla XP bar repurposed as the level bar, and
29 award rows spread across both modes. What it does not have is anything that survives a single match.
`mp.kills`, `zb.kills`, `mi.kills` and `zb.points` are all wiped between games, so nothing in the pack
can answer "how many zombies have I killed, ever" or "what is the deepest round I have reached".

Vanilla's Advancement screen is the natural home for that: a browsable, per-player, persistent,
already-localized UI. It is also an evaluation engine. A criterion on the `minecraft:tick` trigger with
an `entity_scores` condition unlocks the instant a scoreboard crosses a threshold, with no command, no
polling function and nothing for the pack to schedule. This feature keeps lifetime counters and lets
vanilla watch them.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Lifetime milestones pay out (Priority: P1)

A player kills zombies across several sessions. The moment their lifetime kill count crosses 250, a
vanilla advancement toast appears, a chat line tells them what they unlocked and how much XP it paid,
and their Zombies level bar moves.

**Why this priority**: This is the feature. Without the counters and the payout, the tree is decoration.

**Independent Test**: Fully testable with one chain (Zombies kills) and nothing else: set the counter
past a threshold with `/scoreboard` and watch it fire on the next tick.

**Acceptance Scenarios**:

1. **Given** a player at 249 lifetime Zombies kills, **When** they kill one zombie, **Then** the tier-1
   Zombies kills advancement unlocks within a tick, a toast shows, and their `zb.xp_total` rises by that
   tier's XP.
2. **Given** a player who has already unlocked that tier, **When** they kill a thousand more zombies,
   **Then** nothing re-fires and no further XP is paid for it.
3. **Given** a player who logs out and rejoins, **When** they check the Advancement screen, **Then**
   their unlocked challenges are intact and the counters behind the locked ones are too.
4. **Given** a single event that crosses two thresholds at once (a large round bonus, a Nuke), **When**
   it resolves, **Then** both tiers unlock and both XP payouts land.

---

### User Story 2 - One MGS tab, three branches (Priority: P2)

A player opens the Advancement screen and finds a single MGS tab. It roots into three branches,
Multiplayer, Missions and Zombies, and each branch holds chains that read outward from easiest to
hardest. Every entry states what it wants and what it pays.

**Why this priority**: The unlock machinery is worth nothing if a player cannot find out what to chase.
It is separable from Story 1: the tree can be browsed before a single counter is wired.

**Independent Test**: Load the pack on a fresh world and open the Advancement screen. Exactly one MGS
tab exists, all three branch roots hang off it, and no entry is unreadable or untitled.

**Acceptance Scenarios**:

1. **Given** a freshly loaded pack, **When** a player opens the Advancement screen, **Then** there is
   exactly one MGS tab, and its root, the three branch roots and every chain's first tier are visible.
2. **Given** a chain of four tiers, **When** the player has unlocked the second, **Then** the third is
   visible and the fourth follows vanilla's normal visibility rules for its parent.
3. **Given** any entry in the tab, **When** the player hovers it, **Then** the title and description are
   in the pack's language file like every other piece of MGS text.

---

### User Story 3 - Challenges that a score cannot express (Priority: P3)

Some things worth rewarding are moments, not totals: finishing a mission without dying, reaching round 20
alone. These unlock at the instant they happen, from the code that already detects them.

**Why this priority**: It is the smaller half of the catalog and depends on nothing in Stories 1 and 2,
but it is what stops the tree from being a wall of counters.

**Independent Test**: Complete a mission without dying and observe the unlock; complete one after dying
once and observe that it does not fire.

**Acceptance Scenarios**:

1. **Given** a player finishing a mission with zero deaths, **When** the victory resolves, **Then** the
   flawless challenge unlocks and pays.
2. **Given** a player finishing a mission having died once, **When** the victory resolves, **Then**
   nothing unlocks, and the challenge stays available for a later attempt.
3. **Given** any such challenge, **When** the player meets its condition a second time, **Then** it pays
   nothing further.

---

### User Story 4 - Retuning stays safe (Priority: P4)

The maintainer changes a threshold or a payout, rebuilds, and reloads onto a live server. Nobody loses an
unlock, nobody is paid twice, and players who now qualify under the new numbers get it on the next tick
with no admin step at all.

**Why this priority**: The existing XP system made exactly this promise (`progression/recompute_all`),
and a challenge system that needed a manual repair pass after every retune would be worse than it.

**Independent Test**: Lower a threshold below a player's current counter, rebuild, reload, and watch the
tier unlock by itself.

**Acceptance Scenarios**:

1. **Given** a player with unlocked tiers, **When** the pack version is bumped and rebuilt, **Then**
   their unlocks are still present and no XP is paid again.
2. **Given** a threshold lowered below a player's counter, **When** the pack reloads, **Then** the newly
   qualifying tier unlocks within a tick and pays once.
3. **Given** a threshold raised above a player's counter, **When** the pack reloads, **Then** an already
   unlocked tier stays unlocked and nothing is taken back.

---

### Edge Cases

- An event pays several units at once (a Nuke power-up, a round bonus multiplied by the round number).
  The counter must move by the real count, not by one.
- A counter that only makes sense as a high-water mark (deepest round) must not fall back when a shorter
  game is played.
- A refund in Zombies raises points back up. The points-spent stream already treats a refund as spent;
  the challenge counter inherits that and must not go negative.
- Two players cross a threshold on the same tick from the same team-wide award.
- A player is offline when a retune lands. Their unlock must resolve when they next log in, not be lost.
- The pack is loaded on a world where players already have MGS XP banked from before this feature. Their
  lifetime counters legitimately start at zero, and nothing may pretend otherwise.
- An operator revokes a challenge whose counter still qualifies. Vanilla will grant it again, and it will
  pay again. That is the same self-healing that makes retuning work, and is accepted rather than fought.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST track per-player lifetime counters that persist across matches, logouts and
  server restarts, separately for each branch of the tree.
- **FR-002**: Counters MUST be fed from the points where the pack already recognizes the event, without
  adding a second set of call sites to keep in sync.
- **FR-003**: The system MUST present the catalog as exactly one advancement tab, whose root parents
  three branch roots: Multiplayer, Missions and Zombies.
- **FR-004**: A threshold challenge MUST unlock from its own criteria as soon as the counter qualifies,
  without the pack running any command to grant it.
- **FR-005**: A challenge whose condition is a moment rather than a total MUST use an unreachable
  criterion and be granted explicitly by the code that detects the moment.
- **FR-006**: Unlocking MUST pay that tier's XP into the branch's existing `xp_total` / `xp_prog` / level
  pipeline, through the award table rather than by writing the progression scoreboards directly.
- **FR-007**: Each unlock MUST be paid at most once per player for as long as it stays unlocked.
- **FR-008**: Unlock feedback MUST tell the player what they unlocked and how much XP it paid, using the
  same message conventions as the rest of the progression system.
- **FR-009**: Advancement identifiers MUST NOT contain the pack version, so a pack update never wipes a
  player's unlocked challenges. Reward functions MAY be versioned like any other function.
- **FR-010**: Every threshold, XP payout, title, description and icon MUST live in one catalog, so
  retuning is a single-file edit.
- **FR-011**: Retuning MUST require no admin repair step. A rebuild and a reload MUST be enough for a
  newly qualifying player to unlock.
- **FR-012**: The per-event cost of tracking MUST be one command, independent of how many advancements
  exist, and MUST NOT introduce any new per-tick function.
- **FR-013**: Chains that read a scoreboard the pack already maintains MUST read it directly rather than
  mirroring it into a second counter.
- **FR-014**: Missions MUST award XP for its own play (kills, headshots, completing a mission), into the
  same pool its challenges pay. It awards none today, so its branch would otherwise hang off a mode
  whose level bar never moves.
- **FR-015**: Mission kills MUST NOT be counted by the Multiplayer kills challenge, whose nodes are
  written in terms of killing players.
- **FR-016**: Each chain MUST hold enough tiers that the tab reads as a wide tree rather than a tall
  column, and MUST start low enough that a new player can reach its first tier in a session.

### Key Entities

- **Branch**: One of the three sub-roots. Places chains in the tree and names the XP pool their payouts
  go into.
- **Stat**: A per-player lifetime number. Either a running count (kills, revives, missions completed) or a
  high-water mark (deepest round). Some branches read an existing objective instead of owning a new one.
- **Chain**: An ordered set of tiers over a single stat, rendered as one line of the tree.
- **Tier**: One advancement. Carries a threshold, an XP payout, a frame, a title, a description, an icon.
- **Event challenge**: A single advancement with no threshold, granted by the code that detects it.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A player who has never opened the pack before can see, in one tab, every challenge
  available to them and what each one pays, without reading any documentation.
- **SC-002**: Tracking costs at most one command per already-existing award event, and zero commands on
  ticks where nothing is earned. The pack adds no function that runs per tick for this feature.
- **SC-003**: Each pool is worth roughly eight to thirty sessions of bonus XP, spread so that no single
  unlock outweighs a good match.
- **SC-007**: The tab is roughly as wide as it is tall, and a player who has never opened the pack can
  reach the first tier of most chains within one session.
- **SC-008**: A mission that is played and completed moves the Multiplayer level bar, by an amount in the
  same range as a Multiplayer match.
- **SC-004**: Changing any threshold or payout requires editing exactly one file, rebuilding, and
  reloading. No command is run afterwards.
- **SC-005**: A pack version bump followed by a reload leaves every player's unlocks and counters intact,
  verified in game.
- **SC-006**: Crossing a threshold pays exactly once, verified by continuing to earn well past it.

## Assumptions

- Cosmetic only. Nothing in the pack is gated behind an unlocked challenge, matching the existing rule
  that levels unlock nothing.
- **Missions challenges pay Multiplayer XP.** Missions is built on the multiplayer side already: it
  reuses `mp.class`, `mp.team`, `mp.default`, the multiplayer loadout and class functions, and
  `progression/tick_player` shows the Multiplayer level everywhere outside a Zombies game, so a missions
  player is looking at their Multiplayer bar while they play. A third curve would be a separate feature.
- **Missions gains ordinary XP awards too** (FR-014). It had none before this feature, so a Missions
  branch on the challenge tree would otherwise sit on top of a mode where the bar never moves.
- The two XP pools stay independent. There is no combined MGS level.
- Advancements are the only UI. No separate menu, dialog or scoreboard display is in scope.
- Counters start at zero for everyone, including players with XP banked from before this feature. The
  pack has never recorded lifetime stats, so there is nothing to backfill from.
- The `advancements` gamerule is on. Players who turn it off lose the toast, which is their choice.
