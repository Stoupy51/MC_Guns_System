#version 330

uniform sampler2D InSampler;
uniform sampler2D InDepthSampler;
uniform sampler2D ClassifySampler;

layout(std140) uniform FlashConfig {
    vec3 Color;
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 1
#define INTENSITY 1.5
#define MAXDIST 20.0
#define NEAR 0.1
#define FAR 1536.0
#define BLURR 10.0
#define FOV 70
#define CK tan(float(FOV) / 360.0 * 3.14159265358979) * 2.0

float LinearizeDepth(float depth) {
    float z = depth * 2.0 - 1.0;
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));
}

void main() {
    vec2 inSize = vec2(textureSize(InSampler, 0));
    bool flashMode = texture(ClassifySampler, vec2(0.5, 0.5)).r > 0.5;

    fragColor = texture(InSampler, texCoord);

    if (flashMode) {
        vec2 oneTexel = 1.0 / inSize;
        float aspectRatio = inSize.x / inSize.y;

        float depth = LinearizeDepth(texture(InDepthSampler, texCoord).r);
        vec2 screenCoords = (texCoord - 0.5) * vec2(aspectRatio, 1.0) * CK * depth;
        float dist = length(vec3(screenCoords, depth));

        if (dist < MAXDIST) {
            vec4 blurColor = fragColor
                + texture(InSampler, texCoord + vec2(oneTexel.x * BLURR, 0.0))
                + texture(InSampler, texCoord - vec2(oneTexel.x * BLURR, 0.0))
                + texture(InSampler, texCoord + vec2(0.0, oneTexel.y * BLURR))
                + texture(InSampler, texCoord - vec2(0.0, oneTexel.y * BLURR));
            blurColor /= 5.0;

            vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * Color;

            fragColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9)
                           * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0)) + vec3(1.0);
            fragColor.rgb += INTENSITY * lightColor * 0.1;
        }
    }

    fragColor = vec4(fragColor.rgb, 1.0);

#if DEBUG
    if (gl_FragCoord.x >= 50.0 && gl_FragCoord.x < 100.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = pass 3 runs
    }
#endif
}
