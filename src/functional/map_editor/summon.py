""" Rebuilding a saved map's markers, one iterator and marker summon per element kind. """
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS, EDITOR_MODES, MODE_LIST


# Classes
@dataclass(frozen=True)
class SummonIterator:
	""" How one save type's markers are rebuilt: a temp copy of the saved list, walked by a recursive function. """
	storage: str
	""" `{ns}:temp` path of the list being walked. """
	function: str
	""" Iterator under `maps/editor/`. """
	tagged: bool
	""" Whether the iterator reads the element tag to put on its markers from `<storage>_tag`. """


# Constants
SUMMON_ITERATORS: dict[str, SummonIterator] = {
	"spawn":           SummonIterator(storage="_spawn_iter",       function="summon_spawn_iter",           tagged=True),
	"point":           SummonIterator(storage="_point_iter",       function="summon_point_iter",           tagged=True),
	"enemy":           SummonIterator(storage="_enemy_edit_iter",  function="summon_enemy_edit_iter",      tagged=False),
	"start_command":   SummonIterator(storage="_start_cmd_iter",   function="summon_start_command_iter",   tagged=False),
	"respawn_command": SummonIterator(storage="_respawn_cmd_iter", function="summon_respawn_command_iter", tagged=False),
	"zb_object":       SummonIterator(storage="_zb_iter",          function="summon_zb_object_iter",       tagged=True),
}
""" Iterator of every save type that has markers, keyed by `ElementDef.save_type`. """


# Functions
def write_editor_summon() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	summon_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_mode matches {i} run function {ns}:v{version}/maps/editor/summon_existing/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/summon_existing", f"""
# Base coordinates marker, in every mode.
execute store result score #bx {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #by {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #bz {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]
execute store result storage {ns}:temp _pos.x double 1 run scoreboard players get #bx {ns}.data
execute store result storage {ns}:temp _pos.y double 1 run scoreboard players get #by {ns}.data
execute store result storage {ns}:temp _pos.z double 1 run scoreboard players get #bz {ns}.data
function {ns}:v{version}/maps/editor/summon_base_marker with storage {ns}:temp _pos

execute if data storage {ns}:temp map_edit.map.start_function run data modify entity @n[tag={ns}.element.base_coordinates] data.start_function set from storage {ns}:temp map_edit.map.start_function
execute if data storage {ns}:temp map_edit.map.tick_function run data modify entity @n[tag={ns}.element.base_coordinates] data.tick_function set from storage {ns}:temp map_edit.map.tick_function

{summon_dispatch}
""")

	for mode_key, mode_info in EDITOR_MODES.items():
		summon_lines: list[str] = [
			line
			for etype in mode_info.slots if ALL_ELEMENTS[etype].save_type in SUMMON_ITERATORS
			for line in start_iterator(ns, version, etype)
		]
		write_versioned_function(
			f"maps/editor/summon_existing/{mode_key}",
			"\n".join(summon_lines) if summon_lines else "# No mode-specific elements to summon"
		)

	write_versioned_function("maps/editor/summon_base_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.base_coordinates"]}}
""")

	# List of relative [x, y, z, yaw]; the tag comes from {ns}:temp _spawn_iter_tag.
	write_versioned_function("maps/editor/summon_spawn_iter", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _spawn_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _spawn_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _spawn_iter[0][2]

scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

data modify storage {ns}:temp _spawn_rot.yaw set from storage {ns}:temp _spawn_iter[0][3]

execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #rz {ns}.data

data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_iter_tag

function {ns}:v{version}/maps/editor/summon_spawn_marker with storage {ns}:temp _spos

execute as @n[tag={ns}.new_spawn_marker] run data modify entity @s data.yaw set from storage {ns}:temp _spawn_rot.yaw
tag @e[tag={ns}.new_spawn_marker] remove {ns}.new_spawn_marker

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/maps/editor/summon_spawn_iter
""")

	write_versioned_function("maps/editor/summon_spawn_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)","{ns}.new_spawn_marker"]}}
""")

	# List of relative [x, y, z]; the tag comes from {ns}:temp _point_iter_tag.
	write_versioned_function("maps/editor/summon_point_iter", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _point_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _point_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _point_iter[0][2]

scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

execute store result storage {ns}:temp _ppos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _ppos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _ppos.z double 1 run scoreboard players get #rz {ns}.data

data modify storage {ns}:temp _ppos.tag set from storage {ns}:temp _point_iter_tag

function {ns}:v{version}/maps/editor/summon_point_marker with storage {ns}:temp _ppos

data remove storage {ns}:temp _point_iter[0]
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter
""")

	write_versioned_function("maps/editor/summon_point_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)"]}}
""")

	# List of {pos:[x,y,z], function:"..."}.
	write_versioned_function("maps/editor/summon_enemy_edit_iter", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[2]

scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

execute store result storage {ns}:temp _epos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _epos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _epos.z double 1 run scoreboard players get #rz {ns}.data

function {ns}:v{version}/maps/editor/summon_enemy_marker with storage {ns}:temp _epos

execute as @n[tag={ns}.new_enemy_marker] run data modify entity @s data.function set from storage {ns}:temp _enemy_edit_iter[0].function
tag @e[tag={ns}.new_enemy_marker] remove {ns}.new_enemy_marker

data remove storage {ns}:temp _enemy_edit_iter[0]
execute if data storage {ns}:temp _enemy_edit_iter[0] run function {ns}:v{version}/maps/editor/summon_enemy_edit_iter
""")

	write_versioned_function("maps/editor/summon_enemy_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.enemy","{ns}.new_enemy_marker"]}}
""")

	# List of {pos:[x,y,z], command:"..."}.
	write_versioned_function("maps/editor/summon_start_command_iter", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[2]

scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

execute store result storage {ns}:temp _cpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _cpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _cpos.z double 1 run scoreboard players get #rz {ns}.data

function {ns}:v{version}/maps/editor/summon_start_command_marker with storage {ns}:temp _cpos

execute as @n[tag={ns}.new_start_cmd_marker] run data modify entity @s data.command set from storage {ns}:temp _start_cmd_iter[0].command
tag @e[tag={ns}.new_start_cmd_marker] remove {ns}.new_start_cmd_marker

data remove storage {ns}:temp _start_cmd_iter[0]
execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_start_command_iter
""")

	write_versioned_function("maps/editor/summon_start_command_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.start_command","{ns}.new_start_cmd_marker"]}}
""")

	# List of {pos:[x,y,z], command:"..."}.
	write_versioned_function("maps/editor/summon_respawn_command_iter", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[2]

scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

execute store result storage {ns}:temp _rcpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _rcpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _rcpos.z double 1 run scoreboard players get #rz {ns}.data

function {ns}:v{version}/maps/editor/summon_respawn_command_marker with storage {ns}:temp _rcpos

execute as @n[tag={ns}.new_respawn_cmd_marker] run data modify entity @s data.command set from storage {ns}:temp _respawn_cmd_iter[0].command
tag @e[tag={ns}.new_respawn_cmd_marker] remove {ns}.new_respawn_cmd_marker

data remove storage {ns}:temp _respawn_cmd_iter[0]
execute if data storage {ns}:temp _respawn_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_respawn_command_iter
""")

	write_versioned_function("maps/editor/summon_respawn_command_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.respawn_command","{ns}.new_respawn_cmd_marker"]}}
""")

	# List of compounds {pos:[x,y,z], rotation:[yaw,pitch], ...}; the tag comes from {ns}:temp _zb_iter_tag.
	write_versioned_function("maps/editor/summon_zb_object_iter", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[2]

scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

execute store result storage {ns}:temp _zbpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _zbpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _zbpos.z double 1 run scoreboard players get #rz {ns}.data

data modify storage {ns}:temp _zbpos.tag set from storage {ns}:temp _zb_iter_tag

function {ns}:v{version}/maps/editor/summon_zb_marker with storage {ns}:temp _zbpos

execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data set from storage {ns}:temp _zb_iter[0]

# Fields older maps lack, which the config UI would show as blank rows.
execute as @n[tag={ns}.new_zb_marker] run function {ns}:v{version}/maps/editor/backfill_zb_defaults

# The entity Rotation is synced too, for model displays.
execute if data storage {ns}:temp _zb_iter[0].rotation as @n[tag={ns}.new_zb_marker] run data modify entity @s data.yaw set from storage {ns}:temp _zb_iter[0].rotation[0]
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s Rotation[0] set from entity @s data.yaw

tag @e[tag={ns}.new_zb_marker] remove {ns}.new_zb_marker

data remove storage {ns}:temp _zb_iter[0]
execute if data storage {ns}:temp _zb_iter[0] run function {ns}:v{version}/maps/editor/summon_zb_object_iter
""")

	write_versioned_function("maps/editor/summon_zb_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)","{ns}.new_zb_marker"]}}
""")


def start_iterator(ns: str, version: str, etype: str) -> list[str]:
	""" Lines copying one element's saved list and starting its summon iterator, then a blank separator. """
	einfo = ALL_ELEMENTS[etype]
	iterator: SummonIterator = SUMMON_ITERATORS[einfo.save_type]
	return [
		f"data modify storage {ns}:temp {iterator.storage} set from storage {ns}:temp map_edit.map.{einfo.save_path}",
		*([f'data modify storage {ns}:temp {iterator.storage}_tag set value "{ns}.element.{etype}"'] if iterator.tagged else []),
		f"execute if data storage {ns}:temp {iterator.storage}[0] run function {ns}:v{version}/maps/editor/{iterator.function}",
		"",
	]

