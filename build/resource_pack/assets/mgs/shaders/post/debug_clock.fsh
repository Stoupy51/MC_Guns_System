#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    fragColor = texture(InSampler, texCoord);
    vec4 clock = texture(ClockSampler, vec2(0.5));

    // Bottom strip (texCoord.y grows upward): red if the clock never armed, green while running, blue once settled.
    // Its width is the elapsed time, one tenth of the screen per tick, so a stuck clock is obvious at a glance.
    if (texCoord.y < 0.03) {
        float ticks = mgs_elapsed(clock, GameTime);
        fragColor = clock.a < 0.25 ? vec4(1.0, 0.0, 0.0, 1.0) : clock.a > 0.75 ? vec4(0.0, 0.0, 1.0, 1.0) : vec4(0.0, 1.0, 0.0, 1.0);
        if (texCoord.x > fract(ticks / 10.0)) fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
}
