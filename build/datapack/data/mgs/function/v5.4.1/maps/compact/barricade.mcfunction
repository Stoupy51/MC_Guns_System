
#> mgs:v5.4.1/maps/compact/barricade
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
execute unless data storage mgs:temp map_edit.map.shared.barricade.block_enabled run data modify storage mgs:temp map_edit.map.shared.barricade.block_enabled set from storage mgs:temp _save_zb.block_enabled
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.block_enabled
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp map_edit.map.shared.barricade.block_enabled
execute if score #differs mgs.data matches 0 run data remove storage mgs:temp _save_zb.block_enabled
execute unless data storage mgs:temp map_edit.map.shared.barricade.block_disabled run data modify storage mgs:temp map_edit.map.shared.barricade.block_disabled set from storage mgs:temp _save_zb.block_disabled
data remove storage mgs:temp _cmp
data modify storage mgs:temp _cmp set from storage mgs:temp _save_zb.block_disabled
execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set from storage mgs:temp map_edit.map.shared.barricade.block_disabled
execute if score #differs mgs.data matches 0 run data remove storage mgs:temp _save_zb.block_disabled
execute if data storage mgs:temp _save_zb{radius:2} run data remove storage mgs:temp _save_zb.radius
data modify storage mgs:temp map_edit.map.barricades append from storage mgs:temp _save_zb

