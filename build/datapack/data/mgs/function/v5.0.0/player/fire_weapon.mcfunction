
#> mgs:v5.0.0/player/fire_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Shader: spawn muzzle flash marker (mode 1)
# entity_effect: R=254/255, G=1/255, B=0, A=1 → detected by particle.vsh → placed at pixel (0,0)
execute at @s anchored eyes run particle minecraft:entity_effect{color:[0.99607843,0.00392157,0.0,1.0],scale:1f} ^ ^ ^1 0 0 0 0 1 force @s

# For weapons with pellet count, set bullets_to_fire appropriately
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.0.0/projectile/summon_loop

# Shoot with hitscan raycast
function mgs:v5.0.0/player/shoot

