#version 330

// Smooth zoom interpolation feedback loop.
// Reads FOV sentinel pixel directly from main framebuffer (spawned immediately on zoom).
// Separate from scope zoom markers (pixel 1,0) which are delayed 5 ticks.
uniform sampler2D MainSampler;
uniform sampler2D SmoothZoomSampler;  // Previous frame's smooth zoom (persistent feedback)

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254
#define ZOOM_LERP_SPEED 0.12  // Per-frame interpolation (~0.33s to 90% at 60fps)

void main() {
    // Read FOV sentinel at pixel (3, 0) - spawned immediately on zoom (no 5-tick delay)
    // R=254, G=mode(12-14), B=viewDist, A=255
    ivec4 pFov = ivec4(round(texelFetch(MainSampler, ivec2(3, 0), 0) * 255.0));
    bool fovActive = (pFov.r == MARKER_RED && pFov.a == 255
                      && pFov.g >= 12 && pFov.g <= 14);
    int fovZoomLevel = fovActive ? (pFov.g - 10) : 0;  // 2=center, 3=x3, 4=x4

    // 3rd person detection from sentinel B (camera-to-particle distance)
    float cameraDist = fovActive ? (float(pFov.b) / 255.0 * 10.0) : 0.0;
    bool thirdPerson = cameraDist > 2.0;

    // Target zoom magnification (UV scale toward center).
    // Higher = stronger FOV reduction (texCoord = mix(texCoord, 0.5, zoom)).
    //   0.0  = no magnification (normal FOV)
    //   0.25 = ~1.33x (center-only zoom, no scope)
    //   0.30 = ~1.43x (scope x3)
    //   0.45 = ~1.82x (scope x4)
    float targetZoom = 0.0;
    if (fovActive && !thirdPerson) {
        if (fovZoomLevel == 2) targetZoom = 0.25;       // Center-only: subtle
        else if (fovZoomLevel == 3) targetZoom = 0.30;   // Scope x3: moderate
        else if (fovZoomLevel == 4) targetZoom = 0.45;   // Scope x4: strong
    }

    float prevZoom = texture(SmoothZoomSampler, vec2(0.5, 0.5)).r;
    float smoothZoom = mix(prevZoom, targetZoom, ZOOM_LERP_SPEED);

    fragColor = vec4(smoothZoom, 0.0, 0.0, 1.0);
}
