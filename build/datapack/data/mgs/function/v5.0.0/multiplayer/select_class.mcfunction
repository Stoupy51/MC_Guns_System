
#> mgs:v5.0.0/multiplayer/select_class
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s ["",{"translate": "mgs.select_your_class","color":"gold","bold":true}]
tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s ["",{"text": "[Assault]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 11"}, "hover_event": {"action": "show_text", "value": "Versatile frontline\nMain: AK47\nSecondary: M1911"}},{"text":" Versatile frontline","color":"gray","italic":true}]
tellraw @s ["",{"text": "[Rifleman]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 12"}, "hover_event": {"action": "show_text", "value": "Accurate mid-range\nMain: M16A4\nSecondary: M9"}},{"text":" Accurate mid-range","color":"gray","italic":true}]
tellraw @s ["",{"text": "[Support]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 13"}, "hover_event": {"action": "show_text", "value": "Suppressive heavy\nMain: M249\nSecondary: GLOCK17"}},{"text":" Suppressive heavy","color":"gray","italic":true}]
tellraw @s ["",{"text": "[Sniper]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 14"}, "hover_event": {"action": "show_text", "value": "Long-range precision\nMain: M24 4\nSecondary: DEAGLE"}},{"text":" Long-range precision","color":"gray","italic":true}]
tellraw @s ["",{"text": "[SMG]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 15"}, "hover_event": {"action": "show_text", "value": "Close quarters\nMain: MP7\nSecondary: GLOCK18"}},{"text":" Close quarters","color":"gray","italic":true}]
tellraw @s ["",{"text": "[Shotgunner]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 16"}, "hover_event": {"action": "show_text", "value": "Breaching / CQB\nMain: SPAS12\nSecondary: M9"}},{"text":" Breaching / CQB","color":"gray","italic":true}]
tellraw @s ["",{"text": "[Engineer]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 17"}, "hover_event": {"action": "show_text", "value": "Objective / demolitions\nMain: MP5\nSecondary: MAKAROV"}},{"text":" Objective / demolitions","color":"gray","italic":true}]
tellraw @s ["",{"text": "[Medic]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 18"}, "hover_event": {"action": "show_text", "value": "Team sustain\nMain: FAMAS\nSecondary: M1911"}},{"text":" Team sustain","color":"gray","italic":true}]
tellraw @s ["",{"text": "[Marksman]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 19"}, "hover_event": {"action": "show_text", "value": "Semi-auto precision\nMain: SVD\nSecondary: GLOCK17"}},{"text":" Semi-auto precision","color":"gray","italic":true}]
tellraw @s ["",{"text": "[Heavy]", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 20"}, "hover_event": {"action": "show_text", "value": "Armored suppressor\nMain: RPK\nSecondary: MAKAROV"}},{"text":" Armored suppressor","color":"gray","italic":true}]
tellraw @s {"text":"============================================","color":"dark_gray"}

