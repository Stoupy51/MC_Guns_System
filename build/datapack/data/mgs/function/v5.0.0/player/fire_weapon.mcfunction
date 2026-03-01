
#> mgs:v5.0.0/player/fire_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Shader: spawn muzzle flash marker (mode 1)
# R=254.5/255, G=1.5/255, B=0 → particle.vsh places at pixel (0,0)
# Flash auto-expires via alpha decay check in vsh (~2-5 ticks)
execute at @s anchored eyes run particle minecraft:entity_effect{color:[0.99803922,0.00588235,0.0,1.0]} ^ ^ ^1 0 0 0 0 1 force @s

# For weapons with pellet count, set bullets_to_fire appropriately
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.0.0/projectile/summon_loop

# Shoot with hitscan raycast
function mgs:v5.0.0/player/shoot

