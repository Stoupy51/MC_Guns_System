
#> mgs:v5.3.0/maps/editor/summon_zb_marker
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/summon_zb_object_iter with storage mgs:temp _zbpos
#			mgs:v5.3.0/maps/editor/handle_zb_object with storage mgs:temp _zbpos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#

$execute if score #ed_retry mgs.data matches 1 unless data storage mgs:temp map_edit.missed_before[{x:$(x),y:$(y),z:$(z)}] run return 0
$execute unless loaded $(x) $(y) $(z) run return run function mgs:v5.3.0/maps/editor/note_unloaded {x:$(x),y:$(y),z:$(z)}
$execute if score #ed_retry mgs.data matches 1 run function mgs:v5.3.0/maps/editor/keep_loaded {x:$(x),z:$(z)}
$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","$(tag)","mgs.new_zb_marker"]}

