
#> mgs:v5.4.2/grenade/flash_area
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/grenade/flash_apply with storage mgs:temp flash
#
# @args		radius_float (unknown)
#

$execute as @a[distance=..$(radius_float)] at @s run function mgs:v5.4.2/grenade/flash_check

