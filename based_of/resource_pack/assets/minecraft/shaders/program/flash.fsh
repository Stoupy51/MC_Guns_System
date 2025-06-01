/* Flash Shader
 * This shader creates a dynamic flash effect in Minecraft, simulating light sources with depth-based
 * intensity and blur effects. It uses both color and depth information to create realistic lighting
 * that respects the 3D environment.
 * 
 * Key features:
 * - Depth-based light attenuation
 * - Directional blur effect
 * - Configurable light color and intensity
 * - FOV-aware light projection
 * - Distance-based falloff
 */

#version 150
 
// Input textures for color and depth information
uniform sampler2D DiffuseSampler;      // Main color texture
uniform sampler2D DiffuseDepthSampler; // Depth buffer texture

// Configuration uniforms
uniform vec2 InSize;                   // Screen size in pixels
uniform vec3 Color;                    // Color of the flash effect
 
// Vertex shader inputs
in vec2 texCoord;                      // Current texture coordinates
in vec2 oneTexel;                      // Size of one texel (1.0/screenSize)
in float aspectRatio;                  // Screen aspect ratio
flat in float mode;                    // Effect mode (0 = off, >0 = on)

// Output color
out vec4 outColor;
 
// Shader configuration constants
#define INTENSITY 1.5                  // Overall intensity of the flash effect
#define MAXDIST 20.0                   // Maximum distance for the effect
#define NEAR 0.1                       // Near clipping plane
#define FAR 1536.0                     // Far clipping plane
#define BLURR 10.0                     // Blur radius in texels
#define FOV 70                         // Field of view in degrees
#define CK tan(FOV / 360.0 * 3.14159265358979) * 2.0  // FOV to screen space conversion factor

/**
 * Converts depth buffer value to linear depth in world space
 * @param depth The depth value from the depth buffer
 * @return Linear depth in world space units
 */
float LinearizeDepth(float depth) {
    float z = depth * 2.0 - 1.0;  // Convert from [0,1] to [-1,1]
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));    
}

void main() {
    // Get the base color from the main texture
    outColor = texture(DiffuseSampler, texCoord);

    // Only apply flash effect if mode is enabled
    if (mode > 0.0) {
        // Get and linearize the depth at current pixel
        float depth = LinearizeDepth(texture(DiffuseDepthSampler, texCoord).r);

        // Calculate screen-space coordinates adjusted for depth and FOV
        vec2 screenCoords = (texCoord - 0.5) * vec2(aspectRatio, 1.0) * CK * depth;
        float dist = length(vec3(screenCoords, depth));

        // Apply effect only within maximum distance
        if (dist < MAXDIST) {
            // Create a 5-point blur effect by sampling neighboring pixels
            vec4 blurColor = outColor
                           + texture(DiffuseSampler, texCoord + vec2(oneTexel.x * BLURR, 0.0)) 
                           + texture(DiffuseSampler, texCoord - vec2(oneTexel.x * BLURR, 0.0)) 
                           + texture(DiffuseSampler, texCoord + vec2(0.0, oneTexel.y * BLURR)) 
                           + texture(DiffuseSampler, texCoord - vec2(0.0, oneTexel.y * BLURR));
            blurColor /= 5.0;  // Average the blur samples

            // Calculate light color with distance-based falloff
            vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * Color;

            // Apply the flash effect with intensity modulation
            // First term: Base color modulation with blur-based intensity
            // Second term: Additional light contribution
            outColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9) * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0))  + vec3(1.0);
            outColor.rgb += INTENSITY * lightColor * 0.1;
        }
    }
    // Ensure full opacity in the output
    outColor = vec4(outColor.rgb, 1.0);
}