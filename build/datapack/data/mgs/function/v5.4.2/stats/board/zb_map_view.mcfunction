
#> mgs:v5.4.2/stats/board/zb_map_view
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/board/zb_map_trigger with storage mgs:temp _lb_view
#
# @args		i (unknown)
#			f (unknown)
#

$data modify storage mgs:temp _lb_view.map set from storage mgs:maps zombies[$(i)]
$data modify storage mgs:temp _lb_view.bucket set value "$(f)"
execute if data storage mgs:temp _lb_view{f:0} run data modify storage mgs:temp _lb_view.bucket set value "all"
data modify storage mgs:temp _lb_view.id set from storage mgs:temp _lb_view.map.id
data modify storage mgs:temp _lb_view.name set from storage mgs:temp _lb_view.map.name
data remove storage mgs:temp _lb_view.map
function mgs:v5.4.2/stats/board/zb_map_path with storage mgs:temp _lb_view

