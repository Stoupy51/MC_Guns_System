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
    // Signature: R in [1-10] (very dim dust)
    if (ic.r >= 1 && ic.r <= 10) {
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
        } else if (ic.b >= 1 && ic.b <= 10) {
            // FOV markers: both G>0 AND B in dim range (immediate zoom FOV reduction)
            // Same G encoding as zoom but B=0.02 instead of 0 distinguishes them
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
