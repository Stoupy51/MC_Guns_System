
#> mgs:v5.1.0/maps/editor/summon_start_command_iter
#
# @within	mgs:v5.1.0/maps/editor/summon_existing/multiplayer
#			mgs:v5.1.0/maps/editor/summon_existing/zombies
#			mgs:v5.1.0/maps/editor/summon_existing/missions
#			mgs:v5.1.0/maps/editor/summon_start_command_iter
#

execute store result score #rx mgs.data run data get storage mgs:temp _start_cmd_iter[0].pos[0]
execute store result score #ry mgs.data run data get storage mgs:temp _start_cmd_iter[0].pos[1]
execute store result score #rz mgs.data run data get storage mgs:temp _start_cmd_iter[0].pos[2]

scoreboard players operation #rx mgs.data += #base_x mgs.data
scoreboard players operation #ry mgs.data += #base_y mgs.data
scoreboard players operation #rz mgs.data += #base_z mgs.data

execute store result storage mgs:temp _cpos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _cpos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _cpos.z double 1 run scoreboard players get #rz mgs.data

function mgs:v5.1.0/maps/editor/summon_start_command_marker with storage mgs:temp _cpos

execute as @n[tag=mgs.new_start_cmd_marker] run data modify entity @s data.command set from storage mgs:temp _start_cmd_iter[0].command
tag @e[tag=mgs.new_start_cmd_marker] remove mgs.new_start_cmd_marker

data remove storage mgs:temp _start_cmd_iter[0]
execute if data storage mgs:temp _start_cmd_iter[0] run function mgs:v5.1.0/maps/editor/summon_start_command_iter

