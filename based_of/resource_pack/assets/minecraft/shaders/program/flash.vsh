#version 150

in vec4 Position;

uniform sampler2D AuxSampler;
uniform mat4 ProjMat;
uniform vec2 InSize;

out vec2 texCoord;
out vec2 oneTexel;
out float aspectRatio;
flat out float mode;

void main(){
    vec4 outPos = ProjMat * vec4(Position.xy, 0.0, 1.0);
    gl_Position = vec4(outPos.xy, 0.2, 1.0);

    texCoord = outPos.xy * 0.5 + 0.5;
    oneTexel = 1.0 / InSize;
    aspectRatio = InSize.x / InSize.y;
    mode = texture(AuxSampler, vec2(0.125, 0.5)).r * 255.0;
}