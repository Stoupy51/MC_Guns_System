
#> mgs:v5.3.0/maps/inflate/leaderboard_fields
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/maps/inflate/leaderboard
#

function mgs:v5.3.0/maps/inflate/rotation
execute unless data storage mgs:temp _inf.board run data modify storage mgs:temp _inf.board set value "level_zb"
execute unless data storage mgs:temp _inf.map_id run data modify storage mgs:temp _inf.map_id set value ""
execute unless data storage mgs:temp _inf.players run data modify storage mgs:temp _inf.players set value "all"

