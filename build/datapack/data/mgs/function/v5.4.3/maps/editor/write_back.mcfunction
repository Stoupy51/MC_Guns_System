
#> mgs:v5.4.3/maps/editor/write_back
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/maps/editor/do_save with storage mgs:temp map_edit
#
# @args		mode (unknown)
#			idx (unknown)
#

$data modify storage mgs:maps $(mode)[$(idx)] set from storage mgs:temp map_edit.map

