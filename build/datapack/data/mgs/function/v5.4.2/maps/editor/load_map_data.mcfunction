
#> mgs:v5.4.2/maps/editor/load_map_data
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/enter with storage mgs:temp map_edit
#			mgs:v5.4.2/maps/editor/do_save with storage mgs:temp map_edit
#
# @args		mode (unknown)
#			idx (unknown)
#

$data modify storage mgs:temp map_edit.map set from storage mgs:maps $(mode)[$(idx)]

