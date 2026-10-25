
#> mgs:v5.3.0/maps/editor/tp_to_map
#
# @within	mgs:v5.3.0/maps/editor/enter with storage mgs:temp _tp
#			mgs:v5.3.0/maps/editor/invite_all with storage mgs:temp _tp [ as @a[scores={mgs.mp.map_edit=1}] ]
#
# @args		dimension (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute in $(dimension) run tp @s $(x) $(y) $(z)

