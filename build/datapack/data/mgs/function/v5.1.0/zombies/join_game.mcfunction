
#> mgs:v5.1.0/zombies/join_game
#
# @within	mgs:v5.1.0/zombies/setup "hover_event": {"action": "show_text", "value": "Start the zombies game"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.1.0/zombies/stop"}, "hover_event": {"action": "show_text", "value": "Stop the zombies game"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "dark_aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.1.0/multiplayer/show_teams"}, "hover_event": {"action": "show_text", "value": "Show which players have team assignments"}}, "\ud83d\udc65 Roster", "]"]," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.1.0/zombies/join_game"}, "hover_event": {"action": "show_text", "value": "Join the ongoing zombies game as a late joiner"}}, "+ Join", "]"]]
#

# Require an active game
execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_zombies_game_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.zb.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_zombies_game","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.zb.in_game 1
team join mgs.zombies @s
scoreboard players set @s mgs.zb.points 500
scoreboard players set @s mgs.zb.kills 0
scoreboard players set @s mgs.zb.downs 0
scoreboard players set @s mgs.zb.passive 0
scoreboard players set @s mgs.zb.ability 0
scoreboard players set @s mgs.zb.ability_cd 0
scoreboard players set @s mgs.mp.spectate_timer 0
scoreboard players set @s mgs.mp.death_count 0
attribute @s minecraft:max_health base reset
attribute @s minecraft:entity_interaction_range base set 5

# Setup player
gamemode adventure @s

# Reset stamina so the stamina system re-inits this player at full (it owns the hunger bar)
scoreboard players set @s mgs.stam_seen 0

# Enable class menu and show class selection
tag @s add mgs.give_class_menu
function mgs:v5.1.0/multiplayer/select_class

# Apply class if already chosen
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

scoreboard players operation @s mgs.zb.prev_kills = @s mgs.total_kills

# Teleport to spawn
function mgs:v5.1.0/zombies/respawn_tp

# Call map join script (executed as the joining player)
function mgs:v5.1.0/shared/maps/call_join_script_at_base

# Announce
tellraw @a ["",{"selector":"@s","color":"dark_green"},[{"text":" ","color":"dark_green"}, {"translate":"mgs.joined_the_zombies_game"}]]

