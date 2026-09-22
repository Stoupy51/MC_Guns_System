#version 330
#extension GL_ARB_separate_shader_objects : require

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

// Vanilla copies the held item's depth into the main depth buffer here, right before post effects.
// Writing 1.0 instead, the near plane itself, lets a post effect recognise the gun. Nothing else
// reads main depth after this point: it is cleared before the GUI is drawn.
void main() {
    float depth = texelFetch(InSampler, ivec2(gl_FragCoord.xy), 0).r;
    if (depth == 0.0) {
        discard;
    }
    gl_FragDepth = 1.0;
}
