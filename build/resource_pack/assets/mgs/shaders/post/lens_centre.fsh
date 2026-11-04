#version 330
#extension GL_ARB_separate_shader_objects : require

#define GRID 32

// The markers are looked for in a centred square three quarters of the screen high, cut into GRID x GRID blocks.
int lens_block(ivec2 inSize) {
    return (inSize.y * 3 / 4 + GRID - 1) / GRID;
}

ivec2 lens_origin(ivec2 inSize) {
    return inSize / 2 - GRID / 2 * lens_block(inSize);
}

uniform sampler2D BlocksSampler;
uniform sampler2D PreviousSampler;
uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// Pixel 0 holds the blue marker and pixel 1 the green one, in screen UV, x in rg and y in ba, 16 bits each.
// A frame without the marker (a muzzle flash over it, a dark cave) keeps the last position.
void main() {
    int marker = int(gl_FragCoord.x);
    vec2 sum = vec2(0.0);
    float weight = 0.0;
    for (int y = 0; y < GRID; y++) {
        for (int x = 0; x < GRID; x++) {
            vec4 cell = texelFetch(BlocksSampler, ivec2(x + marker * GRID, y), 0);
            sum += (vec2(x, y) + cell.rg) * cell.a;
            weight += cell.a;
        }
    }
    if (weight == 0.0) {
        fragColor = texelFetch(PreviousSampler, ivec2(marker, 0), 0);
        return;
    }

    ivec2 inSize = textureSize(InSampler, 0);
    vec2 uv = (vec2(lens_origin(inSize)) + sum / weight * float(lens_block(inSize))) / vec2(inSize);
    vec2 high = floor(uv * 255.0) / 255.0;
    vec2 low = fract(uv * 255.0);
    fragColor = vec4(high.x, low.x, high.y, low.y);
}
