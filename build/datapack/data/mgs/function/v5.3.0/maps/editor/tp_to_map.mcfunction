
#> mgs:v5.3.0/maps/editor/tp_to_map
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/enter with storage mgs:temp _tp
#			mgs:v5.3.0/players/editor_invite with storage mgs:temp _tp
#
# @args		dimension (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute in $(dimension) run tp @s $(x) $(y) $(z)

