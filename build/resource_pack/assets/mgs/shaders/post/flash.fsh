#version 330

uniform sampler2D InSampler;
uniform sampler2D InDepthSampler;
uniform sampler2D ClassifySampler;

layout(std140) uniform FlashConfig {
    vec3 Color;
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 0
#define INTENSITY 1.5
#define MAXDIST 20.0
#define NEAR 0.1
#define FAR 1536.0
#define BLURR 10.0
#define FOV 70
#define CK tan(float(FOV) / 360.0 * 3.14159265358979) * 2.0
#define PAP_COLOR vec3(0.6, 0.0, 1.0)

float LinearizeDepth(float depth) {
    // 26.2 uses a REVERSED-Z depth buffer (near = 1.0, far/sky = 0.0). Un-reverse it back to
    // forward-Z (near = 0.0, far = 1.0) so the classic perspective linearization below is valid.
    // Without this, the sky (depth 0.0) linearizes to ~near and the muzzle flash floods the whole
    // screen instead of lighting only nearby blocks.
    depth = 1.0 - depth;
    float z = depth * 2.0 - 1.0;
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));
}

void main() {
    vec2 inSize = vec2(textureSize(InSampler, 0));
    float classifyR = texture(ClassifySampler, vec2(0.5, 0.5)).r;
    bool flashMode = classifyR > 0.5;
    bool papFlash  = flashMode && (classifyR < 0.85);
    vec3 flashColor = papFlash ? PAP_COLOR : Color;

    fragColor = texture(InSampler, texCoord);

    if (flashMode) {
        float aspectRatio = inSize.x / inSize.y;
        vec2 oneTexel = 1.0 / inSize;

        // Depth-based light/bloom effect
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

            vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * flashColor;

            fragColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9)
                           * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0)) + vec3(1.0);
            fragColor.rgb += INTENSITY * lightColor * 0.1;
        }
    }

    fragColor = vec4(fragColor.rgb, 1.0);

#if DEBUG
    if (gl_FragCoord.x >= 50.0 && gl_FragCoord.x < 100.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = pass 3 runs
    }
#endif
}
