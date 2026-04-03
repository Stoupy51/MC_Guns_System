
#> mgs:v5.0.0/missions/map_select
#
# @within	mgs:v5.0.0/missions/setup "hover_event": {"action": "show_text", "value": "Browse and select a mission map"}}, "Select Map", "]"]]
#

tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s [{"text":"","color":"aqua","bold":true},"  🗺 ",{"translate":"mgs.select_mission_map"}]
tellraw @s {"text":"============================================","color":"dark_gray"}

# Copy maps list for iteration
data modify storage mgs:temp _map_iter set from storage mgs:maps missions
scoreboard players set #map_idx mgs.data 0
execute if data storage mgs:temp _map_iter[0] run function mgs:v5.0.0/missions/map_select_entry with storage mgs:temp _map_iter[0]

execute unless data storage mgs:maps missions[0] run tellraw @s ["  ",{"translate":"mgs.no_mission_maps_create_one_in_the_map_editor_first","color":"red"}]
tellraw @s {"text":"============================================","color":"dark_gray"}

