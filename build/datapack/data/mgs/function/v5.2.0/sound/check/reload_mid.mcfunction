
#> mgs:v5.2.0/sound/check/reload_mid
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/player/tick
#

scoreboard players set #divisor mgs.data 2
execute store result score #half mgs.data run data get storage mgs:gun all.stats.reload_time
scoreboard players operation #half mgs.data /= #divisor mgs.data
scoreboard players operation #remaining mgs.data = @s mgs.cooldown
scoreboard players operation #remaining mgs.data -= #total_tick mgs.data

# Half the cooldown: the mid sound plays.
execute if score #remaining mgs.data = #half mgs.data run function mgs:v5.2.0/sound/player_mid with storage mgs:gun all.sounds

