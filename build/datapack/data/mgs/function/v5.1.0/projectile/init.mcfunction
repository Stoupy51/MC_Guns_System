
#> mgs:v5.1.0/projectile/init
#
# @executed	anchored eyes & positioned ^ ^ ^0.69
#
# @within	mgs:v5.1.0/projectile/summon [ anchored eyes & positioned ^ ^ ^0.69 ]
#			mgs:v5.1.0/projectile/summon [ anchored eyes & positioned ^ ^ ^0 ]
#

tag @s add mgs.slow_bullet

# For damage attribution.
data modify entity @s data.shooter set from entity @n[tag=mgs.ticking] UUID

data modify entity @s data.config set from storage mgs:temp proj

# The Ray Gun has no projectile model.
execute store success score #is_ray_gun mgs.data if data entity @s data.config{base_weapon:"ray_gun"}
execute if score #is_ray_gun mgs.data matches 0 run function mgs:v5.1.0/projectile/set_model with entity @s data.config

execute store result score @s mgs.data run data get storage mgs:temp proj.proj_lifetime

# From the look direction, then back.
function mgs:v5.1.0/shared/calc_velocity

