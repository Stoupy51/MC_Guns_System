
#> mgs:v5.2.0/sound/check/pump
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/player/tick
#

scoreboard players set #divisor mgs.data 2
execute store result score #half mgs.data run data get storage mgs:gun all.stats.cooldown
scoreboard players operation #half mgs.data /= #divisor mgs.data
scoreboard players operation #remaining mgs.data = @s mgs.cooldown
scoreboard players operation #remaining mgs.data -= #total_tick mgs.data

# Half the cooldown: the pump plays and throws the shell out.
execute if score #remaining mgs.data = #half mgs.data run function mgs:v5.2.0/sound/pump with storage mgs:gun all.sounds
execute if score #remaining mgs.data = #half mgs.data run function mgs:v5.2.0/casing/main

