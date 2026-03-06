
#> mgs:v5.0.0/maps/editor/save_exit
#
# @within	???
#

# Only process if in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Preserve session-modified enemy config before reloading
data modify storage mgs:temp _session_enemy_config set from storage mgs:temp map_edit.map.enemy_config

# Reload map data (preserves metadata like id, name, description, scripts)
execute store result storage mgs:temp map_edit.idx int 1 run scoreboard players get @s mgs.mp.map_idx
function mgs:v5.0.0/maps/editor/load_map_data with storage mgs:temp map_edit

# Restore session-modified enemy config
execute if data storage mgs:temp _session_enemy_config run data modify storage mgs:temp map_edit.map.enemy_config set from storage mgs:temp _session_enemy_config
data remove storage mgs:temp _session_enemy_config

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

# Cleanup and exit
function mgs:v5.0.0/maps/editor/cleanup
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.map_saved","color":"green"}]

