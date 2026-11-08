
#> mgs:v5.4.1/maps/inflate/mystery_box_pos
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/inflate
#			mgs:v5.4.1/maps/inflate/mystery_box_pos
#

data modify storage mgs:temp _inf set from storage mgs:temp _inf_src[0]
function mgs:v5.4.1/maps/inflate/mystery_box_pos_fields
data modify storage mgs:temp _inf_map.mystery_box.positions append from storage mgs:temp _inf
data remove storage mgs:temp _inf_src[0]
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/mystery_box_pos

