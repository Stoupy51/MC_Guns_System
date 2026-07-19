
#> mgs:v5.1.0/zombies/dog_portal_tick
#
# @executed	as @e[tag=mgs.dog_portal] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=mgs.dog_portal] & at @s ]
#

particle minecraft:electric_spark ~ ~0.3 ~ 0.25 0.4 0.25 0.06 4 normal @a[distance=..48]
particle minecraft:crit ~ ~0.1 ~ 0.3 0.05 0.3 0.02 2 normal @a[distance=..32]

scoreboard players remove @s mgs.zb.rise_tick 1
execute if score @s mgs.zb.rise_tick matches ..0 run function mgs:v5.1.0/zombies/dog_portal_strike

