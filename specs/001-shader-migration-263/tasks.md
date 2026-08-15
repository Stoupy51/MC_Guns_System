---

description: "Task list for the 26.3 shader migration"
---

# Tasks: 26.3 Shader Migration

**Input**: [spec.md](spec.md), [plan.md](plan.md), and the line-referenced research in [TODO_26.3_SHADERS.md](../../TODO_26.3_SHADERS.md)

**Tests**: No automated tests. This is shader work; every task closes on a named in-game check, per constitution principle V.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 pipeline survives, US2 Iris, US3 dead code, US4 `/posteffect`

## Path Conventions

Single project. Generation code under `src/functional/`, assets under `assets/`, build output under `build/`.

---

## Phase 1: Setup

**Purpose**: A 26.3 environment that can actually tell you whether a shader compiled.

- [ ] T001 Install a 26.3 client on a Vulkan-capable driver and confirm the launcher log reports the SPIR-V compile path
- [ ] T002 Point `beet.yml` `stewbeet.livereload.minecraft` at the 26.3 install so `beet watch` reloads the right client
- [ ] T003 Confirm F3+T fully clears `failedPostEffects`, since a GLSL error blacklists an effect until resource reload

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Answer the questions that decide whether the planned architecture is even possible. Nothing below this phase should be written until all of it is answered.

**CRITICAL**: T007 is the highest-risk item in the feature. If the sentinel does not survive OIT, the parameter channel needs redesigning and every later estimate is wrong.

- [ ] T004 Register a two-line blit-only `minecraft:post_effect/end_of_frame.json` and confirm it loads, runs on Fancy, and appears in the F3 `post_effects` debug entry
- [ ] T005 Establish the minimum valid GLSL header for a post `.fsh`: `#version` value, whether `layout(location)` is required on `in`/`out`, and that `#include <minecraft:...>` resolves under `shaders/include/`
- [ ] T006 [P] Confirm `persistent: true` 1x1 targets survive across frames and across a resource reload
- [ ] T007 Confirm the marker sentinel still reaches `applyPostEffects` under OIT: stand in water and behind glass, then read pixels (0,0) to (3,0)
- [ ] T008 [P] Confirm `minecraft:main` depth is world depth and not hand depth once a post effect is active, which `FLASH_FSH` depends on
- [ ] T009 [P] Check whether 26.3's `render3dCrosshair` path changes anything for the custom crosshair

**Checkpoint**: The host is proven. The port can start.

---

## Phase 3: User Story 1 - The visual pipeline survives the version bump (Priority: P1) MVP

**Goal**: Zoom, muzzle flash, spread feedback and the custom crosshair all work on 26.3 with no graphics-settings requirement.

**Independent Test**: Fancy graphics, no Iris. Scope, fire, take a flashbang. All three render; F3 lists `minecraft:end_of_frame`.

### Restructure first, so the port lands in its final home

- [ ] T010 [US1] Split `src/functional/shaders.py` into the `src/functional/shaders/` package laid out in plan.md, moving code only, and confirm `beet build` output is byte-identical before touching any GLSL
- [ ] T011 [US1] Move `SPREAD_COPY_FSH` to `src/functional/shaders/passes/spread.py` and port it, the simplest shader, to establish the header from T005

### Port the GLSL, one shader at a time

- [ ] T012 [P] [US1] Port `CLASSIFY_FSH` in `src/functional/shaders/passes/classify.py` and verify it reads the sentinel pixels proven in T007
- [ ] T013 [P] [US1] Port `ZOOM_LERP_FSH` in `src/functional/shaders/passes/zoom.py` and verify the feedback loop still lerps smoothly across frames
- [ ] T014 [US1] Port `FLASH_FSH` in `src/functional/shaders/passes/flash.py`, rewriting `LinearizeDepth` around `#ifdef RENDERPEARL_DEPTH_IS_ZERO_TO_ONE` (depends on T008)
- [ ] T015 [US1] Port `ZOOM_FSH` in `src/functional/shaders/passes/zoom.py`: bicubic sampling, the 1536² spark sheet input, and the custom crosshair. Largest file, most to verify
- [ ] T016 [US1] Port `PARTICLE_VSH` / `PARTICLE_FSH` in `src/functional/shaders/particle.py`: `#moj_import <minecraft:fog.glsl>` becomes `#include`, and the near-plane `gl_Position.z` uses the depth macro
- [ ] T017 [US1] Re-verify the `Globals` / `ScreenSize` UBO note in the `PARTICLE_VSH` comment. The fixed-NDC workaround may be unnecessary now, or mandatory for a new reason under Vulkan
- [ ] T018 [US1] Re-validate `discard` semantics and core shader overrides end to end on the Vulkan backend

### Rehost on `end_of_frame`

- [ ] T019 [US1] Write `get_end_of_frame_json()` in `src/functional/shaders/chain.py` as a declarative pass list: classify, spread_copy, zoom_lerp, flash, zoom, blit. `flash` reads `minecraft:main` directly instead of a composited `final`
- [ ] T020 [US1] Register the chain as `Mem.ctx.assets["minecraft"].post_effects["end_of_frame"]` in `src/functional/shaders/__init__.py`
- [ ] T021 [US1] Verify the idle frame is pixel-identical to no post effect (FR-002, SC-002) by screenshotting with and without the pack and diffing
- [ ] T022 [US1] Verify the 2D GUI is not warped, since `guiRenderer.render()` runs after post effects, and that the custom crosshair sits correctly against real HUD elements
- [ ] T023 [US1] Verify a player without the resource pack joins, plays and leaves with no client log spam

**Checkpoint**: The pack is playable on 26.3. This is the shippable MVP.

---

## Phase 4: User Story 3 - Dead code is gone, not carried forward (Priority: P2)

**Goal**: Nothing in the tree exists only to satisfy 26.2.

Ordered before User Story 2 on purpose: it is not blocked on an external Iris release, and every day it waits is a day someone ports something dead.

- [ ] T024 [US3] Delete `TRANSPARENCY_FSH` and the transparency pass with all 12 of its sampler inputs (~135 lines)
- [ ] T025 [US3] Delete `OUTLINE_ZOOM_FSH`, `get_entity_outline_json()` and the `entity_outline` registration (~145 lines)
- [ ] T026 [US3] Verify glow outlines now warp with the zoom for free, since `applyPostEffects` runs after `blitEntityOutline`
- [ ] T027 [US3] Rewrite the package docstring in `src/functional/shaders/__init__.py`: no Fabulous requirement, new ordering, new depth guarantees, and the current status of the `MARKER_MODES` sentinel contract
- [ ] T028 [P] [US3] Remove every "requires Fabulous" and "Improved Transparency" mention from in-game messages, `beet.yml` comments (`mgs_custom_crosshair`) and the README
- [ ] T029 [US3] Revisit `src/functional/weapon/hud/hit_indicator.py`: its font-glyph arc exists only because no post-shader path was available. Decide port or replace, and delete the TODO either way
- [ ] T030 [US3] Set `beet.yml` `minecraft: "26.3"` and update the README's "MC Guns System 26.2" heading
- [ ] T031 [US3] Delete `TODO_26.3_SHADERS.md`, folding anything still true into the package docstring
- [ ] T032 [US3] `ruff check src --fix` and a clean `beet build`

**Checkpoint**: The tree contains only live code.

---

## Phase 5: User Story 2 - Effects work with an Iris shaderpack loaded (Priority: P2)

**Goal**: Zoom, flash and crosshair render over an Iris shaderpack.

**Blocked externally**: Iris has no 26.3 branch as of 2026-07-29.

- [ ] T033 [US2] Wait for an Iris 26.3 build, then re-read `mixin/state_tracking/MixinPostChain.java`. If it stops being an empty class, stop and re-research: the whole story changes
- [ ] T034 [US2] Sanity test with BSL and Complementary: flash bloom, scope distortion, custom crosshair
- [ ] T035 [US2] Specifically verify depth reads with shaders on. Iris uses the main depth texture as `depthtex0`, but 26.3's `consistentDepthRequired` path is a vanilla path Iris partially replaces. This is the most fragile point in the feature
- [ ] T036 [US2] Check for banding from double tonemapping (we receive already-tonemapped sRGB and cannot undo it). If bad, soften the flash multiplier on unusual luminance distributions, or document the limitation and accept it

**Checkpoint**: Shaderpack users get effects for the first time.

---

## Phase 6: User Story 4 - Long-lived per-player effects on `/posteffect` (Priority: P3)

**Goal**: Per-player states that last more than a tick move off the sentinel channel.

Optional. Do not start it until User Stories 1 and 3 have shipped and settled.

- [ ] T037 [US4] Decide which states move: scope overlay, PaP tint, downed desaturation, spectator tint. The 1-tick muzzle flash stays on the particle marker (FR-008)
- [ ] T038 [US4] Implement defensive `posteffect clear` on player join, on respawn, and on game and round end. Effects persist in player NBT, so this is non-negotiable (FR-007)
- [ ] T039 [US4] Handle the lerp-freeze problem: an effect must stay applied for the duration of its own fade-out, or the smooth zoom snaps when it is removed
- [ ] T040 [US4] Verify no effect is added and removed within a single tick, since the packet is only sent when the list is dirty at end of tick
- [ ] T041 [US4] If splitting per plan.md architecture B: reserve `minecraft:main` pixels for the state handoff and document the contract next to `MARKER_MODES`

---

## Dependencies & Execution Order

- **Phase 1 (Setup)**: no dependencies
- **Phase 2 (Foundational)**: blocks everything. T007 in particular
- **Phase 3 (US1)**: T010 before all other US1 work. T014 depends on T008. T019 depends on every port task
- **Phase 4 (US3)**: depends on Phase 3, since deleting the old chain before the new one works leaves no fallback
- **Phase 5 (US2)**: depends on Phase 3 and on an external Iris release
- **Phase 6 (US4)**: depends on Phase 3, independent of Phases 4 and 5

### Parallel Opportunities

- T006, T008, T009 are independent verifications
- T012 and T013 touch different pass modules
- T028 is documentation and can run alongside any code task

---

## Implementation Strategy

Ship User Story 1, then User Story 3, and stop. That is a complete, correct 26.3 pack.
User Stories 2 and 4 are upside and neither blocks a release.

Do not delete anything (Phase 4) until Phase 3 is verified in-game. The deleted code is the only
fallback if the rehost turns out to be wrong.

## Notes

- F3+T after every GLSL fix. A compile error blacklists the effect until resource reload
- Keep the `DEBUG` blocks in the shaders; they earn their keep during a port
- Commit per shader ported, not per phase
