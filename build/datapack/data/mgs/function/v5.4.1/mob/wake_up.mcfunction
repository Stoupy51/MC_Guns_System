
#> mgs:v5.4.1/mob/wake_up
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/mob/tick
#			mgs:v5.4.1/mob/init
#

tag @s remove mgs.mob_sleeping
scoreboard players operation @s mgs.mob.timer = @s mgs.mob.active_time

