
#> mgs:v5.0.0/zombies/barriers/setup_iter
#
# @within	mgs:v5.0.0/zombies/barriers/setup
#			mgs:v5.0.0/zombies/barriers/setup_iter
#

# Assign incrementing ID
scoreboard players add #barrier_counter mgs.data 1

# Read position (relative) and convert to absolute
execute store result score #bx mgs.data run data get storage mgs:temp _barrier_iter[0].pos[0]
execute store result score #by mgs.data run data get storage mgs:temp _barrier_iter[0].pos[1]
execute store result score #bz mgs.data run data get storage mgs:temp _barrier_iter[0].pos[2]
scoreboard players operation #bx mgs.data += #gm_base_x mgs.data
scoreboard players operation #by mgs.data += #gm_base_y mgs.data
scoreboard players operation #bz mgs.data += #gm_base_z mgs.data

# Read yaw from rotation[0]: float -> score*100 -> double*0.01
execute store result score #byaw mgs.data run data get storage mgs:temp _barrier_iter[0].rotation[0] 100

# Store positions and yaw for place_at macro
execute store result storage mgs:temp _bplace.x double 1 run scoreboard players get #bx mgs.data
execute store result storage mgs:temp _bplace.y double 1 run scoreboard players get #by mgs.data
execute store result storage mgs:temp _bplace.z double 1 run scoreboard players get #bz mgs.data
execute store result storage mgs:temp _bplace.yaw double 0.01 run scoreboard players get #byaw mgs.data

# Summon block_display
function mgs:v5.0.0/zombies/barriers/place_at with storage mgs:temp _bplace

# Copy all zb_object data onto the display (stores block_enabled, block_disabled, radius, etc.)
execute as @n[tag=mgs._barrier_new_d] run data modify entity @s data set from storage mgs:temp _barrier_iter[0]

# Set initial block_state from block_enabled
execute as @n[tag=mgs._barrier_new_d] run data modify entity @s block_state set from entity @s data.block_enabled

# Set scoreboards on display
scoreboard players operation @n[tag=mgs._barrier_new_d] mgs.zb.barrier.id = #barrier_counter mgs.data
execute store result score @n[tag=mgs._barrier_new_d] mgs.zb.barrier.radius run data get storage mgs:temp _barrier_iter[0].radius
scoreboard players set @n[tag=mgs._barrier_new_d] mgs.zb.barrier.state 0
scoreboard players set @n[tag=mgs._barrier_new_d] mgs.zb.barrier.r_timer 0
scoreboard players set @n[tag=mgs._barrier_new_d] mgs.zb.barrier.rp_timer 0

# Remove temporary tag
tag @e[tag=mgs._barrier_new_d] remove mgs._barrier_new_d

# Continue iteration
data remove storage mgs:temp _barrier_iter[0]
execute if data storage mgs:temp _barrier_iter[0] run function mgs:v5.0.0/zombies/barriers/setup_iter

