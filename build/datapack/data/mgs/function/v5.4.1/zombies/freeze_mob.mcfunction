
#> mgs:v5.4.1/zombies/freeze_mob
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/freeze_world [ as @e[tag=mgs.zombie_round] ]
#

tag @s add mgs.zb_frozen_ai
data merge entity @s {NoAI:1b}

