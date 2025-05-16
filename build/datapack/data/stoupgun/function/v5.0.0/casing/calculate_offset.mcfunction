
#> stoupgun:v5.0.0/casing/calculate_offset
#
# @within	stoupgun:v5.0.0/casing/process_vectors
#

### Transform local casing offsets into world-space coordinates using the gun's orientation vectors

# 1) Load local offset values from storage and scale to integers (x1000)
# These represent the desired offset in the gun's local coordinate system
execute store result score #offset_x stoupgun.data run data get storage stoupgun:gun stats.casing_offset[0] 1000
execute store result score #offset_y stoupgun.data run data get storage stoupgun:gun stats.casing_offset[1] 1000
execute store result score #offset_z stoupgun.data run data get storage stoupgun:gun stats.casing_offset[2] 1000

# 2) Project local offsets onto world-space axes using orientation vectors
# Each vector (binormal/normal/tangent) contributes to the final world position
# Binormal vector (local X) contribution
scoreboard players operation #off_bx stoupgun.data = #binormal_x stoupgun.data
scoreboard players operation #off_bx stoupgun.data *= #offset_x stoupgun.data
# Normal vector (local Y) contribution
scoreboard players operation #off_nx stoupgun.data = #normal_x stoupgun.data
scoreboard players operation #off_nx stoupgun.data *= #offset_y stoupgun.data
# Tangent vector (local Z) contribution
scoreboard players operation #off_tx stoupgun.data = #tangent_x stoupgun.data
scoreboard players operation #off_tx stoupgun.data *= #offset_z stoupgun.data

# 3) Combine vector contributions and convert back to decimal coordinates
# Sum all contributions for X coordinate
scoreboard players operation #pos_new_x stoupgun.data = #off_bx stoupgun.data
scoreboard players operation #pos_new_x stoupgun.data += #off_nx stoupgun.data
scoreboard players operation #pos_new_x stoupgun.data += #off_tx stoupgun.data
scoreboard players operation #pos_new_x stoupgun.data /= #1000 stoupgun.data

# 4) Add base position to get final world coordinates
scoreboard players operation #pos_new_x stoupgun.data += #pos_initial_x stoupgun.data

# Repeat same process for Y coordinate
# Project local offsets onto world Y axis
scoreboard players operation #off_by stoupgun.data = #binormal_y stoupgun.data
scoreboard players operation #off_by stoupgun.data *= #offset_x stoupgun.data
scoreboard players operation #off_ny stoupgun.data = #normal_y stoupgun.data
scoreboard players operation #off_ny stoupgun.data *= #offset_y stoupgun.data
scoreboard players operation #off_ty stoupgun.data = #tangent_y stoupgun.data
scoreboard players operation #off_ty stoupgun.data *= #offset_z stoupgun.data

# Combine and convert Y coordinate
scoreboard players operation #pos_new_y stoupgun.data = #off_by stoupgun.data
scoreboard players operation #pos_new_y stoupgun.data += #off_ny stoupgun.data
scoreboard players operation #pos_new_y stoupgun.data += #off_ty stoupgun.data
scoreboard players operation #pos_new_y stoupgun.data /= #1000 stoupgun.data
scoreboard players operation #pos_new_y stoupgun.data += #pos_initial_y stoupgun.data

# Repeat same process for Z coordinate
# Project local offsets onto world Z axis
scoreboard players operation #off_bz stoupgun.data = #binormal_z stoupgun.data
scoreboard players operation #off_bz stoupgun.data *= #offset_x stoupgun.data
scoreboard players operation #off_nz stoupgun.data = #normal_z stoupgun.data
scoreboard players operation #off_nz stoupgun.data *= #offset_y stoupgun.data
scoreboard players operation #off_tz stoupgun.data = #tangent_z stoupgun.data
scoreboard players operation #off_tz stoupgun.data *= #offset_z stoupgun.data

# Combine and convert Z coordinate
scoreboard players operation #pos_new_z stoupgun.data = #off_bz stoupgun.data
scoreboard players operation #pos_new_z stoupgun.data += #off_nz stoupgun.data
scoreboard players operation #pos_new_z stoupgun.data += #off_tz stoupgun.data
scoreboard players operation #pos_new_z stoupgun.data /= #1000 stoupgun.data
scoreboard players operation #pos_new_z stoupgun.data += #pos_initial_z stoupgun.data

