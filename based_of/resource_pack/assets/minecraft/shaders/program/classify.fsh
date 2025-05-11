# version 150

uniform sampler2D DiffuseSampler;
uniform sampler2D ParticlesSampler;
uniform sampler2D ParticlesDepthSampler;
uniform vec2 AuxSize0;
uniform float Time;

in vec2 texCoord;
in vec2 oneTexel;

out vec4 outColor;

# define TIMEMULT 1000000.0
# define TICK 0.05 * TIMEMULT 
#define PRIME1 7331.0
#define PRIME2 235747.0
#define SPRITECOUNT 9.0
#define MARKERS 5

int intmod(int i, int base) {
    return i - (i / base * base);
}

vec4 encodeInt(int i) {
    int r = intmod(i, 256);
    i = i / 256;
    int g = intmod(i, 256);
    i = i / 256;
    int b = intmod(i, 256);
    return vec4(float(r) / 255.0, float(g) / 255.0, float(b) / 255.0, 1.0);
}

int decodeInt(vec4 ivec) {
    ivec.rgb *= 255.0;
    int num = 0;
    num += int(ivec.r);
    num += int(ivec.g) * 255;
    num += int(ivec.b) * 255 * 255;
    return num;
}

int roundF(float f) {
    return int(floor(f + 0.5));
}

void main() {
    outColor = vec4(0.0);

    float lastM = texture(DiffuseSampler, vec2(0.125, 0.5)).r * 255.0;
    float lastZ = texture(DiffuseSampler, vec2(0.875, 0.5)).r * 255.0;
    int lastO = decodeInt(texture(DiffuseSampler, vec2(0.625, 0.5)));
    int lastT = decodeInt(texture(DiffuseSampler, vec2(0.375, 0.5)));
    int currT = roundF(Time * TIMEMULT);
    lastT -= int(currT < lastT) * int(TIMEMULT);
    int tickI = roundF(TICK);

    float m0 = 0.0;
    vec2 coords = vec2(oneTexel.x * (floor(AuxSize0.x / 2.0) + 0.5), oneTexel.y * 0.5);
    float d = texture(ParticlesDepthSampler, coords).r;
    vec4 val = texture(ParticlesSampler, coords);
    if (d <= 0.0 && val.a > 0.0) {
        m0 = round(val.r * MARKERS);
    }

    bool isZoomer = m0 > 3.5 && m0 < 5.5;

    if (0.0 < texCoord.x && texCoord.x < 0.25 && !isZoomer) {
        outColor = vec4(m0 / 255.0, 0.0, 0.0, 1.0);
    } else if (0.25 < texCoord.x && texCoord.x < 0.5 && (lastM == 0.0 && !isZoomer || currT - lastT > tickI)) {
        outColor = encodeInt(roundF(Time * TIMEMULT));
    } else if (0.5 < texCoord.x && texCoord.x < 0.75) {
        if (lastM == 0.0 && !isZoomer || currT - lastT > tickI || abs(float(currT - lastT)) < 1000.0) {
            outColor = vec4(mod(floor(Time * PRIME1 + float(lastO) * PRIME2), SPRITECOUNT) / 255.0, 0.0, 0.0, 1.0);
        } else {
            outColor = encodeInt(lastO);
        }
    } else if (0.75 < texCoord.x && texCoord.x < 1.0) {
        if (isZoomer) {
            outColor = vec4(m0 / 255.0, 0.0, 0.0, 1.0);
        } else if (lastZ < 3.5 || lastZ > 5.5){
            outColor = vec4(5.0 / 255.0, 0.0, 0.0, 1.0);
        } else {
            outColor = vec4(lastZ / 255.0, 0.0, 0.0, 1.0);
        }
    }
}