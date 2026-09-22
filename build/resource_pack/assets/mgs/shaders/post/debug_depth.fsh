#version 330
#extension GL_ARB_separate_shader_objects : require

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// Magenta: exactly 1.0, the gun as marked by the integrate_depth override.
// Yellow: closer than a tenth of a block, where a shaderpack that squashes hand depth would put the gun.
// Blue: nothing written (sky). Grey: world distance, white near and black at 64 blocks.
void main() {
    float depth = texelFetch(DepthSampler, ivec2(texCoord * vec2(textureSize(InSampler, 0))), 0).r;
    float blocks = 0.05 / max(depth, 1.0e-6);
    vec3 shade = vec3(1.0 - clamp(blocks / 64.0, 0.0, 1.0));
    fragColor = vec4(depth >= 1.0 ? vec3(1.0, 0.0, 1.0) : depth <= 0.0 ? vec3(0.1, 0.2, 0.6) : blocks < 0.1 ? vec3(1.0, 1.0, 0.0) : shade, 1.0);
}
