#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;
uniform sampler2D DepthSampler;
uniform sampler2D SparkSampler;

layout(std140) uniform FlashConfig {
    vec4 Color;      // rgb tint of the scene light, a = 1 to tint the sprite as Pack-a-Punch
    vec4 Spark;      // xy = sprite centre in screen space, zw = sprite size
    float Duration;  // ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

#define INTENSITY 1.5
#define MAXDIST 20.0
#define NEAR 0.1
#define FAR 1536.0
#define BLURR 10.0
#define FOV 70
#define CK tan(float(FOV) / 360.0 * 3.14159265358979) * 2.0
#define SPRITE_SQRT 3

// The depth buffer is reversed (cleared to 0, compared GREATER), so near is 1 and the sky is 0.
// Un-reverse before the classic perspective linearization, or the sky reads as point blank and the
// burst floods the whole screen.
float LinearizeDepth(float depth) {
    float z = (1.0 - depth) * 2.0 - 1.0;
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));
}

void main() {
    vec4 clock = texture(ClockSampler, vec2(0.5));
    fragColor = texture(InSampler, texCoord);

    // Decay to nothing well before the id is removed, so the burst is two frames rather than a tick.
    float life = 1.0 - clamp(mgs_elapsed(clock, GameTime) / Duration, 0.0, 1.0);
    if (life <= 0.0) return;

    vec2 inSize = vec2(textureSize(InSampler, 0));
    float aspectRatio = inSize.x / inSize.y;
    vec2 oneTexel = 1.0 / inSize;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

    float depth = LinearizeDepth(texture(DepthSampler, texCoord).r);
    float dist = length(vec3(screenCoord * CK * depth, depth));
    if (dist < MAXDIST) {
        vec4 blurColor = fragColor
            + texture(InSampler, texCoord + vec2(oneTexel.x * BLURR, 0.0))
            + texture(InSampler, texCoord - vec2(oneTexel.x * BLURR, 0.0))
            + texture(InSampler, texCoord + vec2(0.0, oneTexel.y * BLURR))
            + texture(InSampler, texCoord - vec2(0.0, oneTexel.y * BLURR));
        blurColor /= 5.0;

        vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * Color.rgb * life;
        fragColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9)
                       * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0)) + vec3(1.0);
        fragColor.rgb += INTENSITY * lightColor * 0.1;
    }

    // The sprite is picked from the activation stamp, so it stays the same sprite for the whole
    // burst instead of resampling scene entropy every frame.
    vec2 lb = Spark.xy - Spark.zw / 2.0;
    vec2 ub = Spark.xy + Spark.zw / 2.0;
    if (screenCoord.x > lb.x && screenCoord.y > lb.y && screenCoord.x < ub.x && screenCoord.y < ub.y) {
        float noise = fract(sin(mgs_unpack_time(clock.rgb) * 1237.0) * 43758.5453);
        int spriteIndex = int(floor(noise * 9.0));
        vec2 spriteOffset = vec2(spriteIndex % SPRITE_SQRT, spriteIndex / SPRITE_SQRT) / float(SPRITE_SQRT);
        vec4 sparkColor = texture(SparkSampler, (screenCoord - lb) / (Spark.zw * float(SPRITE_SQRT)) + spriteOffset);
        if (Color.a > 0.5) {
            sparkColor.rgb *= (noise > 0.5) ? vec3(0.85, 0.1, 1.0) : vec3(1.0, 0.1, 0.45);
        }
        fragColor += sparkColor * life;
    }

    fragColor.a = 1.0;
}
