
#> mgs:v5.3.0/sound/check/reload_end
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/tick
#

execute store result score #reload_end mgs.data run data get storage mgs:gun all.stats.reload_end
scoreboard players operation #remaining mgs.data = @s mgs.cooldown
scoreboard players operation #remaining mgs.data -= #total_tick mgs.data
execute if score #remaining mgs.data = #reload_end mgs.data run function mgs:v5.3.0/sound/player_end with storage mgs:gun all.sounds

