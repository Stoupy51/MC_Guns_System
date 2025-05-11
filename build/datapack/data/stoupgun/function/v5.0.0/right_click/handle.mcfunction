
#> stoupgun:v5.0.0/right_click/handle
#
# @within	stoupgun:v5.0.0/player/tick
#

# Decrease pending clicks by 1
scoreboard players remove @s stoupgun.pending_clicks 1

# If SelectedItem is not a gun, stop
data modify storage stoupgun:gun stats set from entity @s SelectedItem.components."minecraft:custom_data".stoupgun.stats
execute unless data storage stoupgun:gun stats run return fail

## Raycast (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html)
# Prepare arguments
data modify storage stoupgun:input with set value {}
data modify storage stoupgun:input with.blocks set value true
data modify storage stoupgun:input with.entities set value true
data modify storage stoupgun:input with.piercing set value 10
data modify storage stoupgun:input with.max_distance set value 128
data modify storage stoupgun:input with.hitbox_shape set value "interaction"
data modify storage stoupgun:input with.on_hit_point set value "function stoupgun:v5.0.0/raycast/on_hit_point"
data modify storage stoupgun:input with.on_targeted_block set value "function stoupgun:v5.0.0/raycast/on_targeted_block"
data modify storage stoupgun:input with.on_targeted_entity set value "function stoupgun:v5.0.0/raycast/on_targeted_entity"

# Run raycast with callbacks
execute anchored eyes positioned ^ ^ ^ run function #bs.raycast:run with storage stoupgun:input

# Playsound
playsound stoupgun:ak47/fire player @s ~ ~1000000 ~ 10000000
playsound stoupgun:common/med_crack player @s ~ ~ ~ 1.0

# Remove storage
data remove storage stoupgun:gun stats

