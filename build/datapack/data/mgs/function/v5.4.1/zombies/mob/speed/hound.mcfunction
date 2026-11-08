
#> mgs:v5.4.1/zombies/mob/speed/hound
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/mob/speed
#

execute if score #zb_round mgs.data matches ..9 run attribute @s minecraft:movement_speed base set 0.36
execute if score #zb_round mgs.data matches 10..19 run attribute @s minecraft:movement_speed base set 0.4
execute if score #zb_round mgs.data matches 20.. run attribute @s minecraft:movement_speed base set 0.44

