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
# ║  1. DATAPACK spawns a dust particle in front of the player             ║
# ║     with a specific color encoding the mode.                           ║
# ║     → fire_weapon.mcfunction  (flash marker, mode 1)                   ║
# ║     → tick.mcfunction         (zoom marker, mode 4)                    ║
# ║                                                                        ║
# ║  2. CORE PARTICLE SHADER (particle.vsh) intercepts ALL particles.      ║
# ║     It detects our marker by range-based color pattern detection.      ║
# ║     R∈[1-10] with B==0 identifies our marker (dust is very dim).      ║
# ║     G==0 → flash (mode 1), G∈[1-10] → zoom (mode 4).                 ║
# ║     Detected markers are REDIRECTED to a small quad at the             ║
# ║     bottom-left of the screen using fixed NDC coordinates.             ║
# ║     The fsh only writes the sentinel at EXACT gl_FragCoord pixels:     ║
# ║     → Mode 1 (flash) → pixel (0, 0)                                    ║
# ║     → Mode 4 (zoom)  → pixel (1, 0)                                    ║
# ║                                                                        ║
# ║  3. POST-EFFECT PIPELINE (transparency.json) runs these passes:        ║
# ║                                                                        ║
# ║     ┌─────────┐   reads exact pixels   ┌──────────┐                    ║
# ║     │  main   ├───────────────────────►│ CLASSIFY │ → 1x1 "classify"   ║
# ║     │ target  │  at (0,60) and (50,60) │  (pass1) │   target w/ mode   ║
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
# ║  WHY dust instead of entity_effect:                                    ║
# ║    dust's scale parameter controls lifetime (random(8-40) × scale).   ║
# ║    scale=0.15 → 1-6 ticks. entity_effect has uncontrollable random   ║
# ║    10-40 tick lifetime that makes flash linger too long.               ║
# ║                                                                        ║
# ║  WHY classify reads from main (not particles):                         ║
# ║    Dust uses Layer.OPAQUE → RenderPipelines.OPAQUE_PARTICLE.           ║
# ║    In Fabulous mode, ParticleFeatureRenderer.renderSolid() renders     ║
# ║    opaque particles to minecraft:main (not minecraft:particles).       ║
# ║    Only translucent particles go to minecraft:particles.               ║
# ║    So our sentinel pixel ends up in main, and classify must read it    ║
# ║    from there.                                                         ║
# ║                                                                        ║
# ║  WHY fixed NDC instead of ScreenSize:                                  ║
# ║    The Globals UBO (which provides ScreenSize) is NOT bound for the    ║
# ║    particle pipeline. PARTICLE_SNIPPET builds from MATRICES_FOG only,  ║
# ║    without GLOBALS_SNIPPET. ScreenSize reads as vec2(0,0) → dividing  ║
# ║    by zero gives infinity → marker at infinity → clipped → no output. ║
# ║    Instead, we use fixed NDC coordinates for the marker quad and the   ║
# ║    fsh writes the sentinel at exact gl_FragCoord pixels (0,0)/(1,0).  ║
# ║                                                                        ║
# ║  WHY range-based detection:                                            ║
# ║    Dust applies a random ~0.48-1.0× color multiplier per channel      ║
# ║    (shared 0.6-1.0 factor × per-channel 0.8-1.0 via darken()).        ║
# ║    Input color 0.02 → vertex Color R∈[2-5] in 8-bit.                 ║
# ║    Checking ranges (R∈[1-10], B==0) handles this randomization.       ║
# ║    G==0 → flash, G∈[1-10] → zoom. B==0 guaranteed (0×anything=0).    ║
# ║                                                                        ║
# ║  WHY deterministic sentinel in particle.fsh:                           ║
# ║    The fsh writes vec4(254/255, mode/255, 0, 1) regardless of the     ║
# ║    raw Color values. This ensures classify always reads exact integer  ║
# ║    values via texelFetch, immune to dust's color randomization.        ║
# ║                                                                        ║
# ║  WHY ScreenSize for pixel placement:                                   ║
# ║    Hardcoded NDC coordinates (e.g. -0.98) map to different pixels at   ║
# ║    different resolutions. ScreenSize (from globals.glsl) lets us       ║
# ║    compute the exact NDC for a given pixel regardless of resolution.   ║
# ║                                                                        ║
# ║  WHY alpha=1.0 forced in particle.fsh:                                 ║
# ║    When alpha < 1, the GPU blends RGB channels before storing them in  ║
# ║    the framebuffer. With alpha=1, stored = src exactly.                ║
# ║                                                                        ║
# ║  WHY flat varyings:                                                    ║
# ║    `flat` prevents interpolation between vertices. Without it,         ║
# ║    markerMode could be interpolated across the quad.                   ║
# ║                                                                        ║
# ╠════════════════════════════════════════════════════════════════════════╣
# ║                      ⚠ REQUIREMENTS ⚠                                 ║
# ║                                                                        ║
# ║  • Graphics MUST be set to "Fabulous!"                                 ║
# ║  • Resource pack must be active and loaded.                            ║
# ║  • Marker particle must be IN FRONT of the camera.                     ║
# ║                                                                        ║
# ╠════════════════════════════════════════════════════════════════════════╣
# ║                         DEBUG MODE                                     ║
# ║                                                                        ║
# ║  Bottom-left debug squares when DEBUG=1:                               ║
# ║    [RED   0-50px]   = transparency pass runs                           ║
# ║    [GREEN 50-100px] = flash pass runs                                  ║
# ║    [BLUE  100-150px]= zoom pass runs (orange/cyan = mode detected)     ║
# ║    [150-200px] = flash sentinel at (0,0) (YELLOW=found, GRAY=empty)    ║
# ║    [200-250px] = zoom sentinel at (1,0)  (YELLOW=found, GRAY=empty)    ║
# ║    [250-300px] = amplified MAIN at (0,0) ×50                           ║
# ║    [300-350px] = amplified MAIN at (1,0) ×50                           ║
# ║    [350-400px] = MAIN DEPTH at (0,0)                                   ║
# ║             GREEN=near(0), RED=far(1), YELLOW=mid                      ║
# ║    [400-450px] = MAIN DEPTH at (1,0)                                   ║
# ║             GREEN=near(0), RED=far(1), YELLOW=mid                      ║
# ║                                                                        ║
# ╚════════════════════════════════════════════════════════════════════════╝
#
# MARKER PIXEL MAP:
#   Mode 1 (flash) → screen pixel (0, 0)   [bottom-left corner]
#   Mode 4 (zoom)  → screen pixel (1, 0)   [one pixel right]
#
# MARKER COLOR ENCODING (dust RGB + scale):
#   Command provides float [R, G, B] (no alpha) + scale (size & lifetime).
#   Dust particles apply a random color multiplier (~0.48-1.0 per channel)
#   via AbstractDustParticle.darken(), so vertex Color.rgb varies.
#   We use very dim colors and range-based detection to handle this.
#
#   Flash: color:[0.02, 0.0, 0.0], scale:0.15
#     R ∈ [2-5] after randomization, G = 0, B = 0
#   Zoom:  color:[0.02, 0.02, 0.0], scale:0.15
#     R ∈ [2-5] after randomization, G ∈ [2-5], B = 0
#
#   Detection: R ∈ [1,10], B == 0 → marker signature.
#   Mode: G == 0 → flash (mode 1), G ∈ [1,10] → zoom (mode 4).
#
#   scale=0.15 → particle lifetime = random(8-40) × 0.15 = 1-6 ticks.
#   Flash auto-expires when particle dies (no alpha threshold needed).
#   Zoom spawned every tick → always at least one live particle.
#
#   fsh writes DETERMINISTIC sentinel (R=254, G=mode, B=0, A=255)
#   so classify always reads exact values via texelFetch.
#


# ============================================================================
# GLSL Shader Sources
# ============================================================================


# ────────────────────────────────────────────────────────────────────────────
# 1. CORE PARTICLE VERTEX SHADER
# ────────────────────────────────────────────────────────────────────────────
PARTICLE_VSH = """\
#version 330

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>
#moj_import <minecraft:projection.glsl>
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

// flat = no interpolation across quad (critical for integer flags)
flat out int markerMode;  // 0=normal particle, 1=flash, 4=zoom

// Quad corner offsets: covers a small area at the bottom-left of the screen.
// The sizing is in NDC (not pixels), so no ScreenSize needed.
// NOTE: The Globals UBO (ScreenSize) is NOT bound for the particle pipeline.
// PARTICLE_SNIPPET only includes MATRICES_FOG_SNIPPET, not GLOBALS_SNIPPET.
const vec2 corners[4] = vec2[4](
    vec2(0.0, 1.0),
    vec2(0.0, 0.0),
    vec2(1.0, 0.0),
    vec2(1.0, 1.0)
);

// Fixed NDC quad size: 0.015 NDC ≈ 8-15 pixels depending on resolution.
// This guarantees coverage of pixel (0,0) and (1,0) at any resolution.
#define MARKER_NDC_SIZE 0.015

// Detect dust marker by color pattern.
// Dust particles apply a random ~0.48-1.0× multiplier per channel
// (DustParticleBase.randomizeColor()). Input 0.02 → R ∈ [2-5] in 8-bit.
// B==0 is guaranteed (0 × anything = 0).
// G channel determines mode: G==0 → flash, G>0 → zoom.
int detectMarkerMode(vec4 color) {
    ivec4 ic = ivec4(round(color * 255.0));
    // Signature: R in [1-10] (very dim dust), B must be 0
    if (ic.r >= 1 && ic.r <= 10 && ic.b == 0) {
        if (ic.g == 0) return 1;                  // Flash: G is zero
        if (ic.g >= 1 && ic.g <= 10) return 4;    // Zoom: G is non-zero
    }
    return 0;  // Not a marker
}

void main() {
    int mode = detectMarkerMode(Color);
    markerMode = mode;

    if (mode != 0) {
        // REDIRECT marker quad to bottom-left corner using FIXED NDC.
        // Both flash and zoom use the same NDC quad covering the corner.
        // The FRAGMENT shader discriminates: flash writes pixel (0,0),
        // zoom writes pixel (1,0), everything else is discarded.
        vec2 base = vec2(-1.0, -1.0);
        vec2 size = vec2(MARKER_NDC_SIZE);

        // z = -1.0 puts the marker at the NEAR PLANE (depth 0.0).
        // Dust uses OPAQUE_PARTICLE pipeline: depth test LEQUAL, depth
        // write ON. Our depth 0.0 always passes (≤ any scene depth).
        gl_Position = vec4(base + corners[gl_VertexID % 4] * size, -1.0, 1.0);

        // Zero out all vanilla varyings (not used for markers)
        sphericalVertexDistance = 0.0;
        cylindricalVertexDistance = 0.0;
        texCoord0 = vec2(0.0);
        vertexColor = vec4(0.0);
        return;
    }

    // Normal particle: vanilla processing
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
PARTICLE_FSH = """\
#version 330

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec2 texCoord0;
in vec4 vertexColor;
flat in int markerMode;  // 0=normal, 1=flash, 4=zoom

out vec4 fragColor;

#define DEBUG 1

void main() {
    if (markerMode > 0) {
        // The VSH places a small NDC quad at the bottom-left corner.
        // Both flash and zoom quads cover the same area.
        // We ONLY write the sentinel at the exact target pixel;
        // all other fragments are discarded to avoid overwriting scene.
        //   Flash → pixel (0, 0)
        //   Zoom  → pixel (1, 0)
        ivec2 fc = ivec2(gl_FragCoord.xy);
        ivec2 target = (markerMode == 1) ? ivec2(0, 0) : ivec2(1, 0);
        if (fc != target) {
            discard;
        }
        // Write DETERMINISTIC sentinel: classify reads exact values.
        // R=254, G=mode, B=0, A=255 — immune to dust color randomization.
        fragColor = vec4(254.0 / 255.0, float(markerMode) / 255.0, 0.0, 1.0);
        return;
    }

    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
    if (color.a < 0.1) {
        discard;
    }
    fragColor = apply_fog(color, sphericalVertexDistance, cylindricalVertexDistance,
        FogEnvironmentalStart, FogEnvironmentalEnd,
        FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
#if DEBUG
    // GREEN TINT on ALL non-marker particles processed by this shader.
    fragColor.g = min(fragColor.g + 0.15, 1.0);
#endif
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 3. POST-PROCESSING: CLASSIFY PASS
# ────────────────────────────────────────────────────────────────────────────
CLASSIFY_FSH = """\
#version 330

// Dust is OPAQUE → renders to minecraft:main (not minecraft:particles).
// ParticleFeatureRenderer.renderSolid() targets the main framebuffer.
uniform sampler2D MainSampler;

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254

void main() {
    // Read the exact sentinel pixels from MAIN (where opaque dust renders).
    // texelFetch = no UV math, no rounding error.
    // Flash sentinel at pixel (0, 0), zoom sentinel at pixel (1, 0)
    ivec4 p1 = ivec4(round(texelFetch(MainSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 p4 = ivec4(round(texelFetch(MainSampler, ivec2(1, 0), 0) * 255.0));

    // Sentinel: R == MARKER_RED, B == 0, A == 255, G == expected mode value
    bool flashActive = (p1.r == MARKER_RED && p1.b == 0 && p1.a == 255 && p1.g == 1);
    bool zoomActive  = (p4.r == MARKER_RED && p4.b == 0 && p4.a == 255 && p4.g == 4);

    // Independent channels: both can be active simultaneously.
    // R = flash, G = zoom. flash.fsh reads R, zoom.fsh reads G.
    fragColor = vec4(flashActive ? 1.0 : 0.0, zoomActive ? 1.0 : 0.0, 0.0, 1.0);
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 4. POST-PROCESSING: TRANSPARENCY COMPOSITING
# ────────────────────────────────────────────────────────────────────────────
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
    if (color.a == 0.0) return;
    color_layers[active_layers] = color;
    depth_layers[active_layers] = depth;
    int jj = active_layers++;
    int ii = jj - 1;
    while (jj > 0 && depth_layers[jj] > depth_layers[ii]) {
        float depthTemp = depth_layers[ii]; depth_layers[ii] = depth_layers[jj]; depth_layers[jj] = depthTemp;
        vec4 colorTemp  = color_layers[ii];  color_layers[ii]  = color_layers[jj];  color_layers[jj]  = colorTemp;
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
    try_insert(texture(ItemEntitySampler,  texCoord), texture(ItemEntityDepthSampler,  texCoord).r);

    vec4 particleColor = texture(ParticlesSampler, texCoord);
    float particleDepth = texture(ParticlesDepthSampler, texCoord).r;
#if DEBUG
    // Debug: show ALL particles including marker quads (don't hide anything)
    try_insert(particleColor, particleDepth);
#else
    // Hide the exact marker sentinel pixels at (0,0) [flash] and (1,0) [zoom]
    // These are in the main layer (not particles), but we still insert particles normally.
    try_insert(particleColor, particleDepth);
#endif

    try_insert(texture(WeatherSampler, texCoord), texture(WeatherDepthSampler, texCoord).r);
    try_insert(texture(CloudsSampler,  texCoord), texture(CloudsDepthSampler,  texCoord).r);

    vec3 texelAccum = color_layers[0].rgb;
    for (int ii = 1; ii < active_layers; ++ii) {
        texelAccum = blend(texelAccum, color_layers[ii]);
    }
    fragColor = vec4(texelAccum.rgb, 1.0);

#if DEBUG
    // ═══ DEBUG SQUARES (bottom-left, 50px wide each, starting at y=5) ═══
    // Sentinel pixels are at (0,0) and (1,0), so debug squares start at y=5
    // to avoid overwriting them during compositing.
    //  [0-50, 5-55]   RED    = transparency pass runs
    //  [150-200]       YELLOW/GRAY = flash sentinel at (0,0)?
    //  [200-250]       YELLOW/GRAY = zoom sentinel at (1,0)?
    //  [250-300]       Amplified MAIN at (0,0) ×50
    //  [300-350]       Amplified MAIN at (1,0) ×50
    //  [350-400]       MAIN DEPTH at (0,0): GREEN=near, RED=far, YELLOW=mid
    //  [400-450]       MAIN DEPTH at (1,0): same color coding

    if (gl_FragCoord.x < 50.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = pass 2 runs
    }

    // Read sentinel pixels from MAIN at (0,0) and (1,0)
    ivec4 dbgFlash = ivec4(round(texelFetch(MainSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 dbgZoom  = ivec4(round(texelFetch(MainSampler, ivec2(1, 0), 0) * 255.0));

    // [150-200] YELLOW if flash sentinel present (R=254), GRAY if empty
    if (gl_FragCoord.x >= 150.0 && gl_FragCoord.x < 200.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        fragColor = (dbgFlash.r == 254) ? vec4(1.0, 1.0, 0.0, 1.0) : vec4(0.1, 0.1, 0.1, 1.0);
    }
    // [200-250] YELLOW if zoom sentinel present (R=254), GRAY if empty
    if (gl_FragCoord.x >= 200.0 && gl_FragCoord.x < 250.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        fragColor = (dbgZoom.r == 254) ? vec4(1.0, 1.0, 1.0, 1.0) : vec4(0.1, 0.1, 0.1, 1.0);
    }

    // [250-300] Amplified raw MAIN color at flash sentinel (0,0) ×50
    if (gl_FragCoord.x >= 250.0 && gl_FragCoord.x < 300.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        vec4 raw = texelFetch(MainSampler, ivec2(0, 0), 0);
        fragColor = vec4(clamp(raw.rgb * 50.0, 0.0, 1.0), 1.0);
    }
    // [300-350] Amplified raw MAIN color at zoom sentinel (1,0) ×50
    if (gl_FragCoord.x >= 300.0 && gl_FragCoord.x < 350.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        vec4 raw = texelFetch(MainSampler, ivec2(1, 0), 0);
        fragColor = vec4(clamp(raw.rgb * 50.0, 0.0, 1.0), 1.0);
    }
    // [350-400] MAIN DEPTH at flash sentinel pixel (0,0)
    if (gl_FragCoord.x >= 350.0 && gl_FragCoord.x < 400.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        float d = texelFetch(MainDepthSampler, ivec2(0, 0), 0).r;
        if (d <= 0.001) {
            fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = near plane (sentinel wrote!)
        } else if (d >= 0.999) {
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = far/cleared (sky)
        } else {
            fragColor = vec4(d, d, 0.0, 1.0);       // YELLOW gradient = terrain depth
        }
    }
    // [400-450] MAIN DEPTH at zoom sentinel pixel (1,0)
    if (gl_FragCoord.x >= 400.0 && gl_FragCoord.x < 450.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        float d = texelFetch(MainDepthSampler, ivec2(1, 0), 0).r;
        if (d <= 0.001) {
            fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = near plane (sentinel wrote!)
        } else if (d >= 0.999) {
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = far/cleared (sky)
        } else {
            fragColor = vec4(d, d, 0.0, 1.0);       // YELLOW gradient = terrain depth
        }
    }
#endif
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 5. POST-PROCESSING: MUZZLE FLASH EFFECT
# ────────────────────────────────────────────────────────────────────────────
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
    bool flashMode = texture(ClassifySampler, vec2(0.5, 0.5)).r > 0.5;

    fragColor = texture(InSampler, texCoord);

    if (flashMode) {
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
    if (gl_FragCoord.x >= 50.0 && gl_FragCoord.x < 100.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = pass 3 runs
    }
#endif
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 6. POST-PROCESSING: BARREL DISTORTION ZOOM
# ────────────────────────────────────────────────────────────────────────────
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
    vec4 classifyData = texture(ClassifySampler, vec2(0.5, 0.5));
    bool flashMode = classifyData.r > 0.5;
    bool zoomMode  = classifyData.g > 0.5;

    fragColor = texture(InSampler, texCoord);

    if (zoomMode) {
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
    if (gl_FragCoord.x >= 100.0 && gl_FragCoord.x < 150.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        if (flashMode && zoomMode) {
            fragColor = vec4(1.0, 1.0, 1.0, 1.0);  // White: both detected
        } else if (flashMode) {
            fragColor = vec4(1.0, 0.5, 0.0, 1.0);  // Orange: flash only
        } else if (zoomMode) {
            fragColor = vec4(0.0, 1.0, 1.0, 1.0);  // Cyan: zoom only
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
            "classify": {"width": 1, "height": 1, "persistent": True},
            "final": {},
            "swap":  {},
        },
        "passes": [
            # Pass 1: CLASSIFY - read sentinel pixels from MAIN
            # Dust is OPAQUE → rendered to minecraft:main by renderSolid().
            # Only translucent particles go to minecraft:particles.
            {
                "vertex_shader":   "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/classify",
                "inputs": [
                    {"sampler_name": "Main", "target": "minecraft:main"},
                ],
                "output": "classify",
            },
            # Pass 2: TRANSPARENCY - Fabulous compositing (hides marker pixels)
            {
                "vertex_shader":   "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/transparency",
                "inputs": [
                    {"sampler_name": "Main",             "target": "minecraft:main"},
                    {"sampler_name": "MainDepth",        "target": "minecraft:main",        "use_depth_buffer": True},
                    {"sampler_name": "Translucent",      "target": "minecraft:translucent"},
                    {"sampler_name": "TranslucentDepth", "target": "minecraft:translucent",  "use_depth_buffer": True},
                    {"sampler_name": "ItemEntity",       "target": "minecraft:item_entity"},
                    {"sampler_name": "ItemEntityDepth",  "target": "minecraft:item_entity",  "use_depth_buffer": True},
                    {"sampler_name": "Particles",        "target": "minecraft:particles"},
                    {"sampler_name": "ParticlesDepth",   "target": "minecraft:particles",   "use_depth_buffer": True},
                    {"sampler_name": "Clouds",           "target": "minecraft:clouds"},
                    {"sampler_name": "CloudsDepth",      "target": "minecraft:clouds",      "use_depth_buffer": True},
                    {"sampler_name": "Weather",          "target": "minecraft:weather"},
                    {"sampler_name": "WeatherDepth",     "target": "minecraft:weather",     "use_depth_buffer": True},
                ],
                "output": "final",
            },
            # Pass 3: FLASH - depth-based muzzle flash (if mode 1)
            {
                "vertex_shader":   "minecraft:core/screenquad",
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
                "vertex_shader":   "minecraft:core/screenquad",
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
                "vertex_shader":   "minecraft:core/screenquad",
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
    """Register all shader files and write marker particle commands."""
    ns: str = Mem.ctx.project_id

    Mem.ctx.assets["minecraft"].vertex_shaders["core/particle"]   = VertexShader(PARTICLE_VSH)
    Mem.ctx.assets["minecraft"].fragment_shaders["core/particle"] = FragmentShader(PARTICLE_FSH)

    Mem.ctx.assets[ns].fragment_shaders["post/classify"]    = FragmentShader(CLASSIFY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/transparency"] = FragmentShader(TRANSPARENCY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/flash"]       = FragmentShader(FLASH_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/zoom"]        = FragmentShader(ZOOM_FSH)

    Mem.ctx.assets["minecraft"].post_effects["transparency"] = set_json_encoder(PostEffect(get_post_effect_json(ns)))

    # ── Flash marker: mode 1 ──
    # dust color:[R,0,0] with R=0.02 → vsh detects R∈[1-10], G==0, B==0
    # scale=0.15 → lifetime = random(8-40)×0.15 = 1-6 ticks (brief flash)
    write_versioned_function("player/fire_weapon",
"""
# Shader: spawn muzzle flash marker (mode 1)
# dust R=0.02, G=0, B=0 → particle.vsh detects and places at pixel (0,0)
# scale 0.15 → ~1-6 tick lifetime → flash auto-expires when particle dies
execute at @s anchored eyes run particle minecraft:dust{color:[0.02,0.0,0.0],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s
""")

    # ── Zoom marker: mode 4 ──
    # dust color:[R,G,0] with R=G=0.02 → vsh detects R∈[1-10], G∈[1-10], B==0
    # Spawned every tick while ADS is active
    write_versioned_function("player/tick",
f"""
# Shader: spawn zoom marker (mode 4)
# dust R=0.02, G=0.02, B=0 → particle.vsh detects and places at pixel (2,0)
execute if score @s {ns}.zoom matches 1 at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.02,0.0],scale:0.05}} ^ ^ ^1 0 0 0 0 1 force @s
""")

