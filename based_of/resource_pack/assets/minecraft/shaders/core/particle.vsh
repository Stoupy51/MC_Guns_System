#version 150

in vec3 Position;
in vec2 UV0;
in vec4 Color;
in ivec2 UV2;

uniform sampler2D Sampler0;
uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;

out float vertexDistance;
out float marker;
out vec2 texCoord0;
out vec2 scales;
out vec2 v0;
out vec2 v2;
out vec4 vertexColor;
out vec4 glpos;

#define DUSTRES 8.0
#define DISTANCE 500.0
#define MARKERS 5
#define COLORLIMIT 3.0 / 255.0
#define C0 vec4(1.0, 0.0, 0.0, 18.0 / 255.0)
#define C1 vec4(0.0, 0.0, 1.0, 18.0 / 255.0)
#define C2 vec4(0.0, 1.0, 0.0, 18.0 / 255.0)
#define C3 vec4(0.0, 1.0, 1.0, 18.0 / 255.0)
bool matchMarker(vec2 uv0) {
    vec2 offset = (DUSTRES - 1.0) / vec2(textureSize(Sampler0, 0).xy);
    vec4 tmp0 = texture(Sampler0, uv0) - C0;
    vec4 tmp1 = texture(Sampler0, uv0 + vec2(0.0, -offset.y)) - C1;
    vec4 tmp2 = texture(Sampler0, uv0 + vec2(-offset.x, -offset.y)) - C2;
    vec4 tmp3 = texture(Sampler0, uv0 + vec2(-offset.x, 0.0)) - C3;
    return dot(tmp0, tmp0) + dot(tmp1, tmp1) + dot(tmp2, tmp2) + dot(tmp3, tmp3) == 0.0;
}

float idMarker(vec3 color) {
    bool rz = color.r == 0.0;
    bool gz = color.g == 0.0;
    bool bz = color.b == 0.0;
    bool rnz = color.r > 0.0 && color.r < COLORLIMIT;
    bool gnz = color.g > 0.0 && color.g < COLORLIMIT;
    bool bnz = color.b > 0.0 && color.b < COLORLIMIT;
    return 1.0 * float(rnz && gz && bz) + 2.0 * float(rz && gnz && bz) + 3.0 * float(rz && gz && bnz) + 4.0 * float(rnz && gnz && bz) + 5.0 * float(rnz && gz && bnz);
}

void main() {

    vertexDistance = length((ModelViewMat * vec4(Position, 1.0)).xyz);
    marker = 0.0;
    texCoord0 = UV0;
    scales = vec2(0.0);
    v0 = vec2(0.0);
    v2 = vec2(0.0);
    vertexColor = Color * texelFetch(Sampler2, UV2 / 16, 0);
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);

    vec4 view = ModelViewMat * vec4(Position, 1.0);

    // execute anchored eyes run particle minecraft:dust 0.0 0.0 0.011 0.0 ^ ^ ^-500 0 0 0 0 1 force
    float mv = idMarker(Color.rgb);
    float dist = abs(length(view.xyz) - DISTANCE);
    if (dist >= 2.0 && dist < 10.0) {
        mv = 5.0;
        dist = 0.0;
    }
    if (view.z > 0.0 && dist < 2.0 && mv > 0.0) {
        vec2 offset = DUSTRES / vec2(textureSize(Sampler0, 0).xy);
        vec2 centerpix = -0.5 / vec2(textureSize(Sampler0, 0).xy);
        if (gl_VertexID % 4 == 0) {
            if (matchMarker(UV0 + centerpix)) {
                marker = mv;
                gl_Position = vec4(0.01, -1.0, -1.0, 1.0);
                scales.x = 1.0;
                v0 = view.xy;
            }
        } else if (gl_VertexID % 4 == 1) {
            if (matchMarker(UV0 + vec2(0.0, offset.y) + centerpix)) {
                marker = mv;
                gl_Position = vec4(0.01, -0.99, -1.0, 1.0);
            }
        } else if (gl_VertexID % 4 == 2) {
            if (matchMarker(UV0 + vec2(offset.x, offset.y) + centerpix)) {
                marker = mv;
                gl_Position = vec4(-0.01, -0.99, -1.0, 1.0);
                scales.y = 1.0;
                v2 = view.xy;
            }
        } else {
            if (matchMarker(UV0 + vec2(offset.x, 0.0) + centerpix)) {
                marker = mv;
                gl_Position = vec4(-0.01, -1.0, -1.0, 1.0);
            }
        }
    }
    glpos = gl_Position;
}
