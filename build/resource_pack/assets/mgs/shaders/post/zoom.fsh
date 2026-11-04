#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform IronConfig {
    vec2 Magnify;    // UV pull toward the centre, at the start and at the end of the ramp
    float Duration;  // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    float magnify = mix(Magnify.x, Magnify.y, mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration));
    fragColor = texture(InSampler, mix(texCoord, vec2(0.5), magnify));
}
