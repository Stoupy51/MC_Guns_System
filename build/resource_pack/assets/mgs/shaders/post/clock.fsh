#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    vec4 clock = texture(ClockSampler, vec2(0.5));
    if (clock.a < 0.25) {
        fragColor = vec4(mgs_pack_time(GameTime), MGS_RUNNING);
        return;
    }
    fragColor = mgs_elapsed(clock, GameTime) > MGS_SETTLE_TICKS ? vec4(clock.rgb, 1.0) : clock;
}
