
#> mgs:v5.3.0/maps/editor/summon_zb_marker
#
# @executed	as @a[tag=mgs.map_editor,limit=1]
#
# @within	mgs:v5.3.0/maps/editor/summon_zb_object_iter with storage mgs:temp _zbpos
#			mgs:v5.3.0/maps/editor/handle_zb_object with storage mgs:temp _zbpos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#

$execute unless loaded $(x) $(y) $(z) run return run scoreboard players add #ed_unloaded mgs.data 1
$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","$(tag)","mgs.new_zb_marker"]}

