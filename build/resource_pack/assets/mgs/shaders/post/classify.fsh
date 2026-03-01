#version 330

// Dust is OPAQUE → renders to minecraft:main (not minecraft:particles).
// ParticleFeatureRenderer.renderSolid() targets the main framebuffer.
uniform sampler2D MainSampler;

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254

void main() {
    // Read the exact sentinel pixels from MAIN (where opaque dust renders).
    // texelFetch = no UV math, no rounding error.
    // Flash sentinel at pixel (0, 0), zoom sentinel at pixel (1, 0)
    ivec4 p1 = ivec4(round(texelFetch(MainSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 p4 = ivec4(round(texelFetch(MainSampler, ivec2(1, 0), 0) * 255.0));

    // Sentinel: R == MARKER_RED, B == 0, A == 255, G == expected mode value
    bool flashActive = (p1.r == MARKER_RED && p1.b == 0 && p1.a == 255 && p1.g == 1);
    bool zoomActive  = (p4.r == MARKER_RED && p4.b == 0 && p4.a == 255 && (p4.g == 2 || p4.g == 3 || p4.g == 4));
    int zoomLevel = zoomActive ? p4.g : 0;  // 2=center-only, 3=x3 scope, 4=x4 scope

    // R = flash, G = zoom, B = zoom level (3 or 4) / 255.
    // flash.fsh reads R, zoom.fsh reads G and B.
    fragColor = vec4(
        flashActive ? 1.0 : 0.0,
        zoomActive ? 1.0 : 0.0,
        float(zoomLevel) / 255.0,
        1.0
    );
}
