
#> mgs:v5.0.0/maps/editor/summon_existing
#
# @within	mgs:v5.0.0/maps/editor/enter
#

# Base coordinates marker (at absolute position)
execute store result score #bx mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #by mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #bz mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]
execute store result storage mgs:temp _pos.x double 1 run scoreboard players get #bx mgs.data
execute store result storage mgs:temp _pos.y double 1 run scoreboard players get #by mgs.data
execute store result storage mgs:temp _pos.z double 1 run scoreboard players get #bz mgs.data
function mgs:v5.0.0/maps/editor/summon_base_marker with storage mgs:temp _pos

# Summon spawn point markers (iterate each list)
data modify storage mgs:temp _spawn_iter set from storage mgs:temp map_edit.map.spawning_points.red
scoreboard players set #_spawn_type mgs.data 1
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

data modify storage mgs:temp _spawn_iter set from storage mgs:temp map_edit.map.spawning_points.blue
scoreboard players set #_spawn_type mgs.data 2
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

data modify storage mgs:temp _spawn_iter set from storage mgs:temp map_edit.map.spawning_points.general
scoreboard players set #_spawn_type mgs.data 3
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

# Summon boundary markers
data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.boundaries
scoreboard players set #_point_tag mgs.data 1
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

# Summon out_of_bounds markers
data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.out_of_bounds
scoreboard players set #_point_tag mgs.data 2
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

# Summon search_and_destroy markers
data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.search_and_destroy
scoreboard players set #_point_tag mgs.data 3
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

# Summon domination markers
data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.domination
scoreboard players set #_point_tag mgs.data 4
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

