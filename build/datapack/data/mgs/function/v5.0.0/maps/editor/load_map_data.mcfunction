
#> mgs:v5.0.0/maps/editor/load_map_data
#
# @within	mgs:v5.0.0/maps/editor/enter with storage mgs:temp map_edit
#			mgs:v5.0.0/maps/editor/save_exit with storage mgs:temp map_edit
#
# @args		idx (unknown)
#

$data modify storage mgs:temp map_edit.map set from storage mgs:maps multiplayer[$(idx)]

