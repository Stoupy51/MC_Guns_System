
#> mgs:v5.4.2/maps/compact/wunderfizz
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
execute if data storage mgs:temp _save_zb{name:"Der Wunderfizz"} run data remove storage mgs:temp _save_zb.name
execute if data storage mgs:temp _save_zb{price:1500} run data remove storage mgs:temp _save_zb.price
execute if data storage mgs:temp _save_zb{power:1b} run data remove storage mgs:temp _save_zb.power
execute if data storage mgs:temp _save_zb{all_perks:0b} run data remove storage mgs:temp _save_zb.all_perks
execute if data storage mgs:temp _save_zb{can_start_on:1b} run data remove storage mgs:temp _save_zb.can_start_on
execute if data storage mgs:temp _save_zb{display_item:""} run data remove storage mgs:temp _save_zb.display_item
execute if data storage mgs:temp _save_zb{item_model:""} run data remove storage mgs:temp _save_zb.item_model
data modify storage mgs:temp map_edit.map.wunderfizz append from storage mgs:temp _save_zb

