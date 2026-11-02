
#> mgs:v5.3.0/maps/editor/summon_respawn_command_marker
#
# @executed	as @a[tag=mgs.map_editor,limit=1]
#
# @within	mgs:v5.3.0/maps/editor/summon_respawn_command_iter with storage mgs:temp _rcpos
#			mgs:v5.3.0/maps/editor/handle_respawn_command with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute unless loaded $(x) $(y) $(z) run return run scoreboard players add #ed_unloaded mgs.data 1
$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","mgs.element.respawn_command","mgs.new_respawn_cmd_marker"]}

