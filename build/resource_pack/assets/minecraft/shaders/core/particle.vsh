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
