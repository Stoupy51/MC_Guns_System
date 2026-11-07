
#> mgs:v5.4.0/stats/board/mi_map_path
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/stats/board/mi_map_view with storage mgs:temp _lb_view
#
# @args		id (unknown)
#			name (unknown)
#

$data modify storage mgs:temp _lb_view.path set value 'mi_map."$(id)"'
$data modify storage mgs:temp _lb_view.title set value "$(name)"
function mgs:v5.4.0/stats/board/show with storage mgs:temp _lb_view

