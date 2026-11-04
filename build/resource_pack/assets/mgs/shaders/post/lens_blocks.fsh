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

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// The left GRID columns look for the blue marker, the right ones for the green one.
// rg = mean marker position inside the block, a = share of the block it covers.
void main() {
    ivec2 cell = ivec2(gl_FragCoord.xy);
    int channel = cell.x < GRID ? 2 : 1;
    ivec2 inSize = textureSize(InSampler, 0);
    int block = lens_block(inSize);
    ivec2 start = lens_origin(inSize) + ivec2(cell.x % GRID, cell.y) * block;

    vec2 sum = vec2(0.0);
    float count = 0.0;
    for (int y = 0; y < block; y++) {
        for (int x = 0; x < block; x++) {
            vec3 color = texelFetch(InSampler, start + ivec2(x, y), 0).rgb;
            // The floor keeps the scope's own near-black shading from passing for a marker.
            if (color.r == 0.0 && color[3 - channel] == 0.0 && color[channel] >= 4.0 / 255.0) {
                sum += vec2(x, y) + 0.5;
                count += 1.0;
            }
        }
    }
    fragColor = count > 0.0 ? vec4(sum / (count * float(block)), 0.0, max(count / float(block * block), 1.0 / 255.0)) : vec4(0.0);
}
