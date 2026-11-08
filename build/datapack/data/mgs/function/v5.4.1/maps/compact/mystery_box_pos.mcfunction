
#> mgs:v5.4.1/maps/compact/mystery_box_pos
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
execute if data storage mgs:temp _save_zb{can_start_on:1b} run data remove storage mgs:temp _save_zb.can_start_on
execute if data storage mgs:temp _save_zb{display_item:""} run data remove storage mgs:temp _save_zb.display_item
execute if data storage mgs:temp _save_zb{item_model:""} run data remove storage mgs:temp _save_zb.item_model
execute if data storage mgs:temp _save_zb{location_name:""} run data remove storage mgs:temp _save_zb.location_name
execute if data storage mgs:temp _save_zb{pitch:0.0f} run data remove storage mgs:temp _save_zb.pitch
execute if data storage mgs:temp _save_zb{roll:0} run data remove storage mgs:temp _save_zb.roll
data modify storage mgs:temp map_edit.map.mystery_box.positions append from storage mgs:temp _save_zb

