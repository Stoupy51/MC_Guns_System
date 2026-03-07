
#> mgs:v5.0.0/maps/editor/save_lists/missions
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/do_save
#

# Reset lists
data modify storage mgs:temp map_edit.map.spawning_points.mission set value []
data modify storage mgs:temp map_edit.map.enemies set value []
data modify storage mgs:temp map_edit.map.out_of_bounds set value []
data modify storage mgs:temp map_edit.map.boundaries set value []

# Rebuild from markers
execute as @e[tag=mgs.map_element,tag=mgs.element.mission_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"mission"}
execute as @e[tag=mgs.map_element,tag=mgs.element.enemy] at @s run function mgs:v5.0.0/maps/editor/save_enemy
execute as @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"out_of_bounds"}
execute as @e[tag=mgs.map_element,tag=mgs.element.boundary] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"boundaries"}

