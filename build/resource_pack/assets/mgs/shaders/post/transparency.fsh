#version 330

// ── All 6 Fabulous render targets ──
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

#define DEBUG 1  // Set to 0 for production

// ── Depth-sorted layer compositing (vanilla algorithm) ──
// 6 layers maximum: main (opaque) + 5 translucent layers
vec4 color_layers[6] = vec4[](vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0), vec4(0.0));
float depth_layers[6] = float[](0, 0, 0, 0, 0, 0);
int active_layers = 0;

out vec4 fragColor;

// Insert a layer into the depth-sorted list (back-to-front for alpha blending)
void try_insert(vec4 color, float depth) {
    if (color.a == 0.0) {
        return;  // Skip fully transparent layers
    }
    // Add at the end and bubble-sort backward into position
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

// Alpha-blend source over destination
vec3 blend(vec3 dst, vec4 src) {
    return (dst * (1.0 - src.a)) + src.rgb;
}

void main() {
    // Base layer: opaque main target
    color_layers[0] = vec4(texture(MainSampler, texCoord).rgb, 1.0);
    depth_layers[0] = texture(MainDepthSampler, texCoord).r;
    active_layers = 1;

    // Insert transparent layers
    try_insert(texture(TranslucentSampler, texCoord), texture(TranslucentDepthSampler, texCoord).r);
    try_insert(texture(ItemEntitySampler, texCoord), texture(ItemEntityDepthSampler, texCoord).r);

    // ── PARTICLES LAYER: hide the marker sentinel ──
    // Marker sentinel has:  alpha ~0.01, depth ~0.0005
    // Normal particles have: alpha >= 0.1, depth > 0.01
    // Checking BOTH conditions = no false positives possible.
    vec4 particleColor = texture(ParticlesSampler, texCoord);
    float particleDepth = texture(ParticlesDepthSampler, texCoord).r;
    bool isMarker = (particleColor.a > 0.005 && particleColor.a < 0.02 && particleDepth < 0.01);
    if (!isMarker) {
        try_insert(particleColor, particleDepth);
    }

    try_insert(texture(WeatherSampler, texCoord), texture(WeatherDepthSampler, texCoord).r);
    try_insert(texture(CloudsSampler, texCoord), texture(CloudsDepthSampler, texCoord).r);

    // Composite all layers back-to-front
    vec3 texelAccum = color_layers[0].rgb;
    for (int ii = 1; ii < active_layers; ++ii) {
        texelAccum = blend(texelAccum, color_layers[ii]);
    }

    fragColor = vec4(texelAccum.rgb, 1.0);

#if DEBUG
    // ── DEBUG: RED 50x50 square at bottom-left ──
    // Uses only gl_FragCoord (always available, no uniforms needed).
    // If you see this red square: the transparency compositing pass works.
    // gl_FragCoord.y=0.5 is the bottom row, increasing upward.
    if (gl_FragCoord.x < 50.0 && gl_FragCoord.y < 50.0) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RED = pass 2 runs
    }
#endif
}
