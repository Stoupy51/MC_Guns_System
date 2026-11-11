
#> mgs:v5.4.2/maps/editor/note_unloaded
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/summon_base_marker {x:$(x),y:$(y),z:$(z)}
#			mgs:v5.4.2/maps/editor/summon_spawn_marker {x:$(x),y:$(y),z:$(z)}
#			mgs:v5.4.2/maps/editor/summon_point_marker {x:$(x),y:$(y),z:$(z)}
#			mgs:v5.4.2/maps/editor/summon_enemy_marker {x:$(x),y:$(y),z:$(z)}
#			mgs:v5.4.2/maps/editor/summon_start_command_marker {x:$(x),y:$(y),z:$(z)}
#			mgs:v5.4.2/maps/editor/summon_respawn_command_marker {x:$(x),y:$(y),z:$(z)}
#			mgs:v5.4.2/maps/editor/summon_zb_marker {x:$(x),y:$(y),z:$(z)}
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

scoreboard players add #ed_unloaded mgs.data 1
$data modify storage mgs:temp map_edit.missed append value {x:$(x),y:$(y),z:$(z)}

