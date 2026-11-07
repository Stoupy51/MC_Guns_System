
#> mgs:v5.4.0/shared/summon_oob_at
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/shared/summon_oob_iter with storage mgs:temp _oob_pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			mode (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.oob_point","mgs.$(mode)_entity"]}

