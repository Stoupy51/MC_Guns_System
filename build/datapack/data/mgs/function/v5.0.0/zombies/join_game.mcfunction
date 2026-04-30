
#> mgs:v5.0.0/zombies/join_game
#
# @within	mgs:v5.0.0/zombies/setup "hover_event": {"action": "show_text", "value": "Start the zombies game"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/stop"}, "hover_event": {"action": "show_text", "value": "Stop the zombies game"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "dark_aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/show_teams"}, "hover_event": {"action": "show_text", "value": "Show which players have team assignments"}}, "\ud83d\udc65 Roster", "]"]," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/join_game"}, "hover_event": {"action": "show_text", "value": "Join the ongoing zombies game as a late joiner"}}, "+ Join", "]"]]
#

# Require an active zombies game
execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_zombies_game_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.zb.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_zombies_game","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.zb.in_game 1
scoreboard players set @s mgs.zb.points 500
scoreboard players set @s mgs.zb.kills 0
scoreboard players set @s mgs.zb.downs 0
scoreboard players set @s mgs.zb.passive 0
scoreboard players set @s mgs.zb.ability 0
scoreboard players set @s mgs.zb.ability_cd 0
scoreboard players set @s mgs.mp.spectate_timer 0
scoreboard players set @s mgs.mp.death_count 0

# Setup player
gamemode adventure @s
effect give @s saturation infinite 255 true

# Enable class menu and show class selection
tag @s add mgs.give_class_menu
function mgs:v5.0.0/multiplayer/select_class

# Apply class if already chosen
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# Teleport to spawn
function mgs:v5.0.0/zombies/respawn_tp

# Announce
tellraw @a ["",{"selector":"@s","color":"dark_green"},[{"text":" ","color":"dark_green"}, {"translate":"mgs.joined_the_zombies_game"}]]

