
#> mgs:v5.4.0/stats/board/insert_at
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/stats/board/insert with storage mgs:temp _lb
#
# @args		path (unknown)
#			k (unknown)
#

$data modify storage mgs:stats leaderboards.$(path) insert $(k) from storage mgs:temp _lb.entry

