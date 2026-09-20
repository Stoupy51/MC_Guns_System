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

    // Bottom strip: green while the clock is armed, red if it never armed. Its width is the
    // elapsed time, one tenth of the screen per tick, so a stuck clock is obvious at a glance.
    if (texCoord.y > 0.97) {
        float ticks = mgs_elapsed(clock, GameTime);
        fragColor = vec4(clock.a < 0.5 ? 1.0 : 0.0, clock.a < 0.5 ? 0.0 : 1.0, 0.0, 1.0);
        if (texCoord.x > fract(ticks / 10.0)) fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
}
