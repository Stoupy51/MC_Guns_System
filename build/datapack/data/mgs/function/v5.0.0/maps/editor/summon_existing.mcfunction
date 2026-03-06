
#> mgs:v5.0.0/maps/editor/summon_existing
#
# @within	mgs:v5.0.0/maps/editor/enter
#

# Summon base coordinates marker (common to all modes)
execute store result score #bx mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #by mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #bz mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]
execute store result storage mgs:temp _pos.x double 1 run scoreboard players get #bx mgs.data
execute store result storage mgs:temp _pos.y double 1 run scoreboard players get #by mgs.data
execute store result storage mgs:temp _pos.z double 1 run scoreboard players get #bz mgs.data
function mgs:v5.0.0/maps/editor/summon_base_marker with storage mgs:temp _pos

# Mode-specific elements
execute if score @s mgs.mp.map_mode matches 0 run function mgs:v5.0.0/maps/editor/summon_existing/multiplayer
execute if score @s mgs.mp.map_mode matches 1 run function mgs:v5.0.0/maps/editor/summon_existing/zombies
execute if score @s mgs.mp.map_mode matches 2 run function mgs:v5.0.0/maps/editor/summon_existing/missions

