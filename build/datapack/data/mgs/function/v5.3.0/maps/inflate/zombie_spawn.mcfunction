
#> mgs:v5.3.0/maps/inflate/zombie_spawn
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/maps/inflate
#			mgs:v5.3.0/maps/inflate/zombie_spawn
#

data modify storage mgs:temp _inf set from storage mgs:temp _inf_src[0]
function mgs:v5.3.0/maps/inflate/zombie_spawn_fields
data modify storage mgs:temp _inf_map.spawning_points.zombies append from storage mgs:temp _inf
data remove storage mgs:temp _inf_src[0]
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.3.0/maps/inflate/zombie_spawn

