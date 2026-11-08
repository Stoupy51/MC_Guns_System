
#> mgs:v5.4.1/maps/editor/save_lists/zombies
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/do_save
#

# Reset lists
data modify storage mgs:temp map_edit.map.spawning_points.players set value []
data modify storage mgs:temp map_edit.map.spawning_points.zombies set value []
data modify storage mgs:temp map_edit.map.wallbuys set value []
data modify storage mgs:temp map_edit.map.doors set value []
data modify storage mgs:temp map_edit.map.traps set value []
data modify storage mgs:temp map_edit.map.perks set value []
data modify storage mgs:temp map_edit.map.mystery_box.positions set value []
data modify storage mgs:temp map_edit.map.power_switch set value []
data modify storage mgs:temp map_edit.map.out_of_bounds set value []
data modify storage mgs:temp map_edit.map.boundaries set value []
data modify storage mgs:temp map_edit.map.pap_machines set value []
data modify storage mgs:temp map_edit.map.start_commands set value []
data modify storage mgs:temp map_edit.map.spawning_points.special set value []
data modify storage mgs:temp map_edit.map.barricades set value []
data modify storage mgs:temp map_edit.map.wunderfizz set value []
data remove storage mgs:temp map_edit.map.shared
data remove storage mgs:temp map_edit.map.barriers
data remove storage mgs:temp map_edit.map.leaderboards

# Rebuild from markers
execute as @e[tag=mgs.element.player_spawn_zb] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"player_spawn_zb"}
execute as @e[tag=mgs.element.zombie_spawn] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"zombie_spawn"}
execute as @e[tag=mgs.element.wallbuy] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"wallbuy"}
execute as @e[tag=mgs.element.door] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"door"}
execute as @e[tag=mgs.element.trap] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"trap"}
execute as @e[tag=mgs.element.perk_machine] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"perk_machine"}
execute as @e[tag=mgs.element.mystery_box_pos] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"mystery_box_pos"}
execute as @e[tag=mgs.element.power_switch] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"power_switch"}
execute as @e[tag=mgs.element.out_of_bounds] at @s run function mgs:v5.4.1/maps/editor/save_point {path:"out_of_bounds"}
execute as @e[tag=mgs.element.boundary] at @s run function mgs:v5.4.1/maps/editor/save_point {path:"boundaries"}
execute as @e[tag=mgs.element.pap_machine] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"pap_machine"}
execute as @e[tag=mgs.element.start_command] at @s run function mgs:v5.4.1/maps/editor/save_start_command {path:"start_commands"}
execute as @e[tag=mgs.element.special_spawn] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"special_spawn"}
execute as @e[tag=mgs.element.barricade] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"barricade"}
execute as @e[tag=mgs.element.wunderfizz] at @s run function mgs:v5.4.1/maps/editor/save_zb_object {etype:"wunderfizz"}

