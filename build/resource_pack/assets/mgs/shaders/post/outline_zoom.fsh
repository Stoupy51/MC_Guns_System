#version 330

// Applies the SAME view transform as zoom.fsh to the glow outline buffer.
// GameRenderer.render() composites the outline onto the screen (blitEntityOutline) AFTER
// renderLevel(), i.e. after the transparency chain has already zoomed/distorted the scene —
// so without this pass glowing entities keep their unzoomed outline while the entity itself
// is warped by the zoom. The outline post chain is allowed to read minecraft:main
// (LevelTargetBundle.OUTLINE_TARGETS = {main, entity_outline}), which is where the sentinel
// pixels live, so the zoom state is read straight from the sentinels here.
uniform sampler2D InSampler;          // blurred outline buffer (swap)
uniform sampler2D MainSampler;        // real main target: sentinel pixels
uniform sampler2D SmoothZoomSampler;  // this chain's own smoothed FOV zoom (persistent)

layout(std140) uniform ZoomConfig {
    float Distortion;
};

in vec2 texCoord;
out vec4 fragColor;

#define MARKER_RED 254
#define RADIUS_LEVEL_3 0.14
#define RADIUS_LEVEL_4 0.20

void main() {
    vec2 inSize = vec2(textureSize(InSampler, 0));

    // Scope zoom sentinel at pixel (1,0): G = zoom level (2/3/4), B = camera distance.
    // Same source and timing as classify.fsh, so the outline distortion kicks in on the
    // exact frame the scene distortion does (after the 5-tick scope delay).
    ivec4 p4 = ivec4(round(texelFetch(MainSampler, ivec2(1, 0), 0) * 255.0));
    bool zoomActive = (p4.r == MARKER_RED && p4.a == 255 && p4.g >= 2 && p4.g <= 4);
    int zoomLevel = zoomActive ? p4.g : 0;
    bool notFirstPerson = zoomActive && (float(p4.b) / 255.0 * 10.0) > 1.0;

    // Same smooth FOV zoom as zoom.fsh (own feedback loop, same lerp speed & input)
    float smoothZoom = texture(SmoothZoomSampler, vec2(0.5, 0.5)).r;
    vec2 zoomedUV = (smoothZoom > 0.1) ? mix(texCoord, vec2(0.5), smoothZoom) : texCoord;

    fragColor = texture(InSampler, zoomedUV);

    float aspectRatio = inSize.x / inSize.y;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

    // Same barrel distortion as zoom.fsh (scope levels 3/4, 1st person only)
    if (zoomActive && !notFirstPerson && ((zoomLevel == 3 && length(screenCoord) < RADIUS_LEVEL_3) || (zoomLevel == 4 && length(screenCoord) < RADIUS_LEVEL_4))) {
        float Zoom = float(zoomLevel);
        float RadiusLevel = (zoomLevel == 3) ? RADIUS_LEVEL_3 : RADIUS_LEVEL_4;
        float d = length(screenCoord * Distortion / RadiusLevel);
        float z = sqrt(1.0 - d * d);
        float r = atan(d, z) / 3.1415926535;
        float theta = atan(screenCoord.y, screenCoord.x);

        screenCoord = vec2(cos(theta), sin(theta)) * r / Zoom;
        vec2 pixCoord = screenCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5);
        pixCoord = mix(pixCoord, vec2(0.5), smoothZoom);
        fragColor = texture(InSampler, pixCoord);
    }
}
