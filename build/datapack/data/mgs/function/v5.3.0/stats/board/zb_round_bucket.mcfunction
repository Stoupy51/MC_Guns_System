
#> mgs:v5.3.0/stats/board/zb_round_bucket
#
# @within	mgs:v5.3.0/stats/board/zb_round with storage mgs:temp _lb
#
# @args		map_id (string)
#			n (unknown)
#

$data modify storage mgs:temp _lb.path set value 'zb_map."$(map_id)"."$(n)"'
execute store success score #lb_rec mgs.data run function mgs:v5.3.0/stats/board/insert with storage mgs:temp _lb
execute if score #lb_rec mgs.data matches 1 store result storage mgs:temp _lb.rank int 1 run scoreboard players get #lb_k mgs.data
execute if score #lb_rec mgs.data matches 1 run function mgs:v5.3.0/stats/board/announce with storage mgs:temp _lb

