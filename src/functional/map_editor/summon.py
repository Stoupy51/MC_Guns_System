""" Rebuilding a saved map's markers, one iterator and marker summon per element kind. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS, EDITOR_MODES, MODE_LIST


# Functions
def write_editor_summon() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Summon Existing Elements.
	summon_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_mode matches {i} run function {ns}:v{version}/maps/editor/summon_existing/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/summon_existing", f"""
# Summon base coordinates marker (common to all modes)
execute store result score #bx {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #by {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #bz {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]
execute store result storage {ns}:temp _pos.x double 1 run scoreboard players get #bx {ns}.data
execute store result storage {ns}:temp _pos.y double 1 run scoreboard players get #by {ns}.data
execute store result storage {ns}:temp _pos.z double 1 run scoreboard players get #bz {ns}.data
function {ns}:v{version}/maps/editor/summon_base_marker with storage {ns}:temp _pos

# Restore start_function and tick_function to the base marker from map data
execute if data storage {ns}:temp map_edit.map.start_function run data modify entity @n[tag={ns}.element.base_coordinates] data.start_function set from storage {ns}:temp map_edit.map.start_function
execute if data storage {ns}:temp map_edit.map.tick_function run data modify entity @n[tag={ns}.element.base_coordinates] data.tick_function set from storage {ns}:temp map_edit.map.tick_function

# Mode-specific elements
{summon_dispatch}
""")

	# Per-mode summon functions
	for mode_key, mode_info in EDITOR_MODES.items():
		summon_lines: list[str] = []
		for etype in mode_info.slots:
			einfo = ALL_ELEMENTS[etype]
			if einfo.save_type in ("base", "config"):
				continue  # handled in parent / no markers
			save_path = einfo.save_path
			if einfo.save_type == "spawn":
				summon_lines.append(f'data modify storage {ns}:temp _spawn_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'data modify storage {ns}:temp _spawn_iter_tag set value "{ns}.element.{etype}"')
				summon_lines.append(f'execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/maps/editor/summon_spawn_iter')
				summon_lines.append("")
			elif einfo.save_type == "point":
				summon_lines.append(f'data modify storage {ns}:temp _point_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'data modify storage {ns}:temp _point_iter_tag set value "{ns}.element.{etype}"')
				summon_lines.append(f'execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter')
				summon_lines.append("")
			elif einfo.save_type == "enemy":
				summon_lines.append(f'data modify storage {ns}:temp _enemy_edit_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'execute if data storage {ns}:temp _enemy_edit_iter[0] run function {ns}:v{version}/maps/editor/summon_enemy_edit_iter')
				summon_lines.append("")
			elif einfo.save_type == "start_command":
				summon_lines.append(f'data modify storage {ns}:temp _start_cmd_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_start_command_iter')
				summon_lines.append("")
			elif einfo.save_type == "respawn_command":
				summon_lines.append(f'data modify storage {ns}:temp _respawn_cmd_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'execute if data storage {ns}:temp _respawn_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_respawn_command_iter')
				summon_lines.append("")
			elif einfo.save_type == "zb_object":
				summon_lines.append(f'data modify storage {ns}:temp _zb_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'data modify storage {ns}:temp _zb_iter_tag set value "{ns}.element.{etype}"')
				summon_lines.append(f'execute if data storage {ns}:temp _zb_iter[0] run function {ns}:v{version}/maps/editor/summon_zb_object_iter')
				summon_lines.append("")

		write_versioned_function(
			f"maps/editor/summon_existing/{mode_key}",
			"\n".join(summon_lines) if summon_lines else "# No mode-specific elements to summon"
		)

	# Summon helpers (shared).
	write_versioned_function("maps/editor/summon_base_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.base_coordinates"]}}
""")

	# Summon spawn markers - iterates list of [x,y,z,yaw] relative coords Tag is read from {ns}:temp _spawn_iter_tag (set before calling)
	write_versioned_function("maps/editor/summon_spawn_iter", f"""
# Read relative coordinates from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _spawn_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _spawn_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _spawn_iter[0][2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Read yaw
data modify storage {ns}:temp _spawn_rot.yaw set from storage {ns}:temp _spawn_iter[0][3]

# Prepare position for macro
execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #rz {ns}.data

# Set tag from stored tag
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_iter_tag

# Summon marker with tag
function {ns}:v{version}/maps/editor/summon_spawn_marker with storage {ns}:temp _spos

# Store rotation data on the marker
execute as @n[tag={ns}.new_spawn_marker] run data modify entity @s data.yaw set from storage {ns}:temp _spawn_rot.yaw
tag @e[tag={ns}.new_spawn_marker] remove {ns}.new_spawn_marker

# Advance to next
data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/maps/editor/summon_spawn_iter
""")

	write_versioned_function("maps/editor/summon_spawn_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)","{ns}.new_spawn_marker"]}}
""")

	# Summon point markers - iterates list of [x,y,z] relative coords Tag is read from {ns}:temp _point_iter_tag (set before calling)
	write_versioned_function("maps/editor/summon_point_iter", f"""
# Read relative coordinates
execute store result score #rx {ns}.data run data get storage {ns}:temp _point_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _point_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _point_iter[0][2]

# Add base
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position
execute store result storage {ns}:temp _ppos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _ppos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _ppos.z double 1 run scoreboard players get #rz {ns}.data

# Set tag from stored tag
data modify storage {ns}:temp _ppos.tag set from storage {ns}:temp _point_iter_tag

function {ns}:v{version}/maps/editor/summon_point_marker with storage {ns}:temp _ppos

# Advance
data remove storage {ns}:temp _point_iter[0]
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter
""")

	write_versioned_function("maps/editor/summon_point_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)"]}}
""")

	# Summon enemy markers - iterates list of {pos:[x,y,z], function:"..."} entries
	write_versioned_function("maps/editor/summon_enemy_edit_iter", f"""
# Read relative position from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _epos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _epos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _epos.z double 1 run scoreboard players get #rz {ns}.data

# Summon marker
function {ns}:v{version}/maps/editor/summon_enemy_marker with storage {ns}:temp _epos

# Store function data on the marker
execute as @n[tag={ns}.new_enemy_marker] run data modify entity @s data.function set from storage {ns}:temp _enemy_edit_iter[0].function
tag @e[tag={ns}.new_enemy_marker] remove {ns}.new_enemy_marker

# Advance to next
data remove storage {ns}:temp _enemy_edit_iter[0]
execute if data storage {ns}:temp _enemy_edit_iter[0] run function {ns}:v{version}/maps/editor/summon_enemy_edit_iter
""")

	write_versioned_function("maps/editor/summon_enemy_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.enemy","{ns}.new_enemy_marker"]}}
""")

	# Summon start command markers - iterates list of {pos:[x,y,z], command:"..."} entries
	write_versioned_function("maps/editor/summon_start_command_iter", f"""
# Read relative position from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _cpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _cpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _cpos.z double 1 run scoreboard players get #rz {ns}.data

# Summon marker
function {ns}:v{version}/maps/editor/summon_start_command_marker with storage {ns}:temp _cpos

# Store command on marker
execute as @n[tag={ns}.new_start_cmd_marker] run data modify entity @s data.command set from storage {ns}:temp _start_cmd_iter[0].command
tag @e[tag={ns}.new_start_cmd_marker] remove {ns}.new_start_cmd_marker

# Advance to next
data remove storage {ns}:temp _start_cmd_iter[0]
execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_start_command_iter
""")

	write_versioned_function("maps/editor/summon_start_command_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.start_command","{ns}.new_start_cmd_marker"]}}
""")

	# Summon respawn command markers - iterates list of {pos:[x,y,z], command:"..."} entries
	write_versioned_function("maps/editor/summon_respawn_command_iter", f"""
# Read relative position from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _rcpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _rcpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _rcpos.z double 1 run scoreboard players get #rz {ns}.data

# Summon marker
function {ns}:v{version}/maps/editor/summon_respawn_command_marker with storage {ns}:temp _rcpos

# Store command on marker
execute as @n[tag={ns}.new_respawn_cmd_marker] run data modify entity @s data.command set from storage {ns}:temp _respawn_cmd_iter[0].command
tag @e[tag={ns}.new_respawn_cmd_marker] remove {ns}.new_respawn_cmd_marker

# Advance to next
data remove storage {ns}:temp _respawn_cmd_iter[0]
execute if data storage {ns}:temp _respawn_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_respawn_command_iter
""")

	write_versioned_function("maps/editor/summon_respawn_command_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.respawn_command","{ns}.new_respawn_cmd_marker"]}}
""")

	# Summon zb_object markers - iterates list of compound objects {pos:[x,y,z], rotation:[yaw,pitch], ...} Tag is read from {ns}:temp _zb_iter_tag (set before calling)
	write_versioned_function("maps/editor/summon_zb_object_iter", f"""
# Read relative position from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _zbpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _zbpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _zbpos.z double 1 run scoreboard players get #rz {ns}.data

# Set tag
data modify storage {ns}:temp _zbpos.tag set from storage {ns}:temp _zb_iter_tag

# Summon marker
function {ns}:v{version}/maps/editor/summon_zb_marker with storage {ns}:temp _zbpos

# Copy all compound data onto the marker
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data set from storage {ns}:temp _zb_iter[0]

# Fill in fields the map predates (config UI would otherwise show a blank row)
execute as @n[tag={ns}.new_zb_marker] run function {ns}:v{version}/maps/editor/backfill_zb_defaults

# Set yaw from rotation for the direction indicator (sync entity Rotation too for model displays)
execute if data storage {ns}:temp _zb_iter[0].rotation as @n[tag={ns}.new_zb_marker] run data modify entity @s data.yaw set from storage {ns}:temp _zb_iter[0].rotation[0]
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s Rotation[0] set from entity @s data.yaw

tag @e[tag={ns}.new_zb_marker] remove {ns}.new_zb_marker

# Advance to next
data remove storage {ns}:temp _zb_iter[0]
execute if data storage {ns}:temp _zb_iter[0] run function {ns}:v{version}/maps/editor/summon_zb_object_iter
""")

	write_versioned_function("maps/editor/summon_zb_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)","{ns}.new_zb_marker"]}}
""")

