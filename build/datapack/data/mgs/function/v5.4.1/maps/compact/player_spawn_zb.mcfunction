
#> mgs:v5.4.1/maps/compact/player_spawn_zb
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/save_zb_object
#

execute if data storage mgs:temp _save_zb{group_id:0} run data remove storage mgs:temp _save_zb.group_id
data modify storage mgs:temp map_edit.map.spawning_points.players append from storage mgs:temp _save_zb

