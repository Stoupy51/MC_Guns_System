
#> mgs:v5.0.0/player/fire_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Shader: spawn muzzle flash marker (mode 1: red only)
# 1 block in front, scale 0.01 -> detected by core/particle.vsh -> flash.fsh
execute at @s anchored eyes run particle minecraft:dust{color:[0.011,0.0,0.0],scale:0.01} ^ ^ ^1 0 0 0 0 1 force @s

# For weapons with pellet count, set bullets_to_fire appropriately
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.0.0/projectile/summon_loop

# Shoot with hitscan raycast
function mgs:v5.0.0/player/shoot

