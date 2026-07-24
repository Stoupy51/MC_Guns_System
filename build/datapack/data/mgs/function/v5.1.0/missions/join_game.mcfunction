
#> mgs:v5.1.0/missions/join_game
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/players/mi_join
#			dialog mgs:v5.1.0/missions/setup
#

# Require an active game
execute unless data storage mgs:missions game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_mission_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.mi.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_mission","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.mi.in_game 1
scoreboard players set @s mgs.mp.team 1
team join mgs.blue @s
scoreboard players set @s mgs.mi.kills 0
scoreboard players set @s mgs.mi.deaths 0
scoreboard players set @s mgs.mp.death_count 0
scoreboard players set @s mgs.mp.spectate_timer 0

# Setup player
gamemode adventure @s

# Reset stamina so the stamina system re-inits this player at full (it owns the hunger bar)
scoreboard players set @s mgs.stam_seen 0

# Enable class menu and show class selection
tag @s add mgs.give_class_menu
function mgs:v5.1.0/multiplayer/select_class

# Apply class if already chosen
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

item replace entity @s hotbar.3 with compass[custom_data={mgs:{compass:true}}]

# Teleport to spawn
function mgs:v5.1.0/missions/respawn_tp

# Call map join script (executed as the joining player)
function mgs:v5.1.0/shared/maps/call_join_script_at_base

# Announce
tellraw @a ["",{"selector":"@s","color":"green"},[{"text":" ","color":"green"}, {"translate":"mgs.joined_the_mission"}]]

