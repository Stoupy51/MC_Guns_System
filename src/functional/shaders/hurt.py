""" Low-health screen overlay: a red vignette that turns into a pulsing one when close to death.

Two tiers rather than a continuous value, because a post effect has no parameters. The heartbeat
runs off `Globals.GameTime` instead of the activation clock so it does not restart on every tier
change, and its period divides 24000 so it stays continuous across the game-time wrap.
"""
# ruff: noqa: E501
# Imports
from dataclasses import dataclass

from beet import FragmentShader
from stewbeet import Mem, write_versioned_function

from .common import HEADER, timed_effect, uniform


# Constants
@dataclass(frozen=True)
class HurtTier:
	""" One severity of the overlay, picked by health as a fraction of the player's maximum. """
	effect_id: str
	""" The id of the overlay, ex: "mgs:hurt" or "mgs:hurt_critical". """
	threshold: float
	""" Fraction of max health at or below which this tier applies. """
	tint: list[float]
	""" rgb of the tint, then the vignette strength at the screen edge. """
	pulse: list[float]
	""" Heartbeat amplitude, then its period in ticks. The period must divide 24000. """
	shape: list[float]
	""" Radius where the vignette starts, then how far the rim desaturates. """
	aberration: float
	""" Radial colour separation at the rim, in fractions of the screen width. """
	fade_in: float
	""" Ticks the overlay takes to reach full strength. """


HURT_TIERS: list[HurtTier] = [
	HurtTier(effect_id="hurt",          threshold=0.40, tint=[1.0, 0.15, 0.12, 0.55], pulse=[0.00, 24.0], shape=[0.35, 0.35], aberration=0.000, fade_in=5.0),
	HurtTier(effect_id="hurt_critical", threshold=0.20, tint=[1.0, 0.05, 0.05, 0.90], pulse=[0.45, 16.0], shape=[0.18, 0.70], aberration=0.004, fade_in=4.0),
]
""" Ordered weakest first: the datapack picks the last tier whose threshold the player is under. """

HURT_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform HurtConfig {
    vec4 Tint;         // rgb tint, a = vignette strength at the screen edge
    vec2 Pulse;        // heartbeat amplitude, then its period in ticks
    vec2 Shape;        // radius where the vignette starts, then rim desaturation
    float Aberration;  // radial colour separation at the rim
    float Duration;    // fade-in length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// Lub-dub rather than a sine: two gaussian thumps, the second weaker and a fifth of a beat later.
float heartbeat(float phase) {
    float lub = exp(-pow(phase * 14.0, 2.0));
    float dub = exp(-pow((phase - 0.22) * 14.0, 2.0)) * 0.6;
    return lub + dub;
}

void main() {
    float t = mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration);
    float beat = 1.0 + Pulse.x * heartbeat(fract(GameTime * 24000.0 / Pulse.y));

    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 fromCentre = (texCoord - 0.5) * vec2(inSize.x / inSize.y, 1.0);
    float vignette = smoothstep(Shape.x, 0.75, length(fromCentre)) * t * beat;

    // Pulling the red channel outward and the blue inward reads as a stressed lens at the rim.
    vec3 color = texture(InSampler, texCoord).rgb;
    if (Aberration > 0.0) {
        vec2 shift = fromCentre * Aberration * vignette;
        color.r = texture(InSampler, texCoord + shift).r;
        color.b = texture(InSampler, texCoord - shift).b;
    }

    color = mix(color, vec3(dot(color, vec3(0.299, 0.587, 0.114))), Shape.y * vignette);
    color = mix(color, color * Tint.rgb + Tint.rgb * 0.35, clamp(Tint.a * vignette, 0.0, 1.0));
    fragColor = vec4(color, 1.0);
}
"""


# Functions
def main() -> None:
	""" Register both hurt tiers, their shader, and the per-tick health watcher. """
	ns: str = Mem.ctx.project_id
	Mem.ctx.assets[ns].fragment_shaders["post/hurt"] = FragmentShader(HURT_FSH)

	for tier in HURT_TIERS:
		timed_effect(
			ns,
			tier.effect_id,
			f"{ns}:post/hurt",
			{"HurtConfig": [
				uniform("Tint", "vec4", tier.tint),
				uniform("Pulse", "vec2", tier.pulse),
				uniform("Shape", "vec2", tier.shape),
				uniform("Aberration", "float", tier.aberration),
				uniform("Duration", "float", tier.fade_in),
			]},
		)
	write_functions(ns)


def write_functions(ns: str) -> None:
	""" Resolve the tier from the health criterion and swap ids only when it changes. """
	version: str = Mem.ctx.project_version

	# `attribute get <scale>` truncates, so a scale of 0.4 yields the health at which 40% is crossed.
	# That keeps the whole check on scores, with no player-NBT read.
	resolve: str = "\n".join(
		f"""execute store result score #hurt_at {ns}.data run attribute @s minecraft:max_health get {tier.threshold}
execute if score @s {ns}.health <= #hurt_at {ns}.data run scoreboard players set #hurt_tier {ns}.data {index + 1}"""
		for index, tier in enumerate(HURT_TIERS)
	)
	write_versioned_function("player/hurt_resolve", f"""
# @s = an in-game, non-spectating player. `attribute get <scale>` truncates, so a scale of 0.4
# yields the health at which 40% is crossed, keeping the whole check on scores with no NBT read.
{resolve}
""")

	# Every player is checked, not just the ones in a game, so that leaving one takes the overlay
	# off. A player outside a game resolves to tier 0 and falls through to the swap.
	gate: str = f"execute unless entity @s[gamemode=spectator] if score @s {ns}"
	write_versioned_function("player/hurt_tick", f"""
scoreboard players set #hurt_tier {ns}.data 0
{gate}.mp.in_game matches 1 run function {ns}:v{version}/player/hurt_resolve
{gate}.mi.in_game matches 1 run function {ns}:v{version}/player/hurt_resolve
{gate}.zb.in_game matches 1 run function {ns}:v{version}/player/hurt_resolve
execute if score @s {ns}.hurt_fx = #hurt_tier {ns}.data run return 0
function {ns}:v{version}/player/hurt_swap
""")

	remove: str = "\n".join(
		f"execute if score @s {ns}.hurt_fx matches {index + 1} run posteffect remove @s {ns}:{tier.effect_id}"
		for index, tier in enumerate(HURT_TIERS)
	)
	add: str = "\n".join(
		f"execute if score #hurt_tier {ns}.data matches {index + 1} run posteffect add @s {ns}:{tier.effect_id}"
		for index, tier in enumerate(HURT_TIERS)
	)
	write_versioned_function("player/hurt_swap", f"""
{remove}
{add}
scoreboard players operation @s {ns}.hurt_fx = #hurt_tier {ns}.data
""")

