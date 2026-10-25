
#> mgs:v5.3.0/grenade/flash_area
#
# @executed	at @s
#
# @within	mgs:v5.3.0/grenade/flash_apply with storage mgs:temp flash
#
# @args		radius_float (unknown)
#

$execute as @a[distance=..$(radius_float)] at @s run function mgs:v5.3.0/grenade/flash_check

