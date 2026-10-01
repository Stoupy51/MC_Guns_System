
#> mgs:v5.1.0/sound/check/pump
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

scoreboard players set #divisor mgs.data 2
execute store result score #half mgs.data run data get storage mgs:gun all.stats.cooldown
scoreboard players operation #half mgs.data /= #divisor mgs.data

# Half the cooldown: the mid sound plays.
execute if score @s mgs.cooldown = #half mgs.data run function mgs:v5.1.0/sound/pump with storage mgs:gun all.sounds

