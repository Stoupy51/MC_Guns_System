
#> mgs:v5.3.0/player/stamina_refill
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/stamina_bar
#

scoreboard players add @s mgs.stam_sat 50
scoreboard players operation #stam_sat_cap mgs.data = @s mgs.food
scoreboard players add #stam_sat_cap mgs.data 1
scoreboard players operation #stam_sat_cap mgs.data *= #25 mgs.data
scoreboard players operation @s mgs.stam_sat < #stam_sat_cap mgs.data
effect give @s minecraft:saturation 1 0 true

