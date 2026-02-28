
#> mgs:v5.0.0/projectile/tick
#
# @executed	as @e[tag=mgs.slow_bullet] & at @s
#
# @within	mgs:v5.0.0/tick [ as @e[tag=mgs.slow_bullet] & at @s ]
#

# Apply gravity (subtract from Y velocity)
execute store result score #proj_gravity mgs.data run data get entity @s data.config.proj_gravity
scoreboard players operation @s bs.vel.y -= #proj_gravity mgs.data

# Move the projectile using Bookshelf's move module with collision detection
function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:true,on_collision:"function mgs:v5.0.0/projectile/on_collision"}}

# If collision was detected, explode and stop processing
execute if entity @s[tag=mgs.exploding] run return run function mgs:v5.0.0/projectile/explode

# Trail particles: flame + smoke
particle flame ~ ~ ~ 0.05 0.05 0.05 0.02 3 force @a[distance=..128]
particle smoke ~ ~ ~ 0.1 0.1 0.1 0.01 2 force @a[distance=..128]

# Decrement lifetime
scoreboard players remove @s mgs.data 1

# If lifetime expired, explode
execute if score @s mgs.data matches ..0 run function mgs:v5.0.0/projectile/explode

