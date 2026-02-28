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
