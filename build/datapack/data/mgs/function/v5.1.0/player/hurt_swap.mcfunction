
#> mgs:v5.1.0/player/hurt_swap
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/hurt_tick
#

execute if score @s mgs.hurt_fx matches 1 run posteffect remove @s mgs:hurt
execute if score @s mgs.hurt_fx matches 2 run posteffect remove @s mgs:hurt_critical
execute if score #hurt_tier mgs.data matches 1 run posteffect add @s mgs:hurt
execute if score #hurt_tier mgs.data matches 2 run posteffect add @s mgs:hurt_critical
scoreboard players operation @s mgs.hurt_fx = #hurt_tier mgs.data

