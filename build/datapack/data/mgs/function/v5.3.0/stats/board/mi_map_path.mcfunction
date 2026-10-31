
#> mgs:v5.3.0/stats/board/mi_map_path
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/mi_map_view with storage mgs:temp _lb_view
#
# @args		id (unknown)
#			name (unknown)
#

$data modify storage mgs:temp _lb_view.path set value 'mi_map."$(id)"'
$data modify storage mgs:temp _lb_view.title set value "$(name)"
function mgs:v5.3.0/stats/board/show with storage mgs:temp _lb_view

