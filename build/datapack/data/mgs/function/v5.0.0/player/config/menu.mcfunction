
#> mgs:v5.0.0/player/config/menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

tellraw @s {"text":"=======================================","color":"dark_gray"}
tellraw @s ["",[{"text":"","color":"gold","bold":true},"       🎮 ",{"translate":"mgs.player_settings"}," 🎮"]]
tellraw @s {"text":"=======================================","color":"dark_gray"}
execute if score @s mgs.player.hitmarker matches 1 run tellraw @s ["  ",{"translate":"mgs.hitmarker_sound"},": ",{"text":"ON","color":"green"},{"text":" ✔ ","color":"green"},[{"text": "[", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 2"}, "hover_event": {"action": "show_text", "value": "Toggle hitmarker Sound on entity hit"}}, "Toggle", "]"]]
execute unless score @s mgs.player.hitmarker matches 1 run tellraw @s ["  ",{"translate":"mgs.hitmarker_sound"},": ",{"translate":"mgs.off","color":"red"},{"text":" ✘","color":"red"},[{"text": "[", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 2"}, "hover_event": {"action": "show_text", "value": "Toggle hitmarker Sound on entity hit"}}, "Toggle", "]"]]
execute if score @s mgs.player.damage_debug matches 1 run tellraw @s ["  ",{"translate":"mgs.damage_debug"},": ",{"text":"ON","color":"green"},{"text":" ✔ ","color":"green"},[{"text": "[", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 3"}, "hover_event": {"action": "show_text", "value": "Toggle damage numbers in chat"}}, "Toggle", "]"]]
execute unless score @s mgs.player.damage_debug matches 1 run tellraw @s ["  ",{"translate":"mgs.damage_debug"},": ",{"translate":"mgs.off","color":"red"},{"text":" ✘","color":"red"},[{"text": "[", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 3"}, "hover_event": {"action": "show_text", "value": "Toggle damage numbers in chat"}}, "Toggle", "]"]]
tellraw @s ["  ",{"translate":"mgs.multiplayer"},": ",[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 4"}, "hover_event": {"action": "show_text", "value": "Open multiplayer class selection menu"}}, "Select Class", "]"]]
tellraw @s {"text":"=======================================","color":"dark_gray"}
tellraw @s ["  ",{"translate":"mgs.use_2","color":"gray","italic":true}," ",[{"text":"/","color":"aqua","italic":true}, {"translate":"mgs.trigger_mgs_player_config"}]," ",{"translate":"mgs.to_reopen","color":"gray","italic":true}]

