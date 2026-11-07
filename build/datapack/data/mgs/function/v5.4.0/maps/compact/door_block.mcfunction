
#> mgs:v5.4.0/maps/compact/door_block
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/save_zb_object
#			mgs:v5.4.0/maps/compact/door
#

data modify storage mgs:temp _door_block set value {}
data modify storage mgs:temp _door_block.pos set from storage mgs:temp _save_zb.pos
data remove storage mgs:temp _save_zb.pos
function mgs:v5.4.0/maps/compact/door_link with storage mgs:temp _save_zb

