
#> mgs:v5.3.0/stats/board/zb_map_path
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/zb_map_view with storage mgs:temp _lb_view
#
# @args		id (unknown)
#			bucket (unknown)
#			name (unknown)
#

$data modify storage mgs:temp _lb_view.path set value 'zb_map."$(id)"."$(bucket)"'
$data modify storage mgs:temp _lb_view.title set value "$(name)"
function mgs:v5.3.0/stats/board/show with storage mgs:temp _lb_view

