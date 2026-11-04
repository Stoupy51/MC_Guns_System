
#> mgs:v5.3.0/maps/editor/summon_in
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/summon_all with storage mgs:temp map_edit.force [ as @a[tag=mgs.map_editor,limit=1] ]
#			mgs:v5.3.0/maps/editor/summon_retry with storage mgs:temp map_edit.force
#
# @args		dimension (unknown)
#

$execute in $(dimension) run function mgs:v5.3.0/maps/editor/summon_existing
function mgs:v5.3.0/maps/editor/refresh_displays

