
#> mgs:v5.4.1/maps/inflate/special_spawn_fields
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/inflate/special_spawn
#

function mgs:v5.4.1/maps/inflate/rotation
execute unless data storage mgs:temp _inf.activation_box run data modify storage mgs:temp _inf.activation_box set value []
execute unless data storage mgs:temp _inf.walk_to run data modify storage mgs:temp _inf.walk_to set value []
execute unless data storage mgs:temp _inf.rise_ticks run data modify storage mgs:temp _inf.rise_ticks set value 20
execute unless data storage mgs:temp _inf.min_round run data modify storage mgs:temp _inf.min_round set value 0
execute unless data storage mgs:temp _inf.max_round run data modify storage mgs:temp _inf.max_round set value 0
execute unless data storage mgs:temp _inf.arrival run data modify storage mgs:temp _inf.arrival set value "portal"
execute unless data storage mgs:temp _inf.mob run data modify storage mgs:temp _inf.mob set value {entity:"wolf"}
execute unless data storage mgs:temp _inf.group_id run data modify storage mgs:temp _inf.group_id set value 0

