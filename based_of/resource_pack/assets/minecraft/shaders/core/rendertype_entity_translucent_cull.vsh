#version 150

#moj_import <light.glsl>
#moj_import <fog.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in vec2 UV1;
in ivec2 UV2;
in vec3 Normal;

uniform sampler2D Sampler0;
uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform mat3 IViewRotMat;
uniform int FogShape;

uniform vec3 Light0_Direction;
uniform vec3 Light1_Direction;

out float vertexDistance;
out float fogVertexDistance;
out float reticle;
out float yoffset;
out vec4 vertexColor;
out vec2 texCoord0;
out vec2 texCoord1;
out vec2 texCoord2;
out vec3 normal;
out vec4 gpos;
out vec4 ruv;

#define RSIZE 128.0
#define RSIZEL 1024.0
#define UVFUDGE 0.999
#define M_ALPHA 17.0 / 255.0
#define R vec4(1.0, 0.0, 0.0, M_ALPHA)
#define G vec4(0.0, 1.0, 0.0, M_ALPHA)
#define B vec4(0.0, 0.0, 1.0, M_ALPHA)
#define M vec4(1.0, 0.0, 1.0, M_ALPHA)
#define Y vec4(1.0, 1.0, 0.0, M_ALPHA)
#define C vec4(0.0, 1.0, 1.0, M_ALPHA)
#define W vec4(1.0, 1.0, 1.0, M_ALPHA)
#define Ws vec4(254.0 / 255.0, 254.0 / 255.0, 254.0 / 255.0, M_ALPHA)

void main() {
    gpos = ProjMat * ModelViewMat * vec4(Position, 1.0);
    gl_Position = gpos;
    gpos /= gpos.w;

    fogVertexDistance = fog_distance(ModelViewMat, IViewRotMat * Position, FogShape);
    vertexDistance = length((ModelViewMat * vec4(Position, 1.0)).xyz);
    vertexColor = minecraft_mix_light(Light0_Direction, Light1_Direction, Normal, Color) * texelFetch(Sampler2, UV2 / 16, 0);
    texCoord0 = UV0;
    texCoord1 = UV1;
    texCoord2 = UV2;
    normal = normalize((ProjMat * ModelViewMat * vec4(Normal, 0.0)).xyz);
    vec2 sides = 1.0 / textureSize(Sampler0, 0);
    reticle = 0.0;
    vec4 tmpcol = texture(Sampler0, UV0);
    if (vertexDistance < 2.0 && (tmpcol.a == M_ALPHA || tmpcol.a == 0.0)) {
        if (gl_VertexID % 4 == 0) {
            if (tmpcol == R) {
                sides *= RSIZE;
                yoffset = sides.y;
                sides *= UVFUDGE;
                reticle = 1.0;
                ruv = vec4(UV0, UV0 + vec2(sides.x, sides.y));
            } else if (tmpcol == G) {
                sides *= RSIZEL;
                yoffset = sides.y;
                sides *= UVFUDGE;
                reticle = -1.0;
                ruv = vec4(UV0, UV0 + vec2(sides.x, sides.y));
            } else if (tmpcol == Y || (tmpcol.a == 0.0 && texture(Sampler0, UV0 + vec2(0.0, sides.y * RSIZE)) == Y)) {
                reticle = 100.0;
            }
        } else if (gl_VertexID % 4 == 1) {
            if (tmpcol == B) {
                sides *= RSIZE;
                yoffset = sides.y;
                sides *= UVFUDGE;
                reticle = 1.0;
                ruv = vec4(UV0 + vec2(0.0, -sides.y), UV0 + vec2(sides.x, 0.0));
            } else if (tmpcol == W) {
                sides *= RSIZEL;
                yoffset = sides.y;
                sides *= UVFUDGE;
                reticle = -1.0;
                ruv = vec4(UV0 + vec2(0.0, -sides.y), UV0 + vec2(sides.x, 0.0));
            } else if (tmpcol == Ws || (tmpcol.a == 0.0 && texture(Sampler0, UV0 + vec2(0.0, sides.y * RSIZE)) == Ws)) {
                reticle = 100.0;
            }
        } else if (gl_VertexID % 4 == 2) {
            if (tmpcol == W) {
                sides *= RSIZE;
                yoffset = sides.y;
                sides *= UVFUDGE;
                reticle = 1.0;
                ruv = vec4(UV0 + vec2(-sides.x, -sides.y), UV0);
            } else if (tmpcol == B) {
                sides *= RSIZEL;
                yoffset = sides.y;
                sides *= UVFUDGE;
                reticle = -1.0;
                ruv = vec4(UV0 + vec2(-sides.x, -sides.y), UV0);
            } else if (tmpcol == C || (tmpcol.a == 0.0 && texture(Sampler0, UV0 + vec2(0.0, sides.y * RSIZE)) == C)) {
                reticle = 100.0;
            }
        } else if (gl_VertexID % 4 == 3) {
            if (tmpcol == G) {
                sides *= RSIZE;
                yoffset = sides.y;
                sides *= UVFUDGE;
                reticle = 1.0;
                ruv = vec4(UV0 + vec2(-sides.x, 0.0), UV0 + vec2(0.0, sides.y));
            } else if (tmpcol == R) {
                sides *= RSIZEL;
                yoffset = sides.y;
                sides *= UVFUDGE;
                reticle = -1.0;
                ruv = vec4(UV0 + vec2(-sides.x, 0.0), UV0 + vec2(0.0, sides.y));
            } else if (tmpcol == M || (tmpcol.a == 0.0 && texture(Sampler0, UV0 + vec2(0.0, sides.y * RSIZE)) == M)) {
                reticle = 100.0;
            }
        }
    } 
}
