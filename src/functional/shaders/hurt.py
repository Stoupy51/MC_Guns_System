""" Low-health screen overlay: a red vignette that turns into a pulsing one when close to death.

Two tiers rather than a continuous value, because a post effect has no parameters. Each tier has a
fade-out twin, since regeneration can refill the bar in a second and a removed chain vanishes on
the spot. The heartbeat runs off `Globals.GameTime` instead of the activation clock so it does not
restart on every tier change, and its period divides 24000 so it survives the game-time wrap.
"""
# Imports
from dataclasses import dataclass

from beet import FragmentShader
from stewbeet import Mem, write_versioned_function

from .common import HEADER, timed_effect, uniform

# Constants
FADE_OUT_TICKS: int = 40
""" How long an overlay lingers after the health that caused it is gone. """


@dataclass(frozen=True)
class HurtTier:
	""" One severity of the overlay, picked by health as a fraction of the player's maximum. """
	effect_id: str
	threshold: float
	""" Fraction of max health at or below which this tier applies. """
	tint: list[float]
	""" rgb of the tint, then the vignette strength at the screen edge. """
	pulse: list[float]
	""" Heartbeat amplitude, then its period in ticks. The period must divide 24000. """
	shape: list[float]
	""" Where the vignette starts (0 centre, 1 screen edge), then how far the rim desaturates. """
	aberration: float
	""" Radial colour separation at the rim, in fractions of the screen width. """
	fade_in: float
	""" Ticks the overlay takes to reach full strength. """


HURT_TIERS: list[HurtTier] = [
	HurtTier(effect_id="hurt",          threshold=0.40, tint=[1.0, 0.15, 0.12, 0.55], pulse=[0.00, 24.0], shape=[0.62, 0.35], aberration=0.000, fade_in=5.0),
	HurtTier(effect_id="hurt_critical", threshold=0.20, tint=[1.0, 0.05, 0.05, 0.90], pulse=[0.45, 16.0], shape=[0.40, 0.70], aberration=0.004, fade_in=4.0),
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
    vec2 Shape;        // where the vignette starts (0 centre, 1 edge), then rim desaturation
    vec2 Fade;         // overall strength at the start and at the end of the ramp
    float Aberration;  // radial colour separation at the rim
    float Duration;    // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

// Lub-dub rather than a sine: two gaussian thumps, the second weaker and a fifth of a beat later.
float heartbeat(float phase) {
    float lub = exp(-pow(phase * 14.0, 2.0));
    float dub = exp(-pow((phase - 0.22) * 14.0, 2.0)) * 0.6;
    return lub + dub;
}

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float valueNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x), mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}

float fbm(vec2 p) {
    return valueNoise(p) * 0.55 + valueNoise(p * 2.1 + 17.0) * 0.30 + valueNoise(p * 4.3 + 41.0) * 0.15;
}

void main() {
    float strength = mix(Fade.x, Fade.y, mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration));
    float ticks = GameTime * 24000.0;
    float thump = Pulse.x * heartbeat(fract(ticks / Pulse.y)) * strength;

    // The beat moves the overlay itself rather than brightening it: the red edge surges inward on
    // each thump, and the whole frame jolts a hair toward the centre and dims, like a pulse behind the eyes.
    vec2 uv = mix(texCoord, vec2(0.5), 0.012 * thump);

    // A superellipse hugs the screen edges and corners instead of drawing a circle in the middle,
    // and slowly drifting noise breaks its outline into uneven tendrils creeping in from the rim.
    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 edge = abs(texCoord - 0.5) * 2.0;
    float rim = pow(pow(edge.x, 4.0) + pow(edge.y, 4.0), 0.25);
    float noise = fbm((texCoord - 0.5) * vec2(inSize.x / inSize.y, 1.0) * 3.5 + vec2(0.0, ticks * 0.004));
    float vignette = smoothstep(Shape.x - 0.3 * thump, 1.05, rim + (noise - 0.5) * 0.4) * strength;

    // Pulling the red channel outward and the blue inward reads as a stressed lens at the rim.
    vec3 color = texture(InSampler, uv).rgb;
    if (Aberration > 0.0) {
        vec2 shift = (texCoord - 0.5) * Aberration * 8.0 * vignette;
        color.r = texture(InSampler, uv + shift).r;
        color.b = texture(InSampler, uv - shift).b;
    }
    color *= 1.0 - 0.12 * thump;

    color = mix(color, vec3(dot(color, vec3(0.299, 0.587, 0.114))), clamp(Shape.y * vignette, 0.0, 1.0));
    color = mix(color, color * Tint.rgb + Tint.rgb * 0.35, clamp(Tint.a * vignette, 0.0, 1.0));
    fragColor = vec4(color, 1.0);
}
"""


# Functions
def main() -> None:
	""" Register every tier and its fade-out twin, their shader, and the per-tick health watcher. """
	ns: str = Mem.ctx.project_id
	Mem.ctx.assets[ns].fragment_shaders["post/hurt"] = FragmentShader(HURT_FSH)

	for tier in HURT_TIERS:
		register_variant(ns, tier, fading_out=False)
		register_variant(ns, tier, fading_out=True)
	write_functions(ns)


def register_variant(ns: str, tier: HurtTier, fading_out: bool) -> None:
	""" Register one tier, either ramping in over its fade-in or out over FADE_OUT_TICKS. """
	timed_effect(
		ns,
		f"{tier.effect_id}{'_out' if fading_out else ''}",
		f"{ns}:post/hurt",
		{"HurtConfig": [
			uniform("Tint", "vec4", tier.tint),
			uniform("Pulse", "vec2", tier.pulse),
			uniform("Shape", "vec2", tier.shape),
			uniform("Fade", "vec2", [1.0, 0.0] if fading_out else [0.0, 1.0]),
			uniform("Aberration", "float", tier.aberration),
			uniform("Duration", "float", float(FADE_OUT_TICKS) if fading_out else tier.fade_in),
		]},
	)


def write_functions(ns: str) -> None:
	""" Resolve the tier from the health criterion and swap ids only when it changes. """
	version: str = Mem.ctx.project_version
	levels: list[tuple[int, HurtTier]] = list(enumerate(HURT_TIERS, start=1))

	resolve: str = "\n".join(
		f"""execute store result score #hurt_at {ns}.data run attribute @s minecraft:max_health get {tier.threshold}
execute if score @s {ns}.health <= #hurt_at {ns}.data run scoreboard players set #hurt_tier {ns}.data {level}"""
		for level, tier in levels
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
execute unless score @s {ns}.hurt_fx matches -2147483648.. run scoreboard players set @s {ns}.hurt_fx 0
execute if score @s {ns}.hurt_fx = #hurt_tier {ns}.data run return 0
execute if score #hurt_tier {ns}.data > @s {ns}.hurt_fx run function {ns}:v{version}/player/hurt_rise
execute if score #hurt_tier {ns}.data < @s {ns}.hurt_fx run function {ns}:v{version}/player/hurt_fall
scoreboard players operation @s {ns}.hurt_fx = #hurt_tier {ns}.data
""")

	remove_current: str = "\n".join(
		f"execute if score @s {ns}.hurt_fx matches {level} run posteffect remove @s {ns}:{tier.effect_id}" for level, tier in levels
	)
	add_new: str = "\n".join(
		f"execute if score #hurt_tier {ns}.data matches {level} run posteffect add @s {ns}:{tier.effect_id}" for level, tier in levels
	)

	# Getting worse: the stronger tier ramps in over a few ticks, and a lingering fade would only stack on it.
	write_versioned_function("player/hurt_rise", f"""
function {ns}:v{version}/player/hurt_out_clear
{remove_current}
{add_new}
""")

	start_fade: str = "\n".join(
		f"execute if score @s {ns}.hurt_fx matches {level} run posteffect add @s {ns}:{tier.effect_id}_out" for level, tier in levels
	)
	write_versioned_function("player/hurt_fall", f"""
# Healing: the tier being left hands over to its fade-out twin, while any lower tier still owed ramps in
function {ns}:v{version}/player/hurt_out_clear
{remove_current}
{start_fade}
scoreboard players operation @s {ns}.hurt_out = @s {ns}.hurt_fx
scoreboard players set @s {ns}.hurt_out_until {FADE_OUT_TICKS + 1}
scoreboard players operation @s {ns}.hurt_out_until += #total_tick {ns}.data
{add_new}
""")

	remove_fade: str = "\n".join(
		f"execute if score @s {ns}.hurt_out matches {level} run posteffect remove @s {ns}:{tier.effect_id}_out" for level, tier in levels
	)
	write_versioned_function("player/hurt_out_clear", f"""
{remove_fade}
scoreboard players reset @s {ns}.hurt_out
scoreboard players reset @s {ns}.hurt_out_until
""")

