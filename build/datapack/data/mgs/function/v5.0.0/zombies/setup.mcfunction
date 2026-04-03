
#> mgs:v5.0.0/zombies/setup
#
# @within	mgs:config "hover_event": {"action": "show_text", "value": "Open the multiplayer game setup menu"}}, "Game Setup", "]"]," ",[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/setup"}, "hover_event": {"action": "show_text", "value": "Open the zombies setup menu"}}, "Zombies Setup", "]"]," ",[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/missions/setup"}, "hover_event": {"action": "show_text", "value": "Open the mission setup menu"}}, "Mission Setup", "]"]]
#

tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s [{"text":"","color":"dark_green","bold":true},"       🧟 ",{"translate":"mgs.zombies_setup"}," 🧟"]
tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s ["",["","  ",{"translate":"mgs.map"},": "],[{"text": "[", "color": "dark_green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/map_select"}, "hover_event": {"action": "show_text", "value": "Browse and select a zombies map"}}, "Select Map", "]"]]
tellraw @s ""
tellraw @s ["",["","  ",{"translate":"mgs.actions"},": "],[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/start"}, "hover_event": {"action": "show_text", "value": "Start the zombies game"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/stop"}, "hover_event": {"action": "show_text", "value": "Stop the zombies game"}}, "\u25a0 STOP", "]"]]
tellraw @s {"text":"============================================","color":"dark_gray"}

