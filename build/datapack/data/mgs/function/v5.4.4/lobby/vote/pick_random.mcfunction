
#> mgs:v5.4.4/lobby/vote/pick_random
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/resolve with storage mgs:temp _lv_pick
#			mgs:v5.4.4/lobby/zombies/resolve with storage mgs:temp _lv_pick
#			mgs:v5.4.4/lobby/missions/resolve with storage mgs:temp _lv_pick
#
# @args		max (unknown)
#

$execute store result storage mgs:temp _lv_pick.i int 1 run random value 0..$(max)
function mgs:v5.4.4/lobby/vote/pick_winner with storage mgs:temp _lv_pick

