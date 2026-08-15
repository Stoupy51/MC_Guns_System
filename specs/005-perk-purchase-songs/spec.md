# Feature Specification: Perk Purchase Songs

**Feature Branch**: `005-perk-purchase-songs`

**Created**: 2026-08-15

**Status**: Draft

**Input**: [src/functional/zombies/README.md](../../src/functional/zombies/README.md) §7, "Zombies - perk purchase songs (mostly HUMAN)".

## User Scenarios & Testing *(mandatory)*

Buying a perk in Black Ops plays the perk's jingle. The pack has 10 of the 14 clips staged in
`assets/zombies_perk_songs/` and none of them wired: they are not under `assets/sounds/`, so the sound
auto-registration never sees them.

Most of the remaining work is not code. Four clips have to be sourced by a human, and one filename is
misspelled.

### User Story 1 - Buying a perk plays its jingle (Priority: P1)

A player buys Juggernog and hears the Juggernog jingle, the way every Black Ops player expects.

**Why this priority**: It is the entire feature, and it works for 10 of the 14 perks with assets that
already exist. The four missing clips do not block it.

**Independent Test**: Buy each of the 10 perks that have a staged clip and confirm each plays its own,
distinct jingle.

**Acceptance Scenarios**:

1. **Given** a perk with a registered song, **When** a player buys it, **Then** that perk's jingle plays.
2. **Given** a perk with no song asset yet, **When** a player buys it, **Then** the purchase completes normally with no error and no missing-sound warning in the log.
3. **Given** two players buy perks at nearby machines at the same time, **When** both jingles play, **Then** neither is silenced by the other in a way that reads as a bug.

---

### User Story 2 - The remaining four clips exist (Priority: P2)

Electric Cherry, Widow's Wine, Timeslip and Dying Wish get their jingles too.

**Why this priority**: A human has to source the audio, so it cannot be scheduled like code. The
README marks it as explicitly the last thing on the list.

**Independent Test**: Buy each of the four and confirm a jingle plays.

**Acceptance Scenarios**:

1. **Given** a newly added clip dropped into the sounds folder, **When** the pack is rebuilt, **Then** it registers and plays with no code change.

### Edge Cases

- `assets/zombies_perk_songs/jungernog.ogg` is misspelled. Wiring it as-is registers a sound nobody can find.
- Perks can also be granted without a purchase: by the random-perk power-up, by Wunderfizz, and by a Who's Who or Tombstone restore. Whether those play a jingle is a design decision, not an oversight.
- A restore that regrants five perks at once would play five jingles simultaneously.
- The Wunderfizz jingle mentioned in the README is a machine sound, not a perk sound, and does not fit the per-perk naming scheme.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Perk songs MUST live at `assets/sounds/zombies/perks/<perk_id>.ogg`, using the perk ids from `PERK_DEFINITIONS`, so the existing auto-registration exposes them as `mgs:zombies/perks/<perk_id>`.
- **FR-002**: `jungernog.ogg` MUST be renamed to `juggernog.ogg`.
- **FR-003**: The song MUST play from the generated `zombies/perks/apply/<perk_id>` function, which `apply.py` already writes per perk from `PerkDef`.
- **FR-004**: Whether a perk has a song MUST be data on `PerkDef`, not a hand-maintained list somewhere else, so a new perk without audio stays silent automatically.
- **FR-005**: A perk with no song MUST produce no missing-sound warning and no behavior change.
- **FR-006**: The song MUST follow the power-up sound conventions established by `pu_snd` in `src/functional/zombies/rewards/powerups/types.py`.
- **FR-007**: A decision MUST be recorded on whether non-purchase grants (power-up, Wunderfizz, Who's Who and Tombstone restores) play the jingle, and it MUST be implemented rather than left to fall out of the code.

### Key Entities

- **Perk song**: One .ogg per perk id, auto-registered from its path, played by that perk's apply function.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 10 staged clips play on purchase, each on the right perk.
- **SC-002**: The 4 perks without clips buy normally with a clean client log.
- **SC-003**: Adding an .ogg for a missing perk makes it play with no code change beyond the `PerkDef` flag.
- **SC-004**: A Tombstone or Who's Who restore does not produce an unbearable pile-up of simultaneous jingles.

## Assumptions

- The existing `assets/sounds/` auto-registration picks up any .ogg under it, the same way `zombies/powerups/*` works today.
- The 10 staged clips are the correct final-seconds cuts and need no re-editing.
- Sourcing the 4 missing clips is a human task and is explicitly last.
- The optional Wunderfizz jingle is out of scope here; it is a machine sound and belongs with the Wunderfizz code.
