
#> mgs:v5.3.0/maps/compact/door_new
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/save_zb_object
#			mgs:v5.3.0/maps/compact/door_link
#

data modify storage mgs:temp _door_new set from storage mgs:temp _save_zb
data modify storage mgs:temp _door_new.blocks set value []
data modify storage mgs:temp map_edit.map.doors append from storage mgs:temp _door_new

