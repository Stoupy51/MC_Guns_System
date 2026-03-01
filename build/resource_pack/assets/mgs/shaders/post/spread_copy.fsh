#version 330

// Copy the smooth spread value from classify alpha to the persistent buffer.
// This creates a one-frame delay feedback loop:
//   classify reads smooth_spread (prev frame) → computes lerped value → writes to classify.a
//   spread_copy reads classify.a → writes to smooth_spread (for next frame)
uniform sampler2D ClassifySampler;

in vec2 texCoord;
out vec4 fragColor;

void main() {
    fragColor = vec4(texture(ClassifySampler, vec2(0.5, 0.5)).a, 0.0, 0.0, 1.0);
}
