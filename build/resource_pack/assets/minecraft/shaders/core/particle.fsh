#version 330

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec2 texCoord0;
in vec4 vertexColor;
flat in int isMarker;
flat in ivec4 iColor;

out vec4 fragColor;

void main() {
    if (isMarker == 1) {
        // ── MARKER SENTINEL ──
        // Write exact R, G, B from original particle color.
        // Force alpha = 255/255 = 1.0 so the framebuffer stores exactly
        // what we write (no blending corruption regardless of blend equation).
        // classify.fsh will read this pixel and verify R==254, B==0, A==255.
        fragColor = vec4(float(iColor.r), float(iColor.g), float(iColor.b), 255.0) / 255.0;
        return;
    }

    // ── NORMAL PARTICLE RENDERING (vanilla behavior) ──
    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
    if (color.a < 0.1) {
        discard;
    }
    fragColor = apply_fog(color, sphericalVertexDistance, cylindricalVertexDistance,
        FogEnvironmentalStart, FogEnvironmentalEnd,
        FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
}
