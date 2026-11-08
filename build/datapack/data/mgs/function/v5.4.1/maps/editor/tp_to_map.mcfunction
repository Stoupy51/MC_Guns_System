
#> mgs:v5.4.1/maps/editor/tp_to_map
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/enter with storage mgs:temp _tp
#			mgs:v5.4.1/players/editor_invite with storage mgs:temp _tp
#
# @args		dimension (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute in $(dimension) run tp @s $(x) $(y) $(z)

