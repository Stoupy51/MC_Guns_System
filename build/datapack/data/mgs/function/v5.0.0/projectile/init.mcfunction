
#> mgs:v5.0.0/projectile/init
#
# @executed	anchored eyes & positioned ^ ^ ^0.69
#
# @within	mgs:v5.0.0/projectile/summon [ anchored eyes & positioned ^ ^ ^0.69 ]
#

# Tag as slow bullet
tag @s add mgs.slow_bullet

# Store shooter UUID for damage attribution
data modify entity @s data.shooter set from entity @n[tag=mgs.ticking] UUID

# Copy explosion and projectile config from temp storage
data modify entity @s data.config set from storage mgs:temp proj

# Set the visual model on the item_display entity (ray_gun is invisible - no projectile model)
execute store success score #is_ray_gun mgs.data if data entity @s data.config{base_weapon:"ray_gun"}
execute if score #is_ray_gun mgs.data matches 0 run function mgs:v5.0.0/projectile/set_model with entity @s data.config

# Set lifetime score
execute store result score @s mgs.data run data get storage mgs:temp proj.proj_lifetime

# Calculate velocity from the player's look direction and teleport back
function mgs:v5.0.0/shared/calc_velocity

