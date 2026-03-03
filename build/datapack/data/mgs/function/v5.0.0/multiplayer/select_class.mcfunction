
#> mgs:v5.0.0/multiplayer/select_class
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s ["",{"translate": "mgs.select_your_class","color":"gold","bold":true}]
tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s ["",{"translate": "mgs.assault", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 11"}, "hover_event": {"action": "show_text", "value": "Versatile frontline\nMain: AK47\nSecondary: M1911"}},{"translate": "mgs.versatile_frontline","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.rifleman", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 12"}, "hover_event": {"action": "show_text", "value": "Accurate mid-range\nMain: M16A4\nSecondary: M9"}},{"translate": "mgs.accurate_mid_range","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.support", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 13"}, "hover_event": {"action": "show_text", "value": "Suppressive heavy\nMain: M249\nSecondary: GLOCK17"}},{"translate": "mgs.suppressive_heavy","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.sniper", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 14"}, "hover_event": {"action": "show_text", "value": "Long-range precision\nMain: M24 4\nSecondary: DEAGLE"}},{"translate": "mgs.long_range_precision","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.smg", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 15"}, "hover_event": {"action": "show_text", "value": "Close quarters\nMain: MP7\nSecondary: GLOCK18"}},{"translate": "mgs.close_quarters","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.shotgunner", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 16"}, "hover_event": {"action": "show_text", "value": "Breaching / CQB\nMain: SPAS12\nSecondary: M9"}},{"translate": "mgs.breaching_cqb","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.engineer", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 17"}, "hover_event": {"action": "show_text", "value": "Objective / demolitions\nMain: MP5\nSecondary: MAKAROV"}},{"translate": "mgs.objective_demolitions","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.medic", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 18"}, "hover_event": {"action": "show_text", "value": "Team sustain\nMain: FAMAS\nSecondary: M1911"}},{"translate": "mgs.team_sustain","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.marksman", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 19"}, "hover_event": {"action": "show_text", "value": "Semi-auto precision\nMain: SVD\nSecondary: GLOCK17"}},{"translate": "mgs.semi_auto_precision","color":"gray","italic":true}]
tellraw @s ["",{"translate": "mgs.heavy", "color": "green", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 20"}, "hover_event": {"action": "show_text", "value": "Armored suppressor\nMain: RPK\nSecondary: MAKAROV"}},{"translate": "mgs.armored_suppressor","color":"gray","italic":true}]
tellraw @s {"text":"============================================","color":"dark_gray"}

