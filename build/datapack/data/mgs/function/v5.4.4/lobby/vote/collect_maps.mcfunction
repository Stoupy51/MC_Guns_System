
#> mgs:v5.4.4/lobby/vote/collect_maps
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/map_round with storage mgs:lobby multiplayer.preset
#			mgs:v5.4.4/lobby/zombies/open_vote {mode:"zombies",field:"spawning_points.players"}
#			mgs:v5.4.4/lobby/missions/open_vote {mode:"missions",field:"spawning_points.mission"}
#
# @args		mode (string)
#			field (string)
#

$data modify storage mgs:temp _lv_iter set from storage mgs:maps $(mode)
data modify storage mgs:temp _lv_opts set value []
$execute if data storage mgs:temp _lv_iter[0] run function mgs:v5.4.4/lobby/vote/collect_map {field:"$(field)"}
function mgs:v5.4.4/lobby/vote/trim_maps
$data modify storage mgs:lobby $(mode).options set from storage mgs:temp _lv_opts

