
#> mgs:v5.0.0/multiplayer/actual_respawn
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/game_tick [ at @s ]
#

# Stop spectating
spectate @s

# Switch back to adventure
gamemode adventure @s

# Teleport to best spawn point
function mgs:v5.0.0/multiplayer/respawn_tp

# Re-apply permanent saturation (lost on death)
effect give @s saturation infinite 255 true

# Apply current class loadout (positive = standard, negative = custom)
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

