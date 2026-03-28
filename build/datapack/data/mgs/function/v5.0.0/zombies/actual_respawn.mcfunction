
#> mgs:v5.0.0/zombies/actual_respawn
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

# Stop spectating
spectate @s

# Teleport to random player spawn
function mgs:v5.0.0/zombies/respawn_tp

# Re-apply saturation
effect give @s saturation infinite 255 true

# Switch back to adventure
gamemode adventure @s

# Re-give starting weapon on respawn
function mgs:v5.0.0/zombies/inventory/give_respawn_loadout

