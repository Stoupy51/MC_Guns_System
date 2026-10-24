
#> mgs:v5.2.0/maps/editor/summon_existing
#
# @executed	at @s
#
# @within	mgs:v5.2.0/maps/editor/enter [ at @s ]
#

# Base coordinates marker, in every mode.
execute store result score #bx mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #by mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #bz mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]
execute store result storage mgs:temp _pos.x double 1 run scoreboard players get #bx mgs.data
execute store result storage mgs:temp _pos.y double 1 run scoreboard players get #by mgs.data
execute store result storage mgs:temp _pos.z double 1 run scoreboard players get #bz mgs.data
function mgs:v5.2.0/maps/editor/summon_base_marker with storage mgs:temp _pos

execute if data storage mgs:temp map_edit.map.start_command run data modify entity @n[tag=mgs.element.base_coordinates] data.start_command set from storage mgs:temp map_edit.map.start_command
execute if data storage mgs:temp map_edit.map.tick_command run data modify entity @n[tag=mgs.element.base_coordinates] data.tick_command set from storage mgs:temp map_edit.map.tick_command

execute if score @s mgs.mp.map_mode matches 0 run function mgs:v5.2.0/maps/editor/summon_existing/multiplayer
execute if score @s mgs.mp.map_mode matches 1 run function mgs:v5.2.0/maps/editor/summon_existing/zombies
execute if score @s mgs.mp.map_mode matches 2 run function mgs:v5.2.0/maps/editor/summon_existing/missions

