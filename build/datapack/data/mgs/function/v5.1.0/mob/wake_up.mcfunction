
#> mgs:v5.1.0/mob/wake_up
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.1.0/mob/tick
#			mgs:v5.1.0/mob/init
#

tag @s remove mgs.mob_sleeping
scoreboard players operation @s mgs.mob.timer = @s mgs.mob.active_time

