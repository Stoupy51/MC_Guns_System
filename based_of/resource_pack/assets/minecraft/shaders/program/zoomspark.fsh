#version 150

uniform sampler2D DiffuseSampler;
uniform sampler2D SparkTex;
uniform vec2 InSize;
uniform float Distortion;
uniform float Zoom;

in vec2 texCoord;
in vec2 oneTexel;
in float aspectRatio;
flat in vec2 offset;
flat in vec2 lb;
flat in vec2 ub;
flat in vec2 sd;
flat in float mode;
flat in float zmode;

out vec4 outColor;

#define RADIUS 0.14


// from http://www.java-gaming.org/index.php?topic=35123.0
vec4 cubic(float v){
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    float w = 6.0 - x - y - z;
    return vec4(x, y, z, w) * (1.0/6.0);
}

vec4 textureBicubic(sampler2D samp, vec2 texCoords){

    texCoords = texCoords * InSize - 0.5;
    vec2 fxy = fract(texCoords);
    texCoords -= fxy;

    vec4 xcubic = cubic(fxy.x);
    vec4 ycubic = cubic(fxy.y);

    vec4 c = texCoords.xxyy + vec2 (-0.5, +1.5).xyxy;

    vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
    vec4 offsetbc = c + vec4 (xcubic.yw, ycubic.yw) / s;

    offsetbc *= oneTexel.xxyy;

    vec4 sample0 = texture(samp, offsetbc.xz);
    vec4 sample1 = texture(samp, offsetbc.yz);
    vec4 sample2 = texture(samp, offsetbc.xw);
    vec4 sample3 = texture(samp, offsetbc.yw);

    float sx = s.x / (s.x + s.y);
    float sy = s.z / (s.z + s.w);

    return mix(mix(sample3, sample2, sx), mix(sample1, sample0, sx), sy);
}

void main() {
    outColor = texture(DiffuseSampler, texCoord);
    vec2 pixCoord = texCoord;
    vec2 screenCoord = (pixCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

    if (zmode == 4.0 && length(screenCoord) < RADIUS) {
        float d = length(screenCoord * Distortion / RADIUS);
        float z = sqrt(1.0 - d * d);
        float r = atan(d, z) / 3.1415926535;
        float theta = atan(screenCoord.y, screenCoord.x);
        
        screenCoord = vec2(cos(theta), sin(theta)) * r / Zoom;
        pixCoord = screenCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5);
        outColor = textureBicubic(DiffuseSampler, pixCoord);
    } 

    if (mode > 0.0 && screenCoord.x > lb.x && screenCoord.y > lb.y && screenCoord.x < ub.x && screenCoord.y < ub.y) {
        outColor += texture(SparkTex, (screenCoord - lb) / sd  + offset);
    }
}