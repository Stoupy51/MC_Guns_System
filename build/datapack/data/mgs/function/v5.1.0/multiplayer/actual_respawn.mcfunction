
#> mgs:v5.1.0/multiplayer/actual_respawn
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/game_tick [ at @s ]
#

spectate @s

function mgs:v5.1.0/multiplayer/respawn_tp

# The stamina system owns the hunger bar.
scoreboard players set @s mgs.stam_seen 0

# Positive: standard class, negative: custom loadout.
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

gamemode adventure @s

execute if data storage mgs:multiplayer game.map.respawn_commands[0] at @s run function mgs:v5.1.0/shared/run_respawn_commands {mode:"multiplayer"}

# Run as the respawning player.
function mgs:v5.1.0/shared/maps/call_script_at_base {script:"respawn"}

