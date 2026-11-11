
#> mgs:v5.4.2/maps/editor/force_unload
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/cleanup with storage mgs:temp map_edit.force
#
# @args		dimension (unknown)
#			x1 (unknown)
#			z1 (unknown)
#			x2 (unknown)
#			z2 (unknown)
#

$execute in $(dimension) run forceload remove $(x1) $(z1) $(x2) $(z2)

