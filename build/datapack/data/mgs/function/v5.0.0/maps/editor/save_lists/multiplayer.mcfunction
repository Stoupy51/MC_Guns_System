
#> mgs:v5.0.0/maps/editor/save_lists/multiplayer
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/do_save
#

# Reset lists
data modify storage mgs:temp map_edit.map.spawning_points.red set value []
data modify storage mgs:temp map_edit.map.spawning_points.blue set value []
data modify storage mgs:temp map_edit.map.spawning_points.general set value []
data modify storage mgs:temp map_edit.map.out_of_bounds set value []
data modify storage mgs:temp map_edit.map.boundaries set value []
data modify storage mgs:temp map_edit.map.search_and_destroy set value []
data modify storage mgs:temp map_edit.map.domination set value []
data modify storage mgs:temp map_edit.map.hardpoint set value []

# Rebuild from markers
execute as @e[tag=mgs.map_element,tag=mgs.element.red_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"red"}
execute as @e[tag=mgs.map_element,tag=mgs.element.blue_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"blue"}
execute as @e[tag=mgs.map_element,tag=mgs.element.general_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"general"}
execute as @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"out_of_bounds"}
execute as @e[tag=mgs.map_element,tag=mgs.element.boundary] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"boundaries"}
execute as @e[tag=mgs.map_element,tag=mgs.element.search_and_destroy] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"search_and_destroy"}
execute as @e[tag=mgs.map_element,tag=mgs.element.domination] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"domination"}
execute as @e[tag=mgs.map_element,tag=mgs.element.hardpoint] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"hardpoint"}

