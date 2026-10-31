
#> mgs:v5.3.0/stats/board/mi_time
#
# @within	mgs:v5.3.0/stats/mi/player_end with storage mgs:temp _st_one
#
# @args		uuid (unknown)
#			map_id (unknown)
#

scoreboard players set #lb_desc mgs.data 0
$data modify storage mgs:temp _lb set value {uuid:$(uuid),entry:{uuid:$(uuid)},path:'mi_map."$(map_id)"'}
execute store result storage mgs:temp _lb.value int 1 store result storage mgs:temp _lb.entry.value int 1 run scoreboard players get #mi_timer mgs.data
execute store result storage mgs:temp _lb.entry.players int 1 run scoreboard players get #lb_n mgs.data
function mgs:v5.3.0/stats/board/insert with storage mgs:temp _lb

