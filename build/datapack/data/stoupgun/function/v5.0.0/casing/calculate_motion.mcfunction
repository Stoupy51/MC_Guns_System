
#> stoupgun:v5.0.0/casing/calculate_motion
#
# @within	stoupgun:v5.0.0/casing/process_vectors
#

### Calculate motion based on scaled normal, tangent, and binormal vectors

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

