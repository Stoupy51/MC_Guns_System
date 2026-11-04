
#> mgs:v5.3.0/mob/go_sleep
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/mob/tick
#

tag @s add mgs.mob_sleeping
scoreboard players operation @s mgs.mob.timer = @s mgs.mob.sleep_time

