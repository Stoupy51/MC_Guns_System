""" Shared plumbing for every `/posteffect` chain: the GLSL header, the activation clock and the
three-pass skeleton that wraps one fullscreen shader around it.

A post effect has no parameters. The only per-activation signal a chain receives is that
`posteffect add` reallocates its persistent targets at `clear_color`, so a 1x1 persistent target
whose alpha starts at 0 tells the shader "this is frame one". Stamping `Globals.GameTime` there
turns that edge into a wall-clock timer with sub-tick resolution.
"""
# Imports
from beet import FragmentShader, GlslShader, PostEffect
from stewbeet import JsonDict, Mem, set_json_encoder

# Constants
HEADER: str = """#version 330
#extension GL_ARB_separate_shader_objects : require
"""
""" Mandatory preamble for every post shader in 26.3: shaderc rejects unlocated in/out variables. """

SCREENQUAD: str = "minecraft:core/screenquad"
""" Vanilla fullscreen-triangle vertex shader, emitting `texCoord` at location 0. """

CLOCK_GLSL: str = """#ifndef MGS_CLOCK_GLSL
#define MGS_CLOCK_GLSL

// Activation timestamp: GameTime packed across RGB. Alpha 0 is frame one (a fresh persistent target
// reads back as its clear_color), MGS_RUNNING an armed clock, and 1 a clock whose ramps all ended.
#define MGS_RUNNING 0.5
#define MGS_SETTLE_TICKS 1200.0

vec3 mgs_pack_time(float t) {
    vec3 enc = fract(t * vec3(1.0, 255.0, 65025.0));
    return enc - enc.yzz * vec3(1.0 / 255.0, 1.0 / 255.0, 0.0);
}

float mgs_unpack_time(vec3 enc) {
    return dot(enc, vec3(1.0, 1.0 / 255.0, 1.0 / 65025.0));
}

// Ticks since the clock was armed. A settled clock is long expired, so the 24000-tick wrap of
// GameTime can only be crossed once while running. A small negative delta is the server's time sync
// stepping the client clock back, which must hold the ramp at its start rather than end it.
float mgs_elapsed(vec4 clock, float gameTime) {
    if (clock.a < 0.25) return 0.0;
    if (clock.a > 0.75) return 1.0e6;
    float delta = gameTime - mgs_unpack_time(clock.rgb);
    if (delta < -0.5) delta += 1.0;
    return max(delta * 24000.0, 0.0);
}

// Eased 0 to 1 ramp over `duration` ticks, holding at 1 afterwards.
float mgs_ramp(vec4 clock, float gameTime, float duration) {
    float t = clamp(mgs_elapsed(clock, gameTime) / max(duration, 1.0e-4), 0.0, 1.0);
    return t * t * (3.0 - 2.0 * t);
}

#endif
"""
""" Registered as `mgs:clock.glsl`, included by every chain built through `timed_effect`. """

CLOCK_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    vec4 clock = texture(ClockSampler, vec2(0.5));
    if (clock.a < 0.25) {
        fragColor = vec4(mgs_pack_time(GameTime), MGS_RUNNING);
        return;
    }
    fragColor = mgs_elapsed(clock, GameTime) > MGS_SETTLE_TICKS ? vec4(clock.rgb, 1.0) : clock;
}
"""
""" Stamps the activation time on frame one, then marks the clock settled once every ramp has ended. """

COPY_FSH: str = HEADER + """
uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    fragColor = texture(InSampler, texCoord);
}
"""
""" A pass may not sample the target it writes, so the clock and the frame both go through scratch targets. """


# Functions
def register_common(ns: str) -> None:
	""" Register the clock include and the two shaders every timed chain shares. """
	Mem.ctx.assets[ns].glsl_shaders["include/clock"] = GlslShader(CLOCK_GLSL)
	Mem.ctx.assets[ns].fragment_shaders["post/clock"] = FragmentShader(CLOCK_FSH)
	Mem.ctx.assets[ns].fragment_shaders["post/copy"] = FragmentShader(COPY_FSH)


def timed_effect(ns: str, effect_id: str, shader: str, uniforms: JsonDict, inputs: list[JsonDict] | None = None) -> None:
	""" Register a `/posteffect` chain whose clock restarts on every `posteffect add`.

	The apply pass receives `ClockSampler` plus `InSampler` bound to `minecraft:main`, and writes a
	scratch target that a last pass copies back. Sampling main while rendering into it is a GPU
	feedback loop, which shows up as a tiled grid of stale blocks across the screen.
	Extra `inputs` are appended in order, so their `SamplerInfo` entries follow `OutSize`,
	`ClockSize` and `InSize`.

	Args:
		effect_id: path under `assets/<ns>/post_effect/`, the id `/posteffect add` takes.
		shader:    fragment shader id of the apply pass, ex: "mgs:post/flash".
		uniforms:  std140 blocks baked into the apply pass, as `{block_name: [{name, type, value}]}`.
	"""
	passes: list[JsonDict] = [
		{
			"vertex_shader": SCREENQUAD,
			"fragment_shader": f"{ns}:post/clock",
			"inputs": [{"sampler_name": "Clock", "target": "clock"}],
			"output": "clock_next",
		},
		{
			"vertex_shader": SCREENQUAD,
			"fragment_shader": f"{ns}:post/copy",
			"inputs": [{"sampler_name": "In", "target": "clock_next"}],
			"output": "clock",
		},
		{
			"vertex_shader": SCREENQUAD,
			"fragment_shader": shader,
			"inputs": [
				{"sampler_name": "Clock", "target": "clock_next"},
				{"sampler_name": "In", "target": "minecraft:main"},
				*(inputs or []),
			],
			"output": "swap",
			"uniforms": uniforms,
		},
		{
			"vertex_shader": SCREENQUAD,
			"fragment_shader": f"{ns}:post/copy",
			"inputs": [{"sampler_name": "In", "target": "swap"}],
			"output": "minecraft:main",
		},
	]
	chain: JsonDict = {
		"targets": {
			"clock":      {"width": 1, "height": 1, "persistent": True, "clear_color": 0},
			"clock_next": {"width": 1, "height": 1},
			"swap":       {},
		},
		"passes": passes,
	}
	Mem.ctx.assets[ns].post_effects[effect_id] = set_json_encoder(PostEffect(chain), max_level=4)


def uniform(name: str, kind: str, value: float | list[float]) -> JsonDict:
	""" One entry of a baked std140 uniform block.

	>>> uniform("Duration", "float", 2.0)
	{'name': 'Duration', 'type': 'float', 'value': 2.0}
	"""
	return {"name": name, "type": kind, "value": value}

