#version 330

uniform sampler2D InSampler;
uniform sampler2D ClassifySampler;
uniform sampler2D SparkTexSampler;
uniform sampler2D SmoothZoomSampler;  // Smooth FOV zoom factor (persistent feedback)

layout(std140) uniform ZoomConfig {
    float Distortion;
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 0
#define RADIUS_LEVEL_3 0.14
#define RADIUS_LEVEL_4 0.20

// Flash spark sprite sheet: 3x3 grid of 9 different flash sprites (1536x1536 total)
#define SPRITE_COUNT 9
#define SPRITE_SQRT 3

// Flash spark position & scale in screen-space coords:
//   screenCoord = (texCoord - 0.5) * vec2(aspectRatio, 1.0)
// When zooming: centered, slightly below center (muzzle at center of scope)
#define SPARK_POS_ZOOM   vec2(0.0, -0.125)
#define SPARK_SCALE_ZOOM vec2(0.6, 0.6)
// When NOT zooming: offset down-right (muzzle is off-center in hip fire)
#define SPARK_POS_NORMAL   vec2(0.085, -0.11)
#define SPARK_SCALE_NORMAL vec2(0.45, 0.45)

vec4 cubic(float v) {
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    float w = 6.0 - x - y - z;
    return vec4(x, y, z, w) * (1.0 / 6.0);
}

vec4 textureBicubic(sampler2D samp, vec2 texCoords, vec2 texSize) {
    vec2 oneTexel = 1.0 / texSize;
    texCoords = texCoords * texSize - 0.5;
    vec2 fxy = fract(texCoords);
    texCoords -= fxy;

    vec4 xcubic = cubic(fxy.x);
    vec4 ycubic = cubic(fxy.y);

    vec4 c = texCoords.xxyy + vec2(-0.5, 1.5).xyxy;
    vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
    vec4 offsetbc = c + vec4(xcubic.yw, ycubic.yw) / s;
    offsetbc *= oneTexel.xxyy;

    vec4 sample0 = texture(samp, offsetbc.xz);
    vec4 sample1 = texture(samp, offsetbc.yz);
    vec4 sample2 = texture(samp, offsetbc.xw);
    vec4 sample3 = texture(samp, offsetbc.yw);

    float sx = s.x / (s.x + s.y);
    float sy = s.z / (s.z + s.w);

    return mix(mix(sample3, sample2, sx), mix(sample1, sample0, sx), sy);
}

void main() {
    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec4 classifyData = texture(ClassifySampler, vec2(0.5, 0.5));
    bool flashMode = classifyData.r > 0.5;
    bool zoomMode  = classifyData.g > 0.5;
    int rawB = int(round(classifyData.b * 255.0));
    bool thirdPerson = rawB >= 128;  // 3rd person flag packed in high bit of B
    int zoomLevel = thirdPerson ? rawB - 128 : rawB;  // 0, 2, 3, or 4

    // Smooth FOV zoom: scales UV toward center for lower effective FOV
    // 0.0 = normal FOV, 0.15 = ~1.18x, 0.30 = ~1.43x, 0.45 = ~1.82x
    float smoothZoom = texture(SmoothZoomSampler, vec2(0.5, 0.5)).r;
    vec2 zoomedUV = (smoothZoom > 0.001) ? mix(texCoord, vec2(0.5), smoothZoom) : texCoord;

    fragColor = texture(InSampler, zoomedUV);
    float aspectRatio = inSize.x / inSize.y;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

    // Apply barrel distortion if zooming WITH a scope (zoomLevel 3 or 4 only)
    // zoomLevel 2 = zoomed but no scope: skip distortion, FOV reduction still applies above
    // Disabled in 3rd person (barrel distortion makes no sense from behind)
    if (zoomMode && !thirdPerson && ((zoomLevel == 3 && length(screenCoord) < RADIUS_LEVEL_3) || (zoomLevel == 4 && length(screenCoord) < RADIUS_LEVEL_4))) {
        float Zoom = float(zoomLevel);  // 3.0 for _3 weapons, 4.0 for _4 weapons
        float RadiusLevel = (zoomLevel == 3) ? RADIUS_LEVEL_3 : RADIUS_LEVEL_4;
        float d = length(screenCoord * Distortion / RadiusLevel);
        float z = sqrt(1.0 - d * d);
        float r = atan(d, z) / 3.1415926535;
        float theta = atan(screenCoord.y, screenCoord.x);

        screenCoord = vec2(cos(theta), sin(theta)) * r / Zoom;
        vec2 pixCoord = screenCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5);

        // Apply FOV zoom to distorted UV as well
        pixCoord = mix(pixCoord, vec2(0.5), smoothZoom);
        fragColor = textureBicubic(InSampler, pixCoord, inSize);
    }

    // Overlay flash spark texture AFTER zoom (spark is NOT barrel-distorted)
    // The 1536x1536 texture is a 3x3 grid of 9 different flash sprites.
    // Sprite is chosen pseudo-randomly from scene data each frame.
    // Disabled in 3rd person (spark texture overlay makes no sense from behind;
    // the flash bloom/lighting from flash.fsh still applies).
    if (flashMode && !thirdPerson) {
        // Choose position/scale: centered when also zooming, offset when hip-firing
        vec2 sparkPos   = zoomMode ? SPARK_POS_ZOOM   : SPARK_POS_NORMAL;
        vec2 sparkScale = zoomMode ? SPARK_SCALE_ZOOM  : SPARK_SCALE_NORMAL;

        // Bounding box in screen-space
        vec2 lb = sparkPos - sparkScale / 2.0;
        vec2 ub = sparkPos + sparkScale / 2.0;
        vec2 sd = sparkScale * float(SPRITE_SQRT);  // scale for one sprite cell

        // Pseudo-random sprite index (0-8) from scene content.
        // Using depth/color at fixed pixels as entropy — changes with camera position.
        float entropy = texelFetch(InSampler, ivec2(317, 211), 0).r
                      + texelFetch(InSampler, ivec2(211, 317), 0).g;
        int spriteIndex = int(mod(floor(entropy * 7919.0), float(SPRITE_COUNT)));
        vec2 spriteOffset = vec2(spriteIndex % SPRITE_SQRT, spriteIndex / SPRITE_SQRT) / float(SPRITE_SQRT);

        // Additive overlay within the spark bounding box
        if (screenCoord.x > lb.x && screenCoord.y > lb.y &&
            screenCoord.x < ub.x && screenCoord.y < ub.y) {
            fragColor += texture(SparkTexSampler, (screenCoord - lb) / sd + spriteOffset);
        }
    }

    // ── Custom crosshair (vanilla crosshair is transparent) ──
    // Draw a crosshair using color inversion (like vanilla) when NOT zooming.
    // The vanilla crosshair texture is replaced with a transparent one, so the shader
    // handles all crosshair rendering. Hidden during zoom for clean scope view.
    // Smooth spread (from classify A): 0.0=sneak → 1.0=jump, interpolated per-frame
    if (!zoomMode && false) {
        // Smooth spread value (0.0-1.0 from classify alpha, maps to levels 0-4)
        float smoothSpread = classifyData.a * 4.0;  // 0.0-4.0

        // GUI scale: approximate from screen height (~2 at 1080p, ~3 at 1440p, ~4 at 4K)
        float guiScale = max(1.0, round(inSize.y / 540.0));

        // Continuous gap/arm calculation with GUI scale
        // Level mapping: 0→tight(sneak), 1→base, 2→walk, 3→sprint, 4→jump(widest)
        float fGap = (1.5 + smoothSpread * 2.0) * guiScale;
        float fEnd = fGap + 3.0 * guiScale;
        int gap = int(round(fGap));
        int armEnd = int(round(fEnd));

        ivec2 center = ivec2(inSize) / 2;
        ivec2 fc = ivec2(gl_FragCoord.xy);
        int dx = fc.x - center.x;
        int dy = fc.y - center.y;

        // Horizontal arm: |y| within line width, |x| in [gap, armEnd]
        int lineWidth = max(1, int(round(guiScale / 2.0)));
        bool hArm = (abs(dy) < lineWidth) && (abs(dx) >= gap && abs(dx) <= armEnd);
        // Vertical arm: |x| within line width, |y| in [gap, armEnd]
        bool vArm = (abs(dx) < lineWidth) && (abs(dy) >= gap && abs(dy) <= armEnd);

        if (hArm || vArm) {
            // Invert colors at crosshair pixels (same visual effect as vanilla INVERT blend)
            fragColor.rgb = vec3(1.0) - fragColor.rgb;
        }
    }

#if DEBUG
    if (gl_FragCoord.x >= 100.0 && gl_FragCoord.x < 150.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        if (flashMode && zoomMode) {
            fragColor = vec4(1.0, 1.0, 1.0, 1.0);  // White: both detected
        } else if (flashMode) {
            fragColor = vec4(1.0, 0.5, 0.0, 1.0);  // Orange: flash only
        } else if (zoomMode) {
            fragColor = vec4(0.0, 1.0, 1.0, 1.0);  // Cyan: zoom only
        } else {
            fragColor = vec4(0.2, 0.2, 1.0, 1.0);  // Blue: no mode
        }
    }
#endif
}
