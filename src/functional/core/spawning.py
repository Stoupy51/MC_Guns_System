
# Shared OOB marker summoning functions
from stewbeet import Mem, write_versioned_function


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

