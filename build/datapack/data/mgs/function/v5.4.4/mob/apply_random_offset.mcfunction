
#> mgs:v5.4.4/mob/apply_random_offset
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/mob/apply_inaccuracy with storage mgs:temp _rot
#
# @args		max (unknown)
#

$execute store result storage mgs:temp _rot.yaw double 0.1 run random value -$(max)..$(max)
$execute store result storage mgs:temp _rot.pitch double 0.1 run random value -$(max)..$(max)
function mgs:v5.4.4/mob/apply_rotation_offset with storage mgs:temp _rot

