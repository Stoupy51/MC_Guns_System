
#> mgs:v5.0.0/grenade/init
#
# @executed	anchored eyes & positioned ^ ^ ^0.5
#
# @within	mgs:v5.0.0/grenade/summon [ anchored eyes & positioned ^ ^ ^0.5 ]
#

# Tag as grenade
tag @s add mgs.grenade

# Store shooter UUID for damage attribution
data modify entity @s data.shooter set from entity @n[tag=mgs.ticking] UUID

# Copy grenade config from temp storage
data modify entity @s data.config set from storage mgs:temp grenade

# Set the visual model on the item_display entity
function mgs:v5.0.0/grenade/set_model with entity @s data.config

# Set fuse timer from config
execute store result score @s mgs.data run data get entity @s data.config.grenade_fuse

# Launch grace period: disable entity collision for 3 ticks to avoid sticking to the thrower
scoreboard players set @s mgs.grenade_launch 3

# Calculate velocity from the player's look direction
# Step 1: Record current position
execute store result score #proj_ox mgs.data run data get entity @s Pos[0] 1000
execute store result score #proj_oy mgs.data run data get entity @s Pos[1] 1000
execute store result score #proj_oz mgs.data run data get entity @s Pos[2] 1000

# Step 2: Apply accuracy spread to the grenade's rotation
tp @s ~ ~ ~ ~ ~
function mgs:v5.0.0/raycast/accuracy/apply_spread

# Step 3: Get direction vector by teleporting from origin (avoids subtraction)
execute positioned 0.0 0.0 0.0 positioned ^ ^ ^1 run tp @s ~ ~ ~

# Step 4: Read direction directly as velocity components (thousandths of a block)
execute store result score #proj_vx mgs.data run data get entity @s Pos[0] 1000
execute store result score #proj_vy mgs.data run data get entity @s Pos[1] 1000
execute store result score #proj_vz mgs.data run data get entity @s Pos[2] 1000

# Step 5: Multiply direction by speed / 1000 to get velocity
execute store result score #proj_speed mgs.data run data get entity @s data.config.proj_speed
scoreboard players operation #proj_vx mgs.data *= #proj_speed mgs.data
scoreboard players operation #proj_vy mgs.data *= #proj_speed mgs.data
scoreboard players operation #proj_vz mgs.data *= #proj_speed mgs.data
scoreboard players operation #proj_vx mgs.data /= #1000 mgs.data
scoreboard players operation #proj_vy mgs.data /= #1000 mgs.data
scoreboard players operation #proj_vz mgs.data /= #1000 mgs.data

# Step 6: Store velocity into bs.vel scores for bs.move module
scoreboard players operation @s bs.vel.x = #proj_vx mgs.data
scoreboard players operation @s bs.vel.y = #proj_vy mgs.data
scoreboard players operation @s bs.vel.z = #proj_vz mgs.data

# Step 7: Teleport back to original position
execute store result storage mgs:temp grenade_pos.x double 0.001 run scoreboard players get #proj_ox mgs.data
execute store result storage mgs:temp grenade_pos.y double 0.001 run scoreboard players get #proj_oy mgs.data
execute store result storage mgs:temp grenade_pos.z double 0.001 run scoreboard players get #proj_oz mgs.data
function mgs:v5.0.0/grenade/tp_back with storage mgs:temp grenade_pos

