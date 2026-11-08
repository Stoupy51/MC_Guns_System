
#> mgs:v5.4.1/maps/editor/keep_loaded_add
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/keep_loaded with storage mgs:temp map_edit.kept[-1]
#
# @args		dimension (unknown)
#			x (unknown)
#			z (unknown)
#

$execute in $(dimension) run forceload add $(x) $(z)

