#version 330

uniform sampler2D MainSampler;
uniform sampler2D MainDepthSampler;
uniform sampler2D TranslucentSampler;
uniform sampler2D TranslucentDepthSampler;
uniform sampler2D ItemEntitySampler;
uniform sampler2D ItemEntityDepthSampler;
uniform sampler2D ParticlesSampler;
uniform sampler2D ParticlesDepthSampler;
uniform sampler2D CloudsSampler;
uniform sampler2D CloudsDepthSampler;
uniform sampler2D WeatherSampler;
uniform sampler2D WeatherDepthSampler;

in vec2 texCoord;

#define DEBUG 1

vec4 color_layers[6] = vec4[](vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0));
float depth_layers[6] = float[](0, 0, 0, 0, 0, 0);
int active_layers = 0;

out vec4 fragColor;

void try_insert(vec4 color, float depth) {
    if (color.a == 0.0) {
        return;
    }
    color_layers[active_layers] = color;
    depth_layers[active_layers] = depth;
    int jj = active_layers++;
    int ii = jj - 1;
    while (jj > 0 && depth_layers[jj] > depth_layers[ii]) {
        float depthTemp = depth_layers[ii];
        depth_layers[ii] = depth_layers[jj];
        depth_layers[jj] = depthTemp;
        vec4 colorTemp = color_layers[ii];
        color_layers[ii] = color_layers[jj];
        color_layers[jj] = colorTemp;
        jj = ii--;
    }
}

vec3 blend(vec3 dst, vec4 src) {
    return (dst * (1.0 - src.a)) + src.rgb;
}

void main() {
    color_layers[0] = vec4(texture(MainSampler, texCoord).rgb, 1.0);
    depth_layers[0] = texture(MainDepthSampler, texCoord).r;
    active_layers = 1;

    try_insert(texture(TranslucentSampler, texCoord), texture(TranslucentDepthSampler, texCoord).r);
    try_insert(texture(ItemEntitySampler, texCoord), texture(ItemEntityDepthSampler, texCoord).r);

    // ── PARTICLES LAYER: skip the exact marker pixels ──
    // Marker pixels are at known fixed addresses: (0,0) and (2,0).
    // gl_FragCoord.xy has (0.5, 0.5) at the center of pixel (0,0),
    // so pixel (0,0) satisfies: x in [0,1), y in [0,1)
    //    pixel (2,0) satisfies: x in [2,3), y in [0,1)
    // No color-based heuristic needed — exact position check only.
    vec4 particleColor = texture(ParticlesSampler, texCoord);
    float particleDepth = texture(ParticlesDepthSampler, texCoord).r;
    bool isMarkerPixel = (gl_FragCoord.y < 1.0) && (
        (gl_FragCoord.x < 1.0) ||                                        // pixel (0,0): flash
        (gl_FragCoord.x >= 2.0 && gl_FragCoord.x < 3.0)                  // pixel (2,0): zoom
    );
    if (!isMarkerPixel) {
        try_insert(particleColor, particleDepth);
    }

    try_insert(texture(WeatherSampler, texCoord), texture(WeatherDepthSampler, texCoord).r);
    try_insert(texture(CloudsSampler, texCoord), texture(CloudsDepthSampler, texCoord).r);

    vec3 texelAccum = color_layers[0].rgb;
    for (int ii = 1; ii < active_layers; ++ii) {
        texelAccum = blend(texelAccum, color_layers[ii]);
    }

    fragColor = vec4(texelAccum.rgb, 1.0);

#if DEBUG
    if (gl_FragCoord.x < 50.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = pass 2 runs
    }
#endif
}
