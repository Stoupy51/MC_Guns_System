
#> mgs:v5.4.4/lobby/vote/drop_random
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/vote/trim_maps with storage mgs:temp _lv_pick
#
# @args		max (unknown)
#

$execute store result storage mgs:temp _lv_pick.i int 1 run random value 0..$(max)
function mgs:v5.4.4/lobby/vote/drop_at with storage mgs:temp _lv_pick

