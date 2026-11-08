
#> mgs:v5.4.1/stats/board/mi_map_view
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/stats/board/mi_map_trigger with storage mgs:temp _lb_view
#
# @args		i (unknown)
#

$data modify storage mgs:temp _lb_view.map set from storage mgs:maps missions[$(i)]
data modify storage mgs:temp _lb_view.id set from storage mgs:temp _lb_view.map.id
data modify storage mgs:temp _lb_view.name set from storage mgs:temp _lb_view.map.name
data remove storage mgs:temp _lb_view.map
function mgs:v5.4.1/stats/board/mi_map_path with storage mgs:temp _lb_view

