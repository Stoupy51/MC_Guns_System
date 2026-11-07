
#> mgs:v5.4.0/maps/editor/keep_loaded_remove
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/release_kept with storage mgs:temp map_edit.kept[0]
#
# @args		dimension (unknown)
#			x (unknown)
#			z (unknown)
#

$execute in $(dimension) run forceload remove $(x) $(z)

