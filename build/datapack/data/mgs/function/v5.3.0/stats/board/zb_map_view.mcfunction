
#> mgs:v5.3.0/stats/board/zb_map_view
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/zb_map_trigger with storage mgs:temp _lb_view
#
# @args		i (unknown)
#			f (unknown)
#

$data modify storage mgs:temp _lb_view.map set from storage mgs:maps zombies[$(i)]
$data modify storage mgs:temp _lb_view.bucket set value "$(f)"
execute if data storage mgs:temp _lb_view{f:0} run data modify storage mgs:temp _lb_view.bucket set value "all"
data modify storage mgs:temp _lb_view.id set from storage mgs:temp _lb_view.map.id
data modify storage mgs:temp _lb_view.name set from storage mgs:temp _lb_view.map.name
function mgs:v5.3.0/stats/board/zb_map_path with storage mgs:temp _lb_view

