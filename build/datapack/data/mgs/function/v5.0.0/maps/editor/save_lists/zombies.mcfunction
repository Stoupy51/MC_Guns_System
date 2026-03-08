
#> mgs:v5.0.0/maps/editor/save_lists/zombies
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/do_save
#

# Reset lists
data modify storage mgs:temp map_edit.map.spawning_points.players set value []
data modify storage mgs:temp map_edit.map.spawning_points.zombies set value []
data modify storage mgs:temp map_edit.map.wallbuys set value []
data modify storage mgs:temp map_edit.map.doors set value []
data modify storage mgs:temp map_edit.map.traps set value []
data modify storage mgs:temp map_edit.map.perks set value []
data modify storage mgs:temp map_edit.map.mystery_box.positions set value []
data modify storage mgs:temp map_edit.map.out_of_bounds set value []
data modify storage mgs:temp map_edit.map.boundaries set value []

# Rebuild from markers
execute as @e[tag=mgs.map_element,tag=mgs.element.player_spawn_zb] at @s run function mgs:v5.0.0/maps/editor/save_zb_object {path:"spawning_points.players"}
execute as @e[tag=mgs.map_element,tag=mgs.element.zombie_spawn] at @s run function mgs:v5.0.0/maps/editor/save_zb_object {path:"spawning_points.zombies"}
execute as @e[tag=mgs.map_element,tag=mgs.element.wallbuy] at @s run function mgs:v5.0.0/maps/editor/save_zb_object {path:"wallbuys"}
execute as @e[tag=mgs.map_element,tag=mgs.element.door] at @s run function mgs:v5.0.0/maps/editor/save_zb_object {path:"doors"}
execute as @e[tag=mgs.map_element,tag=mgs.element.trap] at @s run function mgs:v5.0.0/maps/editor/save_zb_object {path:"traps"}
execute as @e[tag=mgs.map_element,tag=mgs.element.perk_machine] at @s run function mgs:v5.0.0/maps/editor/save_zb_object {path:"perks"}
execute as @e[tag=mgs.map_element,tag=mgs.element.mystery_box_pos] at @s run function mgs:v5.0.0/maps/editor/save_zb_object {path:"mystery_box.positions"}
execute as @e[tag=mgs.map_element,tag=mgs.element.out_of_bounds] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"out_of_bounds"}
execute as @e[tag=mgs.map_element,tag=mgs.element.boundary] at @s run function mgs:v5.0.0/maps/editor/save_point {path:"boundaries"}

