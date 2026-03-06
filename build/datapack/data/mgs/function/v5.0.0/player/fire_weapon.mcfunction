
#> mgs:v5.0.0/player/fire_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/right_click
#

# Shader: spawn muzzle flash marker (mode 1) - skip for grenades
# dust R=0.02, G=0, B=0 → particle.vsh detects and places at pixel (0,0)
# scale 0.01 → lifetime 0 (1 game tick) → flash auto-expires immediately
execute unless data storage mgs:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function mgs:v5.0.0/player/apply_flash_if_can_see

# For weapons with pellet count, set bullets_to_fire appropriately
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# If weapon is a grenade, throw it instead
execute if data storage mgs:gun all.stats.grenade_type run return run function mgs:v5.0.0/grenade/throw

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.0.0/projectile/summon_loop

# Shoot with hitscan raycast
function mgs:v5.0.0/player/shoot

