# Feature Specification: 26.3 Shader Migration

**Feature Branch**: `001-shader-migration-263`

**Created**: 2026-08-15

**Status**: Draft

**Input**: Existing research document [TODO_26.3_SHADERS.md](../../TODO_26.3_SHADERS.md), written 2026-07-30 against 26.3 Snapshot 3.

## User Scenarios & Testing *(mandatory)*

Minecraft 26.3 removes `minecraft:post_effect/transparency`, which is the single override the whole
visual pipeline in [src/functional/shaders.py](../../src/functional/shaders.py) hangs off.
The system is dead on 26.3, not degraded. The replacement (`minecraft:end_of_frame`) is strictly
better: it needs no Fabulous graphics, it composes with Iris shaderpacks, and it gets clean world depth.

### User Story 1 - The visual pipeline survives the version bump (Priority: P1)

A player on 26.3 aims down sights, fires, and takes a flashbang. Zoom, muzzle flash, spread feedback
and the custom crosshair look exactly as they did on 26.2, with no graphics-settings requirement.

**Why this priority**: Without it, upgrading the pack to 26.3 ships a visibly broken game. Every other
story here is an improvement on top of a pipeline that must first exist.

**Independent Test**: Load the pack on a 26.3 client with Fancy graphics (not Fabulous), scope a
weapon, fire it, and detonate a flashbang. All three effects render, and the F3 `post_effects` debug
entry lists `minecraft:end_of_frame`.

**Acceptance Scenarios**:

1. **Given** a 26.3 client with graphics set to Fast, **When** the player aims down sights, **Then** the smooth zoom lerp plays to completion and holds.
2. **Given** a 26.3 client, **When** the player fires, **Then** the muzzle flash renders on the tick of the shot and is gone the next tick.
3. **Given** no marker particle is present, **When** the frame is rendered, **Then** `end_of_frame` is visually identity (a pixel-for-pixel unmodified frame).
4. **Given** a player without the resource pack, **When** they join, **Then** they play normally with no client log spam and no crash.

---

### User Story 2 - Effects work with an Iris shaderpack loaded (Priority: P2)

A player running BSL or Complementary scopes in and sees the zoom distortion and muzzle flash on top
of their shaderpack's output. This has never worked before.

**Why this priority**: A genuinely new capability rather than a restoration, and it is the single most
requested thing from players who use shaderpacks. It depends on P1 being done and on an Iris 26.3 build
existing, so it cannot lead.

**Independent Test**: Install Iris with a heavy shaderpack, scope a weapon, fire, and take a flashbang.

**Acceptance Scenarios**:

1. **Given** an Iris shaderpack is active, **When** the player scopes, **Then** the zoom distortion applies over the shaderpack's final image.
2. **Given** an Iris shaderpack is active, **When** a flashbang goes off, **Then** the depth-based falloff still tracks world geometry rather than the held weapon.

---

### User Story 3 - Dead code is gone, not carried forward (Priority: P2)

A maintainer opens `shaders.py` and finds only code that runs on 26.3. No transparency compositing, no
duplicate outline zoom chain, no "requires Fabulous" wording anywhere in the pack or its messages.

**Why this priority**: Roughly 280 lines exist only to work around 26.2 constraints that no longer
apply. Porting them wastes the port and leaves permanent confusion about which path is live.

**Independent Test**: Grep the repo for `transparency`, `entity_outline`, `OUTLINE_ZOOM` and "Fabulous";
every hit is either gone or is a historical note in this spec directory.

**Acceptance Scenarios**:

1. **Given** the 26.3 build, **When** a player with entity glow in view scopes in, **Then** the glow outline warps with the zoom without any dedicated outline chain.
2. **Given** the in-game config menu, **When** a player opens the graphics-related entries, **Then** no text asks them to enable Fabulous or Improved Transparency.

---

### User Story 4 - Long-lived per-player effects move to `/posteffect` (Priority: P3)

A downed player's screen desaturates; a spectator gets a tint; a scoped player gets an overlay. These
are driven by the server per player instead of by the particle sentinel channel.

**Why this priority**: Optional. It is a cleaner mechanism for states that last more than a tick, but
the sentinel channel already works and `/posteffect` cannot do the 1-tick muzzle flash at all.

**Independent Test**: Down a player in zombies and confirm the desaturation applies to them only, then
relog and confirm it does not persist.

**Acceptance Scenarios**:

1. **Given** a player with an applied post effect, **When** they disconnect and rejoin, **Then** no stale effect is active.
2. **Given** a player with an applied post effect, **When** the game ends, **Then** the effect is cleared.

### Edge Cases

- A GLSL compile error blacklists the effect until a resource reload. Development requires F3+T after every shader fix; the pack must not depend on an effect silently recovering.
- `/posteffect add` and `remove` in the same tick cancel out before the packet is sent, so any effect must live at least one full tick.
- Post effects persist in player NBT across relog and death, so a crashed round can leave a player permanently scoped unless they are cleared defensively.
- Order-independent transparency composites translucents into `minecraft:main` before post effects run, whereas the 26.2 classify pass read main before compositing. The marker sentinel may no longer survive standing in water or behind glass.
- Shipping any post effect flips `consistentDepthRequired` on permanently for every player with the pack, adding depth targets and an integration pass.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The pack MUST register `minecraft:post_effect/end_of_frame.json` in the `minecraft` namespace and drive zoom, flash, spread and crosshair from it.
- **FR-002**: `end_of_frame` MUST be visually identity when no effect is active, since it cannot be turned off by the player.
- **FR-003**: Every GLSL source MUST compile through shaderc to SPIR-V targeting Vulkan 1.2, using `#include <ns:file.glsl>` rather than `#moj_import`.
- **FR-004**: Depth-dependent shaders MUST branch on `RENDERPEARL_DEPTH_IS_ZERO_TO_ONE` instead of hardcoding reversed-Z assumptions.
- **FR-005**: `TRANSPARENCY_FSH`, `OUTLINE_ZOOM_FSH`, `get_entity_outline_json()` and the `entity_outline` registration MUST be deleted.
- **FR-006**: The pack MUST NOT require Fabulous graphics or Improved Transparency, in behavior or in wording.
- **FR-007**: If `/posteffect` is used at all, the pack MUST clear a player's effects on join, on respawn, and on game end.
- **FR-008**: The 1-tick muzzle flash MUST stay on the particle-marker sentinel channel; `/posteffect` cannot deliver it.
- **FR-009**: `beet.yml` MUST target `minecraft: "26.3"` and the README MUST stop saying 26.2.
- **FR-010**: [src/functional/weapon/hud/hit_indicator.py](../../src/functional/weapon/hud/hit_indicator.py) MUST be reconsidered against the new post-effect host; its font-glyph arc exists only because no post-shader command was available.

### Key Entities

- **Post chain**: A named JSON effect definition with its own private, persistent render targets. Two chains cannot share a lerp buffer, only `minecraft:main`.
- **Marker sentinel**: A dust particle at the near plane carrying packed parameters in reserved pixels of `minecraft:main`, read by the classify pass. Currently the only per-tick parameter channel.
- **Persistent target**: A `persistent: true` 1x1 render target surviving across frames, used by the smooth zoom and spread feedback loops.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zoom, muzzle flash, spread feedback and the custom crosshair all render on a 26.3 client at Fast, Fancy and Fabulous graphics presets.
- **SC-002**: Idle frame cost of `end_of_frame` is three 1x1 passes plus two fullscreen passes, and the idle frame is pixel-identical to no post effect.
- **SC-003**: All 9 GLSL sources compile with zero shaderc errors on a Vulkan-capable driver.
- **SC-004**: `shaders.py` loses roughly 280 lines of dead code and gains no compatibility shim for 26.2.
- **SC-005**: A player with an Iris shaderpack sees zoom and flash, which was impossible before.

## Assumptions

- The migration lands when 26.3 goes stable, not against snapshots. Snapshot work is verification only.
- Iris will publish a 26.3 build; until then User Story 2 cannot be validated and must not block the rest.
- `MixinPostChain` stays an empty class in the Iris 26.3 branch. If it stops being one, User Story 2 needs re-research before any work.
- No parallel 26.2 branch is maintained. The pack moves to 26.3 and does not look back.
- The research in `TODO_26.3_SHADERS.md` was verified against the decompiled sources in [minecraft_source_code/](../../minecraft_source_code/) and is treated as accurate for the version it names.
