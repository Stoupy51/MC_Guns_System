
#> mgs:v5.0.1/player/stamina_wind
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/stamina_tick
#

scoreboard players set @s mgs.stam_out 1
effect clear @s minecraft:saturation
# Out-of-breath feedback
playsound minecraft:entity.player.breath player @s ~ ~ ~ 0.5 0.8
title @s actionbar [{"text":"⚡ ","color":"yellow"},{"translate":"mgs.out_of_breath","color":"gray","italic":true}]

