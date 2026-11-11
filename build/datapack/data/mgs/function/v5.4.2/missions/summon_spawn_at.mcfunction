
#> mgs:v5.4.2/missions/summon_spawn_at
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/missions/summon_spawn_iter with storage mgs:temp _spos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#			yaw (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.spawn_point","$(tag)","mgs.missions_entity"],data:{yaw:$(yaw)}}

