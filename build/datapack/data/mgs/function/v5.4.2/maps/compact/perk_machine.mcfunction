
#> mgs:v5.4.2/maps/compact/perk_machine
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
execute if data storage mgs:temp _save_zb{name:""} run data remove storage mgs:temp _save_zb.name
execute if data storage mgs:temp _save_zb{price:-1} run data remove storage mgs:temp _save_zb.price
execute if data storage mgs:temp _save_zb{partial_price:0} run data remove storage mgs:temp _save_zb.partial_price
execute if data storage mgs:temp _save_zb{perk_id:"juggernog"} run data remove storage mgs:temp _save_zb.perk_id
execute if data storage mgs:temp _save_zb{power:1b} run data remove storage mgs:temp _save_zb.power
execute if data storage mgs:temp _save_zb{display_item:""} run data remove storage mgs:temp _save_zb.display_item
execute if data storage mgs:temp _save_zb{item_model:""} run data remove storage mgs:temp _save_zb.item_model
data modify storage mgs:temp map_edit.map.perks append from storage mgs:temp _save_zb

