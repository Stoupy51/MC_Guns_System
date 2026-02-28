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
