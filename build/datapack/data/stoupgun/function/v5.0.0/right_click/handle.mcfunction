
#> stoupgun:v5.0.0/right_click/handle
#
# @within	stoupgun:v5.0.0/player/tick
#

# Decrease pending clicks by 1
scoreboard players remove @s stoupgun.pending_clicks 1
execute if score @s stoupgun.cooldown matches 1.. run return fail


# If SelectedItem is not a gun, stop
data remove storage stoupgun:gun stats
data modify storage stoupgun:gun stats set from entity @s SelectedItem.components."minecraft:custom_data".stoupgun.stats
execute unless data storage stoupgun:gun stats run return fail

# Set cooldown
execute store result score @s stoupgun.cooldown run data get storage stoupgun:gun stats.cooldown

## Raycast (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html)
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

# Run raycast with callbacks
tag @s add stoupgun.attacker
execute anchored eyes positioned ^ ^ ^ run function #bs.raycast:run with storage stoupgun:input
tag @s remove stoupgun.attacker

# Remove bullet from mag
# TODO
#playsound stoupgun:common/empty player @a[distance=..12]

# TODO: Advanced Playsound
playsound stoupgun:ak47/fire player @s ~ ~1000000 ~ 400000
playsound stoupgun:ak47/fire player @a[distance=0.01..48] ~ ~ ~ 3

