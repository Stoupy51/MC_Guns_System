""" Placing an element: its marker, its defaults and the announce that follows. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..map_editor_defs import ALL_ELEMENTS
from .shared import ZB_ELEMENTS


# Functions
def write_editor_handlers() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("maps/editor/handle_base", f"""
# start_function and tick_function survive the move.
execute if data entity @n[tag={ns}.element.base_coordinates] data.start_function run data modify storage {ns}:temp _base_preserve.start_function set from entity @n[tag={ns}.element.base_coordinates] data.start_function
execute if data entity @n[tag={ns}.element.base_coordinates] data.tick_function run data modify storage {ns}:temp _base_preserve.tick_function set from entity @n[tag={ns}.element.base_coordinates] data.tick_function

kill @e[tag={ns}.element.base_coordinates]

execute store result score #base_x {ns}.data run data get entity @s Pos[0]
execute store result score #base_y {ns}.data run data get entity @s Pos[1]
execute store result score #base_z {ns}.data run data get entity @s Pos[2]

execute store result storage {ns}:temp _pos.x double 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _pos.y double 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _pos.z double 1 run scoreboard players get #base_z {ns}.data
function {ns}:v{version}/maps/editor/summon_base_marker with storage {ns}:temp _pos

execute if data storage {ns}:temp _base_preserve.start_function run data modify entity @n[tag={ns}.element.base_coordinates] data.start_function set from storage {ns}:temp _base_preserve.start_function
execute if data storage {ns}:temp _base_preserve.tick_function run data modify entity @n[tag={ns}.element.base_coordinates] data.tick_function set from storage {ns}:temp _base_preserve.tick_function
data remove storage {ns}:temp _base_preserve

execute as @a[tag={ns}.map_editor] run tellraw @s [{MGS_TAG},{{"text":"Base coordinates set!","color":"light_purple"}}]
""")

	# Spawn points, every mode.
	spawn_tag_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.{etype}"'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "spawn"
	)
	spawn_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo.name} placed!","color":"{einfo.color}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "spawn"
	)

	write_versioned_function("maps/editor/handle_spawn", f"""
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

{spawn_tag_lines}

function {ns}:v{version}/maps/editor/summon_spawn_marker with storage {ns}:temp _pos

# Player yaw, snapped to 45°.
execute store result score #yaw {ns}.data run data get entity @p[tag={ns}.map_editor,distance=..6,sort=nearest] Rotation[0]
scoreboard players add #yaw {ns}.data 742
scoreboard players operation #yaw {ns}.data /= #45 {ns}.data
scoreboard players operation #yaw {ns}.data *= #45 {ns}.data
scoreboard players remove #yaw {ns}.data 720
execute as @n[tag={ns}.new_spawn_marker] store result entity @s data.yaw float 1 run scoreboard players get #yaw {ns}.data
tag @n[tag={ns}.new_spawn_marker] remove {ns}.new_spawn_marker

{spawn_msg_lines}
""")

	# Point elements, every mode.
	point_tag_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.{etype}"'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "point"
	)
	point_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo.name} placed!","color":"{einfo.color}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "point"
	)

	write_versioned_function("maps/editor/handle_point", f"""
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

{point_tag_lines}

function {ns}:v{version}/maps/editor/summon_point_marker with storage {ns}:temp _pos

{point_msg_lines}
""")

	# Enemy (missions).
	write_versioned_function("maps/editor/handle_enemy", f"""
execute unless data storage {ns}:temp map_edit.map.default_enemy_function run data modify storage {ns}:temp map_edit.map.default_enemy_function set value "{ns}:mob/default/level_1 {{\\"entity\\":\\"pillager\\"}}"

execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

function {ns}:v{version}/maps/editor/summon_enemy_marker with storage {ns}:temp _pos

execute as @n[tag={ns}.new_enemy_marker] run data modify entity @s data.function set from storage {ns}:temp map_edit.map.default_enemy_function
tag @e[tag={ns}.new_enemy_marker] remove {ns}.new_enemy_marker

tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Enemy placed!","color":"red"}}]
""")

	# Start command (every mode).
	edit_cmd_btn = Dialogs.btn(
		"Edit Command",
		f'/data modify entity @n[tag={ns}.element.start_command,distance=..10] data.command set value "say Hello from start command"',
		"aqua", "Click to edit the command to run at game start", action="suggest_command"
	)
	write_versioned_function("maps/editor/handle_start_command", f"""
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

function {ns}:v{version}/maps/editor/summon_start_command_marker with storage {ns}:temp _pos

execute as @n[tag={ns}.new_start_cmd_marker] run data modify entity @s data.command set value "say Hello from start command"
tag @e[tag={ns}.new_start_cmd_marker] remove {ns}.new_start_cmd_marker

tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Start Command placed!","color":"aqua"}}]
tellraw @a[tag={ns}.map_editor] ["  ",{edit_cmd_btn}]
""")

	# Respawn command (multiplayer and missions).
	edit_respawn_cmd_btn = Dialogs.btn(
		"Edit Command",
		f'/data modify entity @n[tag={ns}.element.respawn_command,distance=..10] data.command set value "effect give @s minecraft:speed 5 0 true"',
		"dark_aqua", "Click to edit the command to run when players respawn", action="suggest_command"
	)
	write_versioned_function("maps/editor/handle_respawn_command", f"""
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

function {ns}:v{version}/maps/editor/summon_respawn_command_marker with storage {ns}:temp _pos

execute as @n[tag={ns}.new_respawn_cmd_marker] run data modify entity @s data.command set value "effect give @s minecraft:speed 5 0 true"
tag @e[tag={ns}.new_respawn_cmd_marker] remove {ns}.new_respawn_cmd_marker

tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Respawn Command placed!","color":"dark_aqua"}}]
tellraw @a[tag={ns}.map_editor] ["  ",{edit_respawn_cmd_btn}]
""")

	# Zombies objects: detect the type, copy its defaults, take the player's yaw, summon the marker with its data.
	zb_tag_lines: list[str] = []
	for etype in ZB_ELEMENTS:
		zb_tag_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _zbpos.tag set value "{ns}.element.{etype}"')
		zb_tag_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _zb_new set from storage {ns}:temp map_edit.zb_defaults.{etype}')

	zb_msg_lines: list[str] = []
	for etype, einfo in ZB_ELEMENTS.items():
		zb_msg_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo.name} placed!","color":"{einfo.color}"}}]')

	write_versioned_function("maps/editor/handle_zb_object", f"""
execute store result storage {ns}:temp _zbpos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _zbpos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _zbpos.z double 1 run data get entity @s Pos[2]

{chr(10).join(zb_tag_lines)}

function {ns}:v{version}/maps/editor/summon_zb_marker with storage {ns}:temp _zbpos

execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data set from storage {ns}:temp _zb_new

execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data.group_id set from storage {ns}:temp map_edit.zb_defaults.group_id

execute store result score #yaw {ns}.data run data get entity @p[tag={ns}.map_editor,distance=..6,sort=nearest] Rotation[0]

# The power switch sits on a block face, so it snaps to 90°; other objects to 45°.
# 742 = 720 + 45/2 and 765 = 720 + 90/2 make the value positive for rounding; the 720 is removed after.
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players add #yaw {ns}.data 742
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data /= #45 {ns}.data
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data *= #45 {ns}.data
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players add #yaw {ns}.data 765
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data /= #90 {ns}.data
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data *= #90 {ns}.data
scoreboard players remove #yaw {ns}.data 720

# +180°
scoreboard players add #yaw {ns}.data 180

# The entity Rotation is synced at once, so the model display below is oriented right away.
execute as @n[tag={ns}.new_zb_marker] store result entity @s data.yaw float 1 run scoreboard players get #yaw {ns}.data
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s Rotation[0] set from entity @s data.yaw

# Doors take their block from the player's offhand (required).
execute if entity @s[tag={ns}.element.door] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run data modify storage {ns}:temp _zb_offhand_block set from entity @s equipment.offhand.id
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"⚠ ","color":"white"}},{{"text":"Door cancelled! Hold a block in offhand.","color":"red"}}]
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run kill @e[tag={ns}.new_zb_marker]
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run return fail
execute if entity @s[tag={ns}.element.door] as @n[tag={ns}.new_zb_marker] run data modify entity @s data.block set from storage {ns}:temp _zb_offhand_block
data remove storage {ns}:temp _zb_offhand_block

tag @e[tag={ns}.new_zb_marker] remove {ns}.new_zb_marker

# Wallbuy, perk, PaP, mystery box and power switch displays.
function {ns}:v{version}/maps/editor/refresh_displays

{chr(10).join(zb_msg_lines)}
""")

