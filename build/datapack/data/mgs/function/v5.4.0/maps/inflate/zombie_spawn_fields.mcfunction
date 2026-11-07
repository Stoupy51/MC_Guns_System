
#> mgs:v5.4.0/maps/inflate/zombie_spawn_fields
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/inflate/zombie_spawn
#

function mgs:v5.4.0/maps/inflate/rotation
execute unless data storage mgs:temp _inf.activation_box run data modify storage mgs:temp _inf.activation_box set value []
execute unless data storage mgs:temp _inf.walk_to run data modify storage mgs:temp _inf.walk_to set value []
execute unless data storage mgs:temp _inf.rise_ticks run data modify storage mgs:temp _inf.rise_ticks set value 20
execute unless data storage mgs:temp _inf.min_round run data modify storage mgs:temp _inf.min_round set value 0
execute unless data storage mgs:temp _inf.max_round run data modify storage mgs:temp _inf.max_round set value 0
execute unless data storage mgs:temp _inf.arrival run data modify storage mgs:temp _inf.arrival set value "floor"
execute unless data storage mgs:temp _inf.power run data modify storage mgs:temp _inf.power set value 0b
execute unless data storage mgs:temp _inf.mob run data modify storage mgs:temp _inf.mob set value {entity:"zombie"}
execute unless data storage mgs:temp _inf.group_id run data modify storage mgs:temp _inf.group_id set value 0

