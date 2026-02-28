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
