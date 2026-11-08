
#> mgs:v5.4.1/maps/editor/force_load
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/enter with storage mgs:temp map_edit.force
#
# @args		dimension (unknown)
#			x1 (unknown)
#			z1 (unknown)
#			x2 (unknown)
#			z2 (unknown)
#

$execute in $(dimension) run forceload add $(x1) $(z1) $(x2) $(z2)

