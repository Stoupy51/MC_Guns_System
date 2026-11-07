
#> mgs:v5.4.0/zombies/escort/set_trader_speed
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/escort/start with storage mgs:temp _escort [ as @n[tag=mgs.zb_escort_new] ]
#
# @args		speed (unknown)
#

$attribute @s minecraft:movement_speed base set $(speed)

