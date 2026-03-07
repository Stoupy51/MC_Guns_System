
#> mgs:v5.0.0/maps/editor/summon_enemy_marker
#
# @within	mgs:v5.0.0/maps/editor/summon_enemy_edit_iter with storage mgs:temp _epos
#			mgs:v5.0.0/maps/editor/handle_enemy with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","mgs.element.enemy","mgs.new_enemy_marker"]}

