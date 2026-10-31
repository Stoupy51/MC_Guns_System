
#> mgs:v5.3.0/stats/board/admin_next
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/stats/admin/boards {board:"zb_map",label:"Zombies"}
#			mgs:v5.3.0/stats/admin/boards {board:"mi_map",label:"Missions"}
#			mgs:v5.3.0/stats/board/admin_next {board:"$(board)",label:"$(label)"}
#
# @args		board (string)
#			label (string)
#

execute unless data storage mgs:temp _lb_maps[0] run return 0
$data modify storage mgs:temp _lb_maps[0].board set value "$(board)"
$data modify storage mgs:temp _lb_maps[0].label set value "$(label)"
function mgs:v5.3.0/stats/board/admin_button with storage mgs:temp _lb_maps[0]
data remove storage mgs:temp _lb_maps[0]
$function mgs:v5.3.0/stats/board/admin_next {board:"$(board)",label:"$(label)"}

