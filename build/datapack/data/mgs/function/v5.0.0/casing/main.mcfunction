
#> mgs:v5.0.0/casing/main
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Get if player is zooming or not
scoreboard players set #is_zoom mgs.data 0
execute if data storage mgs:gun all.stats.is_zoom run scoreboard players set #is_zoom mgs.data 1

# Extract casing data from gun
scoreboard players set #casing_normal mgs.data 0
scoreboard players set #casing_tangent mgs.data 0
scoreboard players set #casing_binormal mgs.data 0
execute store result score #casing_normal mgs.data run data get storage mgs:gun all.stats.casing_n
execute store result score #casing_tangent mgs.data run data get storage mgs:gun all.stats.casing_t
execute store result score #casing_binormal mgs.data run data get storage mgs:gun all.stats.casing_b

# Stop if no casing data
execute unless data storage mgs:gun all.stats.casing_model run return fail

# Add random variation to the tangent
scoreboard players set #random_variation mgs.data 40
execute store result score #random_variation mgs.data run random value 0..39
scoreboard players remove #random_variation mgs.data 20
scoreboard players operation #casing_tangent mgs.data += #random_variation mgs.data

# Calculate look vectors and motion
execute anchored eyes positioned ^ ^ ^ summon marker run function mgs:v5.0.0/casing/process_vectors

# Prepare casting model and motion
data modify storage mgs:temp casing set value {Item:{components:{}},Motion:[0.0d,0.0d,0.0d],Pos:[0.0d,0.0d,0.0d]}
data modify storage mgs:temp casing.Item.components."minecraft:item_model" set from storage mgs:gun all.stats.casing_model
execute store result storage mgs:temp casing.Motion[0] double 0.001 run scoreboard players get #motion_x mgs.data
execute store result storage mgs:temp casing.Motion[1] double 0.001 run scoreboard players get #motion_y mgs.data
execute store result storage mgs:temp casing.Motion[2] double 0.001 run scoreboard players get #motion_z mgs.data

# Prepare position offset
execute store result storage mgs:temp casing.Pos[0] double 0.001 run scoreboard players get #pos_new_x mgs.data
execute store result storage mgs:temp casing.Pos[1] double 0.001 run scoreboard players get #pos_new_y mgs.data
execute store result storage mgs:temp casing.Pos[2] double 0.001 run scoreboard players get #pos_new_z mgs.data

# Create casing entity
summon item ~ ~ ~ {Tags:["mgs.new","mgs.casing"],Item:{id:"minecraft:stone",count:1,components:{"minecraft:item_model":"air"}},PickupDelay:32767,Age:5990}
execute as @n[type=item,tag=mgs.new] run function mgs:v5.0.0/casing/update_item

