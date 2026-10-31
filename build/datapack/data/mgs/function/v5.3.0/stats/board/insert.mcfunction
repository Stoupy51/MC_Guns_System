
#> mgs:v5.3.0/stats/board/insert
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/board/levels with storage mgs:temp _lb
#			mgs:v5.3.0/stats/board/zb_round with storage mgs:temp _lb
#			mgs:v5.3.0/stats/board/zb_round_bucket with storage mgs:temp _lb
#			mgs:v5.3.0/stats/board/mi_time with storage mgs:temp _lb
#
# @args		path (string)
#			uuid (unknown)
#			value (unknown)
#

$scoreboard players set #lb_new mgs.data $(value)
$execute store success score #lb_has mgs.data store result score #lb_old mgs.data run data get storage mgs:stats leaderboards.$(path)[{uuid:$(uuid)}].value
execute if score #lb_has mgs.data matches 1 if score #lb_desc mgs.data matches 1 if score #lb_old mgs.data >= #lb_new mgs.data run return fail
execute if score #lb_has mgs.data matches 1 if score #lb_desc mgs.data matches 0 if score #lb_old mgs.data <= #lb_new mgs.data run return fail

$data remove storage mgs:stats leaderboards.$(path)[{uuid:$(uuid)}]
$execute unless data storage mgs:stats leaderboards.$(path) run data modify storage mgs:stats leaderboards.$(path) set value []
$data modify storage mgs:temp _lb_walk set from storage mgs:stats leaderboards.$(path)
scoreboard players set #lb_k mgs.data 0
function mgs:v5.3.0/stats/board/walk
execute store result storage mgs:temp _lb.k int 1 run scoreboard players get #lb_k mgs.data
function mgs:v5.3.0/stats/board/insert_at with storage mgs:temp _lb
scoreboard players add #lb_k mgs.data 1
return 1

