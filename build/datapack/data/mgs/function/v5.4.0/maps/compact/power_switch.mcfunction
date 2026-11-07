
#> mgs:v5.4.0/maps/compact/power_switch
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
data modify storage mgs:temp map_edit.map.power_switch append from storage mgs:temp _save_zb

