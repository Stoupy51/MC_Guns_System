
#> mgs:v5.4.0/stats/board/render
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/stats/board/show {path:'$(path)',kind:"$(kind)"}
#			mgs:v5.4.0/stats/board/hologram with storage mgs:temp _lb_cb
#
# @args		path (string)
#			kind (string)
#

data modify storage mgs:temp _lb_lines set value []
$data modify storage mgs:temp _lb_walk set from storage mgs:stats leaderboards.$(path)
scoreboard players set #lb_k mgs.data 0
$function mgs:v5.4.0/stats/board/render_next {kind:"$(kind)"}

