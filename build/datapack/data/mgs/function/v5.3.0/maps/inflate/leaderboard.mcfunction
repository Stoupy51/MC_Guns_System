
#> mgs:v5.3.0/maps/inflate/leaderboard
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/maps/inflate
#			mgs:v5.3.0/maps/inflate/leaderboard
#

data modify storage mgs:temp _inf set from storage mgs:temp _inf_src[0]
function mgs:v5.3.0/maps/inflate/leaderboard_fields
data modify storage mgs:temp _inf_map.leaderboards append from storage mgs:temp _inf
data remove storage mgs:temp _inf_src[0]
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.3.0/maps/inflate/leaderboard

