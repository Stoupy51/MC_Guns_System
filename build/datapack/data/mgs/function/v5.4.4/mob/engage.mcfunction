
#> mgs:v5.4.4/mob/engage
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/mob/tick
#

tag @s add mgs.mob_engaged
scoreboard players operation @s mgs.mob.reaction = @s mgs.mob.reaction_time

