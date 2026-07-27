""" Placing an element: its marker, its defaults and the announce that follows. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG, FunctionalHelpers
from ..map_editor_defs import ALL_ELEMENTS
from .shared import ZB_ELEMENTS


# Functions
def write_editor_handlers() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Handle Base Coordinates.
	write_versioned_function("maps/editor/handle_base", f"""
# Preserve start_function and tick_function from existing base marker
execute if data entity @n[tag={ns}.element.base_coordinates] data.start_function run data modify storage {ns}:temp _base_preserve.start_function set from entity @n[tag={ns}.element.base_coordinates] data.start_function
execute if data entity @n[tag={ns}.element.base_coordinates] data.tick_function run data modify storage {ns}:temp _base_preserve.tick_function set from entity @n[tag={ns}.element.base_coordinates] data.tick_function

# Kill any existing base marker
kill @e[tag={ns}.element.base_coordinates]

# Get position
execute store result score #base_x {ns}.data run data get entity @s Pos[0]
execute store result score #base_y {ns}.data run data get entity @s Pos[1]
execute store result score #base_z {ns}.data run data get entity @s Pos[2]

# Summon permanent marker
execute store result storage {ns}:temp _pos.x double 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _pos.y double 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _pos.z double 1 run scoreboard players get #base_z {ns}.data
function {ns}:v{version}/maps/editor/summon_base_marker with storage {ns}:temp _pos

# Restore preserved start_function and tick_function
execute if data storage {ns}:temp _base_preserve.start_function run data modify entity @n[tag={ns}.element.base_coordinates] data.start_function set from storage {ns}:temp _base_preserve.start_function
execute if data storage {ns}:temp _base_preserve.tick_function run data modify entity @n[tag={ns}.element.base_coordinates] data.tick_function set from storage {ns}:temp _base_preserve.tick_function
data remove storage {ns}:temp _base_preserve

# Announce
execute as @a[tag={ns}.map_editor] run tellraw @s [{MGS_TAG},{{"text":"Base coordinates set!","color":"light_purple"}}]
""")

	# Handle Spawn Point (universal).
	spawn_tag_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.{etype}"'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "spawn"
	)
	spawn_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo.name} placed!","color":"{einfo.color}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "spawn"
	)

	write_versioned_function("maps/editor/handle_spawn", f"""
# Get position for the permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Determine tag from entity
{spawn_tag_lines}

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_spawn_marker with storage {ns}:temp _pos

# Get player rotation and snap to nearest 45 degrees
execute store result score #yaw {ns}.data run data get entity @p[tag={ns}.map_editor,distance=..6,sort=nearest] Rotation[0]
scoreboard players add #yaw {ns}.data 742
scoreboard players operation #yaw {ns}.data /= #45 {ns}.data
scoreboard players operation #yaw {ns}.data *= #45 {ns}.data
scoreboard players remove #yaw {ns}.data 720
execute as @n[tag={ns}.new_spawn_marker] store result entity @s data.yaw float 1 run scoreboard players get #yaw {ns}.data
tag @n[tag={ns}.new_spawn_marker] remove {ns}.new_spawn_marker

# Announce
{spawn_msg_lines}
""")

	# Handle Point Element (universal).
	point_tag_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.{etype}"'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "point"
	)
	point_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo.name} placed!","color":"{einfo.color}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "point"
	)

	write_versioned_function("maps/editor/handle_point", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Determine tag
{point_tag_lines}

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_point_marker with storage {ns}:temp _pos

# Announce
{point_msg_lines}
""")

	# Handle Enemy Element (missions).
	write_versioned_function("maps/editor/handle_enemy", f"""
# Initialize default function if missing
execute unless data storage {ns}:temp map_edit.map.default_enemy_function run data modify storage {ns}:temp map_edit.map.default_enemy_function set value "{ns}:mob/default/level_1 {{\\"entity\\":\\"pillager\\"}}"

# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_enemy_marker with storage {ns}:temp _pos

# Store the default function on the marker
execute as @n[tag={ns}.new_enemy_marker] run data modify entity @s data.function set from storage {ns}:temp map_edit.map.default_enemy_function
tag @e[tag={ns}.new_enemy_marker] remove {ns}.new_enemy_marker

# Announce
tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Enemy placed!","color":"red"}}]
""")

	# Handle Start Command Element (all modes).
	edit_cmd_btn = FunctionalHelpers.btn(
		"Edit Command",
		f'/data modify entity @n[tag={ns}.element.start_command,distance=..10] data.command set value "say Hello from start command"',
		"aqua", "Click to edit the command to run at game start", action="suggest_command"
	)
	write_versioned_function("maps/editor/handle_start_command", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_start_command_marker with storage {ns}:temp _pos

# Set default command on marker
execute as @n[tag={ns}.new_start_cmd_marker] run data modify entity @s data.command set value "say Hello from start command"
tag @e[tag={ns}.new_start_cmd_marker] remove {ns}.new_start_cmd_marker

# Announce + quick edit helper
tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Start Command placed!","color":"aqua"}}]
tellraw @a[tag={ns}.map_editor] ["  ",{edit_cmd_btn}]
""")

	# Handle Respawn Command Element (multiplayer + missions) ───
	edit_respawn_cmd_btn = FunctionalHelpers.btn(
		"Edit Command",
		f'/data modify entity @n[tag={ns}.element.respawn_command,distance=..10] data.command set value "effect give @s minecraft:speed 5 0 true"',
		"dark_aqua", "Click to edit the command to run when players respawn", action="suggest_command"
	)
	write_versioned_function("maps/editor/handle_respawn_command", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_respawn_command_marker with storage {ns}:temp _pos

# Set default command on marker
execute as @n[tag={ns}.new_respawn_cmd_marker] run data modify entity @s data.command set value "effect give @s minecraft:speed 5 0 true"
tag @e[tag={ns}.new_respawn_cmd_marker] remove {ns}.new_respawn_cmd_marker

# Announce + quick edit helper
tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Respawn Command placed!","color":"dark_aqua"}}]
tellraw @a[tag={ns}.map_editor] ["  ",{edit_respawn_cmd_btn}]
""")

	# Handle ZB Object (zombies compound elements).
	# Detect type, copy defaults, get rotation, summon marker with data
	# Build tag detection lines
	zb_tag_lines: list[str] = []
	for etype in ZB_ELEMENTS:
		zb_tag_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _zbpos.tag set value "{ns}.element.{etype}"')
		zb_tag_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _zb_new set from storage {ns}:temp map_edit.zb_defaults.{etype}')

	# Build announce lines
	zb_msg_lines: list[str] = []
	for etype, einfo in ZB_ELEMENTS.items():
		zb_msg_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo.name} placed!","color":"{einfo.color}"}}]')

	write_versioned_function("maps/editor/handle_zb_object", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _zbpos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _zbpos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _zbpos.z double 1 run data get entity @s Pos[2]

# Detect type and copy defaults
{chr(10).join(zb_tag_lines)}

# Summon marker
function {ns}:v{version}/maps/editor/summon_zb_marker with storage {ns}:temp _zbpos

# Copy data compound to marker
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data set from storage {ns}:temp _zb_new

# Apply shared group_id default
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data.group_id set from storage {ns}:temp map_edit.zb_defaults.group_id

# Get player rotation
execute store result score #yaw {ns}.data run data get entity @p[tag={ns}.map_editor,distance=..6,sort=nearest] Rotation[0]

# Snap yaw: the power switch is mounted on a block face, so it only allows the 4 cardinal facings
# (snap to 90°). Every other zb_object snaps to the nearest 45°. (742 = 720 + 45/2 and 765 = 720 + 90/2
# offset the value positive for rounding; 720 is a multiple of both 45 and 90 and is removed again after.)
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players add #yaw {ns}.data 742
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data /= #45 {ns}.data
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data *= #45 {ns}.data
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players add #yaw {ns}.data 765
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data /= #90 {ns}.data
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data *= #90 {ns}.data
scoreboard players remove #yaw {ns}.data 720

# Apply 180° yaw offset
scoreboard players add #yaw {ns}.data 180

# Store yaw on marker (and sync entity Rotation immediately so the model display below is oriented right away)
execute as @n[tag={ns}.new_zb_marker] store result entity @s data.yaw float 1 run scoreboard players get #yaw {ns}.data
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s Rotation[0] set from entity @s data.yaw

# For doors: capture block from player's offhand (required)
execute if entity @s[tag={ns}.element.door] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run data modify storage {ns}:temp _zb_offhand_block set from entity @s equipment.offhand.id
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},"⚠ ",{{"text":"Door cancelled! Hold a block in offhand.","color":"red"}}]
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run kill @e[tag={ns}.new_zb_marker]
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run return fail
execute if entity @s[tag={ns}.element.door] as @n[tag={ns}.new_zb_marker] run data modify entity @s data.block set from storage {ns}:temp _zb_offhand_block
data remove storage {ns}:temp _zb_offhand_block

tag @e[tag={ns}.new_zb_marker] remove {ns}.new_zb_marker

# Refresh model displays right away (wallbuy/perk/pap/mystery box/power switch)
function {ns}:v{version}/maps/editor/refresh_displays

# Announce
{chr(10).join(zb_msg_lines)}
""")

