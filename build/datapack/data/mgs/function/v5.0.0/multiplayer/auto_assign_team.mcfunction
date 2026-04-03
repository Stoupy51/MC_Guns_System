
#> mgs:v5.0.0/multiplayer/auto_assign_team
#
# @executed	as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}]
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/tdm/setup [ as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}] ]
#			mgs:v5.0.0/multiplayer/setup "hover_event": {"action": "show_text", "value": "Join Red Team"}}, "Red", "]"]," ",[{"text": "[", "color": "blue", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/join_blue"}, "hover_event": {"action": "show_text", "value": "Join Blue Team"}}, "Blue", "]"]," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/auto_assign_team"}, "hover_event": {"action": "show_text", "value": "Auto-balance assign"}}, "Auto", "]"]]
#

# Count players on each team
execute store result score #red_count mgs.data if entity @a[scores={mgs.mp.team=1}]
execute store result score #blue_count mgs.data if entity @a[scores={mgs.mp.team=2}]

# Assign to team with fewer players (red if tied)
execute if score #red_count mgs.data <= #blue_count mgs.data run function mgs:v5.0.0/multiplayer/join_red
execute if score #red_count mgs.data > #blue_count mgs.data run function mgs:v5.0.0/multiplayer/join_blue

