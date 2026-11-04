
#> mgs:v5.3.0/maps/editor/release_kept
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/release_kept
#			mgs:v5.3.0/maps/editor/cleanup
#

execute unless data storage mgs:temp map_edit.kept[0] run return 0
function mgs:v5.3.0/maps/editor/keep_loaded_remove with storage mgs:temp map_edit.kept[0]
data remove storage mgs:temp map_edit.kept[0]
function mgs:v5.3.0/maps/editor/release_kept

