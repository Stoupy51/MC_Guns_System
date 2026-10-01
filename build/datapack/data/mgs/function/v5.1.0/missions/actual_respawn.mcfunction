
#> mgs:v5.1.0/missions/actual_respawn
#
# @executed	at @s
#
# @within	mgs:v5.1.0/missions/game_tick [ at @s ]
#

spectate @s

gamemode adventure @s

function mgs:v5.1.0/missions/respawn_tp
scoreboard players set @s mgs.mi.died_here 0

# The stamina system owns the hunger bar.
scoreboard players set @s mgs.stam_seen 0

# Lost on death.
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

item replace entity @s hotbar.3 with compass[custom_data={mgs:{compass:true}}]

execute if data storage mgs:missions game.map.respawn_commands[0] at @s run function mgs:v5.1.0/shared/run_respawn_commands {mode:"missions"}

# Run as the respawning player.
function mgs:v5.1.0/shared/maps/call_script_at_base {script:"respawn"}

