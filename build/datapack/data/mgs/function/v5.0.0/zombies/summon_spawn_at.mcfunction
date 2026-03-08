
#> mgs:v5.0.0/zombies/summon_spawn_at
#
# @within	mgs:v5.0.0/zombies/summon_spawn_iter with storage mgs:temp _spos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			tag (unknown)
#			yaw (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.spawn_point","$(tag)","mgs.gm_entity","mgs.new_spawn"],data:{yaw:$(yaw)}}

