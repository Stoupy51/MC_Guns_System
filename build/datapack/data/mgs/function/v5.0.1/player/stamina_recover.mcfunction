
#> mgs:v5.0.1/player/stamina_recover
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/stamina_tick
#

scoreboard players set @s mgs.stam_out 0
effect clear @s minecraft:hunger
effect give @s minecraft:saturation 2 20 true

