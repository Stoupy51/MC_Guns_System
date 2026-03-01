#version 330

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec2 texCoord0;
in vec4 vertexColor;
flat in int markerMode;  // 0=normal, 1=flash, 3=zoom x3, 4=zoom x4

out vec4 fragColor;

#define DEBUG 1

void main() {
    if (markerMode > 0) {
        // The VSH places a small NDC quad at the bottom-left corner.
        // Both flash and zoom quads cover the same area.
        // We ONLY write the sentinel at the exact target pixel;
        // all other fragments are discarded to avoid overwriting scene.
        //   Flash    → pixel (0, 0)
        //   Zoom x2  → pixel (1, 0)  (G=2, no-scope center-only)
        //   Zoom x3  → pixel (1, 0)  (G=3)
        //   Zoom x4  → pixel (1, 0)  (G=4)
        ivec2 fc = ivec2(gl_FragCoord.xy);
        ivec2 target = (markerMode == 1) ? ivec2(0, 0) : ivec2(1, 0);
        if (fc != target) {
            discard;
        }
        // Write DETERMINISTIC sentinel: classify reads exact values.
        // R=254, G=mode(1/3/4), B=0, A=255 — immune to dust color randomization.
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
