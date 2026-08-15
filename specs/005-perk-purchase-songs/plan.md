# Implementation Plan: Perk Purchase Songs

**Branch**: `005-perk-purchase-songs` | **Date**: 2026-08-15 | **Spec**: [spec.md](spec.md)

## Summary

Move the 10 staged clips from `assets/zombies_perk_songs/` to `assets/sounds/zombies/perks/<perk_id>.ogg`,
add a `has_song` flag to `PerkDef`, and emit one `playsound` line from the per-perk apply function that
`apply.py` already generates.

The code is roughly ten lines. The rest is asset placement, one filename fix, and the decision in FR-007.

## Technical Context

**Language/Version**: Python >=3.14 generating mcfunction through StewBeet

**Primary Dependencies**: beet + StewBeet's `stewbeet.plugins.resource_pack.sounds`, which auto-registers anything under the configured `sounds.folder`

**Storage**: N/A

**Testing**: In-game. Buy each perk and listen

**Target Platform**: Minecraft Java 26.2

**Project Type**: Minecraft resource pack assets plus a generated datapack

**Performance Goals**: One `playsound` per purchase. Not a concern

**Constraints**: A perk with no clip must stay silent with a clean log

**Scale/Scope**: One field on `PerkDef`, one line in `apply.py`, and 10 file moves

## Constitution Check

*GATE: passed.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | The `playsound` is generated from `apply.py`; only the .ogg files are hand-placed, which is what assets are. |
| II. Data-driven definitions | `has_song` is a `PerkDef` field, so the set of perks with jingles is one column in the existing table rather than a second list to keep in sync. |
| III. Typed, linted, readable | One new typed field with a docstring under it. |
| IV. Runtime cost is a design constraint | One `playsound` on a purchase. Nothing per-tick. |
| V. In-game verification | Buying all 14 perks is the test, and it is the only test that means anything here. |

## Project Structure

### Documentation (this feature)

```text
specs/005-perk-purchase-songs/
├── spec.md
├── plan.md              # This file
└── tasks.md
```

### Source Code (repository root)

```text
assets/
├── zombies_perk_songs/         # Staging area, emptied and deleted by this feature
└── sounds/zombies/perks/       # Destination: <perk_id>.ogg, auto-registered as mgs:zombies/perks/<perk_id>

src/functional/zombies/
├── machines/perks/definitions.py   # PerkDef gains has_song; the 10 wired perks set it
├── machines/perks/apply.py         # The generated apply/<perk_id> gains a conditional playsound line
└── rewards/powerups/types.py       # pu_snd: the volume, pitch and audience conventions to match
```

**Structure Decision**: No new module. This feature is a field, a line, and ten files in the right
place. Creating a `songs.py` for it would be more structure than content.

## Complexity Tracking

No violations. One decision is deliberately left to a task rather than settled here (FR-007, whether
non-purchase grants play the jingle) because it is a design call best made with the sound actually
playing in game.
