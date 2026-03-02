
#> mgs:v5.0.0/ammo/infinite_refill
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/decrease
#

# Set player's ammo count to weapon capacity
execute store result score @s mgs.remaining_bullets run data get storage mgs:gun all.stats.capacity

