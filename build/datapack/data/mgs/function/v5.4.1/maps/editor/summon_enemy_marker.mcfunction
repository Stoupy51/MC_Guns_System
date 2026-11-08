
#> mgs:v5.4.1/maps/editor/summon_enemy_marker
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/summon_enemy_edit_iter with storage mgs:temp _epos
#			mgs:v5.4.1/maps/editor/handle_enemy with storage mgs:temp _pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute if score #ed_retry mgs.data matches 1 unless data storage mgs:temp map_edit.missed_before[{x:$(x),y:$(y),z:$(z)}] run return 0
$execute unless loaded $(x) $(y) $(z) run return run function mgs:v5.4.1/maps/editor/note_unloaded {x:$(x),y:$(y),z:$(z)}
$execute if score #ed_retry mgs.data matches 1 run function mgs:v5.4.1/maps/editor/keep_loaded {x:$(x),z:$(z)}
$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.map_element","mgs.element.enemy","mgs.new_enemy_marker"]}

