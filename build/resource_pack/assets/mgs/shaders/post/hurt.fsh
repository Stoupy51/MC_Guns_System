#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform HurtConfig {
    vec4 TintFrom;         // rgb tint, a = vignette strength at the screen edge
    vec4 TintTo;
    vec4 Shape;            // xy = look being left (vignette start, rim desaturation), zw = look being reached
    vec4 PulseAberration;  // xy = heartbeat strength from, to; zw = colour split from, to
    float Duration;        // ticks the blend takes
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

#define HEARTBEAT_TICKS 16.0
#define JOLT_ZOOM 0.02   // how far the frame is pulled toward the centre on a full-strength beat
#define JOLT_DIM 0.20    // how much it darkens on that beat

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
    float t = mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration);
    vec4 tint = mix(TintFrom, TintTo, t);
    vec2 shape = mix(Shape.xy, Shape.zw, t);
    float aberration = mix(PulseAberration.z, PulseAberration.w, t);

    // The beat moves the overlay itself rather than brightening it: the red edge surges inward on
    // each thump, and the whole frame jolts a hair toward the centre and dims, like a pulse behind the eyes.
    float ticks = GameTime * 24000.0;
    float thump = mix(PulseAberration.x, PulseAberration.y, t) * heartbeat(fract(ticks / HEARTBEAT_TICKS));
    vec2 uv = mix(texCoord, vec2(0.5), JOLT_ZOOM * thump);

    // A superellipse hugs the screen edges and corners instead of drawing a circle in the middle,
    // and slowly drifting noise breaks its outline into uneven tendrils creeping in from the rim.
    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 edge = abs(texCoord - 0.5) * 2.0;
    float rim = pow(pow(edge.x, 4.0) + pow(edge.y, 4.0), 0.25);
    float noise = fbm((texCoord - 0.5) * vec2(inSize.x / inSize.y, 1.0) * 3.5 + vec2(0.0, ticks * 0.004));
    float vignette = smoothstep(shape.x - 0.3 * thump, 1.05, rim + (noise - 0.5) * 0.4);

    // Pulling the red channel outward and the blue inward reads as a stressed lens at the rim.
    vec3 color = texture(InSampler, uv).rgb;
    if (aberration > 0.0) {
        vec2 shift = (texCoord - 0.5) * aberration * 8.0 * vignette;
        color.r = texture(InSampler, uv + shift).r;
        color.b = texture(InSampler, uv - shift).b;
    }
    color *= 1.0 - JOLT_DIM * thump;

    color = mix(color, vec3(dot(color, vec3(0.299, 0.587, 0.114))), clamp(shape.y * vignette, 0.0, 1.0));
    color = mix(color, color * tint.rgb + tint.rgb * 0.35, clamp(tint.a * vignette, 0.0, 1.0));
    fragColor = vec4(color, 1.0);
}
