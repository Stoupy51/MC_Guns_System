#version 150

in vec3 Position;
in vec2 UV0;

uniform sampler2D Sampler0;
uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform vec2 ScreenSize;

out vec2 texCoord0;
out float crosshair;

#define CROSSHAIRSIZE 0.05      // target crosshair size as multiple of Y height
#define CROSSHAIRSIZEMIN 80.0   // minimum crosshair size on screen in pix (entire sprite, not just visible portion)
#define SPRITESIZE 64.0         // size of crosshair.png
#define MINTEXSIZE 512.0        // minimum size of crosshair+ui texture

void main() {
    vec4 pos = ProjMat * ModelViewMat * vec4(Position, 1.0);
    vec2 dim = textureSize(Sampler0, 0);
    float ratio = ScreenSize.y / ScreenSize.x;
    texCoord0 = UV0;
    vec2 texCoordTmp = texCoord0;
    crosshair = 0.0;
    int vertexId = gl_VertexID % 4;
    if (vertexId == 0) {
        texCoordTmp.x += 0.5 / dim.x;
        texCoordTmp.y += 0.5 / dim.y;
    }
    else if (vertexId == 1) {
        texCoordTmp.x += 0.5 / dim.x;
        texCoordTmp.y -= 0.5 / dim.y;
    }
    else if (vertexId == 2) {
        texCoordTmp.x -= 0.5 / dim.x;
        texCoordTmp.y -= 0.5 / dim.y;
    }
    else {
        texCoordTmp.x -= 0.5 / dim.x;
        texCoordTmp.y += 0.5 / dim.y;
    }

    vec4 color = texture(Sampler0, texCoordTmp);

    if (color.r == 1.0 && color.g == 0.0 && color.b == 0.0 && color.a == 254.0 / 255.0 && dim.x >= MINTEXSIZE && dim.y >= MINTEXSIZE && abs(pos.x) <= 0.1 * ratio && abs(pos.y) <= 0.1 && Position.z == 0.0) {
        if (pos.x < 0.0) {
            pos.x = -max(CROSSHAIRSIZE * ratio, CROSSHAIRSIZEMIN / ScreenSize.x);
        } else {
            pos.x = max(CROSSHAIRSIZE * ratio, CROSSHAIRSIZEMIN / ScreenSize.x);
        }
        if (pos.y < 0.0) {
            pos.y = -max(CROSSHAIRSIZE, CROSSHAIRSIZEMIN / ScreenSize.y);
        } else {
            pos.y = max(CROSSHAIRSIZE, CROSSHAIRSIZEMIN / ScreenSize.y);
        }
        
        if (int(ScreenSize.x) % 2 == 1) { // handle odd width case
            pos.x -= 1.0 / ScreenSize.x;
        }
        if (int(ScreenSize.y) % 2 == 1) { // handle odd height case
            pos.y -= 1.0 / ScreenSize.y;
        }

        crosshair = 1.0;
        texCoord0 = texCoordTmp;
    }
    gl_Position = pos;
}