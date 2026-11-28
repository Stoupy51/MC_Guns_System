
#> mgs:v5.4.4/stats/board/forget_zb_one
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/stats/board/forget_zb_next with storage mgs:temp _fg
#
# @args		id (unknown)
#			uuid (unknown)
#

$data remove storage mgs:stats leaderboards.zb_map."$(id)"."1"[{uuid:$(uuid)}]
$data remove storage mgs:stats leaderboards.zb_map."$(id)"."2"[{uuid:$(uuid)}]
$data remove storage mgs:stats leaderboards.zb_map."$(id)"."3"[{uuid:$(uuid)}]
$data remove storage mgs:stats leaderboards.zb_map."$(id)"."4"[{uuid:$(uuid)}]

