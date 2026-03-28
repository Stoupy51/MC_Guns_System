
#> mgs:v5.0.0/missions/actual_respawn
#
# @executed	at @s
#
# @within	mgs:v5.0.0/missions/game_tick [ at @s ]
#

# Stop spectating
spectate @s

# Switch back to adventure
gamemode adventure @s

# Teleport to random mission spawn point
function mgs:v5.0.0/missions/respawn_tp

# Re-apply saturation
effect give @s saturation infinite 255 true

# Re-apply class loadout (lost on death)
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# Re-give compass
item replace entity @s hotbar.3 with compass[custom_data={mgs:{compass:true}}]

# Run map-defined respawn commands on this player (if any)
execute if data storage mgs:missions game.map.respawn_commands[0] at @s run function mgs:v5.0.0/missions/run_respawn_commands

