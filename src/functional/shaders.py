
# Imports
from beet import FragmentShader, PostEffect, VertexShader
from stewbeet import *

# ============================================================================ #
#                        SHADER SYSTEM OVERVIEW                                #
# ============================================================================ #
#
# This module implements full-screen post-processing effects (muzzle flash and
# scope zoom) by communicating between the datapack (mcfunctions) and the GPU
# (GLSL shaders) through a "marker particle" trick.
#
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                         HOW IT WORKS                                   ║
# ╠══════════════════════════════════════════════════════════════════════════╣
# ║                                                                        ║
# ║  1. DATAPACK spawns a tiny, near-invisible dust particle in front of   ║
# ║     the player's eyes with a very specific near-black color.           ║
# ║     → fire_weapon.mcfunction  (flash marker, mode 1)                   ║
# ║     → tick.mcfunction         (zoom marker, mode 4)                    ║
# ║                                                                        ║
# ║  2. CORE PARTICLE SHADER (particle.vsh) intercepts ALL particles.      ║
# ║     It detects our marker by its unique color pattern (idMarker()).     ║
# ║     Detected markers are REDIRECTED to a small quad at the very        ║
# ║     bottom-center of the screen (invisible to the player).             ║
# ║     The fragment shader (particle.fsh) writes a SENTINEL value         ║
# ║     (alpha=0.01, grayscale=mode/MARKERS) to that quad area.            ║
# ║                                                                        ║
# ║  3. POST-EFFECT PIPELINE (transparency.json) runs these passes:        ║
# ║                                                                        ║
# ║     ┌─────────┐   reads particles   ┌──────────┐                      ║
# ║     │particles├──────────────────────►│ CLASSIFY │ → 1x1 "classify"    ║
# ║     │ target  │   target center      │  (pass1) │   target with mode   ║
# ║     └─────────┘                      └──────────┘                      ║
# ║                                                                        ║
# ║     ┌──────────────┐                 ┌──────────────┐                  ║
# ║     │ all 6 layers ├────────────────►│ TRANSPARENCY │ → "final" target ║
# ║     │  (fabulous)  │                 │   (pass2)    │   (hides marker) ║
# ║     └──────────────┘                 └──────────────┘                  ║
# ║                                                                        ║
# ║     ┌───────┐  ┌──────────┐         ┌───────┐                         ║
# ║     │ final ├──┤ classify ├────────►│ FLASH │ → "swap" target         ║
# ║     └───────┘  └──────────┘         │(pass3)│   (depth-based effect)  ║
# ║                                      └───────┘                         ║
# ║                                                                        ║
# ║     ┌───────┐  ┌──────────┐         ┌───────┐                         ║
# ║     │ swap  ├──┤ classify ├────────►│ ZOOM  │ → "final" target        ║
# ║     └───────┘  └──────────┘         │(pass4)│   (barrel distortion)   ║
# ║                                      └───────┘                         ║
# ║                                                                        ║
# ║     ┌───────┐                        ┌───────┐                         ║
# ║     │ final ├───────────────────────►│ BLIT  │ → minecraft:main       ║
# ║     └───────┘                        │(pass5)│   (copy to screen)     ║
# ║                                      └───────┘                         ║
# ║                                                                        ║
# ╠══════════════════════════════════════════════════════════════════════════╣
# ║                      ⚠ REQUIREMENTS ⚠                                 ║
# ║                                                                        ║
# ║  • Graphics MUST be set to "Fabulous!" for the post-effect pipeline    ║
# ║    to run. With Fancy/Fast, transparencies aren't composited and       ║
# ║    post_effect/transparency.json is IGNORED entirely.                  ║
# ║                                                                        ║
# ║  • The resource pack must be active and loaded.                        ║
# ║                                                                        ║
# ║  • The marker particle must be IN FRONT of the camera (not behind!)    ║
# ║    because Minecraft frustum-culls particles outside the view frustum  ║
# ║    BEFORE sending them to the GPU. Particles behind the camera are     ║
# ║    never rendered and never reach the vertex shader.                   ║
# ║                                                                        ║
# ╠══════════════════════════════════════════════════════════════════════════╣
# ║                         DEBUG MODE                                     ║
# ║                                                                        ║
# ║  Set DEBUG to 1 (currently ON) to show colored debug indicators:       ║
# ║                                                                        ║
# ║  BOTTOM-LEFT of screen, three 50x50 squares side by side:             ║
# ║    [RED]    = transparency compositing pass (pass 2) is running        ║
# ║    [GREEN]  = flash pass (pass 3) is running                           ║
# ║    [BLUE]   = zoom pass (pass 4) is running                            ║
# ║                                                                        ║
# ║  The zoom pass square color also encodes the detected mode:            ║
# ║    Blue   = pipeline active, no mode detected (mode 0)                 ║
# ║    Orange = muzzle flash detected (modes 1-3)                          ║
# ║    Cyan   = zoom detected (mode 4)                                     ║
# ║                                                                        ║
# ║  IF YOU SEE NO SQUARES: the pipeline isn't loading at all.             ║
# ║    → Check Fabulous graphics, resource pack loaded, check game log     ║
# ║                                                                        ║
# ║  IF YOU SEE RED ONLY: transparency pass works but flash/zoom crash     ║
# ║    → Shader compilation error in flash.fsh or zoom.fsh                 ║
# ║                                                                        ║
# ║  IF YOU SEE RED+GREEN+BLUE but no effects:                             ║
# ║    → Pipeline runs, marker detection fails (particle not reaching GPU) ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝
#
# FILE RELATIONSHIPS:
#   shaders.py             → THIS FILE: generates all shaders + mcfunctions
#   particle.vsh/fsh       → Override minecraft:core/particle (core rendering)
#   classify.fsh           → Post pass 1: reads particles target → 1x1 mode
#   transparency.fsh       → Post pass 2: composites all layers, hides marker
#   flash.fsh              → Post pass 3: applies muzzle flash if mode 1-3
#   zoom.fsh               → Post pass 4: applies barrel distortion if mode 4
#   transparency.json      → Pipeline definition (post_effect/)
#   fire_weapon.mcfunction → Spawns flash marker particle on each shot
#   tick.mcfunction        → Spawns zoom marker particle each tick while ADS
#
# TECHNICAL NOTES:
#   - We do NOT use SamplerInfo uniform blocks. While documented by the
#     community, this block may not be populated on all MC versions.
#     Instead, we use textureSize() (standard GLSL 330) everywhere.
#   - The sentinel in particle.fsh writes to ALL pixels of the redirected
#     quad (not just one pixel), making detection robust against precision.
#   - The Globals uniform block (ScreenSize, GameTime) is ONLY available
#     in core shaders, NOT in post-processing shaders.
#


# ============================================================================
# GLSL Shader Sources
# ============================================================================


# ────────────────────────────────────────────────────────────────────────────
# 1. CORE PARTICLE VERTEX SHADER
# ────────────────────────────────────────────────────────────────────────────
# Overrides: assets/minecraft/shaders/core/particle.vsh
# Role: Processes ALL particle vertices. Detects our marker dust particles
#       by their unique near-black color, then REDIRECTS them to a hidden
#       quad at the bottom of the screen.
# Receives from: Minecraft engine (particle vertex data)
# Sends to: particle.fsh via varyings (marker, vertexColor, etc.)
#
PARTICLE_VSH = """\
#version 330

// ── Minecraft include files ──
// fog.glsl:              Fog uniform block + fog distance functions
// dynamictransforms.glsl: DynamicTransforms block (ModelViewMat, ColorModulator)
// projection.glsl:       Projection block (ProjMat)
// sample_lightmap.glsl:  sample_lightmap() for lightmap lookup (new in 1.21+)
#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>
#moj_import <minecraft:projection.glsl>
#moj_import <minecraft:sample_lightmap.glsl>

// ── Vertex attributes (from Minecraft's particle renderer) ──
in vec3 Position;   // World-space position of this quad corner
in vec2 UV0;        // Texture coordinate for the particle sprite
in vec4 Color;      // Particle color (RGBA) - for dust, set by the command
in ivec2 UV2;       // Lightmap coordinate

uniform sampler2D Sampler2;  // Lightmap texture

// ── Outputs → particle.fsh ──
out float sphericalVertexDistance;    // Fog calculation
out float cylindricalVertexDistance;  // Fog calculation
out vec2 texCoord0;                  // Sprite UV
out vec4 vertexColor;                // Color * lightmap
out float marker;                    // 0=normal particle, >0=marker mode ID

// ── Constants ──
// How many distinct marker modes we support (must match fsh + classify)
#define MARKERS 5

// Maximum color channel value to count as a "marker" signal.
// dust color [0.011, 0, 0] after 8-bit quantization -> ~2/255 = 0.0078
// We accept 0 exclusive to 4/255 = 0.0157
#define COLORLIMIT 4.0 / 255.0

// ── Marker detection function ──
// Identifies marker dust particles by their unique near-black RGB pattern.
// Each mode uses a different combination of nonzero (tiny) channels:
//   Mode 1: R>0 G=0 B=0  -> dust color [0.011, 0.0,   0.0  ] -> FLASH
//   Mode 2: R=0 G>0 B=0  -> dust color [0.0,   0.011, 0.0  ] -> (unused)
//   Mode 3: R=0 G=0 B>0  -> dust color [0.0,   0.0,   0.011] -> (unused)
//   Mode 4: R>0 G>0 B=0  -> dust color [0.011, 0.011, 0.0  ] -> ZOOM
//   Mode 5: R>0 G=0 B>0  -> dust color [0.011, 0.0,   0.011] -> (unused)
//
// Why this is safe: No natural Minecraft particle has ALL channels < 4/255.
// Dust particles apply a random 0.8x-1.0x multiplier, but zero channels
// stay exactly 0.0. Nonzero channels (e.g., 0.011*0.8=0.009) remain under
// COLORLIMIT after the random scaling.
float idMarker(vec3 color) {
    bool rz = color.r == 0.0;                           // Red is exactly zero
    bool gz = color.g == 0.0;                           // Green is exactly zero
    bool bz = color.b == 0.0;                           // Blue is exactly zero
    bool rnz = color.r > 0.0 && color.r < COLORLIMIT;  // Red is tiny nonzero
    bool gnz = color.g > 0.0 && color.g < COLORLIMIT;  // Green is tiny nonzero
    bool bnz = color.b > 0.0 && color.b < COLORLIMIT;  // Blue is tiny nonzero

    return 1.0 * float(rnz && gz && bz)     // Mode 1: R only  -> FLASH
         + 2.0 * float(rz && gnz && bz)     // Mode 2: G only  -> (spare)
         + 3.0 * float(rz && gz && bnz)     // Mode 3: B only  -> (spare)
         + 4.0 * float(rnz && gnz && bz)    // Mode 4: R+G     -> ZOOM
         + 5.0 * float(rnz && gz && bnz);   // Mode 5: R+B     -> (spare)
}

void main() {
    // ── Standard particle vertex processing (same as vanilla) ──
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);

    sphericalVertexDistance = fog_spherical_distance(Position);
    cylindricalVertexDistance = fog_cylindrical_distance(Position);
    texCoord0 = UV0;
    // sample_lightmap: new in 1.21+, replaces texelFetch(Sampler2, UV2/16, 0)
    vertexColor = Color * sample_lightmap(Sampler2, UV2);

    marker = 0.0;

    // ── Marker detection ──
    // The datapack spawns marker particles IN FRONT of the camera:
    //   particle dust{color:[0.011,0.0,0.0],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s
    //
    // CRITICAL: The particle MUST be in front of the camera, not behind!
    // Minecraft frustum-culls particles outside the view frustum BEFORE the GPU.
    // Using ^ ^ ^-500 (behind camera) would silently fail (never rendered).
    //
    // Detection is by COLOR ONLY via idMarker(). No distance or direction check
    // is needed because no natural particle has colors this dark.
    float mv = idMarker(Color.rgb);

    if (mv > 0.0) {
        marker = mv;

        // REDIRECT: Move this particle's quad to a small area at the
        // bottom-center of the screen. particle.fsh will write the
        // sentinel value to ALL pixels in this quad.
        // transparency.fsh then hides these pixels during compositing.
        //
        // NDC: x in [-0.02, 0.02], y in [-1.0, -0.98], z = -0.999
        //   -> About 40x10 pixels at the very bottom of the screen
        //   -> z=-0.999 -> depth buffer ~0.0005 (near plane)
        //   -> Invisible to player (below visible area + hidden by transparency)
        if (gl_VertexID % 4 == 0) {
            gl_Position = vec4(0.02, -1.0, -0.999, 1.0);
        } else if (gl_VertexID % 4 == 1) {
            gl_Position = vec4(0.02, -0.98, -0.999, 1.0);
        } else if (gl_VertexID % 4 == 2) {
            gl_Position = vec4(-0.02, -0.98, -0.999, 1.0);
        } else {
            gl_Position = vec4(-0.02, -1.0, -0.999, 1.0);
        }
    }
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 2. CORE PARTICLE FRAGMENT SHADER
# ────────────────────────────────────────────────────────────────────────────
# Overrides: assets/minecraft/shaders/core/particle.fsh
# Role: For normal particles, renders them with texture+color+fog (vanilla).
#       For marker particles (marker > 0), writes a SENTINEL pixel:
#         color = grayscale(mode/MARKERS), alpha = 0.01
#       to ALL pixels of the redirected quad (not just one pixel).
# Receives from: particle.vsh (marker, vertexColor, texCoord0, fog)
# Sends to: particles render target (read by classify.fsh in post pipeline)
#
# PREVIOUS BUG: We used to compute the exact center pixel via glpos and
# write only there. This was extremely fragile. Now we write to ALL pixels
# in the redirected quad, which is always at the bottom of the screen.
# transparency.fsh hides all of them during compositing.
#
PARTICLE_FSH = """\
#version 330

// fog.glsl:              apply_fog(), FogColor, etc.
// dynamictransforms.glsl: ColorModulator
#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;  // Particle sprite atlas

// ── Inputs from particle.vsh ──
in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec2 texCoord0;
in vec4 vertexColor;
in float marker;  // 0 = normal particle, >0 = marker mode ID

out vec4 fragColor;

#define MARKERS 5  // Must match vsh

void main() {
    if (marker > 0.0) {
        // ── MARKER SENTINEL ──
        // Write to ALL pixels of the redirected quad.
        // The vsh redirected the quad to ~40x10 pixels at screen bottom.
        // Encode the mode as grayscale with sentinel alpha:
        //   r = g = b = mode/MARKERS (e.g., 0.2 for flash, 0.8 for zoom)
        //   alpha = 0.01 (sentinel: normal particles have alpha >= 0.1)
        // classify.fsh reads a pixel in this area and decodes the mode.
        // transparency.fsh hides ALL these pixels during compositing.
        fragColor = vec4(vec3(marker / float(MARKERS)), 0.01);
    } else {
        // ── NORMAL PARTICLE RENDERING (vanilla behavior) ──
        vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
        if (color.a < 0.1) {
            discard;
        }
        fragColor = apply_fog(color, sphericalVertexDistance, cylindricalVertexDistance,
            FogEnvironmentalStart, FogEnvironmentalEnd,
            FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
    }
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 3. POST-PROCESSING: CLASSIFY PASS
# ────────────────────────────────────────────────────────────────────────────
# File: assets/<ns>/shaders/post/classify.fsh
# Role: Reads the particles render target and detects the marker sentinel.
#       Outputs to a tiny 1x1 "classify" target containing the detected mode.
# Receives from: particles target (written by particle.fsh)
# Sends to: classify target (read by flash.fsh, zoom.fsh)
#
# This pass outputs to a 1x1 pixel target. Every subsequent pass reads it
# at UV (0.5, 0.5) to get the current mode. This avoids re-scanning the
# full particles target in every pass.
#
# NOTE: We do NOT use SamplerInfo to get ParticlesSize. Instead we use
# textureSize() which is standard GLSL 330 and always works.
#
CLASSIFY_FSH = """\
#version 330

// ── Samplers: pipeline inputs ──
uniform sampler2D ParticlesSampler;       // Particles target (color)
uniform sampler2D ParticlesDepthSampler;  // Particles target (depth)

in vec2 texCoord;  // Screen UV from screenquad.vsh
out vec4 fragColor;

#define MARKERS 5  // Must match particle.vsh/fsh

void main() {
    // Get the particles target resolution using textureSize (GLSL 330).
    // This replaces the previous SamplerInfo block which may not be
    // populated by the engine in all MC versions.
    ivec2 particlesRes = textureSize(ParticlesSampler, 0);

    // Read the CENTER of the BOTTOM ROW of the particles target.
    // This is where particle.fsh wrote the marker sentinel:
    //   x = center pixel → UV 0.5
    //   y = bottom-ish   → UV = 1.5 / height (second row for safety)
    // We sample a few pixels up from the very bottom to avoid edge clamping.
    // The sentinel quad covers ~10 rows at the bottom, so row 1-2 is safe.
    vec2 sampleUV = vec2(0.5, 1.5 / float(particlesRes.y));
    vec4 pix = texture(ParticlesSampler, sampleUV);
    float depth = texture(ParticlesDepthSampler, sampleUV).r;

    float mode = 0.0;

    // Detect sentinel: alpha ~0.01 AND depth ~0.0005 (near plane).
    // Normal particles: alpha >= 0.1 (others are discarded), depth > 0.01
    // Both conditions prevent false positives from any natural particle.
    if (pix.a > 0.005 && pix.a < 0.02 && depth < 0.01) {
        // Decode mode from red channel: round(r * MARKERS)
        //   r=0.2 -> mode 1 (flash), r=0.8 -> mode 4 (zoom)
        mode = round(pix.r * float(MARKERS));
    }

    // Output: mode/(MARKERS) in red channel of the 1x1 target.
    // flash.fsh and zoom.fsh read it: round(texture(...).r * MARKERS)
    //mode = 4.0;  // DEBUG: Force mode 4 (zoom) to test the pipeline without the datapack
    fragColor = vec4(mode / float(MARKERS), 0.0, 0.0, 1.0);
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 4. POST-PROCESSING: TRANSPARENCY COMPOSITING
# ────────────────────────────────────────────────────────────────────────────
# File: assets/<ns>/shaders/post/transparency.fsh
# Role: Fabulous transparency compositing (merges all 6 render layers).
#       Also HIDES the marker pixel so it's invisible in the final image.
# Receives from: All 6 Fabulous render targets + depth buffers
# Sends to: "final" target (read by flash.fsh)
#
# This is the vanilla transparency.fsh with two additions:
# 1. Before inserting particles, check if the pixel is a marker sentinel
#    (alpha < 0.02 AND depth < 0.01). If so, skip it.
# 2. A debug indicator (red square at bottom-left) to confirm this pass runs.
#
# NOTE: We do NOT import globals.glsl here! The Globals uniform block
# (ScreenSize, GameTime) is ONLY for core shaders. Post-processing shaders
# do NOT have access to it. Using it here would cause a link error.
#
TRANSPARENCY_FSH = """\
#version 330

// ── All 6 Fabulous render targets ──
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

#define DEBUG 1  // Set to 0 for production

// ── Depth-sorted layer compositing (vanilla algorithm) ──
// 6 layers maximum: main (opaque) + 5 translucent layers
vec4 color_layers[6] = vec4[](vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0));
float depth_layers[6] = float[](0, 0, 0, 0, 0, 0);
int active_layers = 0;

out vec4 fragColor;

// Insert a layer into the depth-sorted list (back-to-front for alpha blending)
void try_insert(vec4 color, float depth) {
    if (color.a == 0.0) {
        return;  // Skip fully transparent layers
    }
    // Add at the end and bubble-sort backward into position
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

// Alpha-blend source over destination
vec3 blend(vec3 dst, vec4 src) {
    return (dst * (1.0 - src.a)) + src.rgb;
}

void main() {
    // Base layer: opaque main target
    color_layers[0] = vec4(texture(MainSampler, texCoord).rgb, 1.0);
    depth_layers[0] = texture(MainDepthSampler, texCoord).r;
    active_layers = 1;

    // Insert transparent layers
    try_insert(texture(TranslucentSampler, texCoord), texture(TranslucentDepthSampler, texCoord).r);
    try_insert(texture(ItemEntitySampler, texCoord), texture(ItemEntityDepthSampler, texCoord).r);

    // ── PARTICLES LAYER: hide the marker sentinel ──
    // Marker sentinel has:  alpha ~0.01, depth ~0.0005
    // Normal particles have: alpha >= 0.1, depth > 0.01
    // Checking BOTH conditions = no false positives possible.
    vec4 particleColor = texture(ParticlesSampler, texCoord);
    float particleDepth = texture(ParticlesDepthSampler, texCoord).r;
    bool isMarker = (particleColor.a > 0.005 && particleColor.a < 0.02 && particleDepth < 0.01);
    if (!isMarker) {
        try_insert(particleColor, particleDepth);
    }

    try_insert(texture(WeatherSampler, texCoord), texture(WeatherDepthSampler, texCoord).r);
    try_insert(texture(CloudsSampler, texCoord), texture(CloudsDepthSampler, texCoord).r);

    // Composite all layers back-to-front
    vec3 texelAccum = color_layers[0].rgb;
    for (int ii = 1; ii < active_layers; ++ii) {
        texelAccum = blend(texelAccum, color_layers[ii]);
    }

    fragColor = vec4(texelAccum.rgb, 1.0);

#if DEBUG
    // ── DEBUG: RED 50x50 square at bottom-left ──
    // Uses only gl_FragCoord (always available, no uniforms needed).
    // If you see this red square: the transparency compositing pass works.
    // gl_FragCoord.y=0.5 is the bottom row, increasing upward.
    if (gl_FragCoord.x < 50.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = pass 2 runs
    }
#endif
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 5. POST-PROCESSING: MUZZLE FLASH EFFECT
# ────────────────────────────────────────────────────────────────────────────
# File: assets/<ns>/shaders/post/flash.fsh
# Role: When classify detects modes 1-3 (flash), applies a depth-based
#       muzzle flash: nearby surfaces get brightened with warm colored light
#       that falls off with distance from the camera.
# Receives from: "final" target + main depth buffer + classify target
# Sends to: "swap" target (read by zoom.fsh)
#
# The effect:
#   1. Linearize depth buffer -> world-space distance per pixel
#   2. Compute light intensity based on 1/distance^1.5 falloff
#   3. Apply 5-point cross blur to soften the lighting
#   4. Modulate scene color + add a small additive light term
#
# NOTE: Uses textureSize() instead of SamplerInfo for screen dimensions.
#
FLASH_FSH = """\
#version 330

uniform sampler2D InSampler;        // "final" target (composited scene)
uniform sampler2D InDepthSampler;   // Main depth buffer
uniform sampler2D ClassifySampler;  // 1x1 "classify" target (contains mode)

// ── FlashConfig: tunable parameters from pipeline JSON ──
layout(std140) uniform FlashConfig {
    vec3 Color;  // Flash light color (default: warm [1.0, 0.8, 0.5])
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 1         // Set to 0 for production
#define MARKERS 5       // Must match classify.fsh
#define INTENSITY 1.5   // Overall flash brightness multiplier
#define MAXDIST 20.0    // Max world-space distance affected (blocks)
#define NEAR 0.1        // Camera near plane (blocks)
#define FAR 1536.0      // Camera far plane (blocks)
#define BLURR 10.0      // Blur sample offset in pixels
#define FOV 70          // Assumed field of view (degrees)
// CK converts texCoord offset -> view-space offset at depth=1
#define CK tan(float(FOV) / 360.0 * 3.14159265358979) * 2.0

// Convert depth buffer [0,1] -> linear world-space distance
float LinearizeDepth(float depth) {
    float z = depth * 2.0 - 1.0;  // [0,1] -> [-1,1] NDC
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));
}

void main() {
    // Get screen dimensions from texture (replaces SamplerInfo.InSize)
    vec2 inSize = vec2(textureSize(InSampler, 0));

    // Read mode from 1x1 classify target at its center
    float mode = round(texture(ClassifySampler, vec2(0.5, 0.5)).r * float(MARKERS));

    // Start with composited scene
    fragColor = texture(InSampler, texCoord);

    // Flash: activates for modes 1-3 (currently only mode 1 = red dust)
    if (mode >= 1.0 && mode <= 3.0) {
        vec2 oneTexel = 1.0 / inSize;
        float aspectRatio = inSize.x / inSize.y;

        // Linearize depth to world-space distance at this pixel
        float depth = LinearizeDepth(texture(InDepthSampler, texCoord).r);

        // Convert screen UV -> world-space XY at this depth
        vec2 screenCoords = (texCoord - 0.5) * vec2(aspectRatio, 1.0) * CK * depth;
        float dist = length(vec3(screenCoords, depth));

        if (dist < MAXDIST) {
            // 5-point cross blur (center + 4 cardinal neighbors)
            vec4 blurColor = fragColor
                + texture(InSampler, texCoord + vec2(oneTexel.x * BLURR, 0.0))
                + texture(InSampler, texCoord - vec2(oneTexel.x * BLURR, 0.0))
                + texture(InSampler, texCoord + vec2(0.0, oneTexel.y * BLURR))
                + texture(InSampler, texCoord - vec2(0.0, oneTexel.y * BLURR));
            blurColor /= 5.0;

            // Light intensity: inverse distance^1.5 falloff
            vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * Color;

            // Apply: modulate dark areas + attenuate bright areas + additive term
            fragColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9)
                           * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0)) + vec3(1.0);
            fragColor.rgb += INTENSITY * lightColor * 0.1;
        }
    }

    fragColor = vec4(fragColor.rgb, 1.0);

#if DEBUG
    // ── DEBUG: GREEN 50x50 square at bottom-left, offset x=50 ──
    // If you see this: the flash pass (pass 3) runs successfully.
    if (gl_FragCoord.x >= 50.0 && gl_FragCoord.x < 100.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = pass 3 runs
    }
#endif
}
"""


# ────────────────────────────────────────────────────────────────────────────
# 6. POST-PROCESSING: BARREL DISTORTION ZOOM
# ────────────────────────────────────────────────────────────────────────────
# File: assets/<ns>/shaders/post/zoom.fsh
# Role: When classify detects mode 4, applies barrel distortion zoom
#       in a circular area at screen center, simulating a scope lens.
# Receives from: "swap" target (after flash) + classify
# Sends to: "final" target (then blitted to screen by pass 5)
#
# The effect:
#   - Circular region (RADIUS in aspect-corrected UV) at screen center
#   - Inside: barrel distortion + zoom magnification + bicubic filtering
#   - Outside: passthrough (no change)
#
# NOTE: Uses textureSize() instead of SamplerInfo for all dimensions.
# Contains the main DEBUG indicator showing detected mode.
#
ZOOM_FSH = """\
#version 330

uniform sampler2D InSampler;        // "swap" target (after flash pass)
uniform sampler2D ClassifySampler;  // 1x1 "classify" target

// ── ZoomConfig: tunable parameters from pipeline JSON ──
layout(std140) uniform ZoomConfig {
    float Distortion;  // Barrel distortion strength (default: 0.55)
    float Zoom;        // Magnification factor (default: 4.0)
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 1       // Set to 0 for production
#define MARKERS 5     // Must match classify.fsh
#define RADIUS 0.14   // Scope circle radius (aspect-corrected UV space)

// ── Bicubic interpolation (Catmull-Rom spline weights) ──
vec4 cubic(float v) {
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    float w = 6.0 - x - y - z;
    return vec4(x, y, z, w) * (1.0 / 6.0);
}

// Sample with bicubic filtering (4 bilinear taps for smooth magnification)
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
    // Get screen dimensions from texture (replaces SamplerInfo)
    vec2 inSize = vec2(textureSize(InSampler, 0));

    // Read mode from classify
    float mode = round(texture(ClassifySampler, vec2(0.5, 0.5)).r * float(MARKERS));

    // Start with passthrough
    fragColor = texture(InSampler, texCoord);

    // Zoom: mode 4 (tolerance +/-0.5)
    if (mode >= 3.5 && mode <= 4.5) {
        float aspectRatio = inSize.x / inSize.y;
        // Center-origin, aspect-corrected screen coords
        vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

        if (length(screenCoord) < RADIUS) {
            // Barrel distortion: map flat coords to spherical projection
            float d = length(screenCoord * Distortion / RADIUS);
            float z = sqrt(1.0 - d * d);
            float r = atan(d, z) / 3.1415926535;
            float theta = atan(screenCoord.y, screenCoord.x);

            // Back to UV with magnification
            screenCoord = vec2(cos(theta), sin(theta)) * r / Zoom;
            vec2 pixCoord = screenCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5);

            fragColor = textureBicubic(InSampler, pixCoord, inSize);
        }
    }

#if DEBUG
    // ── DEBUG: Mode indicator at bottom-left, offset x=100 (50x50) ──
    // Color encodes the detected mode from the classify pass:
    //   BLUE   = pipeline active, mode 0 (no marker detected)
    //   ORANGE = flash detected (modes 1-3)
    //   CYAN   = zoom detected (mode 4)
    //
    // This is the MOST IMPORTANT indicator. It tells you:
    //   - The pipeline is running (any colored square visible)
    //   - classify read the particles target successfully
    //   - The mode was decoded correctly
    //
    // IF NO SQUARE: the pipeline doesn't load at all.
    //   → Check Fabulous graphics, resource pack loaded
    //   → Check game log for shader compilation errors
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

def get_post_effect_json(ns: str) -> JsonDict:  # type: ignore[type-arg]
    """Build the transparency post-effect pipeline JSON.

    Overrides minecraft:post_effect/transparency.json.
    5 passes: classify -> transparency -> flash -> zoom -> blit.
    Only runs when Graphics = "Fabulous!".
    """
    return {
        "targets": {
            # 1x1 target storing the detected mode (avoids re-reading particles)
            "classify": {"width": 1, "height": 1},
            # Full-screen working targets (ping-pong)
            "final": {},
            "swap": {},
        },
        "passes": [
            # Pass 1: CLASSIFY - detect marker from particles target
            {
                "vertex_shader": "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/classify",
                "inputs": [
                    {"sampler_name": "Particles", "target": "minecraft:particles"},
                    {"sampler_name": "ParticlesDepth", "target": "minecraft:particles", "use_depth_buffer": True},
                ],
                "output": "classify",
            },
            # Pass 2: TRANSPARENCY - Fabulous compositing (hides marker)
            {
                "vertex_shader": "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/transparency",
                "inputs": [
                    {"sampler_name": "Main", "target": "minecraft:main"},
                    {"sampler_name": "MainDepth", "target": "minecraft:main", "use_depth_buffer": True},
                    {"sampler_name": "Translucent", "target": "minecraft:translucent"},
                    {"sampler_name": "TranslucentDepth", "target": "minecraft:translucent", "use_depth_buffer": True},
                    {"sampler_name": "ItemEntity", "target": "minecraft:item_entity"},
                    {"sampler_name": "ItemEntityDepth", "target": "minecraft:item_entity", "use_depth_buffer": True},
                    {"sampler_name": "Particles", "target": "minecraft:particles"},
                    {"sampler_name": "ParticlesDepth", "target": "minecraft:particles", "use_depth_buffer": True},
                    {"sampler_name": "Clouds", "target": "minecraft:clouds"},
                    {"sampler_name": "CloudsDepth", "target": "minecraft:clouds", "use_depth_buffer": True},
                    {"sampler_name": "Weather", "target": "minecraft:weather"},
                    {"sampler_name": "WeatherDepth", "target": "minecraft:weather", "use_depth_buffer": True},
                ],
                "output": "final",
            },
            # Pass 3: FLASH - depth-based muzzle flash (if mode 1-3)
            {
                "vertex_shader": "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/flash",
                "inputs": [
                    {"sampler_name": "In", "target": "final"},
                    {"sampler_name": "InDepth", "target": "minecraft:main", "use_depth_buffer": True},
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
                    {"sampler_name": "In", "target": "swap", "bilinear": True},
                    {"sampler_name": "Classify", "target": "classify"},
                ],
                "output": "final",
                "uniforms": {
                    "ZoomConfig": [
                        {"name": "Distortion", "type": "float", "value": 0.55},
                        {"name": "Zoom", "type": "float", "value": 4.0},
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
    Since write_versioned_function appends, our particle commands appear
    at the TOP of the merged mcfunctions (before weapon logic).
    """
    ns: str = Mem.ctx.project_id

    # ── Register core particle shaders (override vanilla) ──
    # Replace minecraft:core/particle.vsh and .fsh
    # Processes ALL particles, only modifies our markers by color detection.
    Mem.ctx.assets["minecraft"].vertex_shaders["core/particle"] = VertexShader(PARTICLE_VSH)
    Mem.ctx.assets["minecraft"].fragment_shaders["core/particle"] = FragmentShader(PARTICLE_FSH)

    # ── Register post-processing fragment shaders ──
    # Go to assets/<ns>/shaders/post/<name>.fsh
    # Referenced in pipeline JSON as f"{ns}:post/<name>"
    Mem.ctx.assets[ns].fragment_shaders["post/classify"] = FragmentShader(CLASSIFY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/transparency"] = FragmentShader(TRANSPARENCY_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/flash"] = FragmentShader(FLASH_FSH)
    Mem.ctx.assets[ns].fragment_shaders["post/zoom"] = FragmentShader(ZOOM_FSH)

    # ── Register post-effect pipeline (overrides vanilla transparency) ──
    # Only active when Graphics = "Fabulous!"
    Mem.ctx.assets["minecraft"].post_effects["transparency"] = PostEffect(get_post_effect_json(ns))

    # ── Datapack: spawn marker particles ──
    #
    # COMMUNICATION: mcfunction -> particle -> vsh -> fsh -> classify -> effects
    #
    # The particle MUST be IN FRONT of the camera (^ ^ ^1, not ^ ^ ^-500)!
    # Minecraft frustum-culls particles outside the view frustum BEFORE the GPU.
    # "force" only extends the server send range to 512 blocks, it does NOT
    # bypass client-side frustum culling. Particles behind the camera are
    # never rendered = the vertex shader never runs = nothing happens.

    # ── Flash marker: mode 1 (red channel only) ──
    # Spawned once per shot in fire_weapon (after cooldown/ammo checks).
    # The dust particle persists for ~8-20 ticks, so the flash lasts briefly.
    write_versioned_function("player/fire_weapon",
"""
# Shader: spawn muzzle flash marker (mode 1: red only)
# 1 block in front, scale 0.01 -> detected by core/particle.vsh -> flash.fsh
execute at @s anchored eyes run particle minecraft:dust{color:[0.011,0.0,0.0],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s
""")

    # ── Zoom marker: mode 4 (red + green channels) ──
    # Spawned every tick while ADS is active (zoom score = 1).
    # Multiple particles may coexist (each lives several ticks),
    # but they all encode mode=4, so classify picks it up fine.
    write_versioned_function("player/tick",
f"""
# Shader: spawn zoom marker (mode 4: red+green)
# Every tick while ADS, 1 block in front -> detected by particle.vsh -> zoom.fsh
execute if score @s {ns}.zoom matches 1 at @s anchored eyes run particle minecraft:dust{{color:[0.011,0.011,0.0],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s
""")

