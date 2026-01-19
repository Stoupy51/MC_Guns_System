
#> mgs:v5.0.0/raycast/accuracy/get_value
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/shoot
#

## Order is important: Jump > Sneak > Sprint > Walk > Base
data remove storage mgs:gun accuracy

# If not on ground, return jump accuracy
execute unless predicate mgs:v5.0.0/is_on_ground run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_jump

# If sneaking, return sneak accuracy
execute if predicate mgs:v5.0.0/is_sneaking run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_sneak

# If sprinting, return sprint accuracy
execute if predicate mgs:v5.0.0/is_sprinting run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_sprint

# If moving horizontally, return walk accuracy
execute if predicate mgs:v5.0.0/is_moving run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_walk

# Else, return base accuracy
data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_base

