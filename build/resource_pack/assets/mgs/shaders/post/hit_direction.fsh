#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform HitConfig {
    float Direction;  // degrees clockwise from the top of the screen
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

#define COLOR vec3(1.0, 0.165, 0.165)
#define FULL 8.0
#define FADE_END 14.0
#define SPAN 90.0
#define RADIUS 0.14
#define WIDTH 0.014

void main() {
    fragColor = texture(InSampler, texCoord);

    float life = clamp((FADE_END - clock_elapsed(texture(ClockSampler, vec2(0.5)), GameTime)) / (FADE_END - FULL), 0.0, 1.0);
    if (life <= 0.0) return;

    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 offset = (texCoord - 0.5) * vec2(inSize.x / inSize.y, 1.0);

    // Wrapped into -180..180 so the seam behind the player fades instead of cutting.
    float delta = abs(mod(degrees(atan(offset.x, offset.y)) - Direction + 180.0, 360.0) - 180.0);
    float along = clamp(1.0 - delta / (SPAN / 2.0), 0.0, 1.0);

    // Solid core with soft edges: 2.5 widens the plateau so the ring keeps its thickness.
    float across = clamp((1.0 - abs(length(offset) - RADIUS) / (WIDTH / 2.0)) * 2.5, 0.0, 1.0);

    fragColor.rgb = mix(fragColor.rgb, COLOR, along * across * life);
}
