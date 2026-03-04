
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

# Trail particles: ray_gun = green dust swirl, others = flame + smoke
execute store success score #is_ray_gun mgs.data if data entity @s data.config{base_weapon:"ray_gun"}
execute if score #is_ray_gun mgs.data matches 1 run particle dust{color:[0.0,0.8,0.0],scale:1.5} ~ ~ ~ 0.1 0.1 0.1 0 8 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 1 run particle glow ~ ~ ~ 0.1 0.1 0.1 0 3 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 0 run particle flame ~ ~ ~ 0.05 0.05 0.05 0.02 3 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 0 run particle smoke ~ ~ ~ 0.1 0.1 0.1 0.01 2 force @a[distance=..128]

# Decrement lifetime
scoreboard players remove @s mgs.data 1

# If lifetime expired, explode
execute if score @s mgs.data matches ..0 run function mgs:v5.0.0/projectile/explode

