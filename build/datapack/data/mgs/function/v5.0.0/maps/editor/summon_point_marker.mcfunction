
#> mgs:v5.0.0/maps/editor/summon_point_marker
#
# @within	mgs:v5.0.0/maps/editor/summon_point_iter with storage mgs:temp _ppos
#			mgs:v5.0.0/maps/editor/handle_point with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","$(tag)"]}

