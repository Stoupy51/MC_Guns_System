#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in float fogVertexDistance;
in float reticle;
in float yoffset;
in vec4 vertexColor;
in vec2 texCoord0;
in vec2 texCoord1;
in vec3 normal;
in vec4 gpos;
in vec4 ruv;

out vec4 fragColor;

#define RSCREENSIZE 16.0
#define RSCREENSIZEL 1.5
#define RADIUS 0.14
#define SHADOWSCALE 1.0 / RADIUS / RSCREENSIZEL / 2.0

void main() {
    vec4 color;
    float normdev = length(normal.xyz - vec3(0.0, 0.0, -1.0));
    if (abs(reticle - 1.0) <= 0.000001) {
        vec2 screenSize = round(gl_FragCoord.xy * 2.0 / (gpos.xy + 1.0));
        vec2 uv = (ruv.xy + ruv.zw) * 0.5 + RSCREENSIZE * 2.0 * (gl_FragCoord.xy - 0.5 * screenSize) / vec2(screenSize.y) * (ruv.zw - ruv.xy) * vec2(1.0, -1.0);
        if (vertexDistance < 1.2 && normdev < 0.15 && uv.x > ruv.x && uv.x < ruv.z && uv.y > ruv.y && uv.y < ruv.w) {
            uv.y -= yoffset;
            color = texture(Sampler0, uv);
            color.a *= clamp((0.15 - normdev) * 8.0, 0.0, 1.0) * clamp((1.2 - vertexDistance) * 5.0, 0.0, 1.0);
        } else {
            color = vec4(0.0);
        }
        if (color.a < 0.1) {
            discard;
        }
    } else if (abs(reticle + 1.0) <= 0.000001){
        vec2 screenSize = round(gl_FragCoord.xy * 2.0 / (gpos.xy + 1.0));
        vec2 offset = RSCREENSIZEL * 2.0 * (gl_FragCoord.xy - 0.5 * screenSize) / vec2(screenSize.y);
        vec2 uv = (ruv.xy + ruv.zw) * 0.5 +  offset * (ruv.zw - ruv.xy) * vec2(1.0, -1.0);
        if (vertexDistance < 1.5 && normdev < 0.2 && uv.x > ruv.x && uv.x < ruv.z && uv.y > ruv.y && uv.y < ruv.w) {
            uv.y -= yoffset;
            color = texture(Sampler0, uv);
            float shadow = clamp(pow(length(offset * SHADOWSCALE), 6.0), 0.0, 1.0);
            color.rgb = mix(color.rgb * color.a, vec3(0.0), shadow);
            color.a = max(shadow, color.a);
            color = mix(vec4(0.0, 0.0, 0.0, 1.0), color, clamp((0.2 - normdev) * 8.0, 0.0, 1.0) * clamp((1.5 - vertexDistance) * 5.0, 0.0, 1.0));
        } else {
            color = vec4(0.0, 0.0, 0.0, 1.0);
        }
    } else if (abs(reticle - 100.0) <= 0.0001) {
        discard;
    } else {
        color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
        if (color.a < 0.1) {
            discard;
        }
    }
    fragColor = linear_fog(color, fogVertexDistance, FogStart, FogEnd, FogColor);
}
