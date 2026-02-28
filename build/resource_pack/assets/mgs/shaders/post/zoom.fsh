#version 330

uniform sampler2D InSampler;        // "swap" target (after flash pass)
uniform sampler2D ClassifySampler;  // 1x1 "classify" target

// ── ZoomConfig: tunable parameters from pipeline JSON ──
layout(std140) uniform ZoomConfig {
    float Distortion;  // Barrel distortion strength (default: 0.55)
    float Zoom;        // Magnification factor (default: 4.0)
};

in vec2 texCoord;
out vec4 fragColor;

#define DEBUG 1       // Set to 0 for production
#define MARKERS 5     // Must match classify.fsh
#define RADIUS 0.14   // Scope circle radius (aspect-corrected UV space)

// ── Bicubic interpolation (Catmull-Rom spline weights) ──
vec4 cubic(float v) {
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    float w = 6.0 - x - y - z;
    return vec4(x, y, z, w) * (1.0 / 6.0);
}

// Sample with bicubic filtering (4 bilinear taps for smooth magnification)
vec4 textureBicubic(sampler2D samp, vec2 texCoords, vec2 texSize) {
    vec2 oneTexel = 1.0 / texSize;
    texCoords = texCoords * texSize - 0.5;
    vec2 fxy = fract(texCoords);
    texCoords -= fxy;

    vec4 xcubic = cubic(fxy.x);
    vec4 ycubic = cubic(fxy.y);

    vec4 c = texCoords.xxyy + vec2(-0.5, 1.5).xyxy;
    vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
    vec4 offsetbc = c + vec4(xcubic.yw, ycubic.yw) / s;
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
    // Get screen dimensions from texture (replaces SamplerInfo)
    vec2 inSize = vec2(textureSize(InSampler, 0));

    // Read mode from classify
    float mode = round(texture(ClassifySampler, vec2(0.5, 0.5)).r * float(MARKERS));

    // Start with passthrough
    fragColor = texture(InSampler, texCoord);

    // Zoom: mode 4 (tolerance +/-0.5)
    if (mode >= 3.5 && mode <= 4.5) {
        float aspectRatio = inSize.x / inSize.y;
        // Center-origin, aspect-corrected screen coords
        vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);

        if (length(screenCoord) < RADIUS) {
            // Barrel distortion: map flat coords to spherical projection
            float d = length(screenCoord * Distortion / RADIUS);
            float z = sqrt(1.0 - d * d);
            float r = atan(d, z) / 3.1415926535;
            float theta = atan(screenCoord.y, screenCoord.x);

            // Back to UV with magnification
            screenCoord = vec2(cos(theta), sin(theta)) * r / Zoom;
            vec2 pixCoord = screenCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5);

            fragColor = textureBicubic(InSampler, pixCoord, inSize);
        }
    }

#if DEBUG
    // ── DEBUG: Mode indicator at bottom-left, offset x=100 (50x50) ──
    // Color encodes the detected mode from the classify pass:
    //   BLUE   = pipeline active, mode 0 (no marker detected)
    //   ORANGE = flash detected (modes 1-3)
    //   CYAN   = zoom detected (mode 4)
    //
    // This is the MOST IMPORTANT indicator. It tells you:
    //   - The pipeline is running (any colored square visible)
    //   - classify read the particles target successfully
    //   - The mode was decoded correctly
    //
    // IF NO SQUARE: the pipeline doesn't load at all.
    //   → Check Fabulous graphics, resource pack loaded
    //   → Check game log for shader compilation errors
    if (gl_FragCoord.x >= 100.0 && gl_FragCoord.x < 150.0 && gl_FragCoord.y < 50.0) {
        if (mode >= 0.5 && mode <= 3.5) {
            fragColor = vec4(1.0, 0.5, 0.0, 1.0);  // Orange: flash mode
        } else if (mode >= 3.5 && mode <= 4.5) {
            fragColor = vec4(0.0, 1.0, 1.0, 1.0);  // Cyan: zoom mode
        } else {
            fragColor = vec4(0.2, 0.2, 1.0, 1.0);  // Blue: no mode
        }
    }
#endif
}
