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

#define DEBUG 0

vec4 color_layers[6] = vec4[](vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0));
float depth_layers[6] = float[](0, 0, 0, 0, 0, 0);
int active_layers = 0;

out vec4 fragColor;

void try_insert(vec4 color, float depth) {
    if (color.a == 0.0) return;
    color_layers[active_layers] = color;
    depth_layers[active_layers] = depth;
    int jj = active_layers++;
    int ii = jj - 1;
    while (jj > 0 && depth_layers[jj] > depth_layers[ii]) {
        float depthTemp = depth_layers[ii]; depth_layers[ii] = depth_layers[jj]; depth_layers[jj] = depthTemp;
        vec4 colorTemp  = color_layers[ii];  color_layers[ii]  = color_layers[jj];  color_layers[jj]  = colorTemp;
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
    try_insert(texture(ItemEntitySampler,  texCoord), texture(ItemEntityDepthSampler,  texCoord).r);

    vec4 particleColor = texture(ParticlesSampler, texCoord);
    float particleDepth = texture(ParticlesDepthSampler, texCoord).r;
#if DEBUG
    // Debug: show ALL particles including marker quads (don't hide anything)
    try_insert(particleColor, particleDepth);
#else
    // Hide the exact marker sentinel pixels at (0,0) [flash] and (1,0) [zoom]
    // These are in the main layer (not particles), but we still insert particles normally.
    try_insert(particleColor, particleDepth);
#endif

    try_insert(texture(WeatherSampler, texCoord), texture(WeatherDepthSampler, texCoord).r);
    try_insert(texture(CloudsSampler,  texCoord), texture(CloudsDepthSampler,  texCoord).r);

    vec3 texelAccum = color_layers[0].rgb;
    for (int ii = 1; ii < active_layers; ++ii) {
        texelAccum = blend(texelAccum, color_layers[ii]);
    }
    fragColor = vec4(texelAccum.rgb, 1.0);

#if DEBUG
    // ═══ DEBUG SQUARES (bottom-left, 50px wide each, starting at y=5) ═══
    // Sentinel pixels are at (0,0) and (1,0), so debug squares start at y=5
    // to avoid overwriting them during compositing.
    //  [0-50, 5-55]   RED    = transparency pass runs
    //  [150-200]       YELLOW/GRAY = flash sentinel at (0,0)?
    //  [200-250]       YELLOW/GRAY = zoom sentinel at (1,0)?
    //  [250-300]       Amplified MAIN at (0,0) x50
    //  [300-350]       Amplified MAIN at (1,0) x50
    //  [350-400]       MAIN DEPTH at (0,0): GREEN=near, RED=far, YELLOW=mid
    //  [400-450]       MAIN DEPTH at (1,0): same color coding

    if (gl_FragCoord.x < 50.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = pass 2 runs
    }

    // Read sentinel pixels from MAIN at (0,0) and (1,0)
    ivec4 dbgFlash = ivec4(round(texelFetch(MainSampler, ivec2(0, 0), 0) * 255.0));
    ivec4 dbgZoom  = ivec4(round(texelFetch(MainSampler, ivec2(1, 0), 0) * 255.0));

    // [150-200] YELLOW if flash sentinel present (R=254), GRAY if empty
    if (gl_FragCoord.x >= 150.0 && gl_FragCoord.x < 200.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        fragColor = (dbgFlash.r == 254) ? vec4(1.0, 1.0, 0.0, 1.0) : vec4(0.1, 0.1, 0.1, 1.0);
    }
    // [200-250] YELLOW if zoom sentinel present (R=254), GRAY if empty
    if (gl_FragCoord.x >= 200.0 && gl_FragCoord.x < 250.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        fragColor = (dbgZoom.r == 254) ? vec4(1.0, 1.0, 1.0, 1.0) : vec4(0.1, 0.1, 0.1, 1.0);
    }

    // [250-300] Amplified raw MAIN color at flash sentinel (0,0) x50
    if (gl_FragCoord.x >= 250.0 && gl_FragCoord.x < 300.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        vec4 raw = texelFetch(MainSampler, ivec2(0, 0), 0);
        fragColor = vec4(clamp(raw.rgb * 50.0, 0.0, 1.0), 1.0);
    }
    // [300-350] Amplified raw MAIN color at zoom sentinel (1,0) x50
    if (gl_FragCoord.x >= 300.0 && gl_FragCoord.x < 350.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        vec4 raw = texelFetch(MainSampler, ivec2(1, 0), 0);
        fragColor = vec4(clamp(raw.rgb * 50.0, 0.0, 1.0), 1.0);
    }
    // [350-400] MAIN DEPTH at flash sentinel pixel (0,0)
    if (gl_FragCoord.x >= 350.0 && gl_FragCoord.x < 400.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        float d = texelFetch(MainDepthSampler, ivec2(0, 0), 0).r;
        if (d <= 0.001) {
            fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = near plane (sentinel wrote!)
        } else if (d >= 0.999) {
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = far/cleared (sky)
        } else {
            fragColor = vec4(d, d, 0.0, 1.0);       // YELLOW gradient = terrain depth
        }
    }
    // [400-450] MAIN DEPTH at zoom sentinel pixel (1,0)
    if (gl_FragCoord.x >= 400.0 && gl_FragCoord.x < 450.0 && gl_FragCoord.y >= 5.0 && gl_FragCoord.y < 55.0) {
        float d = texelFetch(MainDepthSampler, ivec2(1, 0), 0).r;
        if (d <= 0.001) {
            fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // GREEN = near plane (sentinel wrote!)
        } else if (d >= 0.999) {
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = far/cleared (sky)
        } else {
            fragColor = vec4(d, d, 0.0, 1.0);       // YELLOW gradient = terrain depth
        }
    }
#endif
}
