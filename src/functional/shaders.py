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
# ║    no random scaling. This allows reliable 8-bit integer detection.    ║
# ║    Dust particles apply a random 0.8-1.0x multiplier that corrupts     ║
# ║    the color values, making detection impossible.                      ║
# ║                                                                        ║
# ║  WHY range-based detection (not exact match):                          ║
# ║    Minecraft packs float RGBA to ARGB int using floor(value * 255).   ║
# ║    Values like 4/255=0.01568627 become floor(3.99999)=3, not 4!       ║
# ║    Using "mid-bin" float values (e.g. 4.5/255) and range checks in    ║
# ║    the vsh (G in [3-5] → zoom) makes detection immune to ±1 error.   ║
# ║                                                                        ║
# ║  WHY alpha threshold for flash:                                        ║
# ║    entity_effect has random 10-40 tick lifetime. Alpha decays by       ║
# ║    1/lifetime per tick. Checking A >= 230 in vsh limits the flash     ║
# ║    sentinel to ~2-5 ticks. Stale particles (A < 230) are still        ║
# ║    hidden (redirected to a dead pixel) but don't write sentinel data.  ║
# ║                                                                        ║
# ║  WHY deterministic sentinel in particle.fsh:                           ║
# ║    The fsh writes vec4(254/255, mode/255, 0, 1) regardless of the     ║
# ║    raw Color values. This ensures classify always reads exact integer  ║
# ║    values via texelFetch, immune to float quantization issues.         ║
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
# ║    [150-200px] = flash marker pixel (YELLOW=present, GRAY=empty)       ║
# ║    [200-250px] = zoom  marker pixel (YELLOW=present, GRAY=empty)       ║
# ║                                                                        ║
# ╚════════════════════════════════════════════════════════════════════════╝
#
# MARKER PIXEL MAP:
#   Mode 1 (flash) → screen pixel (0, 0)   [bottom-left corner]
#   Mode 4 (zoom)  → screen pixel (2, 0)   [2px right of corner]
#
# MARKER COLOR ENCODING (entity_effect RGBA):
#   Command provides float [R, G, B, A]. Minecraft internally packs to ARGB int
#   using floor(value * 255), so float values must be slightly ABOVE the target
#   integer boundary to survive truncation.
#   R = 254.5/255 = 0.99803922   → floor → 254 = MARKER_RED signature
#   G = 1.5/255  = 0.00588235   → floor → 1   = flash mode
#   G = 4.5/255  = 0.01764706   → floor → 4   = zoom mode
#   B = 0                        → always 0 (part of signature)
#   A = 1.0                      → fsh forces A=255 in output
#
#   vsh detects by RANGES (tolerates ±1 quantization).
#   vsh also checks A >= 230 for flash → limits flash to ~2-5 ticks
#   (entity_effect alpha decays each tick; stale particles still hidden).
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

// flat = no interpolation across quad (critical for integer flags)
flat out int markerMode;  // 0=normal particle, 1=flash, 4=zoom

// Alpha threshold for ACTIVATING flash mode signal.
// entity_effect alpha decays by 1/lifetime per tick (lifetime = 10-40 ticks).
// At 230/255 ≈ 0.902, the flash signal lasts ~2-5 ticks depending on lifetime.
// Stale particles (mode -1) are still hidden but DON'T write the sentinel.
#define FLASH_ALPHA_MIN 230

const vec2 corners[4] = vec2[4](
    vec2(0.0, 1.0),
    vec2(0.0, 0.0),
    vec2(1.0, 0.0),
    vec2(1.0, 1.0)
);

ivec2 markerPixel(int mode) {
    if (mode == 1) return ivec2(0, 0);  // flash → bottom-left corner
    if (mode == 4) return ivec2(2, 0);  // zoom  → 2px right of corner
    return ivec2(4, 0);                 // stale → hidden pixel (never read)
}

// Detect entity_effect marker by color pattern.
// Minecraft packs float color to ARGB int using floor(value * 255),
// so the actual vertex Color may be ±1 from the intended value.
// We use ranges to tolerate this quantization.
int detectMarkerMode(vec4 color) {
    ivec4 ic = ivec4(round(color * 255.0));
    // Signature: R near 254, B must be 0
    if (ic.r >= 253 && ic.r <= 255 && ic.b == 0) {
        // Flash: G should be ~1 (range [0-2] covers ±1 quantization)
        if (ic.g >= 0 && ic.g <= 2) {
            // Check alpha to limit flash duration:
            // Fresh particle (A >= 230) → mode 1 (writes sentinel)
            // Stale particle (A < 230)  → mode -1 (hidden, no sentinel)
            return (ic.a >= FLASH_ALPHA_MIN) ? 1 : -1;
        }
        // Zoom: G should be ~4 (range [3-5] covers ±1 quantization)
        if (ic.g >= 3 && ic.g <= 5) return 4;
    }
    return 0;  // Not a marker
}

void main() {
    int mode = detectMarkerMode(Color);
    markerMode = mode;

    if (mode != 0) {
        // REDIRECT marker quad to an exact pixel using ScreenSize.
        ivec2 pixel = markerPixel(mode);  // mode -1 → hidden pixel (4,0)
        vec2 pixelSize = 2.0 / ScreenSize;
        vec2 base = vec2(-1.0) + vec2(pixel) * pixelSize;
        gl_Position = vec4(base + corners[gl_VertexID % 4] * pixelSize, 0.0, 1.0);

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
flat in int markerMode;  // 0=normal, 1=flash, 4=zoom, -1=stale flash

out vec4 fragColor;

void main() {
    if (markerMode != 0) {
        if (markerMode > 0) {
            // Fresh marker: write DETERMINISTIC sentinel values.
            // R=254/255 = signature, G=mode/255 = mode encoding, B=0, A=1.0
            // Alpha=1.0 is critical: prevents GPU blending from corrupting RGB.
            // classify.fsh reads these exact values via texelFetch.
            fragColor = vec4(254.0 / 255.0, float(markerMode) / 255.0, 0.0, 1.0);
        } else {
            // Stale marker (mode -1): write transparent to hide pixel.
            // Redirected to pixel (4,0) which classify never reads.
            discard;
        }
        return;
    }

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
CLASSIFY_FSH = """\
#version 330

uniform sampler2D ParticlesSampler;

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254

void main() {
    // Read the exact marker pixels — texelFetch = no UV math, no rounding error.
    ivec4 p1 = ivec4(round(texelFetch(ParticlesSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 p4 = ivec4(round(texelFetch(ParticlesSampler, ivec2(2, 0), 0) * 255.0));

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

    // Hide the exact marker pixels at (0,0) [flash] and (2,0) [zoom]
    vec4 particleColor = texture(ParticlesSampler, texCoord);
    float particleDepth = texture(ParticlesDepthSampler, texCoord).r;
    bool isMarkerPixel = (gl_FragCoord.y < 1.0) &&
        ((gl_FragCoord.x < 1.0) || (gl_FragCoord.x >= 2.0 && gl_FragCoord.x < 3.0));
    if (!isMarkerPixel) {
        try_insert(particleColor, particleDepth);
    }

    try_insert(texture(WeatherSampler, texCoord), texture(WeatherDepthSampler, texCoord).r);
    try_insert(texture(CloudsSampler,  texCoord), texture(CloudsDepthSampler,  texCoord).r);

    vec3 texelAccum = color_layers[0].rgb;
    for (int ii = 1; ii < active_layers; ++ii) {
        texelAccum = blend(texelAccum, color_layers[ii]);
    }
    fragColor = vec4(texelAccum.rgb, 1.0);

#if DEBUG
    if (gl_FragCoord.x < 50.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = pass 2 runs
    }
    // Diagnostic: is marker data present at expected pixel locations?
    // YELLOW = R=254 found (marker present), DARK GRAY = empty
    ivec4 dbgFlash = ivec4(round(texelFetch(ParticlesSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 dbgZoom  = ivec4(round(texelFetch(ParticlesSampler, ivec2(2, 0), 0) * 255.0));
    if (gl_FragCoord.x >= 150.0 && gl_FragCoord.x < 200.0 && gl_FragCoord.y < 50.0) {
        fragColor = (dbgFlash.r == 254) ? vec4(1.0, 1.0, 0.0, 1.0) : vec4(0.1, 0.1, 0.1, 1.0);
    }
    if (gl_FragCoord.x >= 200.0 && gl_FragCoord.x < 250.0 && gl_FragCoord.y < 50.0) {
        fragColor = (dbgZoom.r == 254) ? vec4(1.0, 1.0, 0.0, 1.0) : vec4(0.1, 0.1, 0.1, 1.0);
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
    if (gl_FragCoord.x >= 50.0 && gl_FragCoord.x < 100.0 && gl_FragCoord.y < 50.0) {
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
    if (gl_FragCoord.x >= 100.0 && gl_FragCoord.x < 150.0 && gl_FragCoord.y < 50.0) {
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
            # Pass 1: CLASSIFY - read exact marker pixels, output mode to 1x1 target
            {
                "vertex_shader":   "minecraft:core/screenquad",
                "fragment_shader": f"{ns}:post/classify",
                "inputs": [
                    {"sampler_name": "Particles", "target": "minecraft:particles"},
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
    # R=254.5/255, G=1.5/255 → "mid-bin" values survive floor truncation
    # entity_effect alpha decays; vsh only activates flash for A >= 230 (~2-5 ticks)
    write_versioned_function("player/fire_weapon",
"""
# Shader: spawn muzzle flash marker (mode 1)
# R=254.5/255, G=1.5/255, B=0 → particle.vsh places at pixel (0,0)
# Flash auto-expires via alpha decay check in vsh (~2-5 ticks)
execute at @s anchored eyes run particle minecraft:entity_effect{color:[0.99803922,0.00588235,0.0,1.0]} ^ ^ ^1 0 0 0 0 1 force @s
""")

    # ── Zoom marker: mode 4 ──
    # R=254.5/255, G=4.5/255 → "mid-bin" values survive floor truncation
    # Spawned every tick while ADS is active
    write_versioned_function("player/tick",
f"""
# Shader: spawn zoom marker (mode 4)
# R=254.5/255, G=4.5/255, B=0 → particle.vsh places at pixel (2,0)
execute if score @s {ns}.zoom matches 1 at @s anchored eyes run particle minecraft:entity_effect{{color:[0.99803922,0.01764706,0.0,1.0]}} ^ ^ ^1 0 0 0 0 1 force @s
""")

