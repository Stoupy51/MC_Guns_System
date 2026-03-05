
#> mgs:v5.0.0/projectile/init
#
# @executed	anchored eyes & positioned ^ ^ ^0.69
#
# @within	mgs:v5.0.0/projectile/summon [ anchored eyes & positioned ^ ^ ^0.69 ]
#

# Tag as slow bullet
tag @s add mgs.slow_bullet

# Store shooter UUID for damage attribution
data modify entity @s data.shooter set from entity @n[tag=mgs.ticking] UUID

# Copy explosion and projectile config from temp storage
data modify entity @s data.config set from storage mgs:temp proj

# Set the visual model on the item_display entity (ray_gun is invisible - no projectile model)
execute store success score #is_ray_gun mgs.data if data entity @s data.config{base_weapon:"ray_gun"}
execute if score #is_ray_gun mgs.data matches 0 run function mgs:v5.0.0/projectile/set_model with entity @s data.config

# Set lifetime score
execute store result score @s mgs.data run data get storage mgs:temp proj.proj_lifetime

# Calculate velocity from the player's look direction
# Step 1: Record current position for teleporting back later
execute store result score #proj_ox mgs.data run data get entity @s Pos[0] 1000
execute store result score #proj_oy mgs.data run data get entity @s Pos[1] 1000
execute store result score #proj_oz mgs.data run data get entity @s Pos[2] 1000

# Step 2: Apply accuracy spread to the marker's rotation
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
execute store result storage mgs:temp proj_pos.x double 0.001 run scoreboard players get #proj_ox mgs.data
execute store result storage mgs:temp proj_pos.y double 0.001 run scoreboard players get #proj_oy mgs.data
execute store result storage mgs:temp proj_pos.z double 0.001 run scoreboard players get #proj_oz mgs.data
function mgs:v5.0.0/projectile/tp_back with storage mgs:temp proj_pos

