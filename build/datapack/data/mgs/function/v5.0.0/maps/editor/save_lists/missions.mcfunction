
#> mgs:v5.0.0/maps/editor/save_lists/missions
#
# @within	mgs:v5.0.0/maps/editor/save_exit
#

# Reset lists
data modify storage mgs:temp map_edit.map.spawning_points.mission set value []
data modify storage mgs:temp map_edit.map.enemies.level_1 set value []
data modify storage mgs:temp map_edit.map.enemies.level_2 set value []
data modify storage mgs:temp map_edit.map.enemies.level_3 set value []
data modify storage mgs:temp map_edit.map.enemies.level_4 set value []
data modify storage mgs:temp map_edit.map.out_of_bounds set value []
data modify storage mgs:temp map_edit.map.boundaries set value []

# Rebuild from markers
execute as @e[tag=mgs.map_element,tag=mgs.element.mission_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"mission"}
execute as @e[tag=mgs.map_element,tag=mgs.element.level_1_enemy] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"enemies.level_1"}
execute as @e[tag=mgs.map_element,tag=mgs.element.level_2_enemy] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"enemies.level_2"}
execute as @e[tag=mgs.map_element,tag=mgs.element.level_3_enemy] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"enemies.level_3"}
execute as @e[tag=mgs.map_element,tag=mgs.element.level_4_enemy] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"enemies.level_4"}
execute as @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"out_of_bounds"}
execute as @e[tag=mgs.map_element,tag=mgs.element.boundary] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"boundaries"}

