
#> mgs:v5.4.4/stats/board/forget_mi_one
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/stats/board/forget_mi_next with storage mgs:temp _fg
#
# @args		id (unknown)
#			uuid (unknown)
#

$data remove storage mgs:stats leaderboards.mi_map."$(id)"[{uuid:$(uuid)}]

