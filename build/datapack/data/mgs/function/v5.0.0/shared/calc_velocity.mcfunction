
#> mgs:v5.0.0/shared/calc_velocity
#
# @executed	anchored eyes & positioned ^ ^ ^0.69
#
# @within	mgs:v5.0.0/projectile/init
#			mgs:v5.0.0/grenade/init
#

# Record current position for teleporting back later
execute store result score #proj_ox mgs.data run data get entity @s Pos[0] 1000
execute store result score #proj_oy mgs.data run data get entity @s Pos[1] 1000
execute store result score #proj_oz mgs.data run data get entity @s Pos[2] 1000

# Apply accuracy spread to the rotation
tp @s ~ ~ ~ ~ ~
function mgs:v5.0.0/raycast/accuracy/apply_spread

# Get direction vector by teleporting from origin
execute positioned 0.0 0.0 0.0 positioned ^ ^ ^1 run tp @s ~ ~ ~

# Read direction as velocity components (thousandths of a block)
execute store result score @s bs.vel.x run data get entity @s Pos[0] 1000
execute store result score @s bs.vel.y run data get entity @s Pos[1] 1000
execute store result score @s bs.vel.z run data get entity @s Pos[2] 1000

# Multiply direction by speed / 1000 to get velocity
execute store result score #proj_speed mgs.data run data get entity @s data.config.proj_speed
scoreboard players operation @s bs.vel.x *= #proj_speed mgs.data
scoreboard players operation @s bs.vel.y *= #proj_speed mgs.data
scoreboard players operation @s bs.vel.z *= #proj_speed mgs.data
scoreboard players operation @s bs.vel.x /= #1000 mgs.data
scoreboard players operation @s bs.vel.y /= #1000 mgs.data
scoreboard players operation @s bs.vel.z /= #1000 mgs.data

# Teleport back to original position
execute store result storage mgs:temp _tp_pos.x double 0.001 run scoreboard players get #proj_ox mgs.data
execute store result storage mgs:temp _tp_pos.y double 0.001 run scoreboard players get #proj_oy mgs.data
execute store result storage mgs:temp _tp_pos.z double 0.001 run scoreboard players get #proj_oz mgs.data
function mgs:v5.0.0/shared/tp_back with storage mgs:temp _tp_pos

