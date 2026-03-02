#version 330

// Dust is OPAQUE → renders to minecraft:main (not minecraft:particles).
// ParticleFeatureRenderer.renderSolid() targets the main framebuffer.
uniform sampler2D MainSampler;
uniform sampler2D SmoothSpreadSampler;  // Previous frame's smooth spread (persistent feedback)

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254
#define SPREAD_LERP_SPEED 0.15  // Per-frame interpolation (~10 frames for 90% convergence at 60fps)

void main() {
    // Read the exact sentinel pixels from MAIN (where opaque dust renders).
    // texelFetch = no UV math, no rounding error.
    // Flash sentinel at pixel (0, 0), zoom sentinel at pixel (1, 0)
    ivec4 p1 = ivec4(round(texelFetch(MainSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 p4 = ivec4(round(texelFetch(MainSampler, ivec2(1, 0), 0) * 255.0));

    // Sentinel: R == MARKER_RED, A == 255, G == expected mode value
    // B now encodes camera-to-particle distance (not checked for detection)
    bool flashActive = (p1.r == MARKER_RED && p1.a == 255 && p1.g == 1);
    bool zoomActive  = (p4.r == MARKER_RED && p4.a == 255 && (p4.g == 2 || p4.g == 3 || p4.g == 4));
    int zoomLevel = zoomActive ? p4.g : 0;  // 2=center-only, 3=x3 scope, 4=x4 scope

    // 3rd person detection from sentinel B (camera-to-particle distance)
    // B = clamp(viewDist / 10.0): ~0.1 in 1st person, ~0.5 in 3rd person
    float cameraDist = 0.0;
    if (flashActive) cameraDist = max(cameraDist, float(p1.b) / 255.0 * 10.0);
    if (zoomActive)  cameraDist = max(cameraDist, float(p4.b) / 255.0 * 10.0);
    bool thirdPerson = cameraDist > 2.0;  // Threshold: >2 blocks from camera → 3rd person

    // Spread (crosshair) sentinel at pixel (2, 0)
    ivec4 p_spread = ivec4(round(texelFetch(MainSampler, ivec2(2, 0), 0) * 255.0));
    bool spreadActive = (p_spread.r == MARKER_RED && p_spread.a == 255
                         && p_spread.g >= 5 && p_spread.g <= 9);
    int spreadLevel = spreadActive ? (p_spread.g - 5) : 1;  // 0-4, default 1 (base)

    // Smooth interpolation: read previous frame's smooth spread from persistent buffer
    float prevSmooth = texture(SmoothSpreadSampler, vec2(0.5, 0.5)).r;
    float targetSpread = float(spreadLevel) / 4.0;  // Normalize to [0.0, 1.0] for 8-bit precision
    float smoothSpread = mix(prevSmooth, targetSpread, SPREAD_LERP_SPEED);

    // R = flash, G = zoom, B = (zoomLevel + thirdPerson*128) / 255, A = smooth spread.
    // flash.fsh reads R, zoom.fsh reads G, B (with 3rd person flag), and A.
    fragColor = vec4(
        flashActive ? 1.0 : 0.0,
        zoomActive ? 1.0 : 0.0,
        float(zoomLevel + (thirdPerson ? 128 : 0)) / 255.0,
        smoothSpread
    );
}
