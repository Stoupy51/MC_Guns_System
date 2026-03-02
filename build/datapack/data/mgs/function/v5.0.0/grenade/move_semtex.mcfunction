
#> mgs:v5.0.0/grenade/move_semtex
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/tick
#

# Apply gravity
execute store result score #proj_gravity mgs.data run data get entity @s data.config.proj_gravity
scoreboard players operation @s bs.vel.y -= #proj_gravity mgs.data

# Move with stick callback (semtex sticks to first surface or entity hit)
# During launch grace period, skip entity collision to avoid sticking to the thrower
scoreboard players remove @s mgs.grenade_launch 1
execute if score @s mgs.grenade_launch matches 0.. run function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:false,on_collision:"function mgs:v5.0.0/grenade/on_stick"}}
execute unless score @s mgs.grenade_launch matches 0.. run function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:true,on_collision:"function mgs:v5.0.0/grenade/on_stick"}}

# Trail particle (white_smoke avoids false-positive with shader marker detection)
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Decrement fuse timer
scoreboard players remove @s mgs.data 1

# If fuse expired, detonate
execute if score @s mgs.data matches ..0 run function mgs:v5.0.0/grenade/detonate

