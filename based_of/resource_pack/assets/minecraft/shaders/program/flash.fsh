#version 150
 
uniform sampler2D DiffuseSampler;
uniform sampler2D DiffuseDepthSampler;

uniform vec2 InSize;
uniform vec3 Color;
 
in vec2 texCoord;
in vec2 oneTexel;
in float aspectRatio;
flat in float mode;

out vec4 outColor;
 
#define INTENSITY 1.5
#define MAXDIST 20.0
#define NEAR 0.1 
#define FAR 1536.0
#define BLURR 10.0
#define FOV 70
#define CK tan(FOV / 360.0 * 3.14159265358979) * 2.0

float LinearizeDepth(float depth) {
    float z = depth * 2.0 - 1.0;
    return (NEAR * FAR) / (FAR + NEAR - z * (FAR - NEAR));    
}

void main(){
    outColor = texture(DiffuseSampler, texCoord);

    if (mode > 0.0) {
        float depth = LinearizeDepth(texture(DiffuseDepthSampler, texCoord).r);

        vec2 screenCoords = (texCoord - 0.5) * vec2(aspectRatio, 1.0) * CK * depth;
        float dist = length(vec3(screenCoords, depth));

        if (dist < MAXDIST) {
            vec4 blurColor = outColor
                           + texture(DiffuseSampler, texCoord + vec2(oneTexel.x * BLURR, 0.0)) 
                           + texture(DiffuseSampler, texCoord - vec2(oneTexel.x * BLURR, 0.0)) 
                           + texture(DiffuseSampler, texCoord + vec2(0.0, oneTexel.y * BLURR)) 
                           + texture(DiffuseSampler, texCoord - vec2(0.0, oneTexel.y * BLURR));
            blurColor /= 5.0;
            vec3 lightColor = clamp((pow(1.0 / (dist + 3.0), 1.5) - 0.01) * 9.0, 0.0, 1.0) * Color;

            outColor.rgb *= (INTENSITY / clamp(length(blurColor.rgb), 0.04, 1.0) * lightColor * 0.9) * (1.0 - clamp(length(blurColor.rgb) / 1.6, 0.0, 1.0))  + vec3(1.0);
            outColor.rgb += INTENSITY * lightColor * 0.1;
        }
    }
    outColor = vec4(outColor.rgb, 1.0);
}