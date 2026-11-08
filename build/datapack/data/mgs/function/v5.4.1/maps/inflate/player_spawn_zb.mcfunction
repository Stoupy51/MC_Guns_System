
#> mgs:v5.4.1/maps/inflate/player_spawn_zb
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/inflate
#			mgs:v5.4.1/maps/inflate/player_spawn_zb
#

data modify storage mgs:temp _inf set from storage mgs:temp _inf_src[0]
function mgs:v5.4.1/maps/inflate/player_spawn_zb_fields
data modify storage mgs:temp _inf_map.spawning_points.players append from storage mgs:temp _inf
data remove storage mgs:temp _inf_src[0]
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/player_spawn_zb

