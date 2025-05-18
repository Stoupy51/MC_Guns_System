
#> stoupgun:v5.0.0/casing/main
#
# @within	stoupgun:v5.0.0/player/right_click
#

# Get if player is zooming or not
scoreboard players set #is_zoom stoupgun.data 0
execute if data storage stoupgun:gun all.stats.is_zoom run scoreboard players set #is_zoom stoupgun.data 1

# Extract casing data from gun
scoreboard players set #casing_normal stoupgun.data 0
scoreboard players set #casing_tangent stoupgun.data 0
scoreboard players set #casing_binormal stoupgun.data 0
execute store result score #casing_normal stoupgun.data run data get storage stoupgun:gun all.stats.casing_n
execute store result score #casing_tangent stoupgun.data run data get storage stoupgun:gun all.stats.casing_t
execute store result score #casing_binormal stoupgun.data run data get storage stoupgun:gun all.stats.casing_b

# Stop if no casing data
execute unless data storage stoupgun:gun all.stats.casing_model run return fail

# Add random variation to the tangent
scoreboard players set #random_variation stoupgun.data 40
execute store result score #random_variation stoupgun.data run random value 0..39
scoreboard players remove #random_variation stoupgun.data 20
scoreboard players operation #casing_tangent stoupgun.data += #random_variation stoupgun.data

# Calculate look vectors and motion
execute anchored eyes positioned ^ ^ ^ summon marker run function stoupgun:v5.0.0/casing/process_vectors

# Prepare casting model and motion
data modify storage stoupgun:temp casing set value {Item:{components:{}},Motion:[0.0d,0.0d,0.0d],Pos:[0.0d,0.0d,0.0d]}
data modify storage stoupgun:temp casing.Item.components."minecraft:item_model" set from storage stoupgun:gun all.stats.casing_model
execute store result storage stoupgun:temp casing.Motion[0] double 0.001 run scoreboard players get #motion_x stoupgun.data
execute store result storage stoupgun:temp casing.Motion[1] double 0.001 run scoreboard players get #motion_y stoupgun.data
execute store result storage stoupgun:temp casing.Motion[2] double 0.001 run scoreboard players get #motion_z stoupgun.data

# Prepare position offset
execute store result storage stoupgun:temp casing.Pos[0] double 0.001 run scoreboard players get #pos_new_x stoupgun.data
execute store result storage stoupgun:temp casing.Pos[1] double 0.001 run scoreboard players get #pos_new_y stoupgun.data
execute store result storage stoupgun:temp casing.Pos[2] double 0.001 run scoreboard players get #pos_new_z stoupgun.data

# Create casing entity
summon item ~ ~ ~ {Tags:["stoupgun.new","stoupgun.casing"],Item:{id:"minecraft:stone",count:1,components:{"minecraft:item_model":"air"}},PickupDelay:32767,Age:5990}
execute as @n[type=item,tag=stoupgun.new] run function stoupgun:v5.0.0/casing/update_item

