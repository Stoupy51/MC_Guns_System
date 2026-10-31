
#> mgs:v5.3.0/stats/board/zb_round
#
# @within	mgs:v5.3.0/stats/zb/player_end with storage mgs:temp _st_one
#
# @args		uuid (unknown)
#			name (unknown)
#			map_id (unknown)
#

scoreboard players set #lb_desc mgs.data 1
$data modify storage mgs:temp _lb set value {uuid:$(uuid),name:"$(name)",map_id:"$(map_id)",entry:{uuid:$(uuid)},path:'zb_map."$(map_id)".all'}
execute store result storage mgs:temp _lb.value int 1 store result storage mgs:temp _lb.entry.value int 1 run scoreboard players get #final_round mgs.data
execute store result storage mgs:temp _lb.entry.players int 1 run scoreboard players get #lb_n mgs.data
function mgs:v5.3.0/stats/board/insert with storage mgs:temp _lb

execute store result storage mgs:temp _lb.n int 1 run scoreboard players get #lb_n mgs.data
function mgs:v5.3.0/stats/board/zb_round_bucket with storage mgs:temp _lb

