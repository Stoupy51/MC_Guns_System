#version 330

// ── Samplers: pipeline inputs ──
uniform sampler2D ParticlesSampler;       // Particles target (color)
uniform sampler2D ParticlesDepthSampler;  // Particles target (depth)

in vec2 texCoord;  // Screen UV from screenquad.vsh
out vec4 fragColor;

#define MARKERS 5  // Must match particle.vsh/fsh

void main() {
    vec2 baseUV = vec2(0.5, 1.5 / float(particlesRes.y));
    float mode = 0.0;
    float bestAlpha = 0.0;
    float bestDepth = 1.0;
    vec4 bestPix = vec4(0.0);

    for (int oy = 0; oy <= 2; ++oy) {
        for (int ox = -1; ox <= 1; ++ox) {
            vec2 sampleUV = baseUV + vec2(float(ox) / float(particlesRes.x), float(oy) / float(particlesRes.y));
            vec4 pix = texture(ParticlesSampler, sampleUV);
            float depth = texture(ParticlesDepthSampler, sampleUV).r;

            // prefer the brightest sentinel-like pixel
            if (pix.a > bestAlpha) {
                bestAlpha = pix.a;
                bestDepth = depth;
                bestPix = pix;
            }
        }
    }

    // relaxed thresholds
    if (bestPix.a > 0.003 && bestPix.a < 0.03 && bestDepth < 0.02) {
        mode = round(bestPix.r * float(MARKERS));
    }
    fragColor = vec4(mode / float(MARKERS), 0.0, 0.0, 1.0);
}
