
#> mgs:v5.1.0/zombies/freeze_mob
#
# @executed	as @e[tag=mgs.zombie_round]
#
# @within	mgs:v5.1.0/zombies/freeze_on [ as @e[tag=mgs.zombie_round] ]
#

tag @s add mgs.zb_frozen_ai
data merge entity @s {NoAI:1b}

