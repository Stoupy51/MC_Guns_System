#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform HurtConfig {
    vec4 Tint;         // rgb tint, a = vignette strength at the screen edge
    vec2 Pulse;        // heartbeat amplitude, then its period in ticks
    vec2 Shape;        // where the vignette starts (0 centre, 1 edge), then rim desaturation
    vec2 Fade;         // overall strength at the start and at the end of the ramp
    float Aberration;  // radial colour separation at the rim
    float Duration;    // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// Lub-dub rather than a sine: two gaussian thumps, the second weaker and a fifth of a beat later.
float heartbeat(float phase) {
    float lub = exp(-pow(phase * 14.0, 2.0));
    float dub = exp(-pow((phase - 0.22) * 14.0, 2.0)) * 0.6;
    return lub + dub;
}

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float valueNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x), mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}

float fbm(vec2 p) {
    return valueNoise(p) * 0.55 + valueNoise(p * 2.1 + 17.0) * 0.30 + valueNoise(p * 4.3 + 41.0) * 0.15;
}

void main() {
    float strength = mix(Fade.x, Fade.y, mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration));
    float ticks = GameTime * 24000.0;
    float thump = Pulse.x * heartbeat(fract(ticks / Pulse.y)) * strength;

    // The beat moves the overlay itself rather than brightening it: the red edge surges inward on
    // each thump, and the whole frame jolts a hair toward the centre and dims, like a pulse behind the eyes.
    vec2 uv = mix(texCoord, vec2(0.5), 0.012 * thump);

    // A superellipse hugs the screen edges and corners instead of drawing a circle in the middle,
    // and slowly drifting noise breaks its outline into uneven tendrils creeping in from the rim.
    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 edge = abs(texCoord - 0.5) * 2.0;
    float rim = pow(pow(edge.x, 4.0) + pow(edge.y, 4.0), 0.25);
    float noise = fbm((texCoord - 0.5) * vec2(inSize.x / inSize.y, 1.0) * 3.5 + vec2(0.0, ticks * 0.004));
    float vignette = smoothstep(Shape.x - 0.3 * thump, 1.05, rim + (noise - 0.5) * 0.4) * strength;

    // Pulling the red channel outward and the blue inward reads as a stressed lens at the rim.
    vec3 color = texture(InSampler, uv).rgb;
    if (Aberration > 0.0) {
        vec2 shift = (texCoord - 0.5) * Aberration * 8.0 * vignette;
        color.r = texture(InSampler, uv + shift).r;
        color.b = texture(InSampler, uv - shift).b;
    }
    color *= 1.0 - 0.12 * thump;

    color = mix(color, vec3(dot(color, vec3(0.299, 0.587, 0.114))), clamp(Shape.y * vignette, 0.0, 1.0));
    color = mix(color, color * Tint.rgb + Tint.rgb * 0.35, clamp(Tint.a * vignette, 0.0, 1.0));
    fragColor = vec4(color, 1.0);
}
