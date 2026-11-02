
#> mgs:v5.3.0/maps/editor/do_save
#
# @within	string in mgs:v5.3.0/maps/editor/save_exit
#			string in mgs:v5.3.0/maps/editor/save_only
#

execute if data storage mgs:temp map_edit{unsafe:1b} run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.not_saved_some_elements_of_this_map_could_not_be_loaded_and_a_sa","fallback":"Not saved: some elements of this map could not be loaded, and a save would erase them.","color":"red"}]
execute if data storage mgs:temp map_edit{unsafe:1b} run return fail
execute if data storage mgs:temp map_edit{loading:1b} run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.not_saved_the_elements_of_this_map_are_still_loading","fallback":"Not saved: the elements of this map are still loading.","color":"red"}]
execute if data storage mgs:temp map_edit{loading:1b} run return fail
execute unless entity @e[type=minecraft:marker,tag=mgs.map_element] run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.not_saved_no_element_of_this_map_is_loaded_and_a_save_would_eras","fallback":"Not saved: no element of this map is loaded, and a save would erase them all.","color":"red"}]
execute unless entity @e[type=minecraft:marker,tag=mgs.map_element] run return fail

# Markers left by an older session, and the extra ones of a kind sharing a block, are not saved.
execute as @e[type=minecraft:marker,tag=mgs.map_element] run function mgs:v5.3.0/maps/editor/session_check
function mgs:v5.3.0/maps/editor/remove_duplicates

# The default enemy function changed this session survives the reload.
data modify storage mgs:temp _session_enemy_fn set from storage mgs:temp map_edit.map.default_enemy_function

# Reloading keeps the metadata (id, name, description, scripts).
execute store result storage mgs:temp map_edit.idx int 1 run scoreboard players get @s mgs.mp.map_idx
function mgs:v5.3.0/maps/editor/load_map_data with storage mgs:temp map_edit

# Only a map without a dimension takes the editor's; otherwise it stays what Settings set.
execute unless data storage mgs:temp map_edit.map.dimension run data modify storage mgs:temp map_edit.map.dimension set from entity @s Dimension

execute if data storage mgs:temp _session_enemy_fn run data modify storage mgs:temp map_edit.map.default_enemy_function set from storage mgs:temp _session_enemy_fn
data remove storage mgs:temp _session_enemy_fn

execute as @n[tag=mgs.element.base_coordinates] at @s run function mgs:v5.3.0/maps/editor/save_base

# For the relative coordinates.
execute store result score #base_x mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #base_y mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #base_z mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]

# Lists are reset and rebuilt from the markers.
execute if score @s mgs.mp.map_mode matches 0 run function mgs:v5.3.0/maps/editor/save_lists/multiplayer
execute if score @s mgs.mp.map_mode matches 1 run function mgs:v5.3.0/maps/editor/save_lists/zombies
execute if score @s mgs.mp.map_mode matches 2 run function mgs:v5.3.0/maps/editor/save_lists/missions

function mgs:v5.3.0/maps/editor/write_back with storage mgs:temp map_edit
return 1

