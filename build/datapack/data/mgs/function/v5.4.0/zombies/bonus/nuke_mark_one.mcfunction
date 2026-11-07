
#> mgs:v5.4.0/zombies/bonus/nuke_mark_one
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:zombies/bonus/nuke [ as @e[tag=mgs.nukable] ]
#

tag @s add mgs.nuked
attribute @s minecraft:attack_damage modifier add mgs:nuke_zero_damage -1 add_multiplied_total

