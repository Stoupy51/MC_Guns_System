#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform CrosshairConfig {
    vec2 Spread;     // movement level 0..4, at the start and at the end of the ramp
    float Duration;  // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    fragColor = texture(InSampler, texCoord);

    float spread = mix(Spread.x, Spread.y, mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration));

    // The HUD scale is not exposed to post shaders, so it is inferred from the window height the
    // same way vanilla picks its default: roughly 2 at 1080p, 3 at 1440p, 4 at 4K.
    vec2 inSize = vec2(textureSize(InSampler, 0));
    float guiScale = max(1.0, round(inSize.y / 540.0));

    int gap = int(round((1.5 + spread * 2.0) * guiScale));
    int armEnd = gap + int(round(3.0 * guiScale));
    int lineWidth = max(1, int(round(guiScale / 2.0)));

    ivec2 offset = ivec2(gl_FragCoord.xy) - ivec2(inSize) / 2;
    bool horizontal = abs(offset.y) < lineWidth && abs(offset.x) >= gap && abs(offset.x) <= armEnd;
    bool vertical = abs(offset.x) < lineWidth && abs(offset.y) >= gap && abs(offset.y) <= armEnd;
    if (horizontal || vertical) {
        fragColor.rgb = vec3(1.0) - fragColor.rgb;
    }
}
