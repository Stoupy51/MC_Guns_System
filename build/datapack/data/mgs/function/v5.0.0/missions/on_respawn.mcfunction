
#> mgs:v5.0.0/missions/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Reset death counter
scoreboard players set @s mgs.mp.death_count 0

# Teleport to random mission spawn point
function mgs:v5.0.0/missions/respawn_tp

# Re-apply saturation
effect give @s saturation infinite 255 true

# Re-apply class loadout (lost on death)
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# Re-give compass
item replace entity @s hotbar.3 with compass[custom_data={mgs:{compass:true}}]

