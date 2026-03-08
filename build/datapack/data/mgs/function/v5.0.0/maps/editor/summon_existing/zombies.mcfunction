
#> mgs:v5.0.0/maps/editor/summon_existing/zombies
#
# @within	mgs:v5.0.0/maps/editor/summon_existing
#

data modify storage mgs:temp _zb_iter set from storage mgs:temp map_edit.map.spawning_points.players
data modify storage mgs:temp _zb_iter_tag set value "mgs.element.player_spawn_zb"
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

data modify storage mgs:temp _zb_iter set from storage mgs:temp map_edit.map.spawning_points.zombies
data modify storage mgs:temp _zb_iter_tag set value "mgs.element.zombie_spawn"
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

data modify storage mgs:temp _zb_iter set from storage mgs:temp map_edit.map.wallbuys
data modify storage mgs:temp _zb_iter_tag set value "mgs.element.wallbuy"
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

data modify storage mgs:temp _zb_iter set from storage mgs:temp map_edit.map.doors
data modify storage mgs:temp _zb_iter_tag set value "mgs.element.door"
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

data modify storage mgs:temp _zb_iter set from storage mgs:temp map_edit.map.traps
data modify storage mgs:temp _zb_iter_tag set value "mgs.element.trap"
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

data modify storage mgs:temp _zb_iter set from storage mgs:temp map_edit.map.perks
data modify storage mgs:temp _zb_iter_tag set value "mgs.element.perk_machine"
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

data modify storage mgs:temp _zb_iter set from storage mgs:temp map_edit.map.mystery_box.positions
data modify storage mgs:temp _zb_iter_tag set value "mgs.element.mystery_box_pos"
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

data modify storage mgs:temp _zb_iter set from storage mgs:temp map_edit.map.power_switch
data modify storage mgs:temp _zb_iter_tag set value "mgs.element.power_switch"
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.0.0/maps/editor/summon_zb_object_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.out_of_bounds
data modify storage mgs:temp _point_iter_tag set value "mgs.element.out_of_bounds"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

data modify storage mgs:temp _point_iter set from storage mgs:temp map_edit.map.boundaries
data modify storage mgs:temp _point_iter_tag set value "mgs.element.boundary"
execute if data storage mgs:temp _point_iter[0] run function mgs:v5.0.0/maps/editor/summon_point_iter

