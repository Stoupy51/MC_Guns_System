
#> mgs:v5.0.0/maps/editor/summon_zb_marker
#
# @within	mgs:v5.0.0/maps/editor/summon_zb_object_iter with storage mgs:temp _zbpos
#			mgs:v5.0.0/maps/editor/handle_zb_object with storage mgs:temp _zbpos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","$(tag)","mgs.new_zb_marker"]}

