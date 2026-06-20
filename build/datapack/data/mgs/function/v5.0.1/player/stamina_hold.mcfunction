
#> mgs:v5.0.1/player/stamina_hold
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/stamina_tick
#

execute store result score #stam_food mgs.data run data get entity @s foodLevel
execute if score #stam_food mgs.data matches 7.. run effect give @s minecraft:hunger 1 255 true
execute if score #stam_food mgs.data matches ..6 run effect clear @s minecraft:hunger

