
#> mgs:v5.1.0/multiplayer/actual_respawn
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/game_tick [ at @s ]
#

# Stop spectating
spectate @s

# Teleport to best spawn point
function mgs:v5.1.0/multiplayer/respawn_tp

# Reset stamina to full on respawn (the stamina system owns the hunger bar)
scoreboard players set @s mgs.stam_seen 0

# Apply current class loadout (positive = standard, negative = custom)
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

# Switch back to adventure
gamemode adventure @s

# Run map-defined respawn commands on this player (if any)
execute if data storage mgs:multiplayer game.map.respawn_commands[0] at @s run function mgs:v5.1.0/shared/run_respawn_commands {mode:"multiplayer"}

# Call map respawn script (executed as the respawning player)
function mgs:v5.1.0/shared/maps/call_respawn_script_at_base

