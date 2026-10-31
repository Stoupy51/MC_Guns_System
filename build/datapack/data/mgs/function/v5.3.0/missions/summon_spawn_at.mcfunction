
#> mgs:v5.3.0/missions/summon_spawn_at
#
# @within	mgs:v5.3.0/missions/summon_spawn_iter with storage mgs:temp _spos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#			name (unknown)
#			yaw (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.spawn_point","$(tag)","mgs.missions_entity"],CustomName:"$(name)",data:{yaw:$(yaw)}}

