
#> mgs:v5.1.0/zombies/set_speed
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/types/fast with storage mgs:temp _zb_speed
#			mgs:v5.1.0/zombies/types/tank with storage mgs:temp _zb_speed
#			mgs:v5.1.0/zombies/types/armed with storage mgs:temp _zb_speed
#			mgs:v5.1.0/zombies/types/aura with storage mgs:temp _zb_speed
#
# @args		value (unknown)
#

$attribute @s minecraft:movement_speed base set $(value)

