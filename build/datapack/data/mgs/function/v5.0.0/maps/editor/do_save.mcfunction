
#> mgs:v5.0.0/maps/editor/do_save
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/save_exit
#			mgs:v5.0.0/maps/editor/save_only
#

# Preserve session-modified default enemy function before reloading
data modify storage mgs:temp _session_enemy_fn set from storage mgs:temp map_edit.map.default_enemy_function

# Reload map data (preserves metadata like id, name, description, scripts)
execute store result storage mgs:temp map_edit.idx int 1 run scoreboard players get @s mgs.mp.map_idx
function mgs:v5.0.0/maps/editor/load_map_data with storage mgs:temp map_edit

# Restore session-modified default enemy function
execute if data storage mgs:temp _session_enemy_fn run data modify storage mgs:temp map_edit.map.default_enemy_function set from storage mgs:temp _session_enemy_fn
data remove storage mgs:temp _session_enemy_fn

# Rebuild base_coordinates from marker
execute as @n[tag=mgs.map_element,tag=mgs.element.base_coordinates] at @s run function mgs:v5.0.0/maps/editor/save_base

# Load base scores for relative computation
execute store result score #base_x mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #base_y mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #base_z mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]

# Save mode-specific lists (reset + rebuild from markers)
execute if score @s mgs.mp.map_mode matches 0 run function mgs:v5.0.0/maps/editor/save_lists/multiplayer
execute if score @s mgs.mp.map_mode matches 1 run function mgs:v5.0.0/maps/editor/save_lists/zombies
execute if score @s mgs.mp.map_mode matches 2 run function mgs:v5.0.0/maps/editor/save_lists/missions

# Write back to storage
function mgs:v5.0.0/maps/editor/write_back with storage mgs:temp map_edit

