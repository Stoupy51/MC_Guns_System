
#> mgs:v5.0.0/maps/editor/menu
#
# @within	mgs:v5.0.0/maps/editor/delete
#

tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s [{"text":"","color":"gold","bold":true},"       🗺 ",{"translate": "mgs.map_editor"}," 🗺"]
tellraw @s {"text":"============================================","color":"dark_gray"}

# Copy maps list for iteration
data modify storage mgs:temp map_menu.list set from storage mgs:maps multiplayer
scoreboard players set #map_menu_idx mgs.data 0

# Show each map
execute if data storage mgs:temp map_menu.list[0] run function mgs:v5.0.0/maps/editor/menu_entry

# No maps message
execute unless data storage mgs:maps multiplayer[0] run tellraw @s [{"translate": "mgs.no_maps_created_yet","color":"gray","italic":true}]

tellraw @s ""
tellraw @s ["  ",[{"text": "[", "color": "green", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/create"}, "hover_event": {"action": "show_text", "value": "Create a new multiplayer map"}}, "+ Create New Map", "]"]]
tellraw @s {"text":"============================================","color":"dark_gray"}

