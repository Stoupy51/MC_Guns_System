
#> mgs:v5.0.0/missions/summon_oob_at
#
# @within	mgs:v5.0.0/missions/summon_oob_iter with storage mgs:temp _oob_pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.oob_point","mgs.gm_entity"]}

