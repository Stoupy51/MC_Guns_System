
#> mgs:v5.0.1/missions/join_game
#
# @within	mgs:v5.0.1/missions/setup "hover_event": {"action": "show_text", "value": "Start the mission"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.1/missions/stop"}, "hover_event": {"action": "show_text", "value": "Stop the mission"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.1/multiplayer/select_class"}, "hover_event": {"action": "show_text", "value": "Select your class"}}, "\u2694 Classes", "]"]," ",[{"text": "[", "color": "dark_aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.1/multiplayer/show_teams"}, "hover_event": {"action": "show_text", "value": "Show which players have team assignments"}}, "\ud83d\udc65 Roster", "]"]," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.1/missions/join_game"}, "hover_event": {"action": "show_text", "value": "Join the ongoing mission as a late joiner"}}, "+ Join", "]"]]
#

# Require an active mission
execute unless data storage mgs:missions game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_mission_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.mi.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_mission","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.mi.in_game 1
scoreboard players set @s mgs.mp.team 1
scoreboard players set @s mgs.mi.kills 0
scoreboard players set @s mgs.mi.deaths 0
scoreboard players set @s mgs.mp.death_count 0
scoreboard players set @s mgs.mp.spectate_timer 0

# Setup player
gamemode adventure @s
effect give @s saturation infinite 255 true

# Enable class menu and show class selection
tag @s add mgs.give_class_menu
function mgs:v5.0.1/multiplayer/select_class

# Apply class if already chosen
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.0.1/multiplayer/apply_class

# Give compass
item replace entity @s hotbar.3 with compass[custom_data={mgs:{compass:true}}]

# Teleport to spawn
function mgs:v5.0.1/missions/respawn_tp

# Call map join script (executed as the joining player)
function mgs:v5.0.1/shared/maps/call_join_script_at_base

# Announce
tellraw @a ["",{"selector":"@s","color":"green"},[{"text":" ","color":"green"}, {"translate":"mgs.joined_the_mission"}]]

