
#> mgs:v5.3.0/maps/inflate/door_fields
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/inflate/door_block
#

function mgs:v5.3.0/maps/inflate/rotation
execute unless data storage mgs:temp _inf.name run data modify storage mgs:temp _inf.name set value "Door"
execute unless data storage mgs:temp _inf.back_name run data modify storage mgs:temp _inf.back_name set value "Door"
execute unless data storage mgs:temp _inf.price run data modify storage mgs:temp _inf.price set value 1000
execute unless data storage mgs:temp _inf.partial_price run data modify storage mgs:temp _inf.partial_price set value 0
execute unless data storage mgs:temp _inf.link_id run data modify storage mgs:temp _inf.link_id set value 1
execute unless data storage mgs:temp _inf.back_group_id run data modify storage mgs:temp _inf.back_group_id set value -1
execute unless data storage mgs:temp _inf.min_round run data modify storage mgs:temp _inf.min_round set value 0
execute unless data storage mgs:temp _inf.block run data modify storage mgs:temp _inf.block set value ""
execute unless data storage mgs:temp _inf.animation run data modify storage mgs:temp _inf.animation set value 0
execute unless data storage mgs:temp _inf.sound run data modify storage mgs:temp _inf.sound set value ""

