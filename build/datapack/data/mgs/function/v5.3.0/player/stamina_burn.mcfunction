
#> mgs:v5.3.0/player/stamina_burn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/stamina_bar
#

scoreboard players remove @s mgs.stam_sat 8
execute if score @s mgs.stam_sat matches ..-1 run scoreboard players set @s mgs.stam_sat 0
effect give @s minecraft:hunger 1 255 true

