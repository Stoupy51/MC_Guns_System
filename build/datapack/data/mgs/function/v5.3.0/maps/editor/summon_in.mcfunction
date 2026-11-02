
#> mgs:v5.3.0/maps/editor/summon_in
#
# @executed	as @a[tag=mgs.map_editor,limit=1]
#
# @within	mgs:v5.3.0/maps/editor/summon_all with storage mgs:temp map_edit.force [ as @a[tag=mgs.map_editor,limit=1] ]
#
# @args		dimension (unknown)
#

$execute in $(dimension) run function mgs:v5.3.0/maps/editor/summon_existing
function mgs:v5.3.0/maps/editor/refresh_displays

