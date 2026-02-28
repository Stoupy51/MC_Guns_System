#version 330

uniform sampler2D InSampler;        // "final" target (composited scene)
uniform sampler2D InDepthSampler;   // Main depth buffer
uniform sampler2D ClassifySampler;  // 1x1 "classify" target (contains mode)

// ── FlashConfig: tunable parameters from pipeline JSON ──
layout(std140) uniform FlashConfig {
    vec3 Color;  // Flash light color (default: warm [1.0, 0.8, 0.5])
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 1         // Set to 0 for production
#define MARKERS 5       // Must match classify.fsh
#define INTENSITY 1.5   // Overall flash brightness multiplier
#define MAXDIST 20.0    // Max world-space distance affected (blocks)
#define NEAR 0.1        // Camera near plane (blocks)
#define FAR 1536.0      // Camera far plane (blocks)
#define BLURR 10.0      // Blur sample offset in pixels
#define FOV 70          // Assumed field of view (degrees)
// CK converts texCoord offset -> view-space offset at depth=1
#define CK tan(float(FOV) / 360.0 * 3.14159265358979) * 2.0

// Convert depth buffer [0,1] -> linear world-space distance
float LinearizeDepth(float depth) {
    float z = depth * 2.0 - 1.0;  // [0,1] -> [-1,1] NDC
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));
}

void main() {
    // Get screen dimensions from texture (replaces SamplerInfo.InSize)
    vec2 inSize = vec2(textureSize(InSampler, 0));

    // Read mode from 1x1 classify target at its center
    float mode = round(texture(ClassifySampler, vec2(0.5, 0.5)).r * float(MARKERS));

    // Start with composited scene
    fragColor = texture(InSampler, texCoord);

    // Flash: activates for modes 1-3 (currently only mode 1 = red dust)
    if (mode >= 1.0 && mode <= 3.0) {
        vec2 oneTexel = 1.0 / inSize;
        float aspectRatio = inSize.x / inSize.y;

        // Linearize depth to world-space distance at this pixel
        float depth = LinearizeDepth(texture(InDepthSampler, texCoord).r);

        // Convert screen UV -> world-space XY at this depth
        vec2 screenCoords = (texCoord - 0.5) * vec2(aspectRatio, 1.0) * CK * depth;
        float dist = length(vec3(screenCoords, depth));

        if (dist < MAXDIST) {
            // 5-point cross blur (center + 4 cardinal neighbors)
            vec4 blurColor = fragColor
                + texture(InSampler, texCoord + vec2(oneTexel.x * BLURR, 0.0))
                + texture(InSampler, texCoord - vec2(oneTexel.x * BLURR, 0.0))
                + texture(InSampler, texCoord + vec2(0.0, oneTexel.y * BLURR))
                + texture(InSampler, texCoord - vec2(0.0, oneTexel.y * BLURR));
            blurColor /= 5.0;

            // Light intensity: inverse distance^1.5 falloff
            vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * Color;

            // Apply: modulate dark areas + attenuate bright areas + additive term
            fragColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9)
                           * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0)) + vec3(1.0);
            fragColor.rgb += INTENSITY * lightColor * 0.1;
        }
    }

    fragColor = vec4(fragColor.rgb, 1.0);

#if DEBUG
    // ── DEBUG: GREEN 50x50 square at bottom-left, offset x=50 ──
    // If you see this: the flash pass (pass 3) runs successfully.
    if (gl_FragCoord.x >= 50.0 && gl_FragCoord.x < 100.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = pass 3 runs
    }
#endif
}
