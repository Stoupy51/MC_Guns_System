
#> mgs:v5.0.0/maps/editor/save_lists/missions
#
# @executed	as @p[tag=mgs.map_editor,distance=..6,sort=nearest]
#
# @within	mgs:v5.0.0/maps/editor/do_save
#

# Reset lists
data modify storage mgs:temp map_edit.map.spawning_points.mission set value []
data modify storage mgs:temp map_edit.map.enemies set value []
data modify storage mgs:temp map_edit.map.out_of_bounds set value []
data modify storage mgs:temp map_edit.map.boundaries set value []
data modify storage mgs:temp map_edit.map.start_commands set value []
data modify storage mgs:temp map_edit.map.respawn_commands set value []

# Rebuild from markers
execute as @e[tag=mgs.element.mission_spawn] at @s run function mgs:v5.0.0/maps/editor/save_spawn {path:"mission"}
execute as @e[tag=mgs.element.enemy] at @s run function mgs:v5.0.0/maps/editor/save_enemy
execute as @e[tag=mgs.element.out_of_bounds] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"out_of_bounds"}
execute as @e[tag=mgs.element.boundary] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"boundaries"}
execute as @e[tag=mgs.element.start_command] at @s run function mgs:v5.0.0/maps/editor/save_start_command {path:"start_commands"}
execute as @e[tag=mgs.element.respawn_command] at @s run function mgs:v5.0.0/maps/editor/save_respawn_command {path:"respawn_commands"}

