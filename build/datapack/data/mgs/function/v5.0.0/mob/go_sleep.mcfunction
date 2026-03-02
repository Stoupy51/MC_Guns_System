
#> mgs:v5.0.0/mob/go_sleep
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.0.0/mob/tick
#

# Add sleeping tag and set timer to sleep duration
tag @s add mgs.mob_sleeping
scoreboard players operation @s mgs.mob.timer = @s mgs.mob.sleep_time

