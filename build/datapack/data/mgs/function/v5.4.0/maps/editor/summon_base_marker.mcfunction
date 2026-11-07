
#> mgs:v5.4.0/maps/editor/summon_base_marker
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/summon_existing with storage mgs:temp _pos
#			mgs:v5.4.0/maps/editor/handle_base with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute if score #ed_retry mgs.data matches 1 unless data storage mgs:temp map_edit.missed_before[{x:$(x),y:$(y),z:$(z)}] run return 0
$execute unless loaded $(x) $(y) $(z) run return run function mgs:v5.4.0/maps/editor/note_unloaded {x:$(x),y:$(y),z:$(z)}
$execute if score #ed_retry mgs.data matches 1 run function mgs:v5.4.0/maps/editor/keep_loaded {x:$(x),z:$(z)}
$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","mgs.element.base_coordinates"]}

