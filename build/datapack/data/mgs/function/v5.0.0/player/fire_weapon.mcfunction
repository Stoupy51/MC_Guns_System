
#> mgs:v5.0.0/player/fire_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# For weapons with pellet count, set bullets_to_fire appropriately
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.0.0/projectile/summon_loop

# Shoot with hitscan raycast
function mgs:v5.0.0/player/shoot

