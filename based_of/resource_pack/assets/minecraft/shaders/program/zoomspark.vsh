#version 150

in vec4 Position;

uniform sampler2D AuxSampler;
uniform mat4 ProjMat;
uniform vec2 InSize;

out vec2 texCoord;
out vec2 oneTexel;
out float aspectRatio;
flat out vec2 offset;
flat out vec2 lb;
flat out vec2 ub;
flat out vec2 sd;
flat out float mode;
flat out float zmode;

#define SPRITECOUNT 9
#define SPRITECOUNTSQRT int(sqrt(SPRITECOUNT))
#define Pos1 vec2(0.0, -0.125)
#define Pos2 vec2(0.085, -0.11)
#define Pos3 vec2(0.2, -0.175)
#define Scale1 vec2(0.6, 0.6)
#define Scale2 vec2(0.45, 0.45)
#define Scale3 vec2(0.6, 0.6)

void main(){
    vec4 outPos = ProjMat * vec4(Position.xy, 0.0, 1.0);
    gl_Position = vec4(outPos.xy, 0.2, 1.0);

    texCoord = outPos.xy * 0.5 + 0.5;
    oneTexel = 1.0 / InSize;
    aspectRatio = InSize.x / InSize.y;
    mode = texture(AuxSampler, vec2(0.125, 0.5)).r * 255.0;
    zmode = texture(AuxSampler, vec2(0.875, 0.5)).r * 255.0;
    if (mode > 0.0) {
        int rawoff = int(texture(AuxSampler, vec2(0.625, 0.5)).r * 255.0);
        offset = vec2(rawoff % SPRITECOUNTSQRT, rawoff / SPRITECOUNTSQRT) / SPRITECOUNTSQRT;
        vec2 pos = vec2(0.0);
        vec2 scale = vec2(0.0);
        if (mode == 1.0) {
            pos = Pos1;
            scale = Scale1;
        } else if (mode == 2.0) {
            pos = Pos2;
            scale = Scale2;
        } else if (mode == 3.0) {
            pos = Pos3;
            scale = Scale3;
        }
        lb = pos - scale / 2.0;
        ub = pos + scale / 2.0;
        sd = scale * vec2(SPRITECOUNTSQRT);
    }
}
