
#> mgs:v5.4.4/lobby/vote/drop_at
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/vote/drop_random with storage mgs:temp _lv_pick
#
# @args		i (unknown)
#

$data remove storage mgs:temp _lv_opts[$(i)]

