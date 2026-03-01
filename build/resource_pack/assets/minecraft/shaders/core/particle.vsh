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
flat out int markerMode;  // 0=normal particle, 1=flash, 3=zoom x3, 4=zoom x4

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
int detectMarkerMode(vec4 color) {
    ivec4 ic = ivec4(round(color * 255.0));
    // Signature: R in [1-10] (very dim dust), B must be 0
    if (ic.r >= 1 && ic.r <= 10 && ic.b == 0) {
        if (ic.g == 0) return 1;                  // Flash: G is zero
        if (ic.g >= 1 && ic.g <= 7) return 3;     // Zoom x3: G from 0.02 → [2-5]
        if (ic.g >= 8 && ic.g <= 25) return 4;    // Zoom x4: G from 0.08 → [10-20]
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
