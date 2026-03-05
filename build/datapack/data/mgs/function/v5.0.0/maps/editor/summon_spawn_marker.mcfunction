
#> mgs:v5.0.0/maps/editor/summon_spawn_marker
#
# @within	mgs:v5.0.0/maps/editor/summon_spawn_iter with storage mgs:temp _spos
#			mgs:v5.0.0/maps/editor/handle_spawn with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","$(tag)","mgs.new_spawn_marker"]}

