""" Low-health screen overlay: a red vignette that turns into a pulsing one when close to death.

A post effect has no parameters, so each id is a transition from one tier's look to another's and
everything the overlay shows (tint, edge, heartbeat, colour split) blends between the two. Exactly
one id is applied at a time. Healing waits for the bar to settle before fading, so a fast
regeneration crossing both thresholds plays one smooth fade instead of two cut-off ones.
"""
# Imports
from dataclasses import dataclass

from beet import FragmentShader
from stewbeet import Mem, write_versioned_function

from .common import HEADER, timed_effect, uniform

# Constants
RISE_TICKS: float = 5.0
""" Getting worse: the overlay reaches its new look quickly, like the hit that caused it. """

FALL_TICKS: int = 40
""" Healing: two seconds from one look to the next, down to nothing at all. """

FALL_DEBOUNCE: int = 10
""" Ticks a lower tier must hold before the fade starts, so regeneration ends up as one transition. """

HEARTBEAT_TICKS: float = 16.0
""" One beat every 0.8 s. Shared by every tier so blending tiers never makes the rhythm stutter. """


@dataclass(frozen=True)
class HurtLook:
	""" Everything the overlay shows at one severity, blended between two looks during a transition. """
	tint: list[float]
	""" rgb of the tint, then the vignette strength at the screen edge. """
	shape: list[float]
	""" Where the vignette starts (0 centre, 1 screen edge), then how far the rim desaturates. """
	heartbeat: float
	""" How hard each beat pushes the edge inward and jolts the frame. """
	aberration: float
	""" Radial colour separation at the rim, in fractions of the screen width. """

	def cleared(self) -> HurtLook:
		""" The same look at zero strength, so fading to nothing keeps its shape and colour. """
		return HurtLook(tint=[*self.tint[:3], 0.0], shape=[self.shape[0], 0.0], heartbeat=0.0, aberration=0.0)


@dataclass(frozen=True)
class HurtTier:
	""" One severity, picked by health as a fraction of the player's maximum. """
	threshold: float
	""" Fraction of max health at or below which this tier applies. """
	look: HurtLook


HURT_TIERS: list[HurtTier] = [
	HurtTier(threshold=0.40, look=HurtLook(tint=[1.0, 0.15, 0.12, 0.55], shape=[0.62, 0.35], heartbeat=0.00, aberration=0.000)),
	HurtTier(threshold=0.20, look=HurtLook(tint=[1.0, 0.05, 0.05, 0.90], shape=[0.40, 0.70], heartbeat=0.45, aberration=0.004)),
]
""" Ordered weakest first. Level 0 is no overlay; tier N here is level N + 1. """

LEVELS: range = range(len(HURT_TIERS) + 1)
""" Overlay levels, 0 being none. """

TRANSITIONS: list[tuple[int, int]] = [(start, end) for start in LEVELS for end in LEVELS if (start, end) != (0, 0)]
""" Every applied id as (from level, to level). A same-level pair holds that look. """

HURT_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform HurtConfig {
    vec4 TintFrom;         // rgb tint, a = vignette strength at the screen edge
    vec4 TintTo;
    vec4 Shape;            // xy = look being left (vignette start, rim desaturation), zw = look being reached
    vec4 PulseAberration;  // xy = heartbeat strength from, to; zw = colour split from, to
    float Duration;        // ticks the blend takes
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

#define HEARTBEAT_TICKS __HEARTBEAT_TICKS__
#define JOLT_ZOOM 0.02   // how far the frame is pulled toward the centre on a full-strength beat
#define JOLT_DIM 0.20    // how much it darkens on that beat

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
    float t = mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration);
    vec4 tint = mix(TintFrom, TintTo, t);
    vec2 shape = mix(Shape.xy, Shape.zw, t);
    float aberration = mix(PulseAberration.z, PulseAberration.w, t);

    // The beat moves the overlay itself rather than brightening it: the red edge surges inward on
    // each thump, and the whole frame jolts a hair toward the centre and dims, like a pulse behind the eyes.
    float ticks = GameTime * 24000.0;
    float thump = mix(PulseAberration.x, PulseAberration.y, t) * heartbeat(fract(ticks / HEARTBEAT_TICKS));
    vec2 uv = mix(texCoord, vec2(0.5), JOLT_ZOOM * thump);

    // A superellipse hugs the screen edges and corners instead of drawing a circle in the middle,
    // and slowly drifting noise breaks its outline into uneven tendrils creeping in from the rim.
    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 edge = abs(texCoord - 0.5) * 2.0;
    float rim = pow(pow(edge.x, 4.0) + pow(edge.y, 4.0), 0.25);
    float noise = fbm((texCoord - 0.5) * vec2(inSize.x / inSize.y, 1.0) * 3.5 + vec2(0.0, ticks * 0.004));
    float vignette = smoothstep(shape.x - 0.3 * thump, 1.05, rim + (noise - 0.5) * 0.4);

    // Pulling the red channel outward and the blue inward reads as a stressed lens at the rim.
    vec3 color = texture(InSampler, uv).rgb;
    if (aberration > 0.0) {
        vec2 shift = (texCoord - 0.5) * aberration * 8.0 * vignette;
        color.r = texture(InSampler, uv + shift).r;
        color.b = texture(InSampler, uv - shift).b;
    }
    color *= 1.0 - JOLT_DIM * thump;

    color = mix(color, vec3(dot(color, vec3(0.299, 0.587, 0.114))), clamp(shape.y * vignette, 0.0, 1.0));
    color = mix(color, color * tint.rgb + tint.rgb * 0.35, clamp(tint.a * vignette, 0.0, 1.0));
    fragColor = vec4(color, 1.0);
}
""".replace("__HEARTBEAT_TICKS__", str(HEARTBEAT_TICKS))


# Functions
def main() -> None:
	""" Register every transition id, the shader, and the per-tick health watcher. """
	ns: str = Mem.ctx.project_id
	Mem.ctx.assets[ns].fragment_shaders["post/hurt"] = FragmentShader(HURT_FSH)

	for start, end in TRANSITIONS:
		register_transition(ns, start, end)
	write_functions(ns)


def look_of(level: int, partner: int) -> HurtLook:
	""" The look shown at `level`; level 0 borrows `partner`'s colour and shape at zero strength. """
	if level > 0:
		return HURT_TIERS[level - 1].look
	return HURT_TIERS[max(partner, 1) - 1].look.cleared()


def register_transition(ns: str, start: int, end: int) -> None:
	""" Register `hurt_<start>_<end>`, blending one look into the other and holding the second. """
	source: HurtLook = look_of(start, end)
	target: HurtLook = look_of(end, start)
	duration: float = RISE_TICKS if end > start else float(FALL_TICKS) if end < start else 1.0
	timed_effect(
		ns,
		f"hurt_{start}_{end}",
		f"{ns}:post/hurt",
		{"HurtConfig": [
			uniform("TintFrom", "vec4", source.tint),
			uniform("TintTo", "vec4", target.tint),
			uniform("Shape", "vec4", [*source.shape, *target.shape]),
			uniform("PulseAberration", "vec4", [source.heartbeat, target.heartbeat, source.aberration, target.aberration]),
			uniform("Duration", "float", duration),
		]},
	)


def write_functions(ns: str) -> None:
	""" Resolve the level from the health criterion and move the one applied id toward it. """
	version: str = Mem.ctx.project_version

	resolve: str = "\n".join(
		f"""execute store result score #hurt_at {ns}.data run attribute @s minecraft:max_health get {tier.threshold}
execute if score @s {ns}.health <= #hurt_at {ns}.data run scoreboard players set #hurt_tier {ns}.data {level}"""
		for level, tier in enumerate(HURT_TIERS, start=1)
	)
	write_versioned_function("player/hurt_resolve", f"""
# @s = an in-game, non-spectating player. `attribute get <scale>` truncates, so a scale of 0.4
# yields the health at which 40% is crossed, keeping the whole check on scores with no NBT read.
{resolve}
""")

	# Every player is checked, not just the ones in a game, so that leaving one takes the overlay
	# off. A player outside a game resolves to level 0 and fades out like any heal.
	gate: str = f"execute unless entity @s[gamemode=spectator] if score @s {ns}"
	write_versioned_function("player/hurt_tick", f"""
scoreboard players set #hurt_tier {ns}.data 0
{gate}.mp.in_game matches 1 run function {ns}:v{version}/player/hurt_resolve
{gate}.mi.in_game matches 1 run function {ns}:v{version}/player/hurt_resolve
{gate}.zb.in_game matches 1 run function {ns}:v{version}/player/hurt_resolve
execute unless score @s {ns}.hurt_fx matches -2147483648.. run scoreboard players set @s {ns}.hurt_fx 0
execute if score @s {ns}.hurt_fx = #hurt_tier {ns}.data run return run scoreboard players reset @s {ns}.hurt_pending
execute if score #hurt_tier {ns}.data > @s {ns}.hurt_fx run return run function {ns}:v{version}/player/hurt_swap

# Healing: wait for the bar to settle, so crossing several thresholds becomes a single fade
scoreboard players add @s {ns}.hurt_pending 1
execute if score @s {ns}.hurt_pending matches {FALL_DEBOUNCE}.. run function {ns}:v{version}/player/hurt_swap
""")

	removes: str = "\n".join(
		f"execute if score @s {ns}.hurt_from matches {start} if score @s {ns}.hurt_fx matches {end} run posteffect remove @s {ns}:hurt_{start}_{end}"
		for start, end in TRANSITIONS
	)
	adds: str = "\n".join(
		f"execute if score #hurt_start {ns}.data matches {start} if score #hurt_tier {ns}.data matches {end} run posteffect add @s {ns}:hurt_{start}_{end}"
		for start, end in TRANSITIONS
	)
	write_versioned_function("player/hurt_swap", f"""
# Start from the look the current id ends on. A hit landing mid-fade starts from the look that fade
# was leaving instead, since that is still close to what is on screen.
scoreboard players operation #hurt_start {ns}.data = @s {ns}.hurt_fx
execute if score #hurt_tier {ns}.data > @s {ns}.hurt_fx if score @s {ns}.hurt_fall_until > #total_tick {ns}.data run scoreboard players operation #hurt_start {ns}.data = @s {ns}.hurt_from

# The new pair always differs from the old one (its end level changed), so this is never the same id twice
{removes}
{adds}
scoreboard players operation @s {ns}.hurt_from = #hurt_start {ns}.data
scoreboard players operation @s {ns}.hurt_fx = #hurt_tier {ns}.data
scoreboard players reset @s {ns}.hurt_pending
scoreboard players reset @s {ns}.hurt_fall_until
scoreboard players reset @s {ns}.hurt_out_until
execute if score #hurt_tier {ns}.data < #hurt_start {ns}.data run function {ns}:v{version}/player/hurt_schedule_fall
""")

	write_versioned_function("player/hurt_schedule_fall", f"""
scoreboard players set @s {ns}.hurt_fall_until {FALL_TICKS}
scoreboard players operation @s {ns}.hurt_fall_until += #total_tick {ns}.data

# Fading to nothing: once the fade has played, the id comes off entirely
execute if score #hurt_tier {ns}.data matches 0 run scoreboard players operation @s {ns}.hurt_out_until = @s {ns}.hurt_fall_until
execute if score #hurt_tier {ns}.data matches 0 run scoreboard players add @s {ns}.hurt_out_until 1
""")

	fade_removes: str = "\n".join(
		f"execute if score @s {ns}.hurt_from matches {start} if score @s {ns}.hurt_fx matches 0 run posteffect remove @s {ns}:hurt_{start}_0"
		for start, end in TRANSITIONS if end == 0
	)
	write_versioned_function("player/hurt_out_clear", f"""
# @s = a player whose fade to nothing has finished playing
{fade_removes}
scoreboard players set @s {ns}.hurt_from 0
scoreboard players reset @s {ns}.hurt_fall_until
scoreboard players reset @s {ns}.hurt_out_until
""")

