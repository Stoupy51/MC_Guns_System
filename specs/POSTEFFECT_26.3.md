# Post effects in 26.3: a course

> Every claim here is read from `26.3` release sources in [minecraft_source_code/](../minecraft_source_code/)
> and from the vanilla assets inside `.minecraft/versions/26.3/26.3.jar`. Nothing is from memory.
> Companion document: [TODO_26.3_SHADERS.md](../TODO_26.3_SHADERS.md), the migration plan.

---

## 1. Where a post effect sits

`GameRenderer.render()` runs this order every frame
([GameRenderer.java:494-501](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L494-L501)):

```
preparePostEffects(requested)   // resolve ids -> PostChain objects
renderLevel()                   // the whole world, OIT translucency, hand, 3D HUD
blitEntityOutline()             // glow outlines composited into main
applyPostEffects()              // <- post effects run here, in list order
guiRenderer.render()            // 2D HUD, never touched by post effects
```

Two consequences you get for free:

- Glow outlines are already in `minecraft:main` when your effect runs, so a screen warp warps them too.
- The 2D GUI is drawn after, so it is never distorted. A crosshair drawn by a post effect is a
  world-space-looking crosshair; the real HUD stays sharp on top.

A `PostChain` is a list of passes. Each pass is one fullscreen triangle
(`renderPass.draw(3, 1, 0, 0)`, [PostPass.java:144](../minecraft_source_code/net/minecraft/client/renderer/PostPass.java#L144))
reading N sampler inputs and writing exactly one output target.

---

## 2. The two ways to get one running

### `minecraft:end_of_frame` (always on)

Put `assets/minecraft/post_effect/end_of_frame.json` in the resource pack. It is prepended to the
request list every frame ([:432](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L432)),
so it **always runs first**, cannot be disabled by any command, and is silent when absent
(`ShaderManager` special-cases the missing-file warning for this id only,
[:353](../minecraft_source_code/net/minecraft/client/renderer/ShaderManager.java#L353)).

It must be in the `minecraft` namespace. `mgs:end_of_frame` does nothing.

### `/posteffect` (per player, server-driven)

```
/posteffect add    <players> <id>
/posteffect remove <players> <id>
/posteffect clear  <players>
/posteffect list   <target>
```

Permission level 2 (`Commands.LEVEL_GAMEMASTERS`). The id is any `assets/<ns>/post_effect/<path>.json`
in the client's resource packs. The server has no idea whether it exists; it just ships the id.

The whole list is sent as one packet,
[ClientboundPostEffectsPacket](../minecraft_source_code/net/minecraft/network/protocol/common/ClientboundPostEffectsPacket.java),
and the client replaces its list wholesale
([LocalPlayer.java:1324](../minecraft_source_code/net/minecraft/client/player/LocalPlayer.java#L1324)).

---

## 3. Command semantics, verified

| Question | Answer | Source |
|---|---|---|
| Can an id appear twice? | No. `add` returns false and the command fails if already present. | [ServerPlayer.java:1092](../minecraft_source_code/net/minecraft/server/level/ServerPlayer.java#L1092) |
| Is the list ordered? | Yes, insertion order, and that is the execution order. | [:1096](../minecraft_source_code/net/minecraft/server/level/ServerPlayer.java#L1096) |
| Can I reorder without clearing? | No. `remove` + `add` moves an effect to the end. | same |
| Does it survive relog? | Yes, stored in player NBT under `post_effects`. | [:463](../minecraft_source_code/net/minecraft/server/level/ServerPlayer.java#L463) |
| Does it survive death? | **No.** `restoreFrom` never copies `postEffects`, so a respawn starts empty. | [:1680](../minecraft_source_code/net/minecraft/server/level/ServerPlayer.java#L1680) |
| Does it survive a dimension change? | Yes, and `sendPostEffects()` is called explicitly on arrival. | [:1216](../minecraft_source_code/net/minecraft/server/level/ServerPlayer.java#L1216) |
| Missing on the client? | Logged once, added to `failedPostEffects`, skipped. No crash. | [GameRenderer.java:531](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L531) |
| Failed to compile? | Blacklisted until the next resource reload. F3+T after every GLSL fix. | [:523-527](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L523-L527) |
| `/execute store result` | `list` stores the effect count, the others store the affected player count. | [PostEffectCommand.java](../minecraft_source_code/net/minecraft/server/commands/PostEffectCommand.java) |

The death behaviour is the useful one: you do not need a defensive clear on respawn. You still need
one on join and on game end, because relog does restore.

---

## 4. The JSON format

```json
{
    "targets": {
        "state": { "width": 1, "height": 1, "persistent": true, "clear_color": 0 },
        "swap":  {}
    },
    "passes": [
        {
            "vertex_shader": "minecraft:core/screenquad",
            "fragment_shader": "mgs:post/hurt",
            "inputs": [
                { "sampler_name": "In",    "target": "minecraft:main", "bilinear": false },
                { "sampler_name": "Depth", "target": "minecraft:main", "use_depth_buffer": true },
                { "sampler_name": "Blood", "location": "mgs:blood", "width": 512, "height": 512 }
            ],
            "output": "swap",
            "uniforms": {
                "HurtConfig": [
                    { "name": "Tint",      "type": "vec3",  "value": [1.0, 0.1, 0.1] },
                    { "name": "Intensity", "type": "float", "value": 0.8 }
                ]
            }
        },
        {
            "vertex_shader": "minecraft:core/screenquad",
            "fragment_shader": "mgs:post/copy",
            "inputs": [ { "sampler_name": "In", "target": "swap" } ],
            "output": "minecraft:main"
        }
    ]
}
```

Rules, from [PostChainConfig.java](../minecraft_source_code/net/minecraft/client/renderer/PostChainConfig.java):

- **Targets.** `width`/`height` default to the screen size. Omitting both gives a fullscreen buffer.
  Format is hardcoded `RGBA8_UNORM` ([PostChain.java:248](../minecraft_source_code/net/minecraft/client/renderer/PostChain.java#L248)),
  so no HDR, 8 bits per channel, everything clamped to [0, 1].
- **`persistent: true`** keeps the target alive across frames. It is cleared to `clear_color` exactly
  once, when it is allocated ([RenderTargetDescriptor.prepare](../minecraft_source_code/com/mojang/blaze3d/resource/RenderTargetDescriptor.java)).
  Non-persistent targets are pooled and you must not assume their contents.
- **External targets.** A post effect may only reference `minecraft:main`
  (`LevelTargetBundle.MAIN_TARGETS`). Referencing `minecraft:entity_outline` or anything else makes
  `isPostEffectValid` reject the whole chain.
- **`sampler_name: "In"`** becomes the GLSL uniform **`InSampler`**. The suffix is added for you
  ([PostChain.java:101](../minecraft_source_code/net/minecraft/client/renderer/PostChain.java#L101)).
- **Texture inputs** resolve to `textures/effect/<path>.png`. `width`/`height` are mandatory and must
  match the real file.
- **`use_depth_buffer: true`** samples the depth texture of that target instead of its colour.
- **Uniforms** are baked from the JSON at load time. Types: `int`, `ivec3`, `float`, `vec2`, `vec3`,
  `vec4`, `matrix4x4` ([UniformValue.java:101](../minecraft_source_code/net/minecraft/client/renderer/UniformValue.java#L101)).
  They are constants. There is no server-side channel to change them.
- A pass must not sample the target it writes, and that includes `minecraft:main`. Reading main
  while rendering into it is a GPU feedback loop that shows up as a tiled grid of stale blocks
  across the screen. Render into a scratch target and copy back, as vanilla `invert` does with
  `swap`.

---

## 5. The GLSL contract

26.3 compiles through shaderc to SPIR-V, but the vanilla post shaders are still `#version 330`.
Here is the real `minecraft:post/box_blur`, unmodified:

```glsl
#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

uniform sampler2D InSampler;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform BlurConfig {
    vec2 BlurDir;
    float Radius;
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() { /* ... */ }
```

What changed and what you must do:

- `#moj_import` is gone. Use `#include <minecraft:globals.glsl>`, resolved under `shaders/include/`.
  Note the include name has **no** `include/` prefix.
- Every `in` and `out` needs an explicit `layout(location = N)`, and the
  `GL_ARB_separate_shader_objects` extension line.
- Vertex/fragment matching is now by location, not by name.
- Use `minecraft:core/screenquad` as the vertex shader unless you need custom varyings. It emits a
  fullscreen triangle from `gl_VertexIndex` with no vertex buffer, and passes `texCoord` at location 0.
  Note `gl_VertexIndex`, not `gl_VertexID`.
- `SamplerInfo` is filled with `OutSize` then one `vec2` per input, in declaration order. Declare only
  the prefix you use; vanilla `spiderclip.fsh` has two samplers and still declares only `InSize`.

### The free uniforms

`POST_PROCESSING_SNIPPET` inherits `GLOBALS_SNIPPET`, so every post pass gets the `Globals` block
bound ([RenderPipelines.java:340](../minecraft_source_code/net/minecraft/client/renderer/RenderPipelines.java#L340)):

```glsl
layout(std140) uniform Globals {
    ivec3 CameraBlockPos;   // floor of the camera position, world space
    float GlintAlpha;
    vec3  CameraOffset;     // fractional part, CameraBlockPos - cameraPos
    float GameTime;         // ((gameTime % 24000) + partialTick) / 24000
    vec2  ScreenSize;
    int   MenuBlurRadius;
    int   UseRgss;
};
```

**`GameTime` is the important one.** It advances with partial ticks, so it has sub-tick resolution,
and it wraps every 24000 ticks (20 minutes). `GameTime * 24000.0` gives you ticks.
`CameraBlockPos` + `CameraOffset` give you the camera in world space, which is enough to do
position-dependent effects without any server channel.

---

## 6. Your three questions

### How do I remove only one effect?

`/posteffect remove <players> <id>`. The list is a plain `List<Identifier>`, `remove` takes the
first match, and there can never be a second because `add` refuses duplicates. Removing an effect
that is not there makes the command fail (success count 0), which is a usable test:

```mcfunction
execute store success score #had mgs.data run posteffect remove @s mgs:hurt_critical
```

One thing to know: removing an effect **destroys its persistent targets**
([GameRenderer.java:546-548](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L546-L548)).
Re-adding it later reallocates them at `clear_color`. Any lerp or accumulator inside that chain
starts from zero again. Same thing happens whenever the level stops rendering, for example in a
menu, because `preparePostEffects(emptyList())` runs on that path
([:503](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L503)).

That reset is not only a hazard. It is the only per-activation signal the client gets, and section 7
turns it into a timer.

### Can an effect last a specific amount of time?

Not from the command. There is no duration argument and no server-side timer; the list only changes
when a command changes it.

From the shader, yes, and with millisecond precision. The recipe:

1. Declare a `1x1` `persistent` target with `clear_color: 0`.
2. On the first frame after `add`, that target is freshly cleared, so alpha is 0. Stamp `GameTime`
   into it and set alpha to 0.5 ("running").
3. Every later frame, read the stamp back, compute `elapsed = GameTime - stamp`, and drive the
   effect from it. When `elapsed` passes your duration, output the input unchanged.
4. Once `elapsed` is far past every duration (60 s here), set alpha to 1 ("settled"), which always
   reads as expired.
5. The server removes the effect on a later tick. The removal destroys the target, so the next `add`
   re-arms the timer automatically.

`clear_color` is ARGB, so `0` means fully transparent black and alpha is a reliable armed flag.
Store the timestamp in RGB only: 24 bits over 24000 ticks is 0.0014 ticks of resolution, about
0.07 ms.

A negative `elapsed` has two causes, and they need opposite answers:

- **The wrap.** Once every 20 minutes `GameTime` jumps from just under 1 back to 0, and the delta
  lands near -24000 ticks. Add a full cycle back. The settled state guarantees a running clock
  crosses the wrap at most once.
- **The server's time sync.** The client's game time is overwritten from the server every second,
  and when the client ran ahead it steps back a tick or two. Clamp to 0. Reading this as "expired"
  ends a fade on its first frames: the overlay vanishes, then pops back.

```glsl
// pass 1: state -> next  (1x1, computes the stamp)
#version 330
#extension GL_ARB_separate_shader_objects : require
#include <minecraft:globals.glsl>

uniform sampler2D StateSampler;
layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

vec3 packTime(float t) {
    vec3 enc = fract(t * vec3(1.0, 255.0, 65025.0));
    return enc - enc.yzz * vec3(1.0 / 255.0, 1.0 / 255.0, 0.0);
}

float elapsed(vec4 state) {
    if (state.a < 0.25) return 0.0;          // not armed yet
    if (state.a > 0.75) return 1.0e6;        // settled
    float delta = GameTime - dot(state.rgb, vec3(1.0, 1.0 / 255.0, 1.0 / 65025.0));
    if (delta < -0.5) delta += 1.0;          // GameTime wrapped
    return max(delta * 24000.0, 0.0);        // time sync stepped the client back
}

void main() {
    vec4 state = texture(StateSampler, vec2(0.5));
    // Alpha 0 means the target was just (re)allocated, so this frame is the activation frame.
    if (state.a < 0.25) {
        fragColor = vec4(packTime(GameTime), 0.5);
        return;
    }
    fragColor = elapsed(state) > 1200.0 ? vec4(state.rgb, 1.0) : state;
}
```

```glsl
// pass 3: apply, with the same elapsed() as pass 1
float life = clamp(elapsed(texture(NextSampler, vec2(0.5))) / 0.6, 0.0, 1.0);  // 0.6 tick = 30 ms
```

Pass 2 copies `next` back into `state`, because a pass may not sample its own output target. Two of
the three passes are `1x1`, so the cost is noise.

### Can the muzzle flash go sub-50 ms?

The command floor is exactly one tick, 50 ms, and that floor is hard.
`postEffectsDirty` is flushed once per player tick at the end of `ServerPlayer.tick()`
([:653](../minecraft_source_code/net/minecraft/server/level/ServerPlayer.java#L653)), while datapack
functions run earlier in the same tick (`tickChildren` pushes `commandFunctions` before `levels`,
[MinecraftServer.java:1089](../minecraft_source_code/net/minecraft/server/MinecraftServer.java#L1089)).
So an `add` reaches the client at the end of the tick it was issued in, which is good, but an
`add` and a `remove` in the **same** tick cancel out and the client sees nothing at all.

The visual duration is a different number from the applied duration. Apply for 2 ticks, fade over
30 ms with the timer above, and the player sees a 30 ms flash. That is 2 frames at 60 fps.

Re-arming one id needs a tick without it, and even that can fail: if the remove and the add
packets land in the same client frame, the chain is never torn down. Two identical ids used
alternately avoid both problems, since a *different* id is always a fresh chain with a fresh clock,
even when swapped within one tick. That lifts the ceiling to one burst per tick. The pack uses two
slots per variant and chooses a 2-tick cooldown (`{ns}.last_muzzle_flash`,
[flash.py](../src/functional/shaders/flash.py)), so bursts are capped at 10 per second by design.

Worth stating plainly: the current flash is screen-centred, not positioned at the shooter
(`FLASH_FSH` computes from `texCoord - 0.5`). So moving it to `/posteffect` loses nothing, and it
lets the `core/particle` override be deleted. That override is worth deleting on its own, because
26.3's changelog now says core shader overrides are explicitly unsupported.

---

## 7. Patterns

### Parameters you do not have

Uniforms are baked. A post effect has no arguments. Three ways around it, in increasing order of
effort:

**One id per value.** Five spread states is five JSON files generated from one Python template.
This is the right answer for anything with a handful of discrete levels: scope x3 and x4, PaP tint,
hurt tiers. It costs nothing at runtime because only the applied chain is instantiated.

**One id per transition.** The same trick, applied to animation. If a value must move smoothly from
A to B, bake *both ends* into the id: `mgs:crosshair_2_3` ramps from spread 2 to spread 3 over its
own clock. Five states become 25 generated files and the ramp is exact regardless of framerate.

**The pixel relay, within a frame only.** An effect can write a value into a few pixels of
`minecraft:main` and any effect *later in the same list* can read it back, which is an ordered
state bus across one frame. It does **not** survive to the next frame: `minecraft:main` is cleared
at the top of every frame ([GameRenderer.java:479](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L479),
plus `LevelRenderer`'s own clear pass), so nothing accumulates there.

That has a consequence worth stating plainly, because it rules out a whole class of designs:
**cross-frame state cannot follow a changing effect id.** Persistent targets are private to one
chain and are destroyed when that chain is removed, and main is wiped every frame, so there is no
place for a lerp to live while the id underneath it changes. Either the whole animation is baked
into one id (the pattern above), or the value has to arrive some other way.

**The camera.** `CameraBlockPos` and `CameraOffset` are free and exact. Anything that depends on
where the player is standing needs no channel at all.

### Fade-out is its own id

Removing an effect kills it on the frame the packet lands, so a chain can never animate its own
exit. Ship the exit as a second effect:

```mcfunction
# entering the scope
posteffect remove @s mgs:zoom_x4_out
posteffect add    @s mgs:zoom_x4

# leaving it, the swap happens in one tick so the client sees no gap
posteffect remove @s mgs:zoom_x4
posteffect add    @s mgs:zoom_x4_out
# and N ticks later
posteffect remove @s mgs:zoom_x4_out
```

Both chains use the section 6 timer. `zoom_x4` ramps 0 to 1 over its first 5 ticks and then holds,
`zoom_x4_out` ramps 1 to 0. Each one is re-armed by its own `add`, so the ramp always starts at the
right place and the duration is exact regardless of framerate. The cost is two JSON files per state,
which is free when they are generated from one Python function.

### Cost

Shipping any post effect flips `consistentDepthRequired` on permanently
([GameRenderer.java:671](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L671)),
which renders hand and 3D HUD depth into a separate target and adds a depth integration pass.

That pass, `core/integrate_depth`, copies the held item's depth back into main **before** post
effects run ([GameRenderer.java:726-741](../minecraft_source_code/net/minecraft/client/renderer/GameRenderer.java#L726-L741)),
and its colour is already in main too. A post effect therefore sees the gun and cannot draw behind
it. The pack overrides that one shader to write gun pixels at exactly `1.0`, the near plane, which no
world geometry can reach, so `mgs:post/flash` skips them. Nothing else reads main depth afterwards:
it is cleared before the GUI.

`end_of_frame` runs for every player with the pack loaded, every frame, forever. Keep it to 1x1
passes and a visually exact identity when nothing is active, or do not ship it at all and put
everything behind `/posteffect`, which costs nothing when nobody has an effect.

### Iris

Post effects compose with Iris shaderpacks. Iris finishes inside `renderLevel()` and its colorspace
pass is injected at that method's tail, both before `applyPostEffects()`. No Iris mixin touches
`getPostChain`, `requestedPostEffects` or `applyPostEffects`. You are overlaying an already
tonemapped sRGB image, so aggressive grading will band, but it works. See
[TODO_26.3_SHADERS.md](../TODO_26.3_SHADERS.md) section 1 for the file-by-file reading.

---

## 8. Checklist before shipping an effect

- [ ] File at `assets/<ns>/post_effect/<name>.json`, GLSL at `assets/<ns>/shaders/post/<name>.fsh`.
- [ ] `#version 330`, the `GL_ARB_separate_shader_objects` line, `layout(location = N)` on every
      `in` and `out`.
- [ ] No external target other than `minecraft:main`.
- [ ] No pass sampling its own output, `minecraft:main` included.
- [ ] Nothing assumes a non-persistent target's previous contents.
- [ ] Re-applying a burst alternates between two ids: the same id removed and re-added can be
      coalesced into one client frame and never re-arm.
- [ ] `posteffect clear` on player join and on game end. A respawn empties the list on its own, but
      any scores mirroring it must be reset (`deathCount` works).
- [ ] F3+T after every GLSL edit, or the client keeps the effect blacklisted.
- [ ] Check `/posteffect list` and the F3 `post_effects` debug line when something does not appear.
