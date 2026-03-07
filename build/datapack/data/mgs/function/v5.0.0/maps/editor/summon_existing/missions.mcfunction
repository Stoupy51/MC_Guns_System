
#> mgs:v5.0.0/maps/editor/summon_existing/missions
#
# @within	mgs:v5.0.0/maps/editor/summon_existing
#

data modify storage mgs:temp _spawn_iter set from storage mgs:temp map_edit.map.spawning_points.mission
data modify storage mgs:temp _spawn_iter_tag set value "mgs.element.mission_spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

data modify storage mgs:temp _enemy_edit_iter set from storage mgs:temp map_edit.map.enemies
execute if data storage mgs:temp _enemy_edit_iter[0] run function mgs:v5.0.0/maps/editor/summon_enemy_edit_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.out_of_bounds
data modify storage mgs:temp _point_iter_tag set value "mgs.element.out_of_bounds"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.boundaries
data modify storage mgs:temp _point_iter_tag set value "mgs.element.boundary"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

