
#> mgs:v5.3.0/maps/compact/zombie_spawn
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/save_zb_object
#

execute if data storage mgs:temp _save_zb{group_id:0} run data remove storage mgs:temp _save_zb.group_id
execute if data storage mgs:temp _save_zb{activation_box:[]} run data remove storage mgs:temp _save_zb.activation_box
execute if data storage mgs:temp _save_zb{walk_to:[]} run data remove storage mgs:temp _save_zb.walk_to
execute if data storage mgs:temp _save_zb{rise_ticks:20} run data remove storage mgs:temp _save_zb.rise_ticks
execute if data storage mgs:temp _save_zb{min_round:0} run data remove storage mgs:temp _save_zb.min_round
execute if data storage mgs:temp _save_zb{max_round:0} run data remove storage mgs:temp _save_zb.max_round
execute if data storage mgs:temp _save_zb{arrival:"floor"} run data remove storage mgs:temp _save_zb.arrival
execute if data storage mgs:temp _save_zb{power:0b} run data remove storage mgs:temp _save_zb.power
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.mob
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set value {entity:"zombie"}
execute if score #differs mgs.data matches 0 run data remove storage mgs:temp _save_zb.mob
data modify storage mgs:temp map_edit.map.spawning_points.zombies append from storage mgs:temp _save_zb

