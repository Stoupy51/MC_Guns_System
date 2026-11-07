
#> mgs:v5.4.0/maps/editor/keep_loaded
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/summon_base_marker {x:$(x),z:$(z)}
#			mgs:v5.4.0/maps/editor/summon_spawn_marker {x:$(x),z:$(z)}
#			mgs:v5.4.0/maps/editor/summon_point_marker {x:$(x),z:$(z)}
#			mgs:v5.4.0/maps/editor/summon_enemy_marker {x:$(x),z:$(z)}
#			mgs:v5.4.0/maps/editor/summon_start_command_marker {x:$(x),z:$(z)}
#			mgs:v5.4.0/maps/editor/summon_respawn_command_marker {x:$(x),z:$(z)}
#			mgs:v5.4.0/maps/editor/summon_zb_marker {x:$(x),z:$(z)}
#
# @args		x (unknown)
#			z (unknown)
#

$data modify storage mgs:temp map_edit.kept append value {x:$(x),z:$(z)}
data modify storage mgs:temp map_edit.kept[-1].dimension set from storage mgs:temp map_edit.force.dimension
function mgs:v5.4.0/maps/editor/keep_loaded_add with storage mgs:temp map_edit.kept[-1]

