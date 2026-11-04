
#> mgs:v5.3.0/ammo/infinite_refill
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/ammo/decrease
#

execute store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity

