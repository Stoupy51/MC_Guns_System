
#> mgs:v5.0.0/maps/editor/summon_start_command_marker
#
# @within	mgs:v5.0.0/maps/editor/summon_start_command_iter with storage mgs:temp _cpos
#			mgs:v5.0.0/maps/editor/handle_start_command with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","mgs.element.start_command","mgs.new_start_cmd_marker"]}

