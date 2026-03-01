
#> mgs:v5.0.0/tick
#
# @within	mgs:v5.0.0/load/tick_verification
#

# Player loop
execute as @e[type=player,sort=random] at @s run function mgs:v5.0.0/player/tick

# Tick function for slow bullets (projectiles)
execute if score #slow_bullet_count mgs.data matches 1.. as @e[tag=mgs.slow_bullet] at @s run function mgs:v5.0.0/projectile/tick

