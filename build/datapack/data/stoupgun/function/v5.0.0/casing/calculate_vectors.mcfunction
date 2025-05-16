
#> stoupgun:v5.0.0/casing/calculate_vectors
#
# @within	stoupgun:v5.0.0/casing/process_vectors
#

### Calculate base vectors (normal, tangent, binormal) from player's look direction

# Store the initial position of the marker (before movement)
tp @s ~ ~ ~ ~ ~
execute store result score #pos_initial_x stoupgun.data run data get entity @s Pos[0] 1000
execute store result score #pos_initial_y stoupgun.data run data get entity @s Pos[1] 1000
execute store result score #pos_initial_z stoupgun.data run data get entity @s Pos[2] 1000

## --- NORMAL VECTOR (Vertical / Y-axis component) ---

# Move the marker 1 block up relative to its local axes
tp @s ^ ^1 ^

# Calculate the normal vector: difference between new position and initial
execute store result score #normal_x stoupgun.data run data get entity @s Pos[0] 1000
execute store result score #normal_y stoupgun.data run data get entity @s Pos[1] 1000
execute store result score #normal_z stoupgun.data run data get entity @s Pos[2] 1000
scoreboard players operation #normal_x stoupgun.data -= #pos_initial_x stoupgun.data
scoreboard players operation #normal_y stoupgun.data -= #pos_initial_y stoupgun.data
scoreboard players operation #normal_z stoupgun.data -= #pos_initial_z stoupgun.data

# Scale into a new set of objectives so raw normals stay intact
scoreboard players operation #scaled_normal_x stoupgun.data = #normal_x stoupgun.data
scoreboard players operation #scaled_normal_x stoupgun.data *= #casing_normal stoupgun.data
scoreboard players operation #scaled_normal_y stoupgun.data = #normal_y stoupgun.data
scoreboard players operation #scaled_normal_y stoupgun.data *= #casing_normal stoupgun.data
scoreboard players operation #scaled_normal_z stoupgun.data = #normal_z stoupgun.data
scoreboard players operation #scaled_normal_z stoupgun.data *= #casing_normal stoupgun.data

## --- TANGENT VECTOR (Forward / Z-axis component) ---

# Move the marker 1 block forward (local Z)
tp @s ^ ^ ^1
execute store result score #tangent_x stoupgun.data run data get entity @s Pos[0] 1000
execute store result score #tangent_y stoupgun.data run data get entity @s Pos[1] 1000
execute store result score #tangent_z stoupgun.data run data get entity @s Pos[2] 1000
scoreboard players operation #tangent_x stoupgun.data -= #pos_initial_x stoupgun.data
scoreboard players operation #tangent_y stoupgun.data -= #pos_initial_y stoupgun.data
scoreboard players operation #tangent_z stoupgun.data -= #pos_initial_z stoupgun.data

# Preserve raw tangents, then scale
scoreboard players operation #scaled_tangent_x stoupgun.data = #tangent_x stoupgun.data
scoreboard players operation #scaled_tangent_x stoupgun.data *= #casing_tangent stoupgun.data
scoreboard players operation #scaled_tangent_y stoupgun.data = #tangent_y stoupgun.data
scoreboard players operation #scaled_tangent_y stoupgun.data *= #casing_tangent stoupgun.data
scoreboard players operation #scaled_tangent_z stoupgun.data = #tangent_z stoupgun.data
scoreboard players operation #scaled_tangent_z stoupgun.data *= #casing_tangent stoupgun.data

## --- BINORMAL VECTOR (Sideways / X-axis component) ---

# Move the marker 1 block to the right (local X)
tp @s ^1 ^ ^
execute store result score #binormal_x stoupgun.data run data get entity @s Pos[0] 1000
execute store result score #binormal_y stoupgun.data run data get entity @s Pos[1] 1000
execute store result score #binormal_z stoupgun.data run data get entity @s Pos[2] 1000
scoreboard players operation #binormal_x stoupgun.data -= #pos_initial_x stoupgun.data
scoreboard players operation #binormal_y stoupgun.data -= #pos_initial_y stoupgun.data
scoreboard players operation #binormal_z stoupgun.data -= #pos_initial_z stoupgun.data

# Preserve raw binormals, then scale
scoreboard players operation #scaled_binormal_x stoupgun.data = #binormal_x stoupgun.data
scoreboard players operation #scaled_binormal_x stoupgun.data *= #casing_binormal stoupgun.data
scoreboard players operation #scaled_binormal_y stoupgun.data = #binormal_y stoupgun.data
scoreboard players operation #scaled_binormal_y stoupgun.data *= #casing_binormal stoupgun.data
scoreboard players operation #scaled_binormal_z stoupgun.data = #binormal_z stoupgun.data
scoreboard players operation #scaled_binormal_z stoupgun.data *= #casing_binormal stoupgun.data

