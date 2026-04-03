
#> mgs:v5.0.0/missions/setup
#
# @within	mgs:config "hover_event": {"action": "show_text", "value": "Open the multiplayer game setup menu"}}, "Game Setup", "]"]," ",[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/setup"}, "hover_event": {"action": "show_text", "value": "Open the zombies setup menu"}}, "Zombies Setup", "]"]," ",[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/missions/setup"}, "hover_event": {"action": "show_text", "value": "Open the mission setup menu"}}, "Mission Setup", "]"]]
#

tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s [{"text":"","color":"aqua","bold":true},"       🎯 ",{"translate":"mgs.missions_setup"}," 🎯"]
tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s ["",["","  ",{"translate":"mgs.map"},": "],[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/missions/map_select"}, "hover_event": {"action": "show_text", "value": "Browse and select a mission map"}}, "Select Map", "]"]]
tellraw @s ""
tellraw @s ["",["","  ",{"translate":"mgs.actions"},": "],[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/missions/start"}, "hover_event": {"action": "show_text", "value": "Start the mission"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/missions/stop"}, "hover_event": {"action": "show_text", "value": "Stop the mission"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/select_class"}, "hover_event": {"action": "show_text", "value": "Select your class"}}, "\u2694 Classes", "]"]]
tellraw @s {"text":"============================================","color":"dark_gray"}

