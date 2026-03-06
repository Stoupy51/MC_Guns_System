
#> mgs:v5.0.0/maps/editor/summon_existing/missions
#
# @within	mgs:v5.0.0/maps/editor/summon_existing
#

# Initialize enemy config with defaults if missing
execute unless data storage mgs:temp map_edit.map.enemy_config run data modify storage mgs:temp map_edit.map.enemy_config set value {level_1:{entity:"pillager",hp:20},level_2:{entity:"pillager",hp:40},level_3:{entity:"pillager",hp:60},level_4:{entity:"pillager",hp:80}}

data modify storage mgs:temp _spawn_iter set from storage mgs:temp map_edit.map.spawning_points.mission
data modify storage mgs:temp _spawn_iter_tag set value "mgs.element.mission_spawn"
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.0.0/maps/editor/summon_spawn_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.enemies.level_1
data modify storage mgs:temp _point_iter_tag set value "mgs.element.level_1_enemy"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.enemies.level_2
data modify storage mgs:temp _point_iter_tag set value "mgs.element.level_2_enemy"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.enemies.level_3
data modify storage mgs:temp _point_iter_tag set value "mgs.element.level_3_enemy"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.enemies.level_4
data modify storage mgs:temp _point_iter_tag set value "mgs.element.level_4_enemy"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.out_of_bounds
data modify storage mgs:temp _point_iter_tag set value "mgs.element.out_of_bounds"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.boundaries
data modify storage mgs:temp _point_iter_tag set value "mgs.element.boundary"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

