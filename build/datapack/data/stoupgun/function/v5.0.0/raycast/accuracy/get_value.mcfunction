
#> stoupgun:v5.0.0/raycast/accuracy/get_value
#
# @within	stoupgun:v5.0.0/player/right_click
#

## Order is important: Jump > Sprint > Sneak > Walk > Base
data remove storage stoupgun:gun accuracy

# If not on ground, return jump accuracy
execute unless predicate stoupgun:v5.0.0/is_on_ground run return run data modify storage stoupgun:gun accuracy set from storage stoupgun:gun stats.acc_jump

# If sprinting, return sprint accuracy
execute if predicate stoupgun:v5.0.0/is_sprinting run return run data modify storage stoupgun:gun accuracy set from storage stoupgun:gun stats.acc_sprint

# If sneaking, return sneak accuracy
execute if predicate stoupgun:v5.0.0/is_sneaking run return run data modify storage stoupgun:gun accuracy set from storage stoupgun:gun stats.acc_sneak

# If moving horizontally, return walk accuracy
execute if predicate stoupgun:v5.0.0/is_moving run return run data modify storage stoupgun:gun accuracy set from storage stoupgun:gun stats.acc_walk

# Else, return base accuracy
data modify storage stoupgun:gun accuracy set from storage stoupgun:gun stats.acc_base

