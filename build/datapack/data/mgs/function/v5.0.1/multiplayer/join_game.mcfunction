
#> mgs:v5.0.1/multiplayer/join_game
#
# @within	mgs:v5.0.1/multiplayer/setup "hover_event": {"action": "show_text", "value": "Start the match"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.1/multiplayer/stop"}, "hover_event": {"action": "show_text", "value": "Stop the match"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.1/multiplayer/select_class"}, "hover_event": {"action": "show_text", "value": "Select your class"}}, "\u2694 Classes", "]"]," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.1/multiplayer/join_game"}, "hover_event": {"action": "show_text", "value": "Join the ongoing game as a late joiner"}}, "+ Join", "]"]]
#

# Require an active game
execute unless data storage mgs:multiplayer game{state:"active"} unless data storage mgs:multiplayer game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_game_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.mp.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_game","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.mp.in_game 1
scoreboard players set @s mgs.mp.kills 0
scoreboard players set @s mgs.mp.deaths 0
scoreboard players set @s mgs.mp.death_count 0
scoreboard players set @s mgs.mp.spectate_timer 0
scoreboard players set @s mgs.last_hit 0
execute store result score @s mgs.hp_prev run data get entity @s Health 1

# Assign to FFA team for ffa mode, otherwise auto-assign to team
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run team join mgs.ffa @s
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} unless score @s mgs.mp.team matches 1.. run function mgs:v5.0.1/multiplayer/auto_assign_team

# Setup player
gamemode adventure @s

attribute @s minecraft:waypoint_receive_range base set 0.0

effect give @s saturation infinite 255 true

# Enable class menu and show class selection
tag @s add mgs.give_class_menu
function mgs:v5.0.1/multiplayer/select_class

# Apply class if already chosen
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.0.1/multiplayer/apply_class

# Teleport to spawn
function mgs:v5.0.1/multiplayer/respawn_tp

# Call map join script (executed as the joining player)
function mgs:v5.0.1/shared/maps/call_join_script_at_base

# Announce
tellraw @a ["",{"selector":"@s","color":"yellow"},[{"text":" ","color":"yellow"}, {"translate":"mgs.joined_the_game"}]]

