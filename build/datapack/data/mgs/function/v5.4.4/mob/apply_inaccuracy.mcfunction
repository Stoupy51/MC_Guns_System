
#> mgs:v5.4.4/mob/apply_inaccuracy
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/mob/fire_weapon
#

execute store result storage mgs:temp _rot.max int 1 run scoreboard players get @s mgs.mob.spread
function mgs:v5.4.4/mob/apply_random_offset with storage mgs:temp _rot

