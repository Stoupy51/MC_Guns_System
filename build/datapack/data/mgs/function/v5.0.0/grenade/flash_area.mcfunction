
#> mgs:v5.0.0/grenade/flash_area
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/flash_apply with storage mgs:temp flash
#
# @args		radius_int (unknown)
#

$execute as @a[distance=..$(radius_int)] at @s run function mgs:v5.0.0/grenade/flash_check

