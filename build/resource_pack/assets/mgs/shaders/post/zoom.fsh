#version 330

uniform sampler2D InSampler;
uniform sampler2D ClassifySampler;
uniform sampler2D SparkTexSampler;

layout(std140) uniform ZoomConfig {
    float Distortion;
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 1
#define RADIUS 0.14

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
    int zoomLevel = int(round(classifyData.b * 255.0));  // 3 or 4 (from classify B channel)

    fragColor = texture(InSampler, texCoord);
    float aspectRatio = inSize.x / inSize.y;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

    // Apply barrel distortion if zooming (zoom level determines magnification)
    if (zoomMode && length(screenCoord) < RADIUS) {
        float Zoom = float(zoomLevel);  // 3.0 for _3 weapons, 4.0 for _4 weapons
        float d = length(screenCoord * Distortion / RADIUS);
        float z = sqrt(1.0 - d * d);
        float r = atan(d, z) / 3.1415926535;
        float theta = atan(screenCoord.y, screenCoord.x);

        screenCoord = vec2(cos(theta), sin(theta)) * r / Zoom;
        vec2 pixCoord = screenCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5);

        fragColor = textureBicubic(InSampler, pixCoord, inSize);
    }

    // Overlay flash spark texture AFTER zoom (spark is NOT barrel-distorted)
    // The 1536x1536 texture is a 3x3 grid of 9 different flash sprites.
    // Sprite is chosen pseudo-randomly from scene data each frame.
    if (flashMode) {
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
