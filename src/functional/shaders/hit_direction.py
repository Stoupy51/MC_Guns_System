""" Hit direction indicator: a red arc ringing the crosshair, pointing at whoever shot the player.

The direction cannot be passed to a shader, so each of the SECTORS directions is its own id, and each exists twice.
Two hits one after the other swap between the two slots, so a new hit is always a brand new chain with a fresh clock.
"""
# Imports
from beet import FragmentShader
from stewbeet import POST_SHADER_HEADER, Mem, post_uniform, timed_post_effect, write_versioned_function

# Constants
SECTORS: int = 36
""" Directions the indicator can tell apart. Must divide 36000 (yaw range in centidegrees) so a sector stays whole. """

FULL_TICKS: float = 8.0
""" How long the arc stays at full strength. """

FADE_END_TICKS: float = 14.0
""" When the arc has faded out completely. """

HOLD_TICKS: int = 15
""" Ticks the id stays applied. It must cover FADE_END_TICKS or the tail gets cut off. """

ARC_SPAN: float = 90.0
""" Degrees covered by the arc, two sectors wide. """

ARC_RADIUS: float = 0.14
ARC_WIDTH: float = 0.014
""" Outer ring radius and thickness, as fractions of the screen height: the HUD scale is not exposed to post shaders. """

HIT_FSH: str = POST_SHADER_HEADER + """
#include <minecraft:globals.glsl>
#include <mgs:clock.glsl>

uniform sampler2D ClockSampler;
uniform sampler2D InSampler;

layout(std140) uniform HitConfig {
    float Direction;  // degrees clockwise from the top of the screen
};

layout(location = 0) in vec2 texCoord;
layout(location = 0) out vec4 fragColor;

#define COLOR vec3(1.0, 0.165, 0.165)
#define FULL __FULL__
#define FADE_END __FADE_END__
#define SPAN __SPAN__
#define RADIUS __RADIUS__
#define WIDTH __WIDTH__

void main() {
    fragColor = texture(InSampler, texCoord);

    float life = clamp((FADE_END - clock_elapsed(texture(ClockSampler, vec2(0.5)), GameTime)) / (FADE_END - FULL), 0.0, 1.0);
    if (life <= 0.0) return;

    vec2 inSize = vec2(textureSize(InSampler, 0));
    vec2 offset = (texCoord - 0.5) * vec2(inSize.x / inSize.y, 1.0);

    // Wrapped into -180..180 so the seam behind the player fades instead of cutting.
    float delta = abs(mod(degrees(atan(offset.x, offset.y)) - Direction + 180.0, 360.0) - 180.0);
    float along = clamp(1.0 - delta / (SPAN / 2.0), 0.0, 1.0);

    // Solid core with soft edges: 2.5 widens the plateau so the ring keeps its thickness.
    float across = clamp((1.0 - abs(length(offset) - RADIUS) / (WIDTH / 2.0)) * 2.5, 0.0, 1.0);

    fragColor.rgb = mix(fragColor.rgb, COLOR, along * across * life);
}
""".replace("__FULL__", str(FULL_TICKS)).replace("__FADE_END__", str(FADE_END_TICKS)).replace("__SPAN__", str(ARC_SPAN)).replace("__RADIUS__", str(ARC_RADIUS)).replace("__WIDTH__", str(ARC_WIDTH))


# Functions
def main() -> None:
	""" Register every sector id, its shader, and the functions that apply and retire them. """
	ns: str = Mem.ctx.project_id
	assert 36000 % SECTORS == 0, f"SECTORS={SECTORS} must divide 36000 (yaw range in centidegrees)"

	Mem.ctx.assets[ns].fragment_shaders["post/hit_direction"] = FragmentShader(HIT_FSH)
	for sector in range(SECTORS):
		for slot in (0, 1):
			timed_post_effect(f"hit_dir_{sector}_{slot}", f"{ns}:post/hit_direction", {
				"HitConfig": [post_uniform("Direction", "float", 360.0 / SECTORS * sector)],
			})
	write_functions(ns)


def write_functions(ns: str) -> None:
	""" The damage listener, then the apply, reorder and retire steps. """
	version: str = Mem.ctx.project_version

	# Centidegrees, so sector widths stay whole for any SECTORS (36000 / 32 = 1125).
	step: int = 36000 // SECTORS
	write_versioned_function("weapon/hit_direction", f"""
# Player victims only.
execute unless entity @s[type=player] run return 0

# Explosion self-hits have no direction (hitscan cannot self-hit).
execute if entity @s[tag={ns}.temp_shooter] run return 0

scoreboard players set #hit_src {ns}.data 0
execute at @s if entity @n[tag={ns}.ticking] run scoreboard players set #hit_src {ns}.data 1
execute at @s if score #hit_src {ns}.data matches 0 if entity @n[tag={ns}.temp_shooter] run scoreboard players set #hit_src {ns}.data 2
execute if score #hit_src {ns}.data matches 0 run return 0

# Yaw toward the shooter (x100) from a scratch marker at the victim facing the shooter.
execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.hit_dir_marker"]}}
execute at @s if score #hit_src {ns}.data matches 1 run tp @n[tag={ns}.hit_dir_marker] ~ ~ ~ facing entity @n[tag={ns}.ticking] eyes
execute at @s if score #hit_src {ns}.data matches 2 run tp @n[tag={ns}.hit_dir_marker] ~ ~ ~ facing entity @n[tag={ns}.temp_shooter] eyes
execute at @s store result score #hit_dir {ns}.data run data get entity @n[tag={ns}.hit_dir_marker] Rotation[0] 100
execute at @s run kill @n[tag={ns}.hit_dir_marker]

# Sector 0..{SECTORS - 1} from the victim's facing (0 front, clockwise; scoreboard %= is floorMod); the half-sector offset centres each sector on its direction.
execute store result score #hit_yaw {ns}.data run data get entity @s Rotation[0] 100
scoreboard players operation #hit_dir {ns}.data -= #hit_yaw {ns}.data
scoreboard players add #hit_dir {ns}.data {step // 2}
scoreboard players operation #hit_dir {ns}.data %= #36000 {ns}.data
scoreboard players operation #hit_dir {ns}.data /= #{step} {ns}.data

function {ns}:v{version}/player/hit_dir_show
""", tags=[f"{ns}:signals/damage"])

	write_versioned_function("player/hit_dir_show", f"""
# @s = the victim, #hit_dir = the sector to show. The other slot makes the new id differ from the applied one.
function {ns}:v{version}/player/hit_dir_clear
execute store success score @s {ns}.hit_dir_slot if score @s {ns}.hit_dir_slot matches 0
scoreboard players operation @s {ns}.hit_dir_sector = #hit_dir {ns}.data

data modify storage {ns}:input hit_dir set value {{"sector":0,"slot":0}}
execute store result storage {ns}:input hit_dir.sector int 1 run scoreboard players get @s {ns}.hit_dir_sector
execute store result storage {ns}:input hit_dir.slot int 1 run scoreboard players get @s {ns}.hit_dir_slot
function {ns}:v{version}/player/hit_dir_add with storage {ns}:input hit_dir

scoreboard players set @s {ns}.hit_dir_off {HOLD_TICKS}
scoreboard players operation @s {ns}.hit_dir_off += #total_tick {ns}.data
""")

	write_versioned_function("player/hit_dir_clear", f"""
# @s = a player, possibly with an arc applied
execute unless score @s {ns}.hit_dir_sector matches -2147483648.. run return 0
data modify storage {ns}:input hit_dir set value {{"sector":0,"slot":0}}
execute store result storage {ns}:input hit_dir.sector int 1 run scoreboard players get @s {ns}.hit_dir_sector
execute store result storage {ns}:input hit_dir.slot int 1 run scoreboard players get @s {ns}.hit_dir_slot
function {ns}:v{version}/player/hit_dir_remove with storage {ns}:input hit_dir
scoreboard players reset @s {ns}.hit_dir_sector
""")

	# Zoom and flash re-add their ids at the end of the list, which would magnify the arc along with the scene.
	# Same id in one tick: the client keeps its clock, only the order changes.
	write_versioned_function("player/hit_dir_to_back", f"""
execute unless score @s {ns}.hit_dir_sector matches -2147483648.. run return 0
data modify storage {ns}:input hit_dir set value {{"sector":0,"slot":0}}
execute store result storage {ns}:input hit_dir.sector int 1 run scoreboard players get @s {ns}.hit_dir_sector
execute store result storage {ns}:input hit_dir.slot int 1 run scoreboard players get @s {ns}.hit_dir_slot
function {ns}:v{version}/player/hit_dir_remove with storage {ns}:input hit_dir
function {ns}:v{version}/player/hit_dir_add with storage {ns}:input hit_dir
""")

	write_versioned_function("player/hit_dir_expire", f"""
# @s = a player whose arc has faded out
function {ns}:v{version}/player/hit_dir_clear
scoreboard players reset @s {ns}.hit_dir_off
""")

	write_versioned_function("player/hit_dir_add", f"$posteffect add @s {ns}:hit_dir_$(sector)_$(slot)\n")
	write_versioned_function("player/hit_dir_remove", f"$posteffect remove @s {ns}:hit_dir_$(sector)_$(slot)\n")

