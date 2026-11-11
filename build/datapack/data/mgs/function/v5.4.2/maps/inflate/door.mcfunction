
#> mgs:v5.4.2/maps/inflate/door
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/inflate
#			mgs:v5.4.2/maps/inflate/door
#

data modify storage mgs:temp _inf_link set from storage mgs:temp _inf_src[0]
data modify storage mgs:temp _inf_blocks set value []
data modify storage mgs:temp _inf_blocks set from storage mgs:temp _inf_link.blocks

# A door saved without blocks is a link of its own block.
execute unless data storage mgs:temp _inf_link.blocks run data modify storage mgs:temp _inf_blocks append value {}
data remove storage mgs:temp _inf_link.blocks
execute if data storage mgs:temp _inf_blocks[0] run function mgs:v5.4.2/maps/inflate/door_block

data remove storage mgs:temp _inf_src[0]
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.2/maps/inflate/door

