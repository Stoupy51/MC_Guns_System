#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform ZoomConfig {
    vec2 Magnify;    // UV pull toward the centre, at the start and at the end of the ramp
    vec2 Barrel;     // lens distortion strength, at the start and at the end of the ramp
    vec2 Lens;       // x = scope magnification divisor, y = lens radius, 0 disables the lens
    float Duration;  // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

vec4 cubic(float v) {
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    return vec4(x, y, z, 6.0 - x - y - z) * (1.0 / 6.0);
}

vec4 textureBicubic(sampler2D samp, vec2 texCoords, vec2 texSize) {
    vec2 oneTexel = 1.0 / texSize;
    texCoords = texCoords * texSize - 0.5;
    vec2 fxy = fract(texCoords);
    texCoords -= fxy;

    vec4 xcubic = cubic(fxy.x);
    vec4 ycubic = cubic(fxy.y);

    vec4 c = texCoords.xxyy + vec2(-0.5, 1.5).xyxy;
    vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
    vec4 offsetbc = (c + vec4(xcubic.yw, ycubic.yw) / s) * oneTexel.xxyy;

    vec4 sample0 = texture(samp, offsetbc.xz);
    vec4 sample1 = texture(samp, offsetbc.yz);
    vec4 sample2 = texture(samp, offsetbc.xw);
    vec4 sample3 = texture(samp, offsetbc.yw);

    float sx = s.x / (s.x + s.y);
    float sy = s.z / (s.z + s.w);
    return mix(mix(sample3, sample2, sx), mix(sample1, sample0, sx), sy);
}

void main() {
    float t = mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration);
    float magnify = mix(Magnify.x, Magnify.y, t);
    float barrel = mix(Barrel.x, Barrel.y, t);

    fragColor = texture(InSampler, mix(texCoord, vec2(0.5), magnify));

    vec2 inSize = vec2(textureSize(InSampler, 0));
    float aspectRatio = inSize.x / inSize.y;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);
    if (Lens.y <= 0.0 || barrel <= 0.0 || length(screenCoord) >= Lens.y) return;

    float d = length(screenCoord * barrel / Lens.y);
    float r = atan(d, sqrt(1.0 - d * d)) / 3.1415926535;
    float theta = atan(screenCoord.y, screenCoord.x);
    vec2 lensCoord = vec2(cos(theta), sin(theta)) * r / Lens.x;
    vec2 pixCoord = mix(lensCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5), vec2(0.5), magnify);
    fragColor = textureBicubic(InSampler, pixCoord, inSize);
}
