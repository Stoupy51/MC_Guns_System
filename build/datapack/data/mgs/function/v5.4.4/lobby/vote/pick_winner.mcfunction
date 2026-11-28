
#> mgs:v5.4.4/lobby/vote/pick_winner
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/vote/pick_random with storage mgs:temp _lv_pick
#			mgs:v5.4.4/lobby/multiplayer/resolve with storage mgs:temp _lv_pick
#			mgs:v5.4.4/lobby/zombies/resolve with storage mgs:temp _lv_pick
#			mgs:v5.4.4/lobby/missions/resolve with storage mgs:temp _lv_pick
#
# @args		mode (string)
#			i (unknown)
#

$data modify storage mgs:lobby $(mode).winner set from storage mgs:lobby $(mode).options[$(i)]

