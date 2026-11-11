
#> mgs:v5.4.2/mob/go_sleep
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/mob/tick
#

tag @s add mgs.mob_sleeping
scoreboard players operation @s mgs.mob.timer = @s mgs.mob.sleep_time

