
#> mgs:v5.0.0/maps/editor/summon_existing/multiplayer
#
# @within	mgs:v5.0.0/maps/editor/summon_existing
#

data modify storage mgs:temp _spawn_iter set from storage mgs:temp map_edit.map.spawning_points.red
data modify storage mgs:temp _spawn_iter_tag set value "mgs.element.red_spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

data modify storage mgs:temp _spawn_iter set from storage mgs:temp map_edit.map.spawning_points.blue
data modify storage mgs:temp _spawn_iter_tag set value "mgs.element.blue_spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

data modify storage mgs:temp _spawn_iter set from storage mgs:temp map_edit.map.spawning_points.general
data modify storage mgs:temp _spawn_iter_tag set value "mgs.element.general_spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.out_of_bounds
data modify storage mgs:temp _point_iter_tag set value "mgs.element.out_of_bounds"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.boundaries
data modify storage mgs:temp _point_iter_tag set value "mgs.element.boundary"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.search_and_destroy
data modify storage mgs:temp _point_iter_tag set value "mgs.element.search_and_destroy"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.domination
data modify storage mgs:temp _point_iter_tag set value "mgs.element.domination"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.hardpoint
data modify storage mgs:temp _point_iter_tag set value "mgs.element.hardpoint"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

