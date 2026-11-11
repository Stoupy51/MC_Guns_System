
#> mgs:v5.4.2/maps/compact/trap
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
execute if data storage mgs:temp _save_zb{price:1000} run data remove storage mgs:temp _save_zb.price
execute if data storage mgs:temp _save_zb{type:0} run data remove storage mgs:temp _save_zb.type
execute if data storage mgs:temp _save_zb{duration:200} run data remove storage mgs:temp _save_zb.duration
execute if data storage mgs:temp _save_zb{cooldown:1200} run data remove storage mgs:temp _save_zb.cooldown
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.effect_radius
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set value [3.0f,2.0f,3.0f]
execute if score #differs mgs.data matches 0 run data remove storage mgs:temp _save_zb.effect_radius
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.offset_pos
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set value [0,0,0]
execute if score #differs mgs.data matches 0 run data remove storage mgs:temp _save_zb.offset_pos
execute if data storage mgs:temp _save_zb{power:1b} run data remove storage mgs:temp _save_zb.power
data modify storage mgs:temp map_edit.map.traps append from storage mgs:temp _save_zb

