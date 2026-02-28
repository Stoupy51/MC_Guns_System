#version 330

uniform sampler2D ParticlesSampler;

in vec2 texCoord;
out vec4 fragColor;

#define MARKERS 5
#define MARKER_RED 254

void main() {
    // ── Read the exact marker pixels ──
    // Mode 1 (flash): placed at pixel (0, 0) by particle.vsh
    // Mode 4 (zoom):  placed at pixel (2, 0) by particle.vsh
    // texelFetch uses integer pixel coordinates — no UV math, no rounding error.
    ivec4 p1 = ivec4(round(texelFetch(ParticlesSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 p4 = ivec4(round(texelFetch(ParticlesSampler, ivec2(2, 0), 0) * 255.0));

    // ── Verify sentinel signature ──
    // R == MARKER_RED: our unique identifier
    // B == 0: part of signature (we never use B channel for anything else)
    // A == 255: confirms particle.fsh wrote it (not a stale clear value)
    // G == expected mode value: confirms this specific mode is active
    bool flashActive = (p1.r == MARKER_RED && p1.b == 0 && p1.a == 255 && p1.g == 1);
    bool zoomActive  = (p4.r == MARKER_RED && p4.b == 0 && p4.a == 255 && p4.g == 4);

    // Flash takes priority over zoom (can't do both at once)
    float mode = 0.0;
    if (flashActive)     mode = 1.0;
    else if (zoomActive) mode = 4.0;

    // Output: encode mode in red channel of the 1x1 target.
    // flash.fsh and zoom.fsh read it: round(texture(...).r * MARKERS)
    fragColor = vec4(mode / float(MARKERS), 0.0, 0.0, 1.0);
}
