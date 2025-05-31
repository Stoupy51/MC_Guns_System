
#> mgs:v5.0.0/raycast/main
#
# @within	mgs:v5.0.0/player/right_click
#

# Handle accuracy
tp @s ~ ~ ~ ~ ~
function mgs:v5.0.0/raycast/accuracy/apply_spread

# Prepare arguments
data modify storage mgs:input with set value {}
data modify storage mgs:input with.blocks set value true
data modify storage mgs:input with.entities set value true
data modify storage mgs:input with.piercing set value 10
data modify storage mgs:input with.max_distance set value 128
data modify storage mgs:input with.hitbox_shape set value "interaction"
data modify storage mgs:input with.ignored_blocks set value "#mgs:v5.0.0/air"
data modify storage mgs:input with.on_hit_point set value "function mgs:v5.0.0/raycast/on_hit_point"
data modify storage mgs:input with.on_targeted_block set value "function mgs:v5.0.0/raycast/on_targeted_block"
data modify storage mgs:input with.on_targeted_entity set value "function mgs:v5.0.0/raycast/on_targeted_entity"

# Launch raycast with callbacks (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html#run-the-raycast)
execute at @s run function #bs.raycast:run with storage mgs:input

# Kill marker
kill @s

