
#> mgs:v5.0.1/grenade/tick
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.1/tick [ as @e[tag=mgs.grenade] & at @s ]
#

# Skip if grenade is stuck (semtex on a surface) or in smoke/flash effect phase
execute if entity @s[tag=mgs.grenade_stuck] run return run function mgs:v5.0.1/grenade/tick_stuck
execute if entity @s[tag=mgs.grenade_active_effect] run return run function mgs:v5.0.1/grenade/tick_effect

# Tumble proportionally to current speed: fast while flying, stops as the grenade comes to rest
# #gr_speed = |vx| + |vy| + |vz| (thousandths of a block per tick)
scoreboard players operation #gr_speed mgs.data = @s bs.vel.x
execute if score #gr_speed mgs.data matches ..-1 run scoreboard players operation #gr_speed mgs.data *= #minus_one mgs.data
scoreboard players operation #gr_sv mgs.data = @s bs.vel.y
execute if score #gr_sv mgs.data matches ..-1 run scoreboard players operation #gr_sv mgs.data *= #minus_one mgs.data
scoreboard players operation #gr_speed mgs.data += #gr_sv mgs.data
scoreboard players operation #gr_sv mgs.data = @s bs.vel.z
execute if score #gr_sv mgs.data matches ..-1 run scoreboard players operation #gr_sv mgs.data *= #minus_one mgs.data
scoreboard players operation #gr_speed mgs.data += #gr_sv mgs.data

# Angle step ≈ 0.44 rad per (block/tick) of speed, in 1e-4 rad units; skip the update when resting
scoreboard players operation #gr_speed mgs.data *= #44 mgs.data
scoreboard players operation #gr_speed mgs.data /= #10 mgs.data
execute if score #gr_speed mgs.data matches 1.. run function mgs:v5.0.1/grenade/spin_tick

# Apply gravity (subtract from Y velocity)
execute store result score #proj_gravity mgs.data run data get entity @s data.config.proj_gravity
scoreboard players operation @s bs.vel.y -= #proj_gravity mgs.data

# Move the grenade using Bookshelf's move module with collision detection
# Grenades use damped_bounce by default (frag/smoke/flash) or stick (semtex)
execute if data entity @s data.config{grenade_type:"semtex"} run return run function mgs:v5.0.1/grenade/move_semtex
function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:false,ignored_blocks:"#mgs:v5.0.1/projectile_pass_through",on_collision:"function mgs:v5.0.1/grenade/on_bounce"}}

# Trail particle (white_smoke avoids false-positive with shader marker detection)
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Decrement fuse timer
scoreboard players remove @s mgs.data 1

# If fuse expired, detonate
execute if score @s mgs.data matches ..0 run function mgs:v5.0.1/grenade/detonate

