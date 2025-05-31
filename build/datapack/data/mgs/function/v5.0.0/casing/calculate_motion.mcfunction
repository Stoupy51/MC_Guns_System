
#> mgs:v5.0.0/casing/calculate_motion
#
# @within	mgs:v5.0.0/casing/process_vectors
#

### Calculate motion based on scaled normal, tangent, and binormal vectors

# Start from scaled normals
scoreboard players operation #motion_x mgs.data = #scaled_normal_x mgs.data
scoreboard players operation #motion_y mgs.data = #scaled_normal_y mgs.data
scoreboard players operation #motion_z mgs.data = #scaled_normal_z mgs.data

# Add scaled tangent
scoreboard players operation #motion_x mgs.data += #scaled_tangent_x mgs.data
scoreboard players operation #motion_y mgs.data += #scaled_tangent_y mgs.data
scoreboard players operation #motion_z mgs.data += #scaled_tangent_z mgs.data

# Add scaled binormal
scoreboard players operation #motion_x mgs.data += #scaled_binormal_x mgs.data
scoreboard players operation #motion_z mgs.data += #scaled_binormal_z mgs.data

## --- SCALE DOWN COMBINED VECTOR ---

# Since vectors are scaled integers (x1000), we need to divide to normalize
scoreboard players operation #motion_x mgs.data /= #1000 mgs.data
scoreboard players operation #motion_y mgs.data /= #1000 mgs.data
scoreboard players operation #motion_z mgs.data /= #1000 mgs.data

