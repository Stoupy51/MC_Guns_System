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
