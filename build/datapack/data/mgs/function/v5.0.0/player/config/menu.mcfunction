
#> mgs:v5.0.0/player/config/menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

tellraw @s {"text":"=======================================","color":"dark_gray"}
tellraw @s ["",{"translate": "mgs.player_settings","color":"gold","bold":true}]
tellraw @s {"text":"=======================================","color":"dark_gray"}
execute if score @s mgs.player.hitmarker matches 1 run tellraw @s ["",{"text":"  Hitmarker Sound: ","color":"white"},{"text":"ON ✔ ","color":"green"},{"translate": "mgs.toggle", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 2"}, "hover_event": {"action": "show_text", "value": "Toggle hitmarker sound on entity hit"}}]
execute unless score @s mgs.player.hitmarker matches 1 run tellraw @s ["",{"text":"  Hitmarker Sound: ","color":"white"},{"text":"OFF ✘ ","color":"red"},{"translate": "mgs.toggle", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 2"}, "hover_event": {"action": "show_text", "value": "Toggle hitmarker sound on entity hit"}}]
execute if score @s mgs.player.damage_debug matches 1 run tellraw @s ["",{"text":"  Damage Debug: ","color":"white"},{"text":"ON ✔ ","color":"green"},{"translate": "mgs.toggle", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 3"}, "hover_event": {"action": "show_text", "value": "Toggle damage numbers in chat"}}]
execute unless score @s mgs.player.damage_debug matches 1 run tellraw @s ["",{"text":"  Damage Debug: ","color":"white"},{"text":"OFF ✘ ","color":"red"},{"translate": "mgs.toggle", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 3"}, "hover_event": {"action": "show_text", "value": "Toggle damage numbers in chat"}}]
tellraw @s {"text":"=======================================","color":"dark_gray"}
tellraw @s ["",{"translate": "mgs.use","color":"gray","italic":true},{"translate": "mgs.trigger_mgs_player_config","color":"aqua","italic":true},{"translate": "mgs.to_reopen","color":"gray","italic":true}]

