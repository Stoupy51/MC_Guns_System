""" Writing the markers back into storage, one save function per element kind. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..map_editor_defs import ALL_ELEMENTS, EDITOR_MODES, MODE_LIST


# Functions
def write_editor_save() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Save and Exit Editor
	save_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_mode matches {i} run function {ns}:v{version}/maps/editor/save_lists/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/save_exit", f"""
# Only process if in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Do the actual save
function {ns}:v{version}/maps/editor/do_save

# Cleanup and exit
function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Map saved and editor closed!","color":"green"}}]
""")

	write_versioned_function("maps/editor/save_only", f"""
# Only process if in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Do the actual save
function {ns}:v{version}/maps/editor/do_save

# Re-give tools (since save clears + re-gives via advancement revoke)
function {ns}:v{version}/maps/editor/give_tools

tellraw @s [{MGS_TAG},{{"text":"Map saved!","color":"green"}}]
""")

	write_versioned_function("maps/editor/do_save", f"""
# Preserve session-modified default enemy function before reloading
data modify storage {ns}:temp _session_enemy_fn set from storage {ns}:temp map_edit.map.default_enemy_function

# Reload map data (preserves metadata like id, name, description, scripts)
execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx
function {ns}:v{version}/maps/editor/load_map_data with storage {ns}:temp map_edit

# Restore session-modified default enemy function
execute if data storage {ns}:temp _session_enemy_fn run data modify storage {ns}:temp map_edit.map.default_enemy_function set from storage {ns}:temp _session_enemy_fn
data remove storage {ns}:temp _session_enemy_fn

# Rebuild base_coordinates from marker
execute as @n[tag={ns}.element.base_coordinates] at @s run function {ns}:v{version}/maps/editor/save_base

# Load base scores for relative computation
execute store result score #base_x {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #base_y {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #base_z {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]

# Save mode-specific lists (reset + rebuild from markers)
{save_dispatch}

# Write back to storage
function {ns}:v{version}/maps/editor/write_back with storage {ns}:temp map_edit
""")

	# Per-mode save lists functions
	for mode_key, mode_info in EDITOR_MODES.items():
		reset_lines: list[str] = []
		rebuild_lines: list[str] = []
		for etype in mode_info.slots:
			einfo = ALL_ELEMENTS[etype]
			if einfo.save_type in ("base", "config"):
				continue  # handled by save_base / no save data

			save_path = einfo.save_path
			if einfo.save_type == "spawn":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				path_suffix = save_path.split(".")[-1]
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_spawn {{path:"{path_suffix}"}}')
			elif einfo.save_type == "point":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_point {{path:"{save_path}"}}')
			elif einfo.save_type == "enemy":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_enemy')
			elif einfo.save_type == "start_command":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_start_command {{path:"{save_path}"}}')
			elif einfo.save_type == "respawn_command":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_respawn_command {{path:"{save_path}"}}')
			elif einfo.save_type == "zb_object":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_zb_object {{path:"{save_path}"}}')
		all_lines: list[str] = []
		if reset_lines:
			all_lines.append("# Reset lists")
			all_lines.extend(reset_lines)
			all_lines.append("")
			all_lines.append("# Rebuild from markers")
			all_lines.extend(rebuild_lines)

		write_versioned_function(
			f"maps/editor/save_lists/{mode_key}",
			"\n".join(all_lines) if all_lines else "# No mode-specific elements to save"
		)

	## Save base coordinates from marker
	write_versioned_function("maps/editor/save_base", f"""
# @s = base_coordinates marker, at its position
execute store result storage {ns}:temp map_edit.map.base_coordinates[0] int 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp map_edit.map.base_coordinates[1] int 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp map_edit.map.base_coordinates[2] int 1 run data get entity @s Pos[2]

# Save start_function and tick_function (absent by default, only written if set on marker)
execute if data entity @s data.start_function run data modify storage {ns}:temp map_edit.map.start_function set from entity @s data.start_function
execute unless data entity @s data.start_function run data remove storage {ns}:temp map_edit.map.start_function
execute if data entity @s data.tick_function run data modify storage {ns}:temp map_edit.map.tick_function set from entity @s data.tick_function
execute unless data entity @s data.tick_function run data remove storage {ns}:temp map_edit.map.tick_function
""")

	## Save a spawn point (macro: path = red/blue/general/etc.)
	write_versioned_function("maps/editor/save_spawn", f"""
# @s = marker entity, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build coordinate array [x, y, z, yaw]
data modify storage {ns}:temp _save_coord set value [0, 0, 0, 0.0f]
execute store result storage {ns}:temp _save_coord[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_coord[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_coord[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_coord[3] set from entity @s data.yaw

# Append to the correct list
$data modify storage {ns}:temp map_edit.map.spawning_points.$(path) append from storage {ns}:temp _save_coord
""")

	## Save a point element (macro: path = boundaries/out_of_bounds/etc.)
	write_versioned_function("maps/editor/save_point", f"""
# @s = marker entity, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build coordinate array [x, y, z]
data modify storage {ns}:temp _save_coord set value [0, 0, 0]
execute store result storage {ns}:temp _save_coord[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_coord[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_coord[2] int 1 run scoreboard players get #az {ns}.data

# Append to the correct list
$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_coord
""")

	## Save an enemy element (pos + function)
	write_versioned_function("maps/editor/save_enemy", f"""
# @s = enemy marker, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build enemy entry {{pos:[x,y,z], function:"..."}}
data modify storage {ns}:temp _save_enemy set value {{pos:[0,0,0],function:""}}
execute store result storage {ns}:temp _save_enemy.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_enemy.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_enemy.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_enemy.function set from entity @s data.function

# Append to enemies list
data modify storage {ns}:temp map_edit.map.enemies append from storage {ns}:temp _save_enemy
""")

	## Save a start command element (pos + command)
	write_versioned_function("maps/editor/save_start_command", f"""
# @s = start command marker, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build start command entry {{pos:[x,y,z],command:"..."}}
data modify storage {ns}:temp _save_start_cmd set value {{pos:[0,0,0],command:""}}
execute store result storage {ns}:temp _save_start_cmd.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_start_cmd.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_start_cmd.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_start_cmd.command set from entity @s data.command

# Append to list path
$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_start_cmd
""")

	## Save a respawn command element (pos + command)
	write_versioned_function("maps/editor/save_respawn_command", f"""
# @s = respawn command marker, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build respawn command entry {{pos:[x,y,z],command:"..."}}
data modify storage {ns}:temp _save_respawn_cmd set value {{pos:[0,0,0],command:""}}
execute store result storage {ns}:temp _save_respawn_cmd.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_respawn_cmd.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_respawn_cmd.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_respawn_cmd.command set from entity @s data.command

# Append to list path
$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_respawn_cmd
""")

	## Save a zb_object element (macro: path = wallbuys/doors/etc.)
	write_versioned_function("maps/editor/save_zb_object", f"""
# @s = marker entity, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Copy marker's data compound as the base entry
data modify storage {ns}:temp _save_zb set from entity @s data

# Overwrite pos with relative coordinates
data modify storage {ns}:temp _save_zb.pos set value [0, 0, 0]
execute store result storage {ns}:temp _save_zb.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_zb.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_zb.pos[2] int 1 run scoreboard players get #az {ns}.data

# Build rotation array from yaw (pitch is always 0)
data modify storage {ns}:temp _save_zb.rotation set value [0.0f, 0.0f]
data modify storage {ns}:temp _save_zb.rotation[0] set from entity @s data.yaw

# Remove internal-only marker fields (yaw is stored in rotation array)
data remove storage {ns}:temp _save_zb.yaw

# Append to the correct list
$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_zb
""")

	## Write map back to storage at the correct index and mode
	write_versioned_function("maps/editor/write_back", f"""
$data modify storage {ns}:maps $(mode)[$(idx)] set from storage {ns}:temp map_edit.map
""")

