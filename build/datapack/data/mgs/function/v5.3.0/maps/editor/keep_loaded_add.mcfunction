
#> mgs:v5.3.0/maps/editor/keep_loaded_add
#
# @executed	as @a[tag=mgs.map_editor,limit=1]
#
# @within	mgs:v5.3.0/maps/editor/keep_loaded with storage mgs:temp map_edit.kept[-1]
#
# @args		dimension (unknown)
#			x (unknown)
#			z (unknown)
#

$execute in $(dimension) run forceload add $(x) $(z)

