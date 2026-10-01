
#> mgs:v5.1.0/casing/calculate_motion
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.1.0/casing/process_vectors
#

### Motion = scaled normal + tangent + binormal.

scoreboard players operation #motion_x mgs.data = #scaled_normal_x mgs.data
scoreboard players operation #motion_y mgs.data = #scaled_normal_y mgs.data
scoreboard players operation #motion_z mgs.data = #scaled_normal_z mgs.data

scoreboard players operation #motion_x mgs.data += #scaled_tangent_x mgs.data
scoreboard players operation #motion_y mgs.data += #scaled_tangent_y mgs.data
scoreboard players operation #motion_z mgs.data += #scaled_tangent_z mgs.data

scoreboard players operation #motion_x mgs.data += #scaled_binormal_x mgs.data
scoreboard players operation #motion_z mgs.data += #scaled_binormal_z mgs.data

# The vectors are x1000 integers.
scoreboard players operation #motion_x mgs.data /= #1000 mgs.data
scoreboard players operation #motion_y mgs.data /= #1000 mgs.data
scoreboard players operation #motion_z mgs.data /= #1000 mgs.data

