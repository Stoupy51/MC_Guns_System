#version 150

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;

in vec2 texCoord0;
in float crosshair;

out vec4 fragColor;

void main() {
    vec4 color = texture(Sampler0, texCoord0);
    if (color.a == 0.0 || (crosshair > 0.9999 && color.r == 1.0 && color.g == 0.0 && color.b == 0.0 && color.a == 254.0 / 255.0)) {
        discard;
    }
    
    fragColor = color * ColorModulator;
}