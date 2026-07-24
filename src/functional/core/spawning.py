
# Shared OOB + spawn marker summoning functions
from stewbeet import Mem, write_versioned_function


def write_tp_player_at(mode: str) -> None:
	""" Write ``<mode>/tp_player_at`` — the macro teleporting @s to a spawn position and yaw. """
	write_versioned_function(f"{mode}/tp_player_at", "$tp @s $(x) $(y) $(z) $(yaw) 0")


def write_summon_spawn_at(mode: str, extra_spawn_tags: tuple[str, ...] = ()) -> None:
	""" Write ``<mode>/summon_spawn_at`` — the macro summoning a spawn-point marker.

	Args:
		mode             (str):   Path segment, e.g. "multiplayer" | "zombies" | "missions".
		extra_spawn_tags (tuple): Extra tag suffixes (without the ``<ns>.`` prefix); zombies passes ``("new_spawn",)``.
	"""
	ns: str = Mem.ctx.project_id
	tags: str = f'"{ns}.spawn_point","$(tag)","{ns}.gm_entity"'
	for tag in extra_spawn_tags:
		tags += f',"{ns}.{tag}"'
	write_versioned_function(f"{mode}/summon_spawn_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:[{tags}],data:{{yaw:$(yaw)}}}}
""")


def write_shared_spawning_functions() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		## Summon OOB markers from map data (relative → absolute)
		## Usage: function shared/summon_oob {mode:"multiplayer"}
		write_versioned_function("shared/summon_oob", f"""
$function {ns}:v{version}/shared/load_base_coordinates {{mode:"$(mode)"}}

$data modify storage {ns}:temp _oob_iter set from storage {ns}:$(mode) game.map.out_of_bounds
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/shared/summon_oob_iter
""")

		write_versioned_function("shared/summon_oob_iter", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _oob_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _oob_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _oob_iter[0][2]
scoreboard players operation #rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _oob_pos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _oob_pos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _oob_pos.z double 1 run scoreboard players get #rz {ns}.data
function {ns}:v{version}/shared/summon_oob_at with storage {ns}:temp _oob_pos
data remove storage {ns}:temp _oob_iter[0]
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/shared/summon_oob_iter
""")

		write_versioned_function("shared/summon_oob_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.oob_point","{ns}.gm_entity"]}}
""")
