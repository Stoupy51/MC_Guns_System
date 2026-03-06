
#> mgs:v5.0.0/multiplayer/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Reset death counter
scoreboard players set @s mgs.mp.death_count 0

# Increment death stats
scoreboard players add @s mgs.mp.deaths 1

# Teleport to best spawn point
function mgs:v5.0.0/multiplayer/respawn_tp

# Re-apply permanent saturation (lost on death)
effect give @s saturation infinite 255 true

# Apply current class loadout (positive = standard, negative = custom)
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

