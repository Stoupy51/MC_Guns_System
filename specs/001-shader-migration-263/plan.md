# Implementation Plan: 26.3 Shader Migration

**Branch**: `001-shader-migration-263` | **Date**: 2026-08-15 | **Spec**: [spec.md](spec.md)

## Summary

Rehost the entire visual pipeline from the removed `minecraft:transparency` post chain onto
`minecraft:end_of_frame`, port all 9 GLSL sources to Vulkan-flavour GLSL compiled through shaderc, and
delete the ~280 lines that only existed to satisfy 26.2's Fabulous compositing requirement.

The order is deliberate: verify the platform first (Phase 0), port shaders in isolation second, rehost
third. Every phase before the rehost is reversible; the rehost is the point of no return for 26.2.

## Technical Context

**Language/Version**: Python >=3.14 for generation, GLSL (Vulkan 1.2 / SPIR-V) for the shaders themselves

**Primary Dependencies**: beet + StewBeet (`stewbeet>=3.6.2`); `Mem.ctx.assets` for post-effect and GLSL registration

**Storage**: N/A. Post-effect state lives in GPU render targets; per-player `/posteffect` state lives in player NBT

**Testing**: In-game only. No unit test can exercise a fragment shader; every task ends in a client check

**Target Platform**: Minecraft Java 26.3 client, Vulkan-capable driver, with and without an Iris shaderpack

**Project Type**: Minecraft resource pack assets generated from a Python build pipeline

**Performance Goals**: `end_of_frame` runs every frame for every player with the pack. Idle cost capped at three 1x1 passes plus two fullscreen passes, and idle output must be pixel-identical to no effect

**Constraints**: No HDR intermediates (`RGBA8_UNORM` is hardcoded). A chain can only read `minecraft:main` plus its own targets. Uniforms are baked from JSON, so no per-frame server values

**Scale/Scope**: One module, [src/functional/shaders.py](../../src/functional/shaders.py). Roughly 600 lines ported and 280 deleted

## Constitution Check

*GATE: passed.*

| Principle | How this plan satisfies it |
|---|---|
| I. Python sources are the only source of truth | All GLSL and post-effect JSON stays generated from `shaders.py`. No hand-written asset lands in `build/`. |
| II. Data-driven definitions | The pass list becomes one declarative structure feeding `get_end_of_frame_json()`, not per-pass copy-paste. |
| III. Typed, linted, readable | `shaders.py` is already near the 300-line guidance; the port is the moment to split it into a package (see structure below). |
| IV. Runtime cost is a design constraint | `end_of_frame` is uncontrollable and always on, so FR-002 (idle identity) and SC-002 (idle budget) are hard requirements, not nice-to-haves. |
| V. In-game verification | Phase 0 is nothing but verification, and every later task names the client check that closes it. |

## Project Structure

### Documentation (this feature)

```text
specs/001-shader-migration-263/
├── spec.md
├── plan.md              # This file
└── tasks.md
```

The existing [TODO_26.3_SHADERS.md](../../TODO_26.3_SHADERS.md) stands in for `research.md`. It is
line-referenced against the decompiled sources and should not be duplicated here; it is deleted once
this feature ships, with anything still true folded into the module docstring.

### Source Code (repository root)

```text
src/functional/
├── shaders.py                  # Today: one module, ~1400 lines, everything
└── shaders/                    # After the port, grouped by feature per the constitution
    ├── __init__.py             # main(): registers end_of_frame + any mgs: command-driven effects
    ├── chain.py                # get_end_of_frame_json(): the declarative pass list
    ├── passes/                 # One module per pass, each owning its GLSL
    │   ├── classify.py         # CLASSIFY_FSH: reads the marker sentinel out of main
    │   ├── spread.py           # SPREAD_COPY_FSH
    │   ├── zoom.py             # ZOOM_FSH + ZOOM_LERP_FSH, the bicubic and spark sheet work
    │   └── flash.py            # FLASH_FSH, LinearizeDepth
    └── particle.py             # PARTICLE_VSH / PARTICLE_FSH core override, the sentinel emitter

assets/textures/                # The 1536² spark sheet, unchanged
```

**Structure Decision**: `shaders.py` becomes `src/functional/shaders/`, grouped by pass rather than by
kind (all GLSL in one file, all JSON in another), because a pass's shader source and its JSON pass
entry only make sense together. This is the constitution's "group by feature, not by kind" rule, and
the port is the only cheap moment to do it.

## Complexity Tracking

No constitution violations. Two costs are accepted deliberately and recorded here so they are not
re-litigated later:

| Accepted cost | Why | Alternative rejected because |
|---|---|---|
| `consistentDepthRequired` permanently on | Shipping any post effect flips it. It is also what gives `FLASH_FSH` clean world depth instead of hand depth. | Not shipping a post effect means not having the feature. |
| `end_of_frame` runs every frame, even idle | It is the only host that works without Fabulous and composes with Iris. | Architecture B (`/posteffect`-gated heavy passes) cannot do the 1-tick flash and cannot share persistent targets across chains. Revisit only if profiling shows the idle cost. |
