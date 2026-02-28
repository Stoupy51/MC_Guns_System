# Imports
from beet import FragmentShader, PostEffect, VertexShader
from stewbeet import JsonDict, Mem, set_json_encoder, write_versioned_function

# ============================================================================ #
#                        SHADER SYSTEM OVERVIEW                                #
# ============================================================================ #
#
# This module implements full-screen post-processing effects (muzzle flash and
# scope zoom) by communicating between the datapack (mcfunctions) and the GPU
# (GLSL shaders) through a "marker particle" trick.
#
# ╔════════════════════════════════════════════════════════════════════════╗
# ║                         HOW IT WORKS                                   ║
# ╠════════════════════════════════════════════════════════════════════════╣
# ║                                                                        ║
# ║  1. DATAPACK spawns an entity_effect particle in front of the player   ║
# ║     with a specific color encoding the mode.                           ║
# ║     → fire_weapon.mcfunction  (flash marker, mode 1)                   ║
# ║     → tick.mcfunction         (zoom marker, mode 4)                    ║
# ║                                                                        ║
# ║  2. CORE PARTICLE SHADER (particle.vsh) intercepts ALL particles.      ║
# ║     It detects our marker by exact 8-bit integer color comparison.     ║
# ║     MARKER_RED = 254 in the R channel is the signature.                ║
# ║     G channel encodes the mode (1=flash, 4=zoom).                      ║
# ║     Detected markers are REDIRECTED to a SINGLE EXACT PIXEL at the     ║
# ║     bottom-left of the screen using ScreenSize from globals.glsl.      ║
# ║     → Mode 1 (flash) → pixel (0, 0)                                    ║
# ║     → Mode 4 (zoom)  → pixel (2, 0)                                    ║
# ║                                                                        ║
# ║  3. POST-EFFECT PIPELINE (transparency.json) runs these passes:        ║
# ║                                                                        ║
# ║     ┌─────────┐   reads exact pixels   ┌──────────┐                    ║
# ║     │particles├───────────────────────►│ CLASSIFY │ → 1x1 "classify"   ║
# ║     │ target  │   at (0,0) and (2,0)   │  (pass1) │   target w/ mode   ║
# ║     └─────────┘                        └──────────┘                    ║
# ║                                                                        ║
# ║     ┌──────────────┐                  ┌──────────────┐                 ║
# ║     │ all 6 layers ├─────────────────►│ TRANSPARENCY │ → "final"       ║
# ║     │  (fabulous)  │                  │   (pass2)    │   (hides px)    ║
# ║     └──────────────┘                  └──────────────┘                 ║
# ║                                                                        ║
# ║     ┌───────┐  ┌──────────┐           ┌───────┐                        ║
# ║     │ final ├──┤ classify ├──────────►│ FLASH │ → "swap" target        ║
# ║     └───────┘  └──────────┘           │(pass3)│                        ║
# ║                                       └───────┘                        ║
# ║                                                                        ║
# ║     ┌───────┐  ┌──────────┐           ┌───────┐                        ║
# ║     │ swap  ├──┤ classify ├──────────►│ ZOOM  │ → "final" target       ║
# ║     └───────┘  └──────────┘           │(pass4)│                        ║
# ║                                       └───────┘                        ║
# ║                                                                        ║
# ║     ┌───────┐                         ┌───────┐                        ║
# ║     │ final ├────────────────────────►│ BLIT  │ → minecraft:main       ║
# ║     └───────┘                         │(pass5)│                        ║
# ║                                       └───────┘                        ║
# ║                                                                        ║
# ╠════════════════════════════════════════════════════════════════════════╣
# ║                    KEY DESIGN DECISIONS                                ║
# ║                                                                        ║
# ║  WHY entity_effect instead of dust:                                    ║
# ║    entity_effect passes RGBA directly as vertex Color attribute with   ║
# ║    no random scaling. This allows exact 8-bit integer detection.       ║
# ║    Dust particles apply a random 0.8-1.0x multiplier that corrupts     ║
# ║    the color values, making exact detection impossible.                ║
# ║                                                                        ║
# ║  WHY ScreenSize for pixel placement:                                   ║
# ║    Hardcoded NDC coordinates (e.g. -0.98) map to different pixels at   ║
# ║    different resolutions. ScreenSize (from globals.glsl) lets us       ║
# ║    compute the exact NDC for a given pixel regardless of resolution.   ║
# ║    This is critical: if the marker lands on the wrong pixel, classify  ║
# ║    reads nothing and mode is always 0.                                 ║
# ║                                                                        ║
# ║  WHY alpha=1.0 forced in particle.fsh:                                 ║
# ║    When alpha < 1, the GPU blends RGB channels before storing them in  ║
# ║    the framebuffer (stored.rgb = src.a * src.rgb + ...). This corrupts ║
# ║    the mode values. With alpha=1, stored = src exactly.                ║
# ║    We force alpha=255 in the fsh so even aging particles work.         ║
# ║                                                                        ║
# ║  WHY flat varyings:                                                    ║
# ║    `flat` prevents interpolation between vertices. Without it, the     ║
# ║    isMarker flag and iColor could be interpolated across the quad,     ║
# ║    giving wrong values at non-vertex fragment positions.               ║
# ║                                                                        ║
# ╠════════════════════════════════════════════════════════════════════════╣
# ║                      ⚠ REQUIREMENTS ⚠                                 ║
# ║                                                                        ║
# ║  • Graphics MUST be set to "Fabulous!" for the post-effect pipeline    ║
# ║    to run. With Fancy/Fast, post_effect/transparency.json is IGNORED.  ║
# ║                                                                        ║
# ║  • The resource pack must be active and loaded.                        ║
# ║                                                                        ║
# ║  • The marker particle must be IN FRONT of the camera (not behind!)    ║
# ║    because Minecraft frustum-culls particles outside the view frustum  ║
# ║    BEFORE sending them to the GPU.                                     ║
# ║                                                                        ║
# ╠════════════════════════════════════════════════════════════════════════╣
# ║                         DEBUG MODE                                     ║
# ║                                                                        ║
# ║  Set DEBUG to 1 (currently ON) to show colored debug indicators:       ║
# ║                                                                        ║
# ║  BOTTOM-LEFT of screen, three 50x50 squares side by side:              ║
# ║    [RED]    = transparency compositing pass (pass 2) is running        ║
# ║    [GREEN]  = flash pass (pass 3) is running                           ║
# ║    [BLUE]   = zoom pass (pass 4) is running                            ║
# ║                                                                        ║
# ║  The zoom pass square color also encodes the detected mode:            ║
# ║    Blue   = pipeline active, no mode detected (mode 0)                 ║
# ║    Orange = muzzle flash detected (mode 1)                             ║
# ║    Cyan   = zoom detected (mode 4)                                     ║
# ║                                                                        ║
# ╚════════════════════════════════════════════════════════════════════════╝
#
# FILE RELATIONSHIPS:
#   shaders.py             → THIS FILE: generates all shaders + mcfunctions
#   particle.vsh/fsh       → Override minecraft:core/particle (core rendering)
#   classify.fsh           → Post pass 1: reads exact pixels → 1x1 mode
#   transparency.fsh       → Post pass 2: composites all layers, hides marker
#   flash.fsh              → Post pass 3: applies muzzle flash if mode 1
#   zoom.fsh               → Post pass 4: applies barrel distortion if mode 4
#   transparency.json      → Pipeline definition (post_effect/)
#   fire_weapon.mcfunction → Spawns flash marker particle on each shot
#   tick.mcfunction        → Spawns zoom marker particle each tick while ADS
#
# MARKER PIXEL MAP:
#   Mode 1 (flash) → screen pixel (0, 0)   [bottom-left corner]
#   Mode 4 (zoom)  → screen pixel (2, 0)   [2px right of corner]
#
# MARKER COLOR ENCODING (entity_effect RGBA):
#   R = 254/255 = 0.99607843  → MARKER_RED signature
#   G = mode/255              → encodes mode (1 or 4)
#   B = 0                     → always 0 (unused, part of signature)
#   A = 1.0                   → doesn't matter; fsh forces A=255 in output
#


# ============================================================================
# GLSL Shader Sources
# ============================================================================


# ────────────────────────────────────────────────────────────────────────────
# 1. CORE PARTICLE VERTEX SHADER
# ────────────────────────────────────────────────────────────────────────────
# Overrides: assets/minecraft/shaders/core/particle.vsh
# Role: Processes ALL particle vertices. Detects our marker entity_effect
#       particles by exact 8-bit integer color comparison (MARKER_RED=254),
#       then REDIRECTS them to single exact pixels at the screen corner.
#       Pixel position is calculated using ScreenSize from globals.glsl,
#       ensuring resolution-independence.
# Inspired by: ShaderSelectorV3 by HalbFettKaese
#
PARTICLE_VSH = """\
#version 330

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>
#moj_import <minecraft:projection.glsl>
#moj_import <minecraft:globals.glsl>
#moj_import <minecraft:sample_lightmap.glsl>

in vec3 Position;
in vec2 UV0;
in vec4 Color;
in ivec2 UV2;

uniform sampler2D Sampler2;

out float sphericalVertexDistance;
out float cylindricalVertexDistance;
out vec2 texCoord0;
out vec4 vertexColor;

// flat: no interpolation between vertices.
// Critical: isMarker and iColor must be identical across all 4 vertices
// of the quad, not interpolated.
flat out int isMarker;
flat out ivec4 iColor;

// ── Marker signature ──
// R channel value (0-255) that identifies a marker particle.
// Chosen to be far from any natural particle color.
#define MARKER_RED 254

// ── Quad corner offsets (UV space, [0,1]²) ──
// Maps gl_VertexID % 4 → corner of the 1-pixel quad.
// Must match Minecraft's particle quad winding order.
const vec2 corners[4] = vec2[4](
    vec2(0.0, 1.0),  // vertex 0: top-left
    vec2(0.0, 0.0),  // vertex 1: bottom-left
    vec2(1.0, 0.0),  // vertex 2: bottom-right
    vec2(1.0, 1.0)   // vertex 3: top-right
);

// ── Pixel address for each mode ──
// Returns the screen pixel (x, y) where the marker for this mode is placed.
// bottom-left origin. Must match the addresses used in classify.fsh and
// transparency.fsh.
//   Mode 1 (flash) → pixel (0, 0)
//   Mode 4 (zoom)  → pixel (2, 0)
ivec2 markerPixel(int mode) {
    if (mode == 1) return ivec2(0, 0);
    if (mode == 4) return ivec2(2, 0);
    return ivec2(0, 0);  // fallback (should never happen)
}

void main() {
    // Convert vertex Color float [0,1] → integer [0,255] for exact comparison.
    // entity_effect particles pass RGBA directly as Color; no random scaling.
    iColor = ivec4(round(Color * 255.0));

    // Detect marker: R == MARKER_RED, B == 0, G > 0 (encodes mode)
    // We do NOT check alpha here because entity_effect alpha can decrease
    // as the particle ages. R, G, B are stable throughout the lifetime.
    int mode = 0;
    if (iColor.r == MARKER_RED && iColor.b == 0 && iColor.g > 0) {
        mode = iColor.g;  // G channel directly encodes the mode (1 or 4)
    }

    // Only handle our two known modes; ignore unknown G values
    isMarker = int(mode == 1 || mode == 4);

    if (isMarker == 1) {
        // ── Pixel-perfect placement using ScreenSize ──
        // ScreenSize is available from globals.glsl in core shaders.
        // This is the critical fix vs. hardcoded NDC: the same NDC value
        // maps to different pixels at 1920x1080 vs 2560x1440 vs 1280x720.
        // Using ScreenSize ensures the marker always lands on the EXACT
        // pixel that classify.fsh will read.
        ivec2 pixel = markerPixel(mode);
        vec2 pixelSize = 2.0 / ScreenSize;          // NDC size of one pixel
        vec2 base = vec2(-1.0) + vec2(pixel) * pixelSize;  // NDC bottom-left of pixel
        gl_Position = vec4(base + corners[gl_VertexID % 4] * pixelSize, 0.0, 1.0);

        // Zero out all other varyings — they're not needed for markers
        sphericalVertexDistance = 0.0;
        cylindricalVertexDistance = 0.0;
        texCoord0 = vec2(0.0);
        vertexColor = vec4(0.0);
        return;
    }

    // ── Vanilla particle vertex processing ──
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
    sphericalVertexDistance = fog_spherical_distance(Position);
    cylindricalVertexDistance = fog_cylindrical_distance(Position);
    texCoord0 = UV0;
    vertexColor = Color * sample_lightmap(Sampler2, UV2);
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 2. CORE PARTICLE FRAGMENT SHADER
# ────────────────────────────────────────────────────────────────────────────
# Overrides: assets/minecraft/shaders/core/particle.fsh
# Role: For markers: writes the exact R, G, B from the original particle
#       color with FORCED alpha=255. The alpha=255 (1.0) ensures no blending
#       occurs with the background — stored value == written value exactly.
#       For normal particles: vanilla behavior.
# Sends to: particles render target (read by classify.fsh in post pipeline)
#
# CRITICAL — WHY FORCE ALPHA=255:
#   GL blend equation for standard alpha: stored.rgb = src.a * src.rgb + (1-src.a) * dst.rgb
#   With src.a = 1.0: stored.rgb = src.rgb (no change, exact)
#   With src.a = 0.01: stored.rgb = 0.01 * src.rgb + 0.99 * dst.rgb (corrupted!)
#   We force alpha=255 in the output so that even if the particle has aged
#   (and its internal alpha has decayed), the written pixel is always exact.
#
PARTICLE_FSH = """\
#version 330

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec2 texCoord0;
in vec4 vertexColor;
flat in int isMarker;
flat in ivec4 iColor;

out vec4 fragColor;

void main() {
    if (isMarker == 1) {
        // ── MARKER SENTINEL ──
        // Write exact R, G, B from original particle color.
        // Force alpha = 255/255 = 1.0 so the framebuffer stores exactly
        // what we write (no blending corruption regardless of blend equation).
        // classify.fsh will read this pixel and verify R==254, B==0, A==255.
        fragColor = vec4(float(iColor.r), float(iColor.g), float(iColor.b), 255.0) / 255.0;
        return;
    }

    // ── NORMAL PARTICLE RENDERING (vanilla behavior) ──
    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
    if (color.a < 0.1) {
        discard;
    }
    fragColor = apply_fog(color, sphericalVertexDistance, cylindricalVertexDistance,
        FogEnvironmentalStart, FogEnvironmentalEnd,
        FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 3. POST-PROCESSING: CLASSIFY PASS
# ────────────────────────────────────────────────────────────────────────────
# File: assets/<ns>/shaders/post/classify.fsh
# Role: Reads the particles render target at EXACT known pixel addresses
#       and detects the marker sentinel. Outputs to a tiny 1x1 "classify"
#       target containing the detected mode.
# Receives from: particles target (written by particle.fsh)
# Sends to: classify target (read by flash.fsh, zoom.fsh)
#
# KEY DIFFERENCE vs. old approach:
#   Old code scanned a region (5x3 loop) and guessed where the marker might
#   be. This failed whenever the marker landed outside the scan region due
#   to resolution differences.
#   New code reads EXACTLY pixel (0,0) for flash and pixel (2,0) for zoom.
#   These are the same pixels the vsh placed the marker at (using ScreenSize).
#
CLASSIFY_FSH = """\
#version 330

uniform sampler2D ParticlesSampler;

in vec2 texCoord;
out vec4 fragColor;

#define MARKERS 5
#define MARKER_RED 254

void main() {
    // ── Read the exact marker pixels ──
    // Mode 1 (flash): placed at pixel (0, 0) by particle.vsh
    // Mode 4 (zoom):  placed at pixel (2, 0) by particle.vsh
    // texelFetch uses integer pixel coordinates — no UV math, no rounding error.
    ivec4 p1 = ivec4(round(texelFetch(ParticlesSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 p4 = ivec4(round(texelFetch(ParticlesSampler, ivec2(2, 0), 0) * 255.0));

    // ── Verify sentinel signature ──
    // R == MARKER_RED: our unique identifier
    // B == 0: part of signature (we never use B channel for anything else)
    // A == 255: confirms particle.fsh wrote it (not a stale clear value)
    // G == expected mode value: confirms this specific mode is active
    bool flashActive = (p1.r == MARKER_RED && p1.b == 0 && p1.a == 255 && p1.g == 1);
    bool zoomActive  = (p4.r == MARKER_RED && p4.b == 0 && p4.a == 255 && p4.g == 4);

    // Flash takes priority over zoom (can't do both at once)
    float mode = 0.0;
    if (flashActive)     mode = 1.0;
    else if (zoomActive) mode = 4.0;

    // Output: encode mode in red channel of the 1x1 target.
    // flash.fsh and zoom.fsh read it: round(texture(...).r * MARKERS)
    fragColor = vec4(mode / float(MARKERS), 0.0, 0.0, 1.0);
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 4. POST-PROCESSING: TRANSPARENCY COMPOSITING
# ────────────────────────────────────────────────────────────────────────────
# File: assets/<ns>/shaders/post/transparency.fsh
# Role: Fabulous transparency compositing (merges all 6 render layers).
#       Also HIDES the marker pixels so they're invisible in the final image.
# Receives from: All 6 Fabulous render targets + depth buffers
# Sends to: "final" target (read by flash.fsh)
#
# Marker pixels are hidden by checking gl_FragCoord against the two known
# pixel addresses. No color-based heuristics needed.
#
TRANSPARENCY_FSH = """\
#version 330

uniform sampler2D MainSampler;
uniform sampler2D MainDepthSampler;
uniform sampler2D TranslucentSampler;
uniform sampler2D TranslucentDepthSampler;
uniform sampler2D ItemEntitySampler;
uniform sampler2D ItemEntityDepthSampler;
uniform sampler2D ParticlesSampler;
uniform sampler2D ParticlesDepthSampler;
uniform sampler2D CloudsSampler;
uniform sampler2D CloudsDepthSampler;
uniform sampler2D WeatherSampler;
uniform sampler2D WeatherDepthSampler;

in vec2 texCoord;

#define DEBUG 1

vec4 color_layers[6] = vec4[](vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0));
float depth_layers[6] = float[](0, 0, 0, 0, 0, 0);
int active_layers = 0;

out vec4 fragColor;

void try_insert(vec4 color, float depth) {
    if (color.a == 0.0) {
        return;
    }
    color_layers[active_layers] = color;
    depth_layers[active_layers] = depth;
    int jj = active_layers++;
    int ii = jj - 1;
    while (jj > 0 && depth_layers[jj] > depth_layers[ii]) {
        float depthTemp = depth_layers[ii];
        depth_layers[ii] = depth_layers[jj];
        depth_layers[jj] = depthTemp;
        vec4 colorTemp = color_layers[ii];
        color_layers[ii] = color_layers[jj];
        color_layers[jj] = colorTemp;
        jj = ii--;
    }
}

vec3 blend(vec3 dst, vec4 src) {
    return (dst * (1.0 - src.a)) + src.rgb;
}

void main() {
    color_layers[0] = vec4(texture(MainSampler, texCoord).rgb, 1.0);
    depth_layers[0] = texture(MainDepthSampler, texCoord).r;
    active_layers = 1;

    try_insert(texture(TranslucentSampler, texCoord), texture(TranslucentDepthSampler, texCoord).r);
    try_insert(texture(ItemEntitySampler, texCoord), texture(ItemEntityDepthSampler, texCoord).r);

    // ── PARTICLES LAYER: skip the exact marker pixels ──
    // Marker pixels are at known fixed addresses: (0,0) and (2,0).
    // gl_FragCoord.xy has (0.5, 0.5) at the center of pixel (0,0),
    // so pixel (0,0) satisfies: x in [0,1), y in [0,1)
    //    pixel (2,0) satisfies: x in [2,3), y in [0,1)
    // No color-based heuristic needed — exact position check only.
    vec4 particleColor = texture(ParticlesSampler, texCoord);
    float particleDepth = texture(ParticlesDepthSampler, texCoord).r;
    bool isMarkerPixel = (gl_FragCoord.y < 1.0) && (
        (gl_FragCoord.x < 1.0) ||                                        // pixel (0,0): flash
        (gl_FragCoord.x >= 2.0 && gl_FragCoord.x < 3.0)                  // pixel (2,0): zoom
    );
    if (!isMarkerPixel) {
        try_insert(particleColor, particleDepth);
    }

    try_insert(texture(WeatherSampler, texCoord), texture(WeatherDepthSampler, texCoord).r);
    try_insert(texture(CloudsSampler, texCoord), texture(CloudsDepthSampler, texCoord).r);

    vec3 texelAccum = color_layers[0].rgb;
    for (int ii = 1; ii < active_layers; ++ii) {
        texelAccum = blend(texelAccum, color_layers[ii]);
    }

    fragColor = vec4(texelAccum.rgb, 1.0);

#if DEBUG
    if (gl_FragCoord.x < 50.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = pass 2 runs
    }
#endif
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 5. POST-PROCESSING: MUZZLE FLASH EFFECT
# ────────────────────────────────────────────────────────────────────────────
# (unchanged from previous version)
#
FLASH_FSH = """\
#version 330

uniform sampler2D InSampler;
uniform sampler2D InDepthSampler;
uniform sampler2D ClassifySampler;

layout(std140) uniform FlashConfig {
    vec3 Color;
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 1
#define MARKERS 5
#define INTENSITY 1.5
#define MAXDIST 20.0
#define NEAR 0.1
#define FAR 1536.0
#define BLURR 10.0
#define FOV 70
#define CK tan(float(FOV) / 360.0 * 3.14159265358979) * 2.0

float LinearizeDepth(float depth) {
    float z = depth * 2.0 - 1.0;
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));
}

void main() {
    vec2 inSize = vec2(textureSize(InSampler, 0));
    float mode = round(texture(ClassifySampler, vec2(0.5, 0.5)).r * float(MARKERS));

    fragColor = texture(InSampler, texCoord);

    if (mode >= 1.0 && mode <= 3.0) {
        vec2 oneTexel = 1.0 / inSize;
        float aspectRatio = inSize.x / inSize.y;

        float depth = LinearizeDepth(texture(InDepthSampler, texCoord).r);
        vec2 screenCoords = (texCoord - 0.5) * vec2(aspectRatio, 1.0) * CK * depth;
        float dist = length(vec3(screenCoords, depth));

        if (dist < MAXDIST) {
            vec4 blurColor = fragColor
                + texture(InSampler, texCoord + vec2(oneTexel.x * BLURR, 0.0))
                + texture(InSampler, texCoord - vec2(oneTexel.x * BLURR, 0.0))
                + texture(InSampler, texCoord + vec2(0.0, oneTexel.y * BLURR))
                + texture(InSampler, texCoord - vec2(0.0, oneTexel.y * BLURR));
            blurColor /= 5.0;

            vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * Color;

            fragColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9)
                           * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0)) + vec3(1.0);
            fragColor.rgb += INTENSITY * lightColor * 0.1;
        }
    }

    fragColor = vec4(fragColor.rgb, 1.0);

#if DEBUG
    if (gl_FragCoord.x >= 50.0 && gl_FragCoord.x < 100.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = pass 3 runs
    }
#endif
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 6. POST-PROCESSING: BARREL DISTORTION ZOOM
# ────────────────────────────────────────────────────────────────────────────
# (unchanged from previous version)
#
ZOOM_FSH = """\
#version 330

uniform sampler2D InSampler;
uniform sampler2D ClassifySampler;

layout(std140) uniform ZoomConfig {
    float Distortion;
    float Zoom;
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 1
#define MARKERS 5
#define RADIUS 0.14

vec4 cubic(float v) {
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    float w = 6.0 - x - y - z;
    return vec4(x, y, z, w) * (1.0 / 6.0);
}

vec4 textureBicubic(sampler2D samp, vec2 texCoords, vec2 texSize) {
    vec2 oneTexel = 1.0 / texSize;
    texCoords = texCoords * texSize - 0.5;
    vec2 fxy = fract(texCoords);
    texCoords -= fxy;

    vec4 xcubic = cubic(fxy.x);
    vec4 ycubic = cubic(fxy.y);

    vec4 c = texCoords.xxyy + vec2(-0.5, 1.5).xyxy;
    vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
    vec4 offsetbc = c + vec4(xcubic.yw, ycubic.yw) / s;
    offsetbc *= oneTexel.xxyy;

    vec4 sample0 = texture(samp, offsetbc.xz);
    vec4 sample1 = texture(samp, offsetbc.yz);
    vec4 sample2 = texture(samp, offsetbc.xw);
    vec4 sample3 = texture(samp, offsetbc.yw);

    float sx = s.x / (s.x + s.y);
    float sy = s.z / (s.z + s.w);

    return mix(mix(sample3, sample2, sx), mix(sample1, sample0, sx), sy);
}

void main() {
    vec2 inSize = vec2(textureSize(InSampler, 0));
    float mode = round(texture(ClassifySampler, vec2(0.5, 0.5)).r * float(MARKERS));

    fragColor = texture(InSampler, texCoord);

    if (mode >= 3.5 && mode <= 4.5) {
        float aspectRatio = inSize.x / inSize.y;
        vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

        if (length(screenCoord) < RADIUS) {
            float d = length(screenCoord * Distortion / RADIUS);
            float z = sqrt(1.0 - d * d);
            float r = atan(d, z) / 3.1415926535;
            float theta = atan(screenCoord.y, screenCoord.x);

            screenCoord = vec2(cos(theta), sin(theta)) * r / Zoom;
            vec2 pixCoord = screenCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5);

            fragColor = textureBicubic(InSampler, pixCoord, inSize);
        }
    }

#if DEBUG
    if (gl_FragCoord.x >= 100.0 && gl_FragCoord.x < 150.0 && gl_FragCoord.y < 50.0) {
        if (mode >= 0.5 && mode <= 3.5) {
            fragColor = vec4(1.0, 0.5, 0.0, 1.0);  // Orange: flash mode
        } else if (mode >= 3.5 && mode <= 4.5) {
            fragColor = vec4(0.0, 1.0, 1.0, 1.0);  // Cyan: zoom mode
        } else {
            fragColor = vec4(0.2, 0.2, 1.0, 1.0);  // Blue: no mode
        }
    }
#endif
}
"""


# ============================================================================
# Post-effect pipeline definition
# ============================================================================

def get_post_effect_json(ns: str) -> JsonDict:
    """Build the transparency post-effect pipeline JSON.

    Overrides minecraft:post_effect/transparency.json.
    5 passes: classify -> transparency -> flash -> zoom -> blit.
    Only runs when Graphics = "Fabulous!".
    """
    return {
        "targets": {
            # 1x1 target storing the detected mode
            "classify": {"width": 1, "height": 1, "persistent": True},
            # Full-screen working targets (ping-pong)
            "final": {},
            "swap": {},
        },
        "passes": [
            # Pass 1: CLASSIFY - read exact marker pixels, output mode to 1x1 target
            {
                "vertex_shader": "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/classify",
                "inputs": [
                    {"sampler_name": "Particles", "target": "minecraft:particles"},
                ],
                "output": "classify",
            },
            # Pass 2: TRANSPARENCY - Fabulous compositing (hides marker pixels)
            {
                "vertex_shader": "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/transparency",
                "inputs": [
                    {"sampler_name": "Main",            "target": "minecraft:main"},
                    {"sampler_name": "MainDepth",       "target": "minecraft:main",        "use_depth_buffer": True},
                    {"sampler_name": "Translucent",     "target": "minecraft:translucent"},
                    {"sampler_name": "TranslucentDepth","target": "minecraft:translucent",  "use_depth_buffer": True},
                    {"sampler_name": "ItemEntity",      "target": "minecraft:item_entity"},
                    {"sampler_name": "ItemEntityDepth", "target": "minecraft:item_entity",  "use_depth_buffer": True},
                    {"sampler_name": "Particles",       "target": "minecraft:particles"},
                    {"sampler_name": "ParticlesDepth",  "target": "minecraft:particles",   "use_depth_buffer": True},
                    {"sampler_name": "Clouds",          "target": "minecraft:clouds"},
                    {"sampler_name": "CloudsDepth",     "target": "minecraft:clouds",      "use_depth_buffer": True},
                    {"sampler_name": "Weather",         "target": "minecraft:weather"},
                    {"sampler_name": "WeatherDepth",    "target": "minecraft:weather",     "use_depth_buffer": True},
                ],
                "output": "final",
            },
            # Pass 3: FLASH - depth-based muzzle flash (if mode 1)
            {
                "vertex_shader": "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/flash",
                "inputs": [
                    {"sampler_name": "In",       "target": "final"},
                    {"sampler_name": "InDepth",  "target": "minecraft:main", "use_depth_buffer": True},
                    {"sampler_name": "Classify", "target": "classify"},
                ],
                "output": "swap",
                "uniforms": {
                    "FlashConfig": [
                        {"name": "Color", "type": "vec3", "value": [1.0, 0.8, 0.5]},
                    ],
                },
            },
            # Pass 4: ZOOM - barrel distortion (if mode 4)
            {
                "vertex_shader": "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/zoom",
                "inputs": [
                    {"sampler_name": "In",       "target": "swap", "bilinear": True},
                    {"sampler_name": "Classify", "target": "classify"},
                ],
                "output": "final",
                "uniforms": {
                    "ZoomConfig": [
                        {"name": "Distortion", "type": "float", "value": 0.55},
                        {"name": "Zoom",       "type": "float", "value": 4.0},
                    ],
                },
            },
            # Pass 5: BLIT - copy final result to screen
            {
                "vertex_shader": "minecraft:core/screenquad",
                "fragment_shader": "minecraft:post/blit",
                "inputs": [
                    {"sampler_name": "In", "target": "final"},
                ],
                "uniforms": {
                    "BlitConfig": [
                        {"name": "ColorModulate", "type": "vec4", "value": [1.0, 1.0, 1.0, 1.0]},
                    ],
                },
                "output": "minecraft:main",
            },
        ],
    }


# ============================================================================
# Main entry point
# ============================================================================

def main() -> None:
    """Register all shader files and write marker particle commands.

    Called from link.py as main_shaders(), BEFORE main_weapon().
    """
    ns: str = Mem.ctx.project_id

    # ── Register core particle shaders (override vanilla) ──
    Mem.ctx.assets["minecraft"].vertex_shaders["core/particle"]   = VertexShader(PARTICLE_VSH)
    Mem.ctx.assets["minecraft"].fragment_shaders["core/particle"] = FragmentShader(PARTICLE_FSH)

    # ── Register post-processing fragment shaders ──
    Mem.ctx.assets[ns].fragment_shaders["post/classify"]    = FragmentShader(CLASSIFY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/transparency"] = FragmentShader(TRANSPARENCY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/flash"]       = FragmentShader(FLASH_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/zoom"]        = FragmentShader(ZOOM_FSH)

    # ── Register post-effect pipeline (overrides vanilla transparency) ──
    Mem.ctx.assets["minecraft"].post_effects["transparency"] = set_json_encoder(PostEffect(get_post_effect_json(ns)))

    # ── Datapack: spawn marker particles ──
    #
    # We use entity_effect particles instead of dust because:
    #   - entity_effect passes RGBA directly as vertex Color (no random scaling)
    #   - Values survive as exact 8-bit integers in the GPU
    #   - Dust applies a random 0.8-1.0x multiplier, corrupting color values
    #
    # MARKER COLOR ENCODING:
    #   R = 254/255 = 0.99607843  → MARKER_RED (signature)
    #   G = mode/255              → mode 1 = 0.00392157, mode 4 = 0.01568627
    #   B = 0.0                   → signature (always 0)
    #   A = 1.0                   → not checked in vsh (may degrade with age)
    #
    # PIXEL PLACEMENT (handled by particle.vsh using ScreenSize):
    #   Mode 1 (flash) → screen pixel (0, 0)
    #   Mode 4 (zoom)  → screen pixel (2, 0)
    #
    # The particle MUST be IN FRONT of the camera (^ ^ ^1, not ^ ^ ^-500)!

    # ── Flash marker: mode 1 (G = 1/255 = 0.00392157) ──
    write_versioned_function("player/fire_weapon",
"""
# Shader: spawn muzzle flash marker (mode 1)
# entity_effect: R=254/255, G=1/255, B=0, A=1 → detected by particle.vsh → placed at pixel (0,0)
execute at @s anchored eyes run particle minecraft:entity_effect{color:[0.99607843,0.00392157,0.0,1.0],scale:1f} ^ ^ ^1 0 0 0 0 1 force @s
""")

    # ── Zoom marker: mode 4 (G = 4/255 = 0.01568627) ──
    write_versioned_function("player/tick",
f"""
# Shader: spawn zoom marker (mode 4)
# entity_effect: R=254/255, G=4/255, B=0, A=1 → detected by particle.vsh → placed at pixel (2,0)
execute if score @s {ns}.zoom matches 1 at @s anchored eyes run particle minecraft:entity_effect{{color:[0.99607843,0.01568627,0.0,1.0],scale:1f}} ^ ^ ^1 0 0 0 0 1 force @s
""")

