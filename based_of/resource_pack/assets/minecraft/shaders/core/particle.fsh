#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in float marker;
in vec2 texCoord0;
in vec2 scales;
in vec2 v0;
in vec2 v2;
in vec4 vertexColor;
in vec4 glpos;

out vec4 fragColor;

#define SIZETHRESH 0.006
#define MARKERS 5

void main() {
    float xpos = floor(round(gl_FragCoord.x * 2.0 / (glpos.x / glpos.w + 1.0)) / 2.0) + 0.5;
    if (marker > 0.0) {
        if (gl_FragCoord.y == 0.5 && gl_FragCoord.x == xpos && scales.x > 0.0 && scales.y > 0.0 && dot(abs(v0 / scales.x - v2 / scales.y), vec2(1.0)) < SIZETHRESH) {
            fragColor = vec4(vec3(marker / MARKERS), 0.01);
        } else {
            discard;
        }
    } else {
        vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
        if (color.a < 0.1 || gl_FragCoord.y == 0.5 && gl_FragCoord.x == xpos) {
            discard;
        }
        fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
    }
}
