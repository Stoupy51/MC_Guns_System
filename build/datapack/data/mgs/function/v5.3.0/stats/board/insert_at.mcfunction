
#> mgs:v5.3.0/stats/board/insert_at
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/board/insert with storage mgs:temp _lb
#
# @args		path (unknown)
#			k (unknown)
#

$data modify storage mgs:stats leaderboards.$(path) insert $(k) from storage mgs:temp _lb.entry

