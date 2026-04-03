
#> mgs:v5.0.0/multiplayer/join_blue
#
# @executed	as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}]
#
# @within	mgs:v5.0.0/multiplayer/auto_assign_team
#			mgs:v5.0.0/multiplayer/setup "hover_event": {"action": "show_text", "value": "Join Red Team"}}, "Red", "]"]," ",[{"text": "[", "color": "blue", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/join_blue"}, "hover_event": {"action": "show_text", "value": "Join Blue Team"}}, "Blue", "]"]," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/auto_assign_team"}, "hover_event": {"action": "show_text", "value": "Auto-balance assign"}}, "Auto", "]"]]
#

scoreboard players set @s mgs.mp.team 2
team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.you_joined","color":"white"},{"translate":"mgs.blue_team","color":"blue","bold":true}]

