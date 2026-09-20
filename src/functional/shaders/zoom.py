""" Aim-down-sights magnification and scope barrel distortion.

Each scope level ships two ids, one that ramps the effect in and one that ramps it out, because a
removed chain stops rendering on the frame the packet lands and can never animate its own exit.
"""
# Imports
from dataclasses import dataclass

from beet import FragmentShader
from stewbeet import Mem, write_versioned_function

from .common import HEADER, timed_effect, uniform

# Constants
IN_TICKS: float = 7.0
""" Ramp into the scope, matching the feel of a 0.12-per-frame lerp at 60 fps. """

OUT_TICKS: float = 4.0
""" Ramp out. Kept short: re-aiming inside this window restarts from zero and visibly snaps. """

DISTORTION: float = 0.55
""" Barrel strength of the lens, unitless. """


@dataclass(frozen=True)
class ScopeLevel:
	""" One aim-down-sights state, named by the `scope_level` stat the weapon carries. """
	level: int
	magnify: float
	""" How far the UV is pulled toward the centre at full zoom, 0.45 being roughly 1.82x. """
	lens_radius: float
	""" Screen-space radius of the barrel distortion, 0 for weapons with no scope. """


SCOPE_LEVELS: list[ScopeLevel] = [
	ScopeLevel(level=2, magnify=0.25, lens_radius=0.00),
	ScopeLevel(level=3, magnify=0.30, lens_radius=0.14),
	ScopeLevel(level=4, magnify=0.45, lens_radius=0.20),
]
""" Level 2 is the centre-only pull used by weapons without a scope, so it has no lens. """

ZOOM_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform ZoomConfig {
    vec2 Magnify;    // UV pull toward the centre, at the start and at the end of the ramp
    vec2 Barrel;     // lens distortion strength, at the start and at the end of the ramp
    vec2 Lens;       // x = scope magnification divisor, y = lens radius, 0 disables the lens
    float Duration;  // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

vec4 cubic(float v) {
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    return vec4(x, y, z, 6.0 - x - y - z) * (1.0 / 6.0);
}

vec4 textureBicubic(sampler2D samp, vec2 texCoords, vec2 texSize) {
    vec2 oneTexel = 1.0 / texSize;
    texCoords = texCoords * texSize - 0.5;
    vec2 fxy = fract(texCoords);
    texCoords -= fxy;

    vec4 xcubic = cubic(fxy.x);
    vec4 ycubic = cubic(fxy.y);

    vec4 c = texCoords.xxyy + vec2(-0.5, 1.5).xyxy;
    vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
    vec4 offsetbc = (c + vec4(xcubic.yw, ycubic.yw) / s) * oneTexel.xxyy;

    vec4 sample0 = texture(samp, offsetbc.xz);
    vec4 sample1 = texture(samp, offsetbc.yz);
    vec4 sample2 = texture(samp, offsetbc.xw);
    vec4 sample3 = texture(samp, offsetbc.yw);

    float sx = s.x / (s.x + s.y);
    float sy = s.z / (s.z + s.w);
    return mix(mix(sample3, sample2, sx), mix(sample1, sample0, sx), sy);
}

void main() {
    float t = mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration);
    float magnify = mix(Magnify.x, Magnify.y, t);
    float barrel = mix(Barrel.x, Barrel.y, t);

    fragColor = texture(InSampler, mix(texCoord, vec2(0.5), magnify));

    vec2 inSize = vec2(textureSize(InSampler, 0));
    float aspectRatio = inSize.x / inSize.y;
    vec2 screenCoord = (texCoord - vec2(0.5)) * vec2(aspectRatio, 1.0);
    if (Lens.y <= 0.0 || barrel <= 0.0 || length(screenCoord) >= Lens.y) return;

    float d = length(screenCoord * barrel / Lens.y);
    float r = atan(d, sqrt(1.0 - d * d)) / 3.1415926535;
    float theta = atan(screenCoord.y, screenCoord.x);
    vec2 lensCoord = vec2(cos(theta), sin(theta)) * r / Lens.x;
    vec2 pixCoord = mix(lensCoord * vec2(1.0 / aspectRatio, 1.0) + vec2(0.5), vec2(0.5), magnify);
    fragColor = textureBicubic(InSampler, pixCoord, inSize);
}
"""


# Functions
def main() -> None:
	""" Register the six zoom ids, their shader, and the aim-down-sights wiring. """
	ns: str = Mem.ctx.project_id
	Mem.ctx.assets[ns].fragment_shaders["post/zoom"] = FragmentShader(ZOOM_FSH)

	for scope in SCOPE_LEVELS:
		register_variant(ns, scope, fading_out=False)
		register_variant(ns, scope, fading_out=True)
	write_functions(ns)


def register_variant(ns: str, scope: ScopeLevel, fading_out: bool) -> None:
	""" Register one direction of one scope level, the ramp running forwards or in reverse. """
	magnify: list[float] = [scope.magnify, 0.0] if fading_out else [0.0, scope.magnify]
	barrel: list[float] = [DISTORTION, 0.0] if fading_out else [0.0, DISTORTION]
	timed_effect(
		ns,
		f"zoom_{scope.level}{'_out' if fading_out else ''}",
		f"{ns}:post/zoom",
		{"ZoomConfig": [
			uniform("Magnify", "vec2", magnify),
			uniform("Barrel", "vec2", barrel),
			uniform("Lens", "vec2", [float(scope.level), scope.lens_radius]),
			uniform("Duration", "float", OUT_TICKS if fading_out else IN_TICKS),
		]},
	)


def write_functions(ns: str) -> None:
	""" Swap ids on the aim-down-sights edges and retire the fade-out once it has played. """
	version: str = Mem.ctx.project_version
	swap_in: str = "\n".join(
		f"execute if score #scope_level {ns}.data matches {scope.level} run function {ns}:v{version}/zoom/fx_enter_{scope.level}"
		for scope in SCOPE_LEVELS
	)

	# `scope_level` is 3 or 4 for scoped weapons and anything else means the centre-only pull.
	write_versioned_function("zoom/fx_enter", f"""
# @s = a player who just entered aim-down-sights
scoreboard players set #scope_level {ns}.data 2
execute store result score #scope_level {ns}.data run data get storage {ns}:gun all.stats.scope_level
execute unless score #scope_level {ns}.data matches 3..4 run scoreboard players set #scope_level {ns}.data 2
function {ns}:v{version}/zoom/fx_clear
{swap_in}
""")

	# Aiming again mid-fade takes the fade-out straight off instead of handing it a successor, so the
	# two directions never stack. The new ramp restarts from zero, which is visible if you tap fast.
	clear: str = "\n".join(
		f"""execute if score @s {ns}.zoom_fx matches {scope.level} run posteffect remove @s {ns}:zoom_{scope.level}
execute if score @s {ns}.zoom_fx matches -{scope.level} run posteffect remove @s {ns}:zoom_{scope.level}_out"""
		for scope in SCOPE_LEVELS
	)
	write_versioned_function("zoom/fx_clear", f"""
{clear}
scoreboard players set @s {ns}.zoom_fx 0
scoreboard players reset @s {ns}.zoom_fx_off
""")

	for scope in SCOPE_LEVELS:
		write_versioned_function(f"zoom/fx_enter_{scope.level}", f"""
posteffect add @s {ns}:zoom_{scope.level}
scoreboard players set @s {ns}.zoom_fx {scope.level}
scoreboard players reset @s {ns}.zoom_fx_off
""")

	leave: str = "\n".join(
		f"""execute if score @s {ns}.zoom_fx matches {scope.level} run posteffect remove @s {ns}:zoom_{scope.level}
execute if score @s {ns}.zoom_fx matches {scope.level} run posteffect add @s {ns}:zoom_{scope.level}_out
execute if score @s {ns}.zoom_fx matches {scope.level} run scoreboard players set @s {ns}.zoom_fx -{scope.level}"""
		for scope in SCOPE_LEVELS
	)
	write_versioned_function("zoom/fx_leave", f"""
# Hand the ramp over to the matching fade-out id, which plays itself out and is retired by fx_tick
execute unless score @s {ns}.zoom_fx matches 1.. run return 0
{leave}
scoreboard players set @s {ns}.zoom_fx_off {int(OUT_TICKS) + 1}
""")

	expire: str = "\n".join(
		f"execute if score @s {ns}.zoom_fx matches -{scope.level} run posteffect remove @s {ns}:zoom_{scope.level}_out"
		for scope in SCOPE_LEVELS
	)
	write_versioned_function("zoom/fx_tick", f"""
# @s = a player whose fade-out is still applied
scoreboard players remove @s {ns}.zoom_fx_off 1
execute if score @s {ns}.zoom_fx_off matches 1.. run return 0
{expire}
scoreboard players set @s {ns}.zoom_fx 0
scoreboard players reset @s {ns}.zoom_fx_off
""")

