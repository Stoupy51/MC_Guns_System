
#> mgs:v5.0.0/casing/calculate_vectors
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/casing/process_vectors
#

### Calculate base vectors (normal, tangent, binormal) from player's look direction

# Store the initial position of the marker (before movement)
tp @s ~ ~ ~ ~ ~
execute store result score #pos_initial_x mgs.data run data get entity @s Pos[0] 1000
execute store result score #pos_initial_y mgs.data run data get entity @s Pos[1] 1000
execute store result score #pos_initial_z mgs.data run data get entity @s Pos[2] 1000

## --- NORMAL VECTOR (Vertical / Y-axis component) ---

# Move the marker 1 block up relative to its local axes
tp @s ^ ^1 ^

# Calculate the normal vector: difference between new position and initial
execute store result score #normal_x mgs.data run data get entity @s Pos[0] 1000
execute store result score #normal_y mgs.data run data get entity @s Pos[1] 1000
execute store result score #normal_z mgs.data run data get entity @s Pos[2] 1000
scoreboard players operation #normal_x mgs.data -= #pos_initial_x mgs.data
scoreboard players operation #normal_y mgs.data -= #pos_initial_y mgs.data
scoreboard players operation #normal_z mgs.data -= #pos_initial_z mgs.data

# Scale into a new set of objectives so raw normals stay intact
scoreboard players operation #scaled_normal_x mgs.data = #normal_x mgs.data
scoreboard players operation #scaled_normal_x mgs.data *= #casing_normal mgs.data
scoreboard players operation #scaled_normal_y mgs.data = #normal_y mgs.data
scoreboard players operation #scaled_normal_y mgs.data *= #casing_normal mgs.data
scoreboard players operation #scaled_normal_z mgs.data = #normal_z mgs.data
scoreboard players operation #scaled_normal_z mgs.data *= #casing_normal mgs.data

## --- TANGENT VECTOR (Forward / Z-axis component) ---

# Move the marker 1 block forward (local Z)
tp @s ^ ^ ^1
execute store result score #tangent_x mgs.data run data get entity @s Pos[0] 1000
execute store result score #tangent_y mgs.data run data get entity @s Pos[1] 1000
execute store result score #tangent_z mgs.data run data get entity @s Pos[2] 1000
scoreboard players operation #tangent_x mgs.data -= #pos_initial_x mgs.data
scoreboard players operation #tangent_y mgs.data -= #pos_initial_y mgs.data
scoreboard players operation #tangent_z mgs.data -= #pos_initial_z mgs.data

# Preserve raw tangents, then scale
scoreboard players operation #scaled_tangent_x mgs.data = #tangent_x mgs.data
scoreboard players operation #scaled_tangent_x mgs.data *= #casing_tangent mgs.data
scoreboard players operation #scaled_tangent_y mgs.data = #tangent_y mgs.data
scoreboard players operation #scaled_tangent_y mgs.data *= #casing_tangent mgs.data
scoreboard players operation #scaled_tangent_z mgs.data = #tangent_z mgs.data
scoreboard players operation #scaled_tangent_z mgs.data *= #casing_tangent mgs.data

## --- BINORMAL VECTOR (Sideways / X-axis component) ---

# Move the marker 1 block to the right (local X)
tp @s ^1 ^ ^
execute store result score #binormal_x mgs.data run data get entity @s Pos[0] 1000
execute store result score #binormal_y mgs.data run data get entity @s Pos[1] 1000
execute store result score #binormal_z mgs.data run data get entity @s Pos[2] 1000
scoreboard players operation #binormal_x mgs.data -= #pos_initial_x mgs.data
scoreboard players operation #binormal_y mgs.data -= #pos_initial_y mgs.data
scoreboard players operation #binormal_z mgs.data -= #pos_initial_z mgs.data

# Preserve raw binormals, then scale
scoreboard players operation #scaled_binormal_x mgs.data = #binormal_x mgs.data
scoreboard players operation #scaled_binormal_x mgs.data *= #casing_binormal mgs.data
scoreboard players operation #scaled_binormal_y mgs.data = #binormal_y mgs.data
scoreboard players operation #scaled_binormal_y mgs.data *= #casing_binormal mgs.data
scoreboard players operation #scaled_binormal_z mgs.data = #binormal_z mgs.data
scoreboard players operation #scaled_binormal_z mgs.data *= #casing_binormal mgs.data

