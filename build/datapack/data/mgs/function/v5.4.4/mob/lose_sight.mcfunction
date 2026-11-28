
#> mgs:v5.4.4/mob/lose_sight
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/mob/tick
#

tag @e[tag=mgs.target,limit=1] remove mgs.target
tag @s remove mgs.mob_engaged

