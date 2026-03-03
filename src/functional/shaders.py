
# Imports
from beet import FragmentShader, PostEffect, Texture, VertexShader
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
# ║     → zoom/main.mcfunction    (zoom marker, mode 3/4)                  ║
# ║                                                                        ║
# ║  2. CORE PARTICLE SHADER (particle.vsh) intercepts ALL particles.      ║
# ║     It detects our marker by range-based color pattern detection.      ║
# ║     R∈[1-10] with B==0 identifies our marker (dust is very dim).       ║
# ║     G==0 → flash (mode 1), G∈[1-10] → zoom (mode 4).                   ║
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
# ║    dust's scale parameter controls lifetime (random(8-40) x scale).    ║
# ║    scale=0.15 → 1-6 ticks. entity_effect has uncontrollable random     ║
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
# ║    without GLOBALS_SNIPPET. ScreenSize reads as vec2(0,0) → dividing   ║
# ║    by zero gives infinity → marker at infinity → clipped → no output.  ║
# ║    Instead, we use fixed NDC coordinates for the marker quad and the   ║
# ║    fsh writes the sentinel at exact gl_FragCoord pixels (0,0)/(1,0).   ║
# ║                                                                        ║
# ║  WHY range-based detection:                                            ║
# ║    Dust applies a random ~0.48-1.0x color multiplier per channel       ║
# ║    (shared 0.6-1.0 factor x per-channel 0.8-1.0 via darken()).         ║
# ║    Input color 0.02 → vertex Color R∈[2-5] in 8-bit.                   ║
# ║    Checking ranges (R∈[1-10], B==0) handles this randomization.        ║
# ║    G==0 → flash, G∈[1-10] → zoom. B==0 guaranteed (0xanything=0).      ║
# ║                                                                        ║
# ║  WHY deterministic sentinel in particle.fsh:                           ║
# ║    The fsh writes vec4(254/255, mode/255, 0, 1) regardless of the      ║
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
# ║    [250-300px] = amplified MAIN at (0,0) x50                           ║
# ║    [300-350px] = amplified MAIN at (1,0) x50                           ║
# ║    [350-400px] = MAIN DEPTH at (0,0)                                   ║
# ║             GREEN=near(0), RED=far(1), YELLOW=mid                      ║
# ║    [400-450px] = MAIN DEPTH at (1,0)                                   ║
# ║             GREEN=near(0), RED=far(1), YELLOW=mid                      ║
# ║                                                                        ║
# ╚════════════════════════════════════════════════════════════════════════╝
#
# MARKER PIXEL MAP:
#   Mode 1 (flash)     → screen pixel (0, 0)   [bottom-left corner]
#   Mode 2-4 (zoom)    → screen pixel (1, 0)   [one pixel right]
#   Mode 5-9 (spread)  → screen pixel (2, 0)   [two pixels right]
#   Mode 12-14 (FOV)   → screen pixel (3, 0)   [three pixels right]
#
# MARKER COLOR ENCODING (dust RGB + scale):
#   Command provides float [R, G, B] (no alpha) + scale (size & lifetime).
#   Dust particles apply a random color multiplier (~0.48-1.0 per channel)
#   via AbstractDustParticle.darken(), so vertex Color.rgb varies.
#   We use very dim colors and range-based detection to handle this.
#
#   Flash: color:[0.02, 0.0, 0.0], scale:0.01
#     R ∈ [2-5] after randomization, G = 0, B = 0
#   Zoom center-only (no scope): color:[0.02, 0.25, 0.0], scale:0.01
#     R ∈ [2-5] after randomization, G ∈ [30-63], B = 0
#   Zoom x3: color:[0.02, 0.02, 0.0], scale:0.01
#     R ∈ [2-5] after randomization, G ∈ [2-5], B = 0
#   Zoom x4: color:[0.02, 0.08, 0.0], scale:0.01
#     R ∈ [2-5] after randomization, G ∈ [10-20], B = 0
#
#   Crosshair spread markers (B > 0, G = 0):
#   Sneak:  color:[0.02, 0.0, 0.02], scale:0.01 → B' ∈ [2-5]
#   Base:   color:[0.02, 0.0, 0.05], scale:0.01 → B' ∈ [6-13]
#   Walk:   color:[0.02, 0.0, 0.12], scale:0.01 → B' ∈ [15-31]
#   Sprint: color:[0.02, 0.0, 0.28], scale:0.01 → B' ∈ [34-71]
#   Jump:   color:[0.02, 0.0, 0.60], scale:0.01 → B' ∈ [73-153]
#
#   FOV markers (B > 0 AND G > 0, immediate zoom FOV reduction):
#   FOV center-only: color:[0.02, 0.25, 0.15] → G' ∈ [30-63], B' ∈ [18-38]
#   FOV x3:          color:[0.02, 0.02, 0.15] → G' ∈ [2-5],   B' ∈ [18-38]
#   FOV x4:          color:[0.02, 0.08, 0.15] → G' ∈ [10-20],  B' ∈ [18-38]
#
#   Detection: R ∈ [1,10] → marker signature.
#   Flash/zoom: B == 0, G encodes mode.
#   Spread: G == 0, B > 0 encodes movement state.
#   FOV: G > 0 AND B ∈ [15-45] → immediate zoom FOV reduction.
#
#   scale=0.01 → particle lifetime = 0 (1 game tick minimum).
#   Flash auto-expires after 1 tick.
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
flat out int markerMode;  // 0=normal, 1=flash, 2-4=zoom, 5-9=spread
flat out float markerViewDist;  // Camera-to-particle distance (for 3rd person detection)

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
// Dust particles apply a random ~0.48-1.0x multiplier per channel
// (DustParticleBase.randomizeColor()). Input 0.02 → R ∈ [2-5] in 8-bit.
// B==0 is guaranteed (0 x anything = 0).
// G channel determines mode:
//   G==0        → flash (mode 1)
//   G∈[1-7]    → zoom x3 (from 0.02, randomized to [2-5])
//   G∈[8-25]   → zoom x4 (from 0.08, randomized to [10-20])
//   G∈[26-80]  → zoom center-only (from 0.25, randomized to [30-63]) — no scope
int detectMarkerMode(vec4 color) {
    ivec4 ic = ivec4(round(color * 255.0));
    // Signature: R in [1-10] (very dim dust) AND fully opaque (a>=250).
    // The alpha check prevents false positives from smoke/large_smoke particles
    // which have alpha ~204 (0.8) and can randomly produce dim grayscale colors
    // in the [1-10] range matching our marker signature.
    if (ic.r >= 1 && ic.r <= 10 && ic.a >= 250) {
        if (ic.b == 0) {
            // Flash/zoom markers: B==0, G encodes mode
            if (ic.g == 0) return 1;                   // Flash: G is zero
            if (ic.g >= 1 && ic.g <= 7) return 3;      // Zoom x3: G from 0.02 → [2-5]
            if (ic.g >= 8 && ic.g <= 25) return 4;     // Zoom x4: G from 0.08 → [10-20]
            if (ic.g >= 26 && ic.g <= 80) return 2;    // Zoom center-only: G from 0.25 → [30-63]
        } else if (ic.g == 0) {
            // Crosshair spread markers: G==0, B>0 encodes movement state
            if (ic.b >= 1 && ic.b <= 5) return 5;     // Sneak: B from 0.02 → [2-5]
            if (ic.b >= 6 && ic.b <= 14) return 6;    // Base: B from 0.05 → [6-13]
            if (ic.b >= 15 && ic.b <= 33) return 7;   // Walk: B from 0.12 → [15-31]
            if (ic.b >= 34 && ic.b <= 72) return 8;   // Sprint: B from 0.28 → [34-71]
            if (ic.b >= 73) return 9;                  // Jump: B from 0.60 → [73-153]
        } else if (ic.b >= 15 && ic.b <= 45) {
            // FOV markers: both G>0 AND B in higher range (B=0.15 → [18-38] after randomization)
            // This separates FOV markers from dim grayscale particles (smoke etc.) which have B≈R∈[1-10]
            // Same G encoding as zoom but B=0.15 instead of 0 distinguishes them
            if (ic.g >= 26 && ic.g <= 80) return 12;  // FOV center-only
            if (ic.g >= 1 && ic.g <= 7) return 13;    // FOV x3
            if (ic.g >= 8 && ic.g <= 25) return 14;   // FOV x4
        }
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
        // zoom writes pixel (1,0), spread writes pixel (2,0).
        vec2 base = vec2(-1.0, -1.0);
        vec2 size = vec2(MARKER_NDC_SIZE);

        // z = -1.0 puts the marker at the NEAR PLANE (depth 0.0).
        // Dust uses OPAQUE_PARTICLE pipeline: depth test LEQUAL, depth
        // write ON. Our depth 0.0 always passes (≤ any scene depth).
        gl_Position = vec4(base + corners[gl_VertexID % 4] * size, -1.0, 1.0);

        // Camera distance for 3rd person detection:
        // Position is camera-relative → length(Position) ≈ 1.0 in 1st person, ≈ 5.0 in 3rd person
        markerViewDist = length(Position);

        // Zero out all vanilla varyings (not used for markers)
        sphericalVertexDistance = 0.0;
        cylindricalVertexDistance = 0.0;
        texCoord0 = vec2(0.0);
        vertexColor = vec4(0.0);
        return;
    }

    // Normal particle: vanilla processing
    markerViewDist = 0.0;
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
flat in int markerMode;  // 0=normal, 1=flash, 2-4=zoom, 5-9=spread
flat in float markerViewDist;  // Camera-to-particle distance

out vec4 fragColor;

#define DEBUG 0

void main() {
    if (markerMode > 0) {
        // The VSH places a small NDC quad at the bottom-left corner.
        // Both flash and zoom quads cover the same area.
        // We ONLY write the sentinel at the exact target pixel;
        // all other fragments are discarded to avoid overwriting scene.
        //   Flash    → pixel (0, 0)
        //   Zoom 2-4 → pixel (1, 0)
        //   Spread 5-9 → pixel (2, 0)
        //   FOV 12-14 → pixel (3, 0)
        ivec2 fc = ivec2(gl_FragCoord.xy);
        ivec2 target;
        if (markerMode == 1) target = ivec2(0, 0);        // Flash
        else if (markerMode >= 12) target = ivec2(3, 0);   // FOV
        else if (markerMode >= 5) target = ivec2(2, 0);    // Spread
        else target = ivec2(1, 0);                          // Zoom (2, 3, 4)
        if (fc != target) {
            discard;
        }
        // Write DETERMINISTIC sentinel with camera distance for 3rd person detection.
        // R=254, G=mode, B=viewDist(normalized 0-1 from 0-10 blocks), A=255.
        // ~0.1 in 1st person, ~0.5 in 3rd person.
        fragColor = vec4(254.0 / 255.0, float(markerMode) / 255.0, clamp(markerViewDist / 10.0, 0.0, 1.0), 1.0);
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
uniform sampler2D SmoothSpreadSampler;  // Previous frame's smooth spread (persistent feedback)

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254
#define SPREAD_LERP_SPEED 0.15  // Per-frame interpolation (~10 frames for 90% convergence at 60fps)

void main() {
    // Read the exact sentinel pixels from MAIN (where opaque dust renders).
    // texelFetch = no UV math, no rounding error.
    // Flash sentinel at pixel (0, 0), zoom sentinel at pixel (1, 0)
    ivec4 p1 = ivec4(round(texelFetch(MainSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 p4 = ivec4(round(texelFetch(MainSampler, ivec2(1, 0), 0) * 255.0));

    // Sentinel: R == MARKER_RED, A == 255, G == expected mode value
    // B now encodes camera-to-particle distance (not checked for detection)
    bool flashActive = (p1.r == MARKER_RED && p1.a == 255 && p1.g == 1);
    bool zoomActive  = (p4.r == MARKER_RED && p4.a == 255 && (p4.g == 2 || p4.g == 3 || p4.g == 4));
    int zoomLevel = zoomActive ? p4.g : 0;  // 2=center-only, 3=x3 scope, 4=x4 scope

    // 3rd person detection from sentinel B (camera-to-particle distance)
    // B = clamp(viewDist / 10.0): ~0.1 in 1st person, ~0.5 in 3rd person
    float cameraDist = 0.0;
    if (flashActive) cameraDist = max(cameraDist, float(p1.b) / 255.0 * 10.0);
    if (zoomActive)  cameraDist = max(cameraDist, float(p4.b) / 255.0 * 10.0);
    bool thirdPerson = cameraDist > 2.0;  // Threshold: >2 blocks from camera → 3rd person

    // Spread (crosshair) sentinel at pixel (2, 0)
    ivec4 p_spread = ivec4(round(texelFetch(MainSampler, ivec2(2, 0), 0) * 255.0));
    bool spreadActive = (p_spread.r == MARKER_RED && p_spread.a == 255
                         && p_spread.g >= 5 && p_spread.g <= 9);
    int spreadLevel = spreadActive ? (p_spread.g - 5) : 1;  // 0-4, default 1 (base)

    // Smooth interpolation: read previous frame's smooth spread from persistent buffer
    float prevSmooth = texture(SmoothSpreadSampler, vec2(0.5, 0.5)).r;
    float targetSpread = float(spreadLevel) / 4.0;  // Normalize to [0.0, 1.0] for 8-bit precision
    float smoothSpread = mix(prevSmooth, targetSpread, SPREAD_LERP_SPEED);

    // R = flash, G = zoom, B = (zoomLevel + thirdPerson*128) / 255, A = smooth spread.
    // flash.fsh reads R, zoom.fsh reads G, B (with 3rd person flag), and A.
    fragColor = vec4(
        flashActive ? 1.0 : 0.0,
        zoomActive ? 1.0 : 0.0,
        float(zoomLevel + (thirdPerson ? 128 : 0)) / 255.0,
        smoothSpread
    );
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 4. POST-PROCESSING: SPREAD COPY (smooth spread feedback loop)
# ────────────────────────────────────────────────────────────────────────────
SPREAD_COPY_FSH = """\
#version 330

// Copy the smooth spread value from classify alpha to the persistent buffer.
// This creates a one-frame delay feedback loop:
//   classify reads smooth_spread (prev frame) → computes lerped value → writes to classify.a
//   spread_copy reads classify.a → writes to smooth_spread (for next frame)
uniform sampler2D ClassifySampler;

in vec2 texCoord;
out vec4 fragColor;

void main() {
    fragColor = vec4(texture(ClassifySampler, vec2(0.5, 0.5)).a, 0.0, 0.0, 1.0);
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 5. POST-PROCESSING: TRANSPARENCY COMPOSITING
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

#define DEBUG 0

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
    //  [250-300]       Amplified MAIN at (0,0) x50
    //  [300-350]       Amplified MAIN at (1,0) x50
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

    // [250-300] Amplified raw MAIN color at flash sentinel (0,0) x50
    if (gl_FragCoord.x >= 250.0 && gl_FragCoord.x < 300.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        vec4 raw = texelFetch(MainSampler, ivec2(0, 0), 0);
        fragColor = vec4(clamp(raw.rgb * 50.0, 0.0, 1.0), 1.0);
    }
    // [300-350] Amplified raw MAIN color at zoom sentinel (1,0) x50
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
# 6. POST-PROCESSING: MUZZLE FLASH EFFECT
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

#define DEBUG 0
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
        float aspectRatio = inSize.x / inSize.y;
        vec2 oneTexel = 1.0 / inSize;

        // Depth-based light/bloom effect
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
# 7. POST-PROCESSING: SMOOTH ZOOM INTERPOLATION (FOV feedback loop)
# ────────────────────────────────────────────────────────────────────────────
ZOOM_LERP_FSH = """\
#version 330

// Smooth zoom interpolation feedback loop.
// Reads FOV sentinel pixel directly from main framebuffer (spawned immediately on zoom).
// Separate from scope zoom markers (pixel 1,0) which are delayed 5 ticks.
uniform sampler2D MainSampler;
uniform sampler2D SmoothZoomSampler;  // Previous frame's smooth zoom (persistent feedback)

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254
#define ZOOM_LERP_SPEED 0.12  // Per-frame interpolation (~0.33s to 90% at 60fps)

void main() {
    // Read FOV sentinel at pixel (3, 0) — spawned immediately on zoom (no 5-tick delay)
    // R=254, G=mode(12-14), B=viewDist, A=255
    ivec4 pFov = ivec4(round(texelFetch(MainSampler, ivec2(3, 0), 0) * 255.0));
    bool fovActive = (pFov.r == MARKER_RED && pFov.a == 255
                      && pFov.g >= 12 && pFov.g <= 14);
    int fovZoomLevel = fovActive ? (pFov.g - 10) : 0;  // 2=center, 3=x3, 4=x4

    // 3rd person detection from sentinel B (camera-to-particle distance)
    float cameraDist = fovActive ? (float(pFov.b) / 255.0 * 10.0) : 0.0;
    bool thirdPerson = cameraDist > 2.0;

    // Target zoom magnification (UV scale toward center).
    // Higher = stronger FOV reduction (texCoord = mix(texCoord, 0.5, zoom)).
    //   0.0  = no magnification (normal FOV)
    //   0.25 = ~1.33x (center-only zoom, no scope)
    //   0.30 = ~1.43x (scope x3)
    //   0.45 = ~1.82x (scope x4)
    float targetZoom = 0.0;
    if (fovActive && !thirdPerson) {
        if (fovZoomLevel == 2) targetZoom = 0.25;       // Center-only: subtle
        else if (fovZoomLevel == 3) targetZoom = 0.30;   // Scope x3: moderate
        else if (fovZoomLevel == 4) targetZoom = 0.45;   // Scope x4: strong
    }

    float prevZoom = texture(SmoothZoomSampler, vec2(0.5, 0.5)).r;
    float smoothZoom = mix(prevZoom, targetZoom, ZOOM_LERP_SPEED);

    fragColor = vec4(smoothZoom, 0.0, 0.0, 1.0);
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 8. POST-PROCESSING: BARREL DISTORTION ZOOM + FOV REDUCTION
# ────────────────────────────────────────────────────────────────────────────
ZOOM_FSH = """\
#version 330

uniform sampler2D InSampler;
uniform sampler2D ClassifySampler;
uniform sampler2D SparkTexSampler;
uniform sampler2D SmoothZoomSampler;  // Smooth FOV zoom factor (persistent feedback)

layout(std140) uniform ZoomConfig {
    float Distortion;
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 0
#define RADIUS_LEVEL_3 0.14
#define RADIUS_LEVEL_4 0.20

// Flash spark sprite sheet: 3x3 grid of 9 different flash sprites (1536x1536 total)
#define SPRITE_COUNT 9
#define SPRITE_SQRT 3

// Flash spark position & scale in screen-space coords:
//   screenCoord = (texCoord - 0.5) * vec2(aspectRatio, 1.0)
// When zooming: centered, slightly below center (muzzle at center of scope)
#define SPARK_POS_ZOOM   vec2(0.0, -0.125)
#define SPARK_SCALE_ZOOM vec2(0.6, 0.6)
// When NOT zooming: offset down-right (muzzle is off-center in hip fire)
#define SPARK_POS_NORMAL   vec2(0.085, -0.11)
#define SPARK_SCALE_NORMAL vec2(0.45, 0.45)

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
    int rawB = int(round(classifyData.b * 255.0));
    bool thirdPerson = rawB >= 128;  // 3rd person flag packed in high bit of B
    int zoomLevel = thirdPerson ? rawB - 128 : rawB;  // 0, 2, 3, or 4

    // Smooth FOV zoom: scales UV toward center for lower effective FOV
    // 0.0 = normal FOV, 0.15 = ~1.18x, 0.30 = ~1.43x, 0.45 = ~1.82x
    float smoothZoom = texture(SmoothZoomSampler, vec2(0.5, 0.5)).r;
    vec2 zoomedUV = mix(texCoord, vec2(0.5), smoothZoom);

    fragColor = texture(InSampler, zoomedUV);
    float aspectRatio = inSize.x / inSize.y;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

    // Apply barrel distortion if zooming WITH a scope (zoomLevel 3 or 4 only)
    // zoomLevel 2 = zoomed but no scope: skip distortion, FOV reduction still applies above
    // Disabled in 3rd person (barrel distortion makes no sense from behind)
    if (zoomMode && !thirdPerson && ((zoomLevel == 3 && length(screenCoord) < RADIUS_LEVEL_3) || (zoomLevel == 4 && length(screenCoord) < RADIUS_LEVEL_4))) {
        float Zoom = float(zoomLevel);  // 3.0 for _3 weapons, 4.0 for _4 weapons
        float RadiusLevel = (zoomLevel == 3) ? RADIUS_LEVEL_3 : RADIUS_LEVEL_4;
        float d = length(screenCoord * Distortion / RadiusLevel);
        float z = sqrt(1.0 - d * d);
        float r = atan(d, z) / 3.1415926535;
        float theta = atan(screenCoord.y, screenCoord.x);

        screenCoord = vec2(cos(theta), sin(theta)) * r / Zoom;
        vec2 pixCoord = screenCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5);

        // Apply FOV zoom to distorted UV as well
        pixCoord = mix(pixCoord, vec2(0.5), smoothZoom);
        fragColor = textureBicubic(InSampler, pixCoord, inSize);
    }

    // Overlay flash spark texture AFTER zoom (spark is NOT barrel-distorted)
    // The 1536x1536 texture is a 3x3 grid of 9 different flash sprites.
    // Sprite is chosen pseudo-randomly from scene data each frame.
    // Disabled in 3rd person (spark texture overlay makes no sense from behind;
    // the flash bloom/lighting from flash.fsh still applies).
    if (flashMode && !thirdPerson) {
        // Choose position/scale: centered when also zooming, offset when hip-firing
        vec2 sparkPos   = zoomMode ? SPARK_POS_ZOOM   : SPARK_POS_NORMAL;
        vec2 sparkScale = zoomMode ? SPARK_SCALE_ZOOM  : SPARK_SCALE_NORMAL;

        // Bounding box in screen-space
        vec2 lb = sparkPos - sparkScale / 2.0;
        vec2 ub = sparkPos + sparkScale / 2.0;
        vec2 sd = sparkScale * float(SPRITE_SQRT);  // scale for one sprite cell

        // Pseudo-random sprite index (0-8) from scene content.
        // Using depth/color at fixed pixels as entropy — changes with camera position.
        float entropy = texelFetch(InSampler, ivec2(317, 211), 0).r
                      + texelFetch(InSampler, ivec2(211, 317), 0).g;
        int spriteIndex = int(mod(floor(entropy * 7919.0), float(SPRITE_COUNT)));
        vec2 spriteOffset = vec2(spriteIndex % SPRITE_SQRT, spriteIndex / SPRITE_SQRT) / float(SPRITE_SQRT);

        // Additive overlay within the spark bounding box
        if (screenCoord.x > lb.x && screenCoord.y > lb.y &&
            screenCoord.x < ub.x && screenCoord.y < ub.y) {
            fragColor += texture(SparkTexSampler, (screenCoord - lb) / sd + spriteOffset);
        }
    }

    // ── Custom crosshair (vanilla crosshair is transparent) ──
    // Draw a crosshair using color inversion (like vanilla) when NOT zooming.
    // The vanilla crosshair texture is replaced with a transparent one, so the shader
    // handles all crosshair rendering. Hidden during zoom for clean scope view.
    // Smooth spread (from classify A): 0.0=sneak → 1.0=jump, interpolated per-frame
    if (!zoomMode) {
        // Smooth spread value (0.0-1.0 from classify alpha, maps to levels 0-4)
        float smoothSpread = classifyData.a * 4.0;  // 0.0-4.0

        // GUI scale: approximate from screen height (~2 at 1080p, ~3 at 1440p, ~4 at 4K)
        float guiScale = max(1.0, round(inSize.y / 540.0));

        // Continuous gap/arm calculation with GUI scale
        // Level mapping: 0→tight(sneak), 1→base, 2→walk, 3→sprint, 4→jump(widest)
        float fGap = (1.5 + smoothSpread * 2.0) * guiScale;
        float fEnd = fGap + 3.0 * guiScale;
        int gap = int(round(fGap));
        int armEnd = int(round(fEnd));

        ivec2 center = ivec2(inSize) / 2;
        ivec2 fc = ivec2(gl_FragCoord.xy);
        int dx = fc.x - center.x;
        int dy = fc.y - center.y;

        // Horizontal arm: |y| within line width, |x| in [gap, armEnd]
        int lineWidth = max(1, int(round(guiScale / 2.0)));
        bool hArm = (abs(dy) < lineWidth) && (abs(dx) >= gap && abs(dx) <= armEnd);
        // Vertical arm: |x| within line width, |y| in [gap, armEnd]
        bool vArm = (abs(dx) < lineWidth) && (abs(dy) >= gap && abs(dy) <= armEnd);

        if (hArm || vArm) {
            // Invert colors at crosshair pixels (same visual effect as vanilla INVERT blend)
            fragColor.rgb = vec3(1.0) - fragColor.rgb;
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
            "smooth_spread": {"width": 1, "height": 1, "persistent": True},
            "smooth_zoom": {"width": 1, "height": 1, "persistent": True},
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
                    {"sampler_name": "SmoothSpread", "target": "smooth_spread"},
                ],
                "output": "classify",
            },
            # Pass 1b: SPREAD COPY - persist smooth spread for next frame's feedback loop
            {
                "vertex_shader":   "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/spread_copy",
                "inputs": [
                    {"sampler_name": "Classify", "target": "classify"},
                ],
                "output": "smooth_spread",
            },
            # Pass 1c: ZOOM LERP - persist smooth zoom for next frame's FOV feedback loop
            # Reads FOV sentinel at pixel (3,0) directly from main framebuffer
            {
                "vertex_shader":   "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/zoom_lerp",
                "inputs": [
                    {"sampler_name": "Main",       "target": "minecraft:main"},
                    {"sampler_name": "SmoothZoom", "target": "smooth_zoom"},
                ],
                "output": "smooth_zoom",
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
            # Pass 3: FLASH - depth-based muzzle flash light/bloom (if mode 1)
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
            # Pass 4: ZOOM - barrel distortion + FOV reduction + flash spark overlay
            # SparkTex is the 1536x1536 flash sprite sheet (3x3 grid of 9 sprites).
            # Spark overlays AFTER zoom so it's not barrel-distorted.
            # Zoom level (x3/x4) is read from classify B channel.
            # SmoothZoom provides smooth FOV reduction factor.
            {
                "vertex_shader":   "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/zoom",
                "inputs": [
                    {"sampler_name": "In",         "target": "swap", "bilinear": True},
                    {"sampler_name": "Classify",   "target": "classify"},
                    {"sampler_name": "SparkTex",   "location": f"{ns}:flash", "width": 1536, "height": 1536, "bilinear": True},
                    {"sampler_name": "SmoothZoom", "target": "smooth_zoom"},
                ],
                "output": "final",
                "uniforms": {
                    "ZoomConfig": [
                        {"name": "Distortion", "type": "float", "value": 0.55},
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

    Mem.ctx.assets[ns].fragment_shaders["post/classify"]     = FragmentShader(CLASSIFY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/spread_copy"]  = FragmentShader(SPREAD_COPY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/zoom_lerp"]    = FragmentShader(ZOOM_LERP_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/transparency"] = FragmentShader(TRANSPARENCY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/flash"]       = FragmentShader(FLASH_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/zoom"]        = FragmentShader(ZOOM_FSH)

    Mem.ctx.assets["minecraft"].post_effects["transparency"] = set_json_encoder(PostEffect(get_post_effect_json(ns)), max_level=4)

    # Register flash spark texture for post-effect overlay (1536x1536 additive spark)
    textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")
    Mem.ctx.assets[ns].textures["effect/flash"] = Texture(source_path=f"{textures_folder}/flash.png")

    # ── Flash marker: mode 1 ──
    # dust color:[R,0,0] with R=0.02 → vsh detects R∈[1-10], G==0, B==0
    # scale=0.01 → lifetime = 0 (1 game tick minimum) → brief flash for rapid fire
    write_versioned_function("player/fire_weapon",
"""
# Shader: spawn muzzle flash marker (mode 1) - skip for grenades
# dust R=0.02, G=0, B=0 → particle.vsh detects and places at pixel (0,0)
# scale 0.01 → lifetime 0 (1 game tick) → flash auto-expires immediately
execute unless data storage mgs:gun all.stats.grenade_type at @s anchored eyes run particle minecraft:dust{color:[0.02,0.0,0.0],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @a[distance=..16]
""")

    # ── Zoom marker: mode 3 (x3) or mode 4 (x4) ──
    # Zoom x3: color:[0.02, 0.02, 0] → G∈[2-5] after randomization → mode 3
    # Zoom x4: color:[0.02, 0.08, 0] → G∈[10-20] after randomization → mode 4
    # Zoom marker spawning is handled in zoom/main (zoom.py) after zoom state
    # resolution, with cooldown guard and 5-tick delay.

