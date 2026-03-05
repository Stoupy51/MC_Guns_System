
#> mgs:v5.0.0/projectile/post_vel
#
# @executed	at @s
#
# @within	mgs:v5.0.0/projectile/tick [ at @s ]
#

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

