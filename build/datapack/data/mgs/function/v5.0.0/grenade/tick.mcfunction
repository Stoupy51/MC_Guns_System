
#> mgs:v5.0.0/grenade/tick
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/tick [ as @e[tag=mgs.grenade] & at @s ]
#

# Skip if grenade is stuck (semtex on a surface) or in smoke/flash effect phase
execute if entity @s[tag=mgs.grenade_stuck] run return run function mgs:v5.0.0/grenade/tick_stuck
execute if entity @s[tag=mgs.grenade_active_effect] run return run function mgs:v5.0.0/grenade/tick_effect

# Apply gravity (subtract from Y velocity)
execute store result score #proj_gravity mgs.data run data get entity @s data.config.proj_gravity
scoreboard players operation @s bs.vel.y -= #proj_gravity mgs.data

# Move the grenade using Bookshelf's move module with collision detection
# Grenades use damped_bounce by default (frag/smoke/flash) or stick (semtex)
execute if data entity @s data.config{grenade_type:"semtex"} run return run function mgs:v5.0.0/grenade/move_semtex
function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:false,on_collision:"function mgs:v5.0.0/grenade/on_bounce"}}

# Trail particle (white_smoke avoids false-positive with shader marker detection)
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Decrement fuse timer
scoreboard players remove @s mgs.data 1

# If fuse expired, detonate
execute if score @s mgs.data matches ..0 run function mgs:v5.0.0/grenade/detonate

