""" Writing the markers back into storage, one save function per element kind. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..map_editor_defs import ALL_ELEMENTS, EDITOR_MODES, MODE_LIST
from .shared import ZB_ELEMENTS, snbt_suggest

# Constants
SAVED_TYPES: tuple[str, ...] = ("spawn", "point", "enemy", "start_command", "respawn_command", "zb_object")
""" Save types rebuilt from their markers on every save, each by its `maps/editor/save_<type>` function. """


# Functions
def write_editor_save() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	save_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_mode matches {i} run function {ns}:v{version}/maps/editor/save_lists/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/save_exit", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

function {ns}:v{version}/maps/editor/do_save

function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Map saved and editor closed!","color":"green"}}]
""")

	write_versioned_function("maps/editor/save_only", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

function {ns}:v{version}/maps/editor/do_save

# The save clears the tools.
function {ns}:v{version}/maps/editor/give_tools

tellraw @s [{MGS_TAG},{{"text":"Map saved!","color":"green"}}]
""")

	write_versioned_function("maps/editor/do_save", f"""
# The default enemy function changed this session survives the reload.
data modify storage {ns}:temp _session_enemy_fn set from storage {ns}:temp map_edit.map.default_enemy_function

# Reloading keeps the metadata (id, name, description, scripts).
execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx
function {ns}:v{version}/maps/editor/load_map_data with storage {ns}:temp map_edit

execute if data storage {ns}:temp _session_enemy_fn run data modify storage {ns}:temp map_edit.map.default_enemy_function set from storage {ns}:temp _session_enemy_fn
data remove storage {ns}:temp _session_enemy_fn

execute as @n[tag={ns}.element.base_coordinates] at @s run function {ns}:v{version}/maps/editor/save_base

# For the relative coordinates.
execute store result score #base_x {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #base_y {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #base_z {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]

# Lists are reset and rebuilt from the markers.
{save_dispatch}

function {ns}:v{version}/maps/editor/write_back with storage {ns}:temp map_edit
""")

	write_save_lists(ns, version)

	write_versioned_function("maps/editor/save_base", f"""
# Run as the base marker, at it.
execute store result storage {ns}:temp map_edit.map.base_coordinates[0] int 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp map_edit.map.base_coordinates[1] int 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp map_edit.map.base_coordinates[2] int 1 run data get entity @s Pos[2]

# Only written when set on the marker.
execute if data entity @s data.start_function run data modify storage {ns}:temp map_edit.map.start_function set from entity @s data.start_function
execute unless data entity @s data.start_function run data remove storage {ns}:temp map_edit.map.start_function
execute if data entity @s data.tick_function run data modify storage {ns}:temp map_edit.map.tick_function set from entity @s data.tick_function
execute unless data entity @s data.tick_function run data remove storage {ns}:temp map_edit.map.tick_function
""")

	## Macro: path is red, blue, general, ...
	write_versioned_function("maps/editor/save_spawn", f"""
# Run as the marker, at it.
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# [x, y, z, yaw]
data modify storage {ns}:temp _save_coord set value [0, 0, 0, 0.0f]
execute store result storage {ns}:temp _save_coord[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_coord[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_coord[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_coord[3] set from entity @s data.yaw

$data modify storage {ns}:temp map_edit.map.spawning_points.$(path) append from storage {ns}:temp _save_coord
""")

	## Macro: path is boundaries, out_of_bounds, ...
	write_versioned_function("maps/editor/save_point", f"""
# Run as the marker, at it.
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# [x, y, z]
data modify storage {ns}:temp _save_coord set value [0, 0, 0]
execute store result storage {ns}:temp _save_coord[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_coord[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_coord[2] int 1 run scoreboard players get #az {ns}.data

$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_coord
""")

	write_versioned_function("maps/editor/save_enemy", f"""
# Run as the enemy marker, at it.
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# {{pos:[x,y,z], function:"..."}}
data modify storage {ns}:temp _save_enemy set value {{pos:[0,0,0],function:""}}
execute store result storage {ns}:temp _save_enemy.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_enemy.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_enemy.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_enemy.function set from entity @s data.function

data modify storage {ns}:temp map_edit.map.enemies append from storage {ns}:temp _save_enemy
""")

	write_versioned_function("maps/editor/save_start_command", f"""
# Run as the start command marker, at it.
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# {{pos:[x,y,z], command:"..."}}
data modify storage {ns}:temp _save_start_cmd set value {{pos:[0,0,0],command:""}}
execute store result storage {ns}:temp _save_start_cmd.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_start_cmd.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_start_cmd.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_start_cmd.command set from entity @s data.command

$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_start_cmd
""")

	write_versioned_function("maps/editor/save_respawn_command", f"""
# Run as the respawn command marker, at it.
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# {{pos:[x,y,z], command:"..."}}
data modify storage {ns}:temp _save_respawn_cmd set value {{pos:[0,0,0],command:""}}
execute store result storage {ns}:temp _save_respawn_cmd.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_respawn_cmd.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_respawn_cmd.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_respawn_cmd.command set from entity @s data.command

$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_respawn_cmd
""")

	## Macro: path is wallbuys, doors, ...
	strip_dispatch: str = write_strip_light_fields()
	write_versioned_function("maps/editor/save_zb_object", f"""
# Run as the marker, at it.
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# The marker's data is the base entry.
data modify storage {ns}:temp _save_zb set from entity @s data

# pos becomes relative.
data modify storage {ns}:temp _save_zb.pos set value [0, 0, 0]
execute store result storage {ns}:temp _save_zb.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_zb.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_zb.pos[2] int 1 run scoreboard players get #az {ns}.data

# Pitch is always 0.
data modify storage {ns}:temp _save_zb.rotation set value [0.0f, 0.0f]
data modify storage {ns}:temp _save_zb.rotation[0] set from entity @s data.yaw

# yaw lives in the rotation array.
data remove storage {ns}:temp _save_zb.yaw
data remove storage {ns}:temp _save_zb._disp_sig
{strip_dispatch}

$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_zb
""")

	## At the map's index, in its mode.
	write_versioned_function("maps/editor/write_back", f"""
$data modify storage {ns}:maps $(mode)[$(idx)] set from storage {ns}:temp map_edit.map
""")


def write_save_lists(ns: str, version: str) -> None:
	""" Write one `save_lists/<mode>` function per editor mode: empty each saved list, then rebuild it from its markers. """
	for mode_key, mode_info in EDITOR_MODES.items():
		saved: list[str] = [etype for etype in mode_info.slots if ALL_ELEMENTS[etype].save_type in SAVED_TYPES]
		resets: list[str] = [f"data modify storage {ns}:temp map_edit.map.{ALL_ELEMENTS[etype].save_path} set value []" for etype in saved]
		rebuilds: list[str] = [
			f"execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/{save_call(etype)}" for etype in saved
		]
		write_versioned_function(
			f"maps/editor/save_lists/{mode_key}",
			"\n".join(["# Reset lists", *resets, "", "# Rebuild from markers", *rebuilds]) if saved else "# No mode-specific elements to save",
		)


def save_call(etype: str) -> str:
	""" The save function one marker runs, with its list path when it takes one.

	>>> save_call("enemy")
	'save_enemy'
	"""
	einfo = ALL_ELEMENTS[etype]
	if einfo.save_type == "enemy":
		return "save_enemy"
	list_path: str = einfo.save_path.split(".")[-1] if einfo.save_type == "spawn" else einfo.save_path
	return f'save_{einfo.save_type} {{path:"{list_path}"}}'


def write_strip_light_fields() -> str:
	""" Write one function per element with light fields, dropping from `_save_zb` each one that holds its default.

	Returns:
		The lines save_zb_object runs to dispatch to them.
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	light_elements: dict[str, tuple[str, ...]] = {etype: einfo.light_fields for etype, einfo in ZB_ELEMENTS.items() if einfo.light_fields}
	for etype, fields in light_elements.items():
		# `set value` on an equal compound changes nothing, so its success says whether the field differs from the default.
		write_versioned_function(f"maps/editor/strip_light_fields/{etype}", "\n".join(
			f"""data remove storage {ns}:temp _light
data modify storage {ns}:temp _light set from storage {ns}:temp _save_zb.{field}
execute store success score #light_differs {ns}.data run data modify storage {ns}:temp _light set value {snbt_suggest(ALL_ELEMENTS[etype].defaults[field])}
execute if score #light_differs {ns}.data matches 0 run data remove storage {ns}:temp _save_zb.{field}"""
			for field in fields
		))
	return "\n".join(
		f"execute if entity @s[tag={ns}.element.{etype}] run function {ns}:v{version}/maps/editor/strip_light_fields/{etype}"
		for etype in light_elements
	)

