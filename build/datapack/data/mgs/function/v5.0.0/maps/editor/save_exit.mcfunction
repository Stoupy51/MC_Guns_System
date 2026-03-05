
#> mgs:v5.0.0/maps/editor/save_exit
#
# @within	???
#

# Only process if in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Initialize save data with existing map info (keep id, name, description, scripts)
execute store result storage mgs:temp map_edit.idx int 1 run scoreboard players get @s mgs.mp.map_idx
function mgs:v5.0.0/maps/editor/load_map_data with storage mgs:temp map_edit

# Rebuild base_coordinates from marker
execute as @n[tag=mgs.map_element,tag=mgs.element.base_coordinates] at @s run function mgs:v5.0.0/maps/editor/save_base

# Load base scores for relative computation
execute store result score #base_x mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #base_y mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #base_z mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]

# Reset all lists
data modify storage mgs:temp map_edit.map.boundaries set value []
data modify storage mgs:temp map_edit.map.spawning_points.red set value []
data modify storage mgs:temp map_edit.map.spawning_points.blue set value []
data modify storage mgs:temp map_edit.map.spawning_points.general set value []
data modify storage mgs:temp map_edit.map.out_of_bounds set value []
data modify storage mgs:temp map_edit.map.search_and_destroy set value []
data modify storage mgs:temp map_edit.map.domination set value []
data modify storage mgs:temp map_edit.map.hardpoint set value []

# Iterate all markers and rebuild lists
execute as @e[tag=mgs.map_element,tag=mgs.element.red_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"red"}
execute as @e[tag=mgs.map_element,tag=mgs.element.blue_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"blue"}
execute as @e[tag=mgs.map_element,tag=mgs.element.general_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"general"}
execute as @e[tag=mgs.map_element,tag=mgs.element.boundary] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"boundaries"}
execute as @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"out_of_bounds"}
execute as @e[tag=mgs.map_element,tag=mgs.element.search_and_destroy] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"search_and_destroy"}
execute as @e[tag=mgs.map_element,tag=mgs.element.domination] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"domination"}
execute as @e[tag=mgs.map_element,tag=mgs.element.hardpoint] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"hardpoint"}

# Write back to storage
function mgs:v5.0.0/maps/editor/write_back with storage mgs:temp map_edit

# Cleanup and exit
function mgs:v5.0.0/maps/editor/cleanup
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.map_saved","color":"green"}]

