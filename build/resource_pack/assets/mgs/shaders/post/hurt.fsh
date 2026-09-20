#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform HurtConfig {
    vec4 Tint;         // rgb tint, a = vignette strength at the screen edge
    vec2 Pulse;        // heartbeat amplitude, then its period in ticks
    vec2 Shape;        // radius where the vignette starts, then rim desaturation
    float Aberration;  // radial colour separation at the rim
    float Duration;    // fade-in length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// Lub-dub rather than a sine: two gaussian thumps, the second weaker and a fifth of a beat later.
float heartbeat(float phase) {
    float lub = exp(-pow(phase * 14.0, 2.0));
    float dub = exp(-pow((phase - 0.22) * 14.0, 2.0)) * 0.6;
    return lub + dub;
}

void main() {
    float t = mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration);
    float beat = 1.0 + Pulse.x * heartbeat(fract(GameTime * 24000.0 / Pulse.y));

    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 fromCentre = (texCoord - 0.5) * vec2(inSize.x / inSize.y, 1.0);
    float vignette = smoothstep(Shape.x, 0.75, length(fromCentre)) * t * beat;

    // Pulling the red channel outward and the blue inward reads as a stressed lens at the rim.
    vec3 color = texture(InSampler, texCoord).rgb;
    if (Aberration > 0.0) {
        vec2 shift = fromCentre * Aberration * vignette;
        color.r = texture(InSampler, texCoord + shift).r;
        color.b = texture(InSampler, texCoord - shift).b;
    }

    color = mix(color, vec3(dot(color, vec3(0.299, 0.587, 0.114))), Shape.y * vignette);
    color = mix(color, color * Tint.rgb + Tint.rgb * 0.35, clamp(Tint.a * vignette, 0.0, 1.0));
    fragColor = vec4(color, 1.0);
}
