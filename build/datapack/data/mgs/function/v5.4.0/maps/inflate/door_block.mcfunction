
#> mgs:v5.4.0/maps/inflate/door_block
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/inflate/door
#			mgs:v5.4.0/maps/inflate/door_block
#

data modify storage mgs:temp _inf set from storage mgs:temp _inf_link
data modify storage mgs:temp _inf merge from storage mgs:temp _inf_blocks[0]
function mgs:v5.4.0/maps/inflate/door_fields
data modify storage mgs:temp _inf_map.doors append from storage mgs:temp _inf
data remove storage mgs:temp _inf_blocks[0]
execute if data storage mgs:temp _inf_blocks[0] run function mgs:v5.4.0/maps/inflate/door_block

