
#> mgs:v5.3.0/maps/compact/door_block
#
# @executed	as @e[tag=mgs.element.player_spawn_zb] & at @s
#
# @within	mgs:v5.3.0/maps/editor/save_zb_object
#			mgs:v5.3.0/maps/compact/door
#

data modify storage mgs:temp _door_block set value {}
data modify storage mgs:temp _door_block.pos set from storage mgs:temp _save_zb.pos
data remove storage mgs:temp _save_zb.pos
function mgs:v5.3.0/maps/compact/door_link with storage mgs:temp _save_zb

