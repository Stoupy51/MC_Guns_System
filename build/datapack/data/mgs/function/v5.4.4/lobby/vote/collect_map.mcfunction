
#> mgs:v5.4.4/lobby/vote/collect_map
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/vote/collect_maps {field:"$(field)"}
#			mgs:v5.4.4/lobby/vote/collect_map {field:"$(field)"}
#
# @args		field (string)
#

$execute if data storage mgs:temp _lv_iter[0].$(field)[0] run function mgs:v5.4.4/lobby/vote/add_map
data remove storage mgs:temp _lv_iter[0]
$execute if data storage mgs:temp _lv_iter[0] run function mgs:v5.4.4/lobby/vote/collect_map {field:"$(field)"}

