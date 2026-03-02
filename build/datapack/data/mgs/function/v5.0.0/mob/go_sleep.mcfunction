
#> mgs:v5.0.0/mob/go_sleep
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.0.0/mob/tick
#

# Add sleeping tag
tag @s add mgs.mob_sleeping

# Set timer to sleep duration
scoreboard players operation @s mgs.mob.timer = @s mgs.mob.sleep_time

