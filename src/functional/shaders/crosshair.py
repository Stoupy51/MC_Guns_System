""" Movement-driven crosshair, drawn by inverting the pixels under its arms.

The vanilla crosshair sprite is replaced by a transparent pixel, so this shader owns the whole
thing. Spread cannot be passed as a parameter, so every from-to pair of the five movement states
gets its own id and bakes the two ends of the ramp as uniforms.
"""
# Imports
from beet import FragmentShader, Texture
from PIL import Image
from stewbeet import Mem, write_versioned_function

from .common import HEADER, timed_effect, uniform

# Constants
SPREAD_LEVELS: int = 5
""" 0 sneak, 1 standing, 2 walking, 3 sprinting, 4 airborne. """

DURATION: float = 4.0
""" Ticks a spread transition takes. A change arriving mid-ramp restarts from the previous end. """

CROSSHAIR_FSH: str = HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform CrosshairConfig {
    vec2 Spread;     // movement level 0..4, at the start and at the end of the ramp
    float Duration;  // ramp length in ticks
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

void main() {
    fragColor = texture(InSampler, texCoord);

    float spread = mix(Spread.x, Spread.y, mgs_ramp(texture(ClockSampler, vec2(0.5)), GameTime, Duration));

    // The HUD scale is not exposed to post shaders, so it is inferred from the window height the
    // same way vanilla picks its default: roughly 2 at 1080p, 3 at 1440p, 4 at 4K.
    vec2 inSize = vec2(textureSize(InSampler, 0));
    float guiScale = max(1.0, round(inSize.y / 540.0));

    int gap = int(round((1.5 + spread * 2.0) * guiScale));
    int armEnd = gap + int(round(3.0 * guiScale));
    int lineWidth = max(1, int(round(guiScale / 2.0)));

    ivec2 offset = ivec2(gl_FragCoord.xy) - ivec2(inSize) / 2;
    bool horizontal = abs(offset.y) < lineWidth && abs(offset.x) >= gap && abs(offset.x) <= armEnd;
    bool vertical = abs(offset.x) < lineWidth && abs(offset.y) >= gap && abs(offset.y) <= armEnd;
    if (horizontal || vertical) {
        fragColor.rgb = vec3(1.0) - fragColor.rgb;
    }
}
"""


# Functions
def main() -> None:
	""" Register the 25 crosshair ids, blank the vanilla sprite, and wire the spread state machine. """
	ns: str = Mem.ctx.project_id
	if not Mem.ctx.meta.get("mgs_custom_crosshair", False):
		# zoom/main calls these every tick, and a call to a missing function fails the caller at load
		for entry_point in ("zoom/crosshair_spread", "zoom/crosshair_base", "zoom/crosshair_clear"):
			write_versioned_function(entry_point, "# Custom crosshair disabled (mgs_custom_crosshair)\n")
		return

	Mem.ctx.assets[ns].fragment_shaders["post/crosshair"] = FragmentShader(CROSSHAIR_FSH)
	Mem.ctx.assets["minecraft"].textures["gui/sprites/hud/crosshair"] = Texture(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))

	for start in range(SPREAD_LEVELS):
		for end in range(SPREAD_LEVELS):
			timed_effect(
				ns,
				f"crosshair_{start}_{end}",
				f"{ns}:post/crosshair",
				{"CrosshairConfig": [
					uniform("Spread", "vec2", [float(start), float(end)]),
					uniform("Duration", "float", DURATION),
				]},
			)
	write_functions(ns)


def write_functions(ns: str) -> None:
	""" Resolve the movement state every tick and swap ids only on a change. """
	version: str = Mem.ctx.project_version

	# Priority matches the accuracy system: airborne beats sprint beats walk beats sneak.
	# Sneaking in the air is a lunge rather than a jump, so it reads as walking.
	write_versioned_function("zoom/crosshair_spread", f"""
scoreboard players set #spread {ns}.data 1
execute if predicate {ns}:v{version}/is_moving unless predicate {ns}:v{version}/is_sprinting run scoreboard players set #spread {ns}.data 2
execute if predicate {ns}:v{version}/is_sprinting run scoreboard players set #spread {ns}.data 3
execute if predicate {ns}:v{version}/is_sneaking run scoreboard players set #spread {ns}.data 0
execute unless predicate {ns}:v{version}/is_on_ground run scoreboard players set #spread {ns}.data 4
execute unless predicate {ns}:v{version}/is_on_ground if predicate {ns}:v{version}/is_sneaking run scoreboard players set #spread {ns}.data 2
function {ns}:v{version}/zoom/crosshair_apply
""")

	# The vanilla sprite is blanked for everyone, so without a gun this still has to draw something.
	write_versioned_function("zoom/crosshair_base", f"""
scoreboard players set #spread {ns}.data 1
function {ns}:v{version}/zoom/crosshair_apply
""")

	write_versioned_function("zoom/crosshair_apply", f"""
# @s = any player, #spread = the level to show
execute unless score @s {ns}.cross_to matches -2147483648.. run return run function {ns}:v{version}/zoom/crosshair_first
execute if score @s {ns}.cross_to = #spread {ns}.data run return 0
function {ns}:v{version}/zoom/crosshair_swap
""")

	write_versioned_function("zoom/crosshair_first", f"""
# @s = a player who has no crosshair id yet, so the ramp starts and ends on the same level
data modify storage {ns}:input crosshair set value {{"from":0,"to":0}}
execute store result storage {ns}:input crosshair.to int 1 run scoreboard players get #spread {ns}.data
data modify storage {ns}:input crosshair.from set from storage {ns}:input crosshair.to
function {ns}:v{version}/zoom/crosshair_add with storage {ns}:input crosshair
scoreboard players operation @s {ns}.cross_from = #spread {ns}.data
scoreboard players operation @s {ns}.cross_to = #spread {ns}.data
""")

	write_versioned_function("zoom/crosshair_swap", f"""
# The applied id is crosshair_<cross_from>_<cross_to>, so the new ramp starts where that one ended
data modify storage {ns}:input crosshair set value {{"from":0,"to":0,"next":0}}
execute store result storage {ns}:input crosshair.from int 1 run scoreboard players get @s {ns}.cross_from
execute store result storage {ns}:input crosshair.to int 1 run scoreboard players get @s {ns}.cross_to
execute store result storage {ns}:input crosshair.next int 1 run scoreboard players get #spread {ns}.data
function {ns}:v{version}/zoom/crosshair_replace with storage {ns}:input crosshair
scoreboard players operation @s {ns}.cross_from = @s {ns}.cross_to
scoreboard players operation @s {ns}.cross_to = #spread {ns}.data
""")

	write_versioned_function("zoom/crosshair_clear", f"""
# @s = a player who is aiming down sights or no longer holding a gun
execute unless score @s {ns}.cross_to matches -2147483648.. run return 0
data modify storage {ns}:input crosshair set value {{"from":0,"to":0}}
execute store result storage {ns}:input crosshair.from int 1 run scoreboard players get @s {ns}.cross_from
execute store result storage {ns}:input crosshair.to int 1 run scoreboard players get @s {ns}.cross_to
function {ns}:v{version}/zoom/crosshair_remove with storage {ns}:input crosshair
scoreboard players reset @s {ns}.cross_from
scoreboard players reset @s {ns}.cross_to
""")

	write_versioned_function("zoom/crosshair_add", f"""
$posteffect add @s {ns}:crosshair_$(from)_$(to)
""")
	write_versioned_function("zoom/crosshair_remove", f"""
$posteffect remove @s {ns}:crosshair_$(from)_$(to)
""")
	write_versioned_function("zoom/crosshair_replace", f"""
$posteffect remove @s {ns}:crosshair_$(from)_$(to)
$posteffect add @s {ns}:crosshair_$(to)_$(next)
""")

