
#> mgs:v5.4.1/player/stamina_refill
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/stamina_bar
#

scoreboard players add @s mgs.stam_sat 50
scoreboard players operation #stam_sat_cap mgs.data = @s mgs.food
scoreboard players add #stam_sat_cap mgs.data 1
scoreboard players operation #stam_sat_cap mgs.data *= #25 mgs.data
scoreboard players operation @s mgs.stam_sat < #stam_sat_cap mgs.data
effect give @s minecraft:saturation 1 0 true

