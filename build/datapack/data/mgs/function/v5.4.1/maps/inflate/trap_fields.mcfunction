
#> mgs:v5.4.1/maps/inflate/trap_fields
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/inflate/trap
#

function mgs:v5.4.1/maps/inflate/rotation
execute unless data storage mgs:temp _inf.price run data modify storage mgs:temp _inf.price set value 1000
execute unless data storage mgs:temp _inf.type run data modify storage mgs:temp _inf.type set value 0
execute unless data storage mgs:temp _inf.duration run data modify storage mgs:temp _inf.duration set value 200
execute unless data storage mgs:temp _inf.cooldown run data modify storage mgs:temp _inf.cooldown set value 1200
execute unless data storage mgs:temp _inf.effect_radius run data modify storage mgs:temp _inf.effect_radius set value [3.0f,2.0f,3.0f]
execute unless data storage mgs:temp _inf.offset_pos run data modify storage mgs:temp _inf.offset_pos set value [0,0,0]
execute unless data storage mgs:temp _inf.power run data modify storage mgs:temp _inf.power set value 1b

