
#> mgs:v5.1.0/grenade/summon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/grenade/summon_loop
#

# Spread from the accuracy value.
function mgs:v5.1.0/raycast/accuracy/get_value

execute anchored eyes positioned ^ ^ ^0.5 summon item_display run function mgs:v5.1.0/grenade/init

