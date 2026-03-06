
#> mgs:v5.0.0/maps/editor/list/missions
#
# @within	???
#

tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s [{"text":"","color":"gold","bold":true},"       🗺 ",{"translate": "mgs.map_editor"}," 🗺"]
tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s ["  ",[{"text": "[", "color": "gold", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/list/multiplayer"}, "hover_event": {"action": "show_text", "value": "View Multiplayer maps"}}, "Multiplayer", "]"],[{"text": "[", "color": "dark_green", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/list/zombies"}, "hover_event": {"action": "show_text", "value": "View Zombies maps"}}, "Zombies", "]"],[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/list/missions"}, "hover_event": {"action": "show_text", "value": "View Missions maps"}}, "Missions", "]"]]
tellraw @s ""

# Copy maps list for iteration
data modify storage mgs:temp map_menu.list set from storage mgs:maps missions
data modify storage mgs:temp map_menu.mode set value "missions"
scoreboard players set #map_menu_idx mgs.data 0

# Show each map
execute if data storage mgs:temp map_menu.list[0] run function mgs:v5.0.0/maps/editor/menu_entry

# No maps message
execute unless data storage mgs:maps missions[0] run tellraw @s [{"translate": "mgs.no_maps_created_yet","color":"gray","italic":true}]

tellraw @s ""
tellraw @s ["  ",[{"text": "[", "color": "green", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/create/missions"}, "hover_event": {"action": "show_text", "value": "Create a new Missions map"}}, "+ Create New Map", "]"]]
tellraw @s {"text":"============================================","color":"dark_gray"}

