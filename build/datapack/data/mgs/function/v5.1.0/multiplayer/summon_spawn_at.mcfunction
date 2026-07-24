
#> mgs:v5.1.0/multiplayer/summon_spawn_at
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/summon_spawn_iter with storage mgs:temp _spos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#			yaw (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.spawn_point","$(tag)","mgs.gm_entity"],data:{yaw:$(yaw)}}

