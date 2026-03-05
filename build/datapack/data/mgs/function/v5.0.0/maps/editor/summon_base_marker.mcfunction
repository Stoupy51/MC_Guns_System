
#> mgs:v5.0.0/maps/editor/summon_base_marker
#
# @within	mgs:v5.0.0/maps/editor/summon_existing with storage mgs:temp _pos
#			mgs:v5.0.0/maps/editor/handle_base with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","mgs.element.base_coordinates"]}

