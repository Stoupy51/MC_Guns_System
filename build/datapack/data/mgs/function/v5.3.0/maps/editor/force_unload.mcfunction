
#> mgs:v5.3.0/maps/editor/force_unload
#
# @executed	as @p[tag=mgs.map_editor,distance=..6,sort=nearest]
#
# @within	mgs:v5.3.0/maps/editor/cleanup with storage mgs:temp map_edit.force
#
# @args		dimension (unknown)
#			x1 (unknown)
#			z1 (unknown)
#			x2 (unknown)
#			z2 (unknown)
#

$execute in $(dimension) run forceload remove $(x1) $(z1) $(x2) $(z2)

