
#> stoupgun:v5.0.0/raycast/main
#
# @within	stoupgun:v5.0.0/player/right_click
#

# Prepare arguments
data modify storage stoupgun:input with set value {}
data modify storage stoupgun:input with.blocks set value true
data modify storage stoupgun:input with.entities set value true
data modify storage stoupgun:input with.piercing set value 10
data modify storage stoupgun:input with.max_distance set value 128
data modify storage stoupgun:input with.hitbox_shape set value "interaction"
data modify storage stoupgun:input with.ignored_blocks set value "#stoupgun:v5.0.0/air"
data modify storage stoupgun:input with.on_hit_point set value "function stoupgun:v5.0.0/raycast/on_hit_point"
data modify storage stoupgun:input with.on_targeted_block set value "function stoupgun:v5.0.0/raycast/on_targeted_block"
data modify storage stoupgun:input with.on_targeted_entity set value "function stoupgun:v5.0.0/raycast/on_targeted_entity"

# Launch raycast with callbacks
tag @s add stoupgun.attacker
execute anchored eyes positioned ^ ^ ^ run function #bs.raycast:run with storage stoupgun:input
tag @s remove stoupgun.attacker

