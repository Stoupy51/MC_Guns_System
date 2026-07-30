# 26.3 Shader Migration — Research & TODO

> Written 2026-07-30 against `26.3 Snapshot 3`, decompiled sources in [minecraft_source_code/](minecraft_source_code/).
> Everything below was verified against that source tree and the Iris repo, not from memory.
> **Nothing here is implemented yet.** Target: whenever 26.3 goes stable.

---

## 0. TL;DR

Three independent things land at once in 26.3, and together they force a full rewrite of
[src/functional/shaders.py](src/functional/shaders.py):

1. **`minecraft:post_effect/transparency` no longer exists.** Fabulous compositing was replaced by
   OIT. Our entire post-processing system hangs off that override, so it is **dead**, not degraded.
2. **Post effects became a first-class, always-available feature** (`minecraft:end_of_frame` +
   `/posteffect`). This is a strictly better host for what we do — no Fabulous requirement, correct
   ordering, and clean world depth.
3. **Shaders are now compiled GLSL → SPIR-V through shaderc, targeting Vulkan 1.2.** `#moj_import`
   is gone. Every one of our 9 GLSL sources needs porting.

And the good news: **post effects compose with Iris shaderpacks**, for free. That is a capability we
have never had.

---

## 1. Iris compatibility — the original question

**Verdict: yes, they stack. The resource-pack post effect runs on top of the shaderpack's final
output, and nothing in Iris cancels it.**

### Vanilla ordering

[GameRenderer.java:485-494](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L485-L494):

```
preparePostEffects()      // resolve the PostChain list
renderLevel()             // → levelRenderer.render(...)   ← the whole Iris pipeline lives here
blitEntityOutline()
applyPostEffects()        // ← post effects run HERE, last
```

`applyPostEffects()` ([:530-539](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L530-L539))
iterates the chains and calls `postChain.process(this.mainRenderTarget, ...)`. The list is built in
[:420-434](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L420-L434):
`end_of_frame` first, then `player.getActivePostEffects()` (server-driven), then the spectator effect.

### Iris ordering

Read from the `26.2` branch of `IrisShaders/Iris`:

| Iris file | Behaviour |
| --- | --- |
| `mixin/state_tracking/MixinPostChain.java` | **Entirely empty class.** No `@Inject`, no cancel, no redirect. |
| `mixin/MixinLevelRenderer.java` | `iris$endLevelRender` → `pipeline.finalizeLevelRendering()`, injected on `popMatrix()` — i.e. the end of `LevelRenderer.render()` ([:284](minecraft_source_code/net/minecraft/client/renderer/LevelRenderer.java#L284), after `frame.execute`). The final pass writes into the main framebuffer. |
| `mixin/MixinGameRenderer.java` | `iris$runColorSpace` → `finalizeGameRendering()`, injected at **TAIL of `renderLevel`** — still before `applyPostEffects()`. |

No Iris mixin touches `getPostChain`, `requestedPostEffects`, `applyPostEffects`, or
`checkEntityPostEffect`. By the time a post effect runs, Iris is completely finished: composite,
final pass, colorspace conversion, all done.

### Consequences, good and bad

- ✅ Muzzle flash, scope zoom and crosshair would work **with shaders on**, for the first time.
- ⚠️ It is an *overlay*, not an integration. A post effect can only read `minecraft:main`
  (`LevelTargetBundle.MAIN_TARGETS`, [:14](minecraft_source_code/net/minecraft/client/renderer/LevelTargetBundle.java#L14)).
  Zero access to `colortex*`, `shadowtex*` or shaderpack uniforms.
- ⚠️ No HDR. `PostChainConfig.InternalTarget` is hardcoded `RGBA8_UNORM`
  ([PostChain.java:254](minecraft_source_code/net/minecraft/client/renderer/PostChain.java#L254)).
  We receive Iris's already-tonemapped sRGB output and cannot undo the tonemap. Aggressive grading
  will band.
- ⚠️ Depth works but is version-fragile. Iris uses Minecraft's main depth texture directly as
  `depthtex0` (`RenderTargets.currentDepthTexture`), so `use_depth_buffer: true` reads real world
  depth. But 26.3's new `consistentDepthRequired` path (§2.4) is a vanilla path Iris partially
  replaces — this is the #1 thing to test with shaders on.
- ⚠️ Double processing. Most packs already do their own DoF/AA/bloom in the final pass. Our zoom
  re-blurs an already-blurred image.
- ⚠️ `end_of_frame` is uncontrollable by design — it applies over the player's shaderpack with no
  opt-out. Keep it visually neutral when idle.
- 🔮 *Speculation:* Iris could add a "disable vanilla post effects" toggle later (OptiFine
  historically kills vanilla post chains when a pack is active). The analysis above describes
  today's code, not a contract.
- ⏳ **Iris has no 26.3 branch** as of writing. Latest branch is `26.2`, latest commit
  2026-07-29. Signatures moved (`renderLevel()` lost its arguments, `LevelRenderer.render` gained
  `consistentDepthRequired`) — routine remap, but untested.

---

## 2. What actually changed in 26.3

### 2.1 The transparency post chain is gone

Only **three** post-chain identifiers are referenced by the engine now:

- `minecraft:blur` — [GameRenderer.java:98](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L98) (menu background)
- `minecraft:entity_outline` — [LevelRenderer.java:106](minecraft_source_code/net/minecraft/client/renderer/LevelRenderer.java#L106)
- whatever `end_of_frame` / `/posteffect` requests

`minecraft:transparency` appears nowhere. `GraphicsPreset.FABULOUS` is now just a preset that flips
`options.improvedTransparency()` ([GraphicsPreset.java:81-108](minecraft_source_code/net/minecraft/client/GraphicsPreset.java#L81-L108)),
which routes to order-independent transparency in
[renderer/oit/](minecraft_source_code/net/minecraft/client/renderer/oit/) — not a post chain.
`LevelTargetBundle` grew `transmittance`, `accumulate`, `oitCloudDepth`,
`oitTerrainWithWaterPatchDepth`.

**⇒ `get_post_effect_json()` and `TRANSPARENCY_FSH` are dead code in 26.3.** No override point, and
nothing to reimplement — vanilla no longer needs us to composite anything.

### 2.2 `end_of_frame` — the replacement host

A resource pack may define `minecraft:post_effect/end_of_frame.json`. It is:

- prepended to the requested list every frame ([GameRenderer.java:426](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L426)),
  so it always runs **before** command-driven effects;
- always on while the pack is loaded, not controllable by `/posteffect`;
- last-pack-wins when several packs define it;
- **silent when absent** — `ShaderManager` special-cases it to skip the "non-existent post effect"
  warning ([ShaderManager.java:214](minecraft_source_code/net/minecraft/client/renderer/ShaderManager.java#L214)).

It only runs when a level is being rendered (`if (this.gameRenderState.shouldRenderLevel)`,
[GameRenderer.java:485](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L485)),
so no cost in menus.

Capabilities relevant to us:

| Need | Available? |
| --- | --- |
| Read `minecraft:main` colour | ✅ |
| Read main depth (`use_depth_buffer: true`) | ✅ [PostChainConfig.java:96](minecraft_source_code/net/minecraft/client/renderer/PostChainConfig.java#L96) |
| Write back to `minecraft:main` | ✅ |
| `persistent: true` 1×1 targets (our lerp feedback loops) | ✅ [PostChain.java:257-263](minecraft_source_code/net/minecraft/client/renderer/PostChain.java#L257-L263) |
| Arbitrary texture inputs (the 1536² spark sheet) | ✅ `TextureInput` |
| Baked uniform blocks | ✅ but **static JSON only** — no per-frame server values |
| Read `translucent` / `particles` / `clouds` / `weather` | ❌ main-only |
| HDR intermediates | ❌ `RGBA8_UNORM` |

### 2.3 `/posteffect` — server-driven, per-player

`/posteffect add|remove|clear|list` at permission level 2
([PostEffectCommand.java](minecraft_source_code/net/minecraft/server/commands/PostEffectCommand.java)),
synced by [ClientboundPostEffectsPacket](minecraft_source_code/net/minecraft/network/protocol/common/ClientboundPostEffectsPacket.java).

Gotchas, all verified:

- **Persisted in player NBT.** `output.store("post_effects", ...)`
  ([ServerPlayer.java:462](minecraft_source_code/net/minecraft/server/level/ServerPlayer.java#L462)).
  Effects survive relog and death → we **must** `posteffect clear` defensively on join / respawn /
  game end, or a crashed round leaves players permanently scoped.
- **One packet per tick, only when dirty**
  ([ServerPlayer.java:652](minecraft_source_code/net/minecraft/server/level/ServerPlayer.java#L652)).
  `add` then `remove` in the *same* tick leaves the list unchanged → the client never sees it. Any
  effect must live ≥ 1 full tick. This makes `/posteffect` a **bad fit for the 1-tick muzzle flash**.
- **Ordered list**, so effects stack: `zoom_x4` + `flash_pap` compose.
- **No parameters.** Uniforms are baked from JSON, so each discrete value needs its own post effect
  file — and each is a separate `PostChain` instance with its **own private persistent targets**,
  which breaks any smooth-lerp feedback loop that spans a state change.
- **Missing on the client → graceful.** Logged, added to `failedPostEffects`, no crash
  ([GameRenderer.java:517-527](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L517-L527)).
  So players without the resource pack are fine.
- **A compile error blacklists the effect until resource reload.** `failedPostEffects` is only
  cleared by `shouldResetFailedPostEffects` on reload
  ([:325-327](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L325-L327)) —
  F3+T after every GLSL fix during development.

### 2.4 `consistentDepthRequired` — a free win we should exploit

`consistentDepthRequired = !this.appliedPostEffects.isEmpty()`
([GameRenderer.java:650](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L650)).
When true, [:666-668](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L666-L668):

```java
GpuTexture depthTexture = consistentDepthRequired ? this.hud3DTarget.getDepthTexture() : this.mainRenderTarget.getDepthTexture();
clearDepthTexture(depthTexture, 0.0);
```

The hand / 3D HUD renders its **depth** into a separate target, leaving main's depth as clean world
depth — while its **colour** still lands in main. That is exactly what `FLASH_FSH` wants: the gun is
visible and lit, but does not pollute the depth-based falloff. `LevelRenderer` does the same for
always-on-top gizmos ([:479-495](minecraft_source_code/net/minecraft/client/renderer/LevelRenderer.java#L479-L495)).

Cost: shipping *any* post effect flips this on permanently — extra depth targets plus a depth
integration pass, for every player with the pack.

### 2.5 The entity_outline override becomes unnecessary

`applyPostEffects()` (line 492) runs **after** `blitEntityOutline()` (line 491). The glow outline is
already composited into main, so our zoom warps scene and outline together.

**⇒ `OUTLINE_ZOOM_FSH` and `get_entity_outline_json()` can be deleted outright** (~130 lines), along
with the whole "outline chain runs its own duplicate smooth-zoom feedback loop" workaround.

### 2.6 Renderer rewrite: `renderpearl`, Vulkan, SPIR-V

New package [com/mojang/renderpearl/](minecraft_source_code/com/mojang/renderpearl/) with
`backend/opengl` **and `backend/vulkan`**. Shaders now go through
[GlslCompiler.java](minecraft_source_code/com/mojang/renderpearl/frontend/shaders/GlslCompiler.java):

- `Shaderc.shaderc_compile_into_spv(...)`, `set_target_env(vulkan, 4202496)` → **Vulkan 1.2**.
  `#version 330` will not survive this; expect `#version 450` and Vulkan-flavour GLSL.
- `set_auto_bind_uniforms(true)`, `set_preserve_bindings(false)` → we do **not** need explicit
  `layout(set=, binding=)`. Good, that keeps the port shallow.
- `set_optimization_level(0)` + `generate_debug_info` → readable errors, at least.
- **`#moj_import` no longer exists anywhere in the source.** Standard `#include <ns:file.glsl>`,
  resolved under `shaders/include/` (`ShaderManager.SHADER_INCLUDE_PATH`,
  [:46](minecraft_source_code/net/minecraft/client/renderer/ShaderManager.java#L46)).
  In beet: `Mem.ctx.assets[ns].glsl_shaders["include/foo"]` → `shaders/include/foo.glsl` (no beet
  change needed; `GlslShader` already has the right scope).
- New macros we get for free: **`RENDERPEARL_DEPTH_IS_ZERO_TO_ONE`** (replaces our hardcoded
  reversed-Z guesswork in `LinearizeDepth` and the particle VSH `gl_Position.z`),
  `RENDERPEARL_EXPLICIT_DEPTH_INVARIANCE`, `RENDERPEARL_INSTANCE_INDEX_INCLUDES_BASE_INSTANCE`.

⚠️ A Vulkan backend also means the marker-particle trick must be re-validated end to end: core
shader overrides, the `Globals`/`ScreenSize` UBO binding situation, and `discard` semantics.

---

## 3. Inventory of [src/functional/shaders.py](src/functional/shaders.py)

| Asset | Fate |
| --- | --- |
| `PARTICLE_VSH` / `PARTICLE_FSH` (core/particle override) | **Port.** Vulkan GLSL, `#include`, use `RENDERPEARL_DEPTH_IS_ZERO_TO_ONE` instead of the hardcoded reversed-Z comment. Keep only if we keep the sentinel channel (§4). |
| `CLASSIFY_FSH` | **Port + rehost** into `end_of_frame`. |
| `SPREAD_COPY_FSH`, `ZOOM_LERP_FSH` | **Port**, unchanged in spirit — `persistent: true` still works. |
| `TRANSPARENCY_FSH` | **Delete** (~135 lines). Vanilla does OIT; nothing to composite. |
| `FLASH_FSH` | **Port.** `LinearizeDepth` rewritten around the depth macro. Main depth is now *cleaner* than before (§2.4). |
| `ZOOM_FSH` | **Port.** Biggest file, most to verify (bicubic, spark sheet, custom crosshair). |
| `OUTLINE_ZOOM_FSH` | **Delete** (~60 lines). Ordering makes it moot (§2.5). |
| `get_post_effect_json()` | **Rewrite** as `end_of_frame.json`; drop the transparency pass and its 12 sampler inputs. |
| `get_entity_outline_json()` | **Delete** (~85 lines). |
| `main()` registration | Rewrite: `post_effects["end_of_frame"]` in the **`minecraft`** namespace, plus any `mgs:` command-driven effects. |
| Docstring / `MARKER_MODES` | Rewrite — the "requires Fabulous" constraint disappears; the sentinel contract may too. |

Net: roughly **−280 lines deleted, ~600 lines ported**.

---

## 4. Target architecture

Two viable shapes. **Recommendation: start with A, move the expensive passes to B later if the
always-on cost shows up in profiling.**

### A — `end_of_frame` as a drop-in replacement (do this first)

Move the current chain verbatim (minus the transparency pass and the outline chain) into
`minecraft:post_effect/end_of_frame.json`. Keep the dust-marker sentinel as the parameter channel.

- ✅ Smallest diff, single chain, all persistent lerp buffers stay in one place.
- ✅ No Fabulous requirement — works on Fast/Fancy.
- ✅ Works with Iris.
- ⚠️ Runs every frame for every player, even idle. Idle cost ≈ three 1×1 passes + two fullscreen
  passes. Must be visually identity when no marker is present.
- ⚠️ Forces `consistentDepthRequired` on permanently (§2.4).

### B — split: cheap always-on state + `/posteffect`-gated heavy passes

- `end_of_frame`: only the 1×1 classify/lerp passes, then stamp the packed state into reserved
  corner pixels of `minecraft:main`. Nearly free.
- `mgs:zoom`, `mgs:flash`, … applied via `/posteffect`: the fullscreen work, reading state back
  from those main pixels. Zero cost when nobody is scoped.
- Works because `end_of_frame` is guaranteed to run first and *is* allowed to output to
  `minecraft:main`.
- Needed because per-chain internal targets are private: a gated effect **cannot** read
  `end_of_frame`'s persistent 1×1 buffers directly, only `minecraft:main`.
- ⚠️ `/posteffect` still can't do the 1-tick flash (§2.3) — the flash stays sentinel-driven either way.

### What `/posteffect` is genuinely good for

Long-lived, parameterless, per-player states where a tick of latency is irrelevant:
scope overlay, thermal/night vision, downed/last-stand desaturation, gas/flashbang, spectator tint.
Not for anything that changes every tick or needs a continuous value.

---

## 5. TODO

### Phase 0 — Verify before writing anything (in this order)

- [ ] Get a 26.3 client with a Vulkan-capable driver; check `--version` reports the SPIR-V path.
- [ ] Write a two-line `end_of_frame.json` (blit only) and confirm it loads, runs on **Fancy**, and
      does not break the F3 `post_effects` debug entry
      ([DebugEntryPostEffects.java](minecraft_source_code/net/minecraft/client/gui/components/debug/DebugEntryPostEffects.java)).
- [ ] Establish the minimum valid GLSL header for a post `.fsh` — `#version 450`? `layout(location)`
      required on `in`/`out`? Confirm `#include <minecraft:...>` resolves.
- [ ] **Confirm the marker sentinel survives to `applyPostEffects` time.** Highest risk item: with
      OIT, translucents are composited into main *before* post effects, whereas today `classify`
      reads main *before* compositing. The marker sits at the near plane so OIT should sort it in
      front, but verify by standing in water / behind glass and checking pixels (0,0)–(3,0).
- [ ] Confirm main depth is world depth (not hand depth) once a post effect is active — should hold
      per §2.4, but it's the foundation of `FLASH_FSH`.
- [ ] Confirm `persistent: true` 1×1 targets still survive across frames and resource reloads.
- [ ] Check whether `render3dCrosshair` ([GameRenderer.java:695](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L695))
      changes anything for our custom crosshair — 26.3 has a 3D crosshair path now.

### Phase 1 — Port the GLSL

- [ ] Bump `#version` and fix whatever shaderc rejects, one shader at a time, starting with the
      simplest (`SPREAD_COPY_FSH`).
- [ ] `#moj_import <minecraft:fog.glsl>` → `#include <minecraft:fog.glsl>` in the particle shaders;
      verify the include names still exist as vanilla assets.
- [ ] Replace the reversed-Z hand-rolled logic with `#ifdef RENDERPEARL_DEPTH_IS_ZERO_TO_ONE` in
      `LinearizeDepth` (`FLASH_FSH`) and in the particle VSH's near-plane `gl_Position`.
- [ ] Re-verify the `Globals` UBO / `ScreenSize` availability note in the `PARTICLE_VSH` comment —
      the fixed-NDC workaround may no longer be necessary, or may now be mandatory for a different
      reason.
- [ ] Keep `DEBUG` blocks; they will earn their keep here.

### Phase 2 — Rehost on `end_of_frame`

- [ ] New `get_end_of_frame_json()`: classify → spread_copy → zoom_lerp → flash → zoom → blit.
      Drop the transparency pass and all 12 of its samplers; `flash` now reads `minecraft:main`
      directly instead of a composited `final`.
- [ ] Register as `Mem.ctx.assets["minecraft"].post_effects["end_of_frame"]`.
- [ ] Delete `TRANSPARENCY_FSH`, `OUTLINE_ZOOM_FSH`, `get_entity_outline_json()`, and the
      `entity_outline` registration.
- [ ] Rewrite the module docstring: no Fabulous requirement, new ordering, new depth guarantees.
- [ ] Verify glow outlines now warp with the zoom for free (§2.5) — should be automatic.
- [ ] Verify the 2D GUI is *not* warped (`guiRenderer.render()` at
      [:501](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L501) is after
      post effects) and that the custom crosshair still sits correctly relative to real HUD elements.

### Phase 3 — `/posteffect` (second wave, optional)

- [ ] Decide what moves off the sentinel channel. Candidates: scope overlay, PaP tint. The 1-tick
      muzzle flash stays on the particle marker.
- [ ] **Defensive `posteffect clear`** on player join, respawn, and game/round end — effects persist
      in player NBT (§2.3). Non-negotiable if we use it at all.
- [ ] Handle the "lerp freezes when the effect is removed" problem: an effect must stay applied for
      the duration of its own fade-out, or the smooth zoom snaps.
- [ ] If splitting per architecture B: reserve main pixels for the state handoff and document the
      contract next to `MARKER_MODES`.

### Phase 4 — Iris validation

- [ ] Wait for an Iris 26.3 build.
- [ ] Sanity test with a heavy pack (BSL / Complementary): flash bloom, scope distortion, crosshair.
- [ ] Specifically check depth reads with shaders on — `FLASH_FSH` depends on main depth, and this is
      where the Iris/vanilla split is most fragile.
- [ ] Check for banding from double tonemapping; if bad, soften the flash multiplier when we detect
      an unusual luminance distribution, or accept it.
- [ ] Re-read `MixinPostChain` in the 26.3 branch — if it stops being an empty class, this whole
      section needs revisiting.

### Phase 5 — Housekeeping

- [ ] `beet.yml`: `minecraft: "26.3"`, and update the README's "MC Guns System 26.2".
- [ ] Drop any remaining "requires Fabulous graphics" wording from in-game messages and docs.
- [ ] `ruff check src --fix`.

---

## 6. Reference index

Local source (26.3 Snapshot 3):

- [GameRenderer.java](minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java) — post effect list, ordering, `consistentDepthRequired`
- [PostChain.java](minecraft_source_code/net/minecraft/client/renderer/PostChain.java) / [PostChainConfig.java](minecraft_source_code/net/minecraft/client/renderer/PostChainConfig.java) — JSON schema, target formats
- [LevelTargetBundle.java](minecraft_source_code/net/minecraft/client/renderer/LevelTargetBundle.java) — which targets a chain may reference
- [ShaderManager.java](minecraft_source_code/net/minecraft/client/renderer/ShaderManager.java) — loading, include path, `end_of_frame` special case
- [PostEffectCommand.java](minecraft_source_code/net/minecraft/server/commands/PostEffectCommand.java) / [ServerPlayer.java](minecraft_source_code/net/minecraft/server/level/ServerPlayer.java) — command, NBT persistence, packet timing
- [GlslCompiler.java](minecraft_source_code/com/mojang/renderpearl/frontend/shaders/GlslCompiler.java) — shaderc → SPIR-V, macros
- [renderer/oit/](minecraft_source_code/net/minecraft/client/renderer/oit/) — what replaced Fabulous compositing

External:

- <https://www.minecraft.net/en-us/article/minecraft-26-3-snapshot-3>
- <https://minecraft.wiki/w/Java_Edition_26.3_Snapshot_3>
- <https://minecraft.wiki/w/Commands/posteffect>
- <https://github.com/IrisShaders/Iris> — `common/src/main/java/net/irisshaders/iris/mixin/`
