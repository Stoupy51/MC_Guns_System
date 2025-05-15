
#> stoupgun:v5.0.0/casing/look_vectors
#
# @within	stoupgun:v5.0.0/casing/main
#

### Calculate motion vectors based on look direction and casing parameters

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

## --- COMBINE SCALED VECTORS INTO FINAL MOTION ---

# Start from scaled normals
scoreboard players operation #motion_x stoupgun.data = #scaled_normal_x stoupgun.data
scoreboard players operation #motion_y stoupgun.data = #scaled_normal_y stoupgun.data
scoreboard players operation #motion_z stoupgun.data = #scaled_normal_z stoupgun.data

# Add scaled tangent
scoreboard players operation #motion_x stoupgun.data += #scaled_tangent_x stoupgun.data
scoreboard players operation #motion_y stoupgun.data += #scaled_tangent_y stoupgun.data
scoreboard players operation #motion_z stoupgun.data += #scaled_tangent_z stoupgun.data

# Add scaled binormal
scoreboard players operation #motion_x stoupgun.data += #scaled_binormal_x stoupgun.data
scoreboard players operation #motion_z stoupgun.data += #scaled_binormal_z stoupgun.data

## --- SCALE DOWN COMBINED VECTOR ---

# Since vectors are scaled integers (x1000), we need to divide to normalize
scoreboard players operation #motion_x stoupgun.data /= #1000 stoupgun.data
scoreboard players operation #motion_y stoupgun.data /= #1000 stoupgun.data
scoreboard players operation #motion_z stoupgun.data /= #1000 stoupgun.data



## Calculate new position vectors based on normal, tangent, binormal and casing offsets

# 1) Load raw offset values (each *1000 in scoreboard)
execute store result score #offset_x stoupgun.data run data get storage stoupgun:gun stats.casing_offset[0] 1000
execute store result score #offset_y stoupgun.data run data get storage stoupgun:gun stats.casing_offset[1] 1000
execute store result score #offset_z stoupgun.data run data get storage stoupgun:gun stats.casing_offset[2] 1000

# 2) Compute each axis' contribution to world-space offset
# Binormal (X-axis)
scoreboard players operation #off_bx stoupgun.data = #binormal_x stoupgun.data
scoreboard players operation #off_bx stoupgun.data *= #offset_x stoupgun.data
# Normal   (Y-axis)
scoreboard players operation #off_nx stoupgun.data = #normal_x stoupgun.data
scoreboard players operation #off_nx stoupgun.data *= #offset_y stoupgun.data
# Tangent  (Z-axis)
scoreboard players operation #off_tx stoupgun.data = #tangent_x stoupgun.data
scoreboard players operation #off_tx stoupgun.data *= #offset_z stoupgun.data

# 3) Sum them and scale down (we did multiply by 1000)
scoreboard players operation #pos_new_x stoupgun.data = #off_bx stoupgun.data
scoreboard players operation #pos_new_x stoupgun.data += #off_nx stoupgun.data
scoreboard players operation #pos_new_x stoupgun.data += #off_tx stoupgun.data
scoreboard players operation #pos_new_x stoupgun.data /= #1000 stoupgun.data

# 4) Add original position
scoreboard players operation #pos_new_x stoupgun.data += #pos_initial_x stoupgun.data

# Repeat X logic for Y and Z…

# Y contributions
scoreboard players operation #off_by stoupgun.data = #binormal_y stoupgun.data
scoreboard players operation #off_by stoupgun.data *= #offset_x stoupgun.data
scoreboard players operation #off_ny stoupgun.data = #normal_y stoupgun.data
scoreboard players operation #off_ny stoupgun.data *= #offset_y stoupgun.data
scoreboard players operation #off_ty stoupgun.data = #tangent_y stoupgun.data
scoreboard players operation #off_ty stoupgun.data *= #offset_z stoupgun.data

scoreboard players operation #pos_new_y stoupgun.data = #off_by stoupgun.data
scoreboard players operation #pos_new_y stoupgun.data += #off_ny stoupgun.data
scoreboard players operation #pos_new_y stoupgun.data += #off_ty stoupgun.data
scoreboard players operation #pos_new_y stoupgun.data /= #1000 stoupgun.data
scoreboard players operation #pos_new_y stoupgun.data += #pos_initial_y stoupgun.data

# Z contributions
scoreboard players operation #off_bz stoupgun.data = #binormal_z stoupgun.data
scoreboard players operation #off_bz stoupgun.data *= #offset_x stoupgun.data
scoreboard players operation #off_nz stoupgun.data = #normal_z stoupgun.data
scoreboard players operation #off_nz stoupgun.data *= #offset_y stoupgun.data
scoreboard players operation #off_tz stoupgun.data = #tangent_z stoupgun.data
scoreboard players operation #off_tz stoupgun.data *= #offset_z stoupgun.data

scoreboard players operation #pos_new_z stoupgun.data = #off_bz stoupgun.data
scoreboard players operation #pos_new_z stoupgun.data += #off_nz stoupgun.data
scoreboard players operation #pos_new_z stoupgun.data += #off_tz stoupgun.data
scoreboard players operation #pos_new_z stoupgun.data /= #1000 stoupgun.data
scoreboard players operation #pos_new_z stoupgun.data += #pos_initial_z stoupgun.data

