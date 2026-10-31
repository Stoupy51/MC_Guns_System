
#> mgs:v5.3.0/stats/board/render
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/show {path:'$(path)',kind:"$(kind)"}
#			mgs:v5.3.0/stats/board/holo_show with entity @s data.lb
#
# @args		path (string)
#			kind (string)
#

data modify storage mgs:temp _lb_lines set value []
$data modify storage mgs:temp _lb_walk set from storage mgs:stats leaderboards.$(path)
scoreboard players set #lb_k mgs.data 0
$function mgs:v5.3.0/stats/board/render_next {kind:"$(kind)"}

