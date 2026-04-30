
#> mgs:v5.0.0/multiplayer/join_game
#
# @within	mgs:v5.0.0/multiplayer/setup "hover_event": {"action": "show_text", "value": "Start the match"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/stop"}, "hover_event": {"action": "show_text", "value": "Stop the match"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/select_class"}, "hover_event": {"action": "show_text", "value": "Select your class"}}, "\u2694 Classes", "]"]," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/join_game"}, "hover_event": {"action": "show_text", "value": "Join the ongoing game as a late joiner"}}, "+ Join", "]"]]
#

# Require an active or preparing game
execute unless data storage mgs:multiplayer game{state:"active"} unless data storage mgs:multiplayer game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_game_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.mp.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_game","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.mp.in_game 1
scoreboard players set @s mgs.mp.kills 0
scoreboard players set @s mgs.mp.deaths 0
scoreboard players set @s mgs.mp.death_count 0
scoreboard players set @s mgs.mp.spectate_timer 0

# Auto-assign team if not already on one
execute unless score @s mgs.mp.team matches 1.. run function mgs:v5.0.0/multiplayer/auto_assign_team

# Setup player (match active game settings)
gamemode adventure @s
attribute @s minecraft:waypoint_receive_range base set 0.0
effect give @s saturation infinite 255 true

# Enable class menu and show class selection
tag @s add mgs.give_class_menu
function mgs:v5.0.0/multiplayer/select_class

# Apply class if already chosen
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# Teleport to spawn
function mgs:v5.0.0/multiplayer/respawn_tp

# Announce
tellraw @a ["",{"selector":"@s","color":"yellow"},[{"text":" ","color":"yellow"}, {"translate":"mgs.joined_the_game"}]]

