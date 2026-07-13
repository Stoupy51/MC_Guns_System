
#> mgs:v5.0.1/projectile/tick
#
# @executed	as @e[tag=mgs.slow_bullet] & at @s
#
# @within	mgs:v5.0.1/tick [ as @e[tag=mgs.slow_bullet] & at @s ]
#

# Apply gravity (subtract from Y velocity)
execute store result score #proj_gravity mgs.data run data get entity @s data.config.proj_gravity
scoreboard players operation @s bs.vel.y -= #proj_gravity mgs.data

# Move the projectile using Bookshelf's move module with collision detection
# (custom ignored_blocks so barrier blocks never stop projectiles)
function #bs.move:apply_vel {scale:0.001,with:{blocks:true,entities:true,ignored_blocks:"#mgs:v5.0.1/projectile_pass_through",on_collision:"function mgs:v5.0.1/projectile/on_collision"}}

# If collision was detected, explode and stop processing
execute at @s run function mgs:v5.0.1/projectile/post_vel

