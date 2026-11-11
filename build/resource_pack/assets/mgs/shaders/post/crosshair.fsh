#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform CrosshairConfig {
    vec2 Spread;     // level 0..5, at the start and at the end of the ramp
    float Duration;  // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    fragColor = texture(InSampler, texCoord);

    // The HUD scale is not exposed to post shaders, so it is inferred from the window height the
    // same way vanilla picks its default: roughly 2 at 1080p, 3 at 1440p, 4 at 4K.
    vec2 inSize = vec2(textureSize(InSampler, 0));
    float guiScale = max(1.0, round(inSize.y / 540.0));

    // The vanilla sprite: a 9 px plus whose centre is texel 7 of a 15 px sprite blitted at ((guiWidth - 15) / 2, (guiHeight - 15) / 2).
    if (Spread.y > 4.5) {
        ivec2 guiSize = ivec2(ceil(inSize / guiScale));
        ivec2 guiPixel = ivec2(gl_FragCoord.xy / guiScale);
        guiPixel.y = guiSize.y - 1 - guiPixel.y;
        ivec2 d = abs(guiPixel - ((guiSize - 15) / 2 + 7));
        if (min(d.x, d.y) == 0 && max(d.x, d.y) <= 4) fragColor.rgb = vec3(1.0) - fragColor.rgb;
        return;
    }

    float start = Spread.x > 4.5 ? Spread.y : Spread.x;
    float spread = mix(start, Spread.y, clock_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration));

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
