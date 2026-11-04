#version 330
#extension GL_ARB_separate_shader_objects : require

#define MARKER_SPAN 0.5625

#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;
uniform sampler2D LensSampler;
uniform sampler2D ReticleSampler;
uniform sampler2D DepthSampler;

layout(std140) uniform SightConfig {
    vec2 Magnify;        // UV pull toward the centre, at the start and at the end of the ramp
    vec2 LensAlpha;      // lens opacity, at the start and at the end of its own window
    vec4 Lens;           // x = scope magnification divisor, y = lens radius (0 disables), z = barrel strength
    vec2 LensTicks;      // the lens cross-fades between these two ticks, apart from the magnification
    float Duration;      // ramp length in ticks
    float ReticleScale;  // side of the reticle over the side of the marker square
    float ReticleAlpha;  // 0 on the way out, where the held model draws its own reticle again
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

bool is_marker(vec3 color) {
    return color.r == 0.0 && (color.g == 0.0) != (color.b == 0.0) && max(color.g, color.b) >= 4.0 / 255.0;
}

vec2 unpack_marker(int marker) {
    vec4 packed = texelFetch(LensSampler, ivec2(marker, 0), 0);
    return packed.rb + packed.ga / 255.0;
}

// Premultiplied 3 x 3 average over the footprint of one screen pixel: the reticle is drawn several times smaller than its texture.
vec4 reticle_at(vec2 uv, vec2 footprint) {
    vec4 sum = vec4(0.0);
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vec4 texel = texture(ReticleSampler, uv + vec2(x, y) * footprint / 3.0);
            sum += vec4(texel.rgb * texel.a, texel.a);
        }
    }
    return sum.a > 0.0 ? vec4(sum.rgb / sum.a, sum.a / 9.0) : vec4(0.0);
}

void main() {
    vec4 clock = texture(ClockSampler, vec2(0.5));
    float magnify = mix(Magnify.x, Magnify.y, mgs_ramp(clock, GameTime, Duration));
    float lensAlpha = mix(LensAlpha.x, LensAlpha.y, smoothstep(LensTicks.x, LensTicks.y, mgs_elapsed(clock, GameTime)));

    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 source = mix(texCoord, vec2(0.5), magnify);
    fragColor = texture(InSampler, source);
    // A marker shows wherever no lens covers it, so the pixels beside it stand in.
    vec2 directions[4] = vec2[](vec2(1.0, 0.0), vec2(-1.0, 0.0), vec2(0.0, 1.0), vec2(0.0, -1.0));
    for (int i = 0; i < 4 && is_marker(fragColor.rgb); i++) {
        fragColor = texture(InSampler, source + directions[i] * 8.0 / inSize);
    }

    // The marker square in pixels of the unmagnified frame, signed to run from the blue texel to the green one.
    vec2 blue = unpack_marker(0) * inSize;
    vec2 green = unpack_marker(1) * inSize;
    vec2 square = (green - blue) / MARKER_SPAN;
    if (abs(square.x) < 2.0 || abs(square.y) < 2.0) return;
    vec2 centre = (blue + green) * 0.5;

    float aspectRatio = inSize.x / inSize.y;
    // The markers were found in the unmagnified frame: this is where the pull above puts their centre on screen.
    vec2 lensCentre = (centre / inSize - 0.5 * magnify) / (1.0 - magnify);
    vec2 screenCoord = (texCoord - lensCentre) * vec2(aspectRatio, 1.0);
    bool inLens = Lens.y > 0.0 && lensAlpha > 0.0 && length(screenCoord) < Lens.y;
    if (inLens) {
        // Always at full strength and faded as a whole: a weak barrel would squash the lens into one pixel.
        float d = length(screenCoord * Lens.z / Lens.y);
        float r = atan(d, sqrt(1.0 - d * d)) / 3.1415926535;
        float theta = atan(screenCoord.y, screenCoord.x);
        vec2 lensCoord = vec2(cos(theta), sin(theta)) * r / Lens.x;
        vec2 pixCoord = mix(lensCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5), vec2(0.5), magnify);
        fragColor = mix(fragColor, textureBicubic(InSampler, pixCoord, inSize), lensAlpha);
    }

    // Outside the lens the sight's body hides the reticle as it hid the reticle quad: the held item is the only depth at exactly 1.0.
    vec2 reticleSize = square * ReticleScale;
    vec2 uv = (source * inSize - centre) / reticleSize + 0.5;
    bool hidden = !inLens && texelFetch(DepthSampler, ivec2(source * inSize), 0).r == 1.0;
    if (hidden || any(lessThan(uv, vec2(0.0))) || any(greaterThan(uv, vec2(1.0)))) return;
    vec4 reticle = reticle_at(uv, (1.0 - magnify) / reticleSize);
    fragColor.rgb = mix(fragColor.rgb, reticle.rgb, reticle.a * ReticleAlpha);
}
