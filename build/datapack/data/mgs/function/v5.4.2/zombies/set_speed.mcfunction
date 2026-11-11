
#> mgs:v5.4.2/zombies/set_speed
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/types/fast with storage mgs:temp _zb_speed
#			mgs:v5.4.2/zombies/types/tank with storage mgs:temp _zb_speed
#			mgs:v5.4.2/zombies/types/armed with storage mgs:temp _zb_speed
#			mgs:v5.4.2/zombies/types/aura with storage mgs:temp _zb_speed
#
# @args		value (unknown)
#

$attribute @s minecraft:movement_speed base set $(value)

