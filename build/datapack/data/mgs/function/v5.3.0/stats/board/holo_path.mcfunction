
#> mgs:v5.3.0/stats/board/holo_path
#
# @within	mgs:v5.3.0/stats/board/holo_place with storage mgs:temp _lb_h
#
# @args		board (unknown)
#			map_id (unknown)
#			players (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#

$data modify storage mgs:temp _lb_h.path set value "$(board)"
$execute if data storage mgs:temp _lb_h{board:"zb_map"} run data modify storage mgs:temp _lb_h.path set value 'zb_map."$(map_id)"."$(players)"'
$execute if data storage mgs:temp _lb_h{board:"mi_map"} run data modify storage mgs:temp _lb_h.path set value 'mi_map."$(map_id)"'
$summon minecraft:marker $(x).5 $(y) $(z).5 {CustomName:"Leaderboard",Tags:["mgs.leaderboard","mgs.zombies_entity","mgs.lb_new"]}
data modify entity @n[type=minecraft:marker,tag=mgs.lb_new] data.lb set from storage mgs:temp _lb_h
tag @e[type=minecraft:marker,tag=mgs.lb_new] remove mgs.lb_new

