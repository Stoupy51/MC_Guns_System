
#> mgs:v5.4.2/ammo/infinite_refill
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/ammo/decrease
#

execute store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity

