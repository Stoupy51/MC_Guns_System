#version 330

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec2 texCoord0;
in vec4 vertexColor;
flat in int markerMode;  // 0=normal, 1=flash, 2-4=zoom, 5-9=spread

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
        ivec2 fc = ivec2(gl_FragCoord.xy);
        ivec2 target;
        if (markerMode == 1) target = ivec2(0, 0);       // Flash
        else if (markerMode >= 5) target = ivec2(2, 0);  // Spread
        else target = ivec2(1, 0);                        // Zoom (2, 3, 4)
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
