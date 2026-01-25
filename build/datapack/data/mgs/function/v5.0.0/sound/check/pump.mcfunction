
#> mgs:v5.0.0/sound/check/pump
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Calculate half of weapon cooldown
scoreboard players set #divisor mgs.data 2
execute store result score #half mgs.data run data get storage mgs:gun all.stats.cooldown
scoreboard players operation #half mgs.data /= #divisor mgs.data

# If current cooldown equals half, play mid cooldown sound and remove tag
execute if score @s mgs.cooldown = #half mgs.data run function mgs:v5.0.0/sound/pump with storage mgs:gun all.sounds

