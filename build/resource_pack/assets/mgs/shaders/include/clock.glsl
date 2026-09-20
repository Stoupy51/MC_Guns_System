#ifndef MGS_CLOCK_GLSL
#define MGS_CLOCK_GLSL

// Activation timestamp: GameTime packed across RGB, alpha 1 marking an armed clock.
// A freshly allocated persistent target reads back as its clear_color, so alpha 0 means frame one.
vec3 mgs_pack_time(float t) {
    vec3 enc = fract(t * vec3(1.0, 255.0, 65025.0));
    return enc - enc.yzz * vec3(1.0 / 255.0, 1.0 / 255.0, 0.0);
}

float mgs_unpack_time(vec3 enc) {
    return dot(enc, vec3(1.0, 1.0 / 255.0, 1.0 / 65025.0));
}

// Ticks since the clock was armed. GameTime wraps every 24000 ticks, and a negative delta can only
// come from that wrap, so it reports as long expired rather than rewinding the animation.
float mgs_elapsed(vec4 clock, float gameTime) {
    if (clock.a < 0.5) return 0.0;
    float delta = (gameTime - mgs_unpack_time(clock.rgb)) * 24000.0;
    return delta < 0.0 ? 1.0e6 : delta;
}

// Eased 0 to 1 ramp over `duration` ticks, holding at 1 afterwards.
float mgs_ramp(vec4 clock, float gameTime, float duration) {
    float t = clamp(mgs_elapsed(clock, gameTime) / max(duration, 1.0e-4), 0.0, 1.0);
    return t * t * (3.0 - 2.0 * t);
}

#endif
