#version 330

uniform sampler2D ParticlesSampler;

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254

void main() {
    // Read the exact marker pixels — texelFetch = no UV math, no rounding error.
    ivec4 p1 = ivec4(round(texelFetch(ParticlesSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 p4 = ivec4(round(texelFetch(ParticlesSampler, ivec2(2, 0), 0) * 255.0));

    // Sentinel: R == MARKER_RED, B == 0, A == 255, G == expected mode value
    bool flashActive = (p1.r == MARKER_RED && p1.b == 0 && p1.a == 255 && p1.g == 1);
    bool zoomActive  = (p4.r == MARKER_RED && p4.b == 0 && p4.a == 255 && p4.g == 4);

    // Independent channels: both can be active simultaneously.
    // R = flash, G = zoom. flash.fsh reads R, zoom.fsh reads G.
    fragColor = vec4(flashActive ? 1.0 : 0.0, zoomActive ? 1.0 : 0.0, 0.0, 1.0);
}
