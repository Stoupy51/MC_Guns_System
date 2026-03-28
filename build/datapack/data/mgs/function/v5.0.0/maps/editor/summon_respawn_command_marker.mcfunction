
#> mgs:v5.0.0/maps/editor/summon_respawn_command_marker
#
# @within	mgs:v5.0.0/maps/editor/summon_respawn_command_iter with storage mgs:temp _rcpos
#			mgs:v5.0.0/maps/editor/handle_respawn_command with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","mgs.element.respawn_command","mgs.new_respawn_cmd_marker"]}

