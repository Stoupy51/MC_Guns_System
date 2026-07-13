
#> mgs:v5.0.1/player/fire_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/right_click
#

# Shader: spawn muzzle flash marker - skip for grenades
# PaP guns use mode 10 (purple dust G=1.0 → ic.g ≥ 81), normal guns use mode 1 (dust G=0)
execute store success score #has_pap_level mgs.data if data storage mgs:gun all.stats.pap_level
execute if score #has_pap_level mgs.data matches 1 unless data storage mgs:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function mgs:v5.0.1/player/apply_pap_flash_if_can_see
execute if score #has_pap_level mgs.data matches 0 unless data storage mgs:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function mgs:v5.0.1/player/apply_flash_if_can_see

# For weapons with pellet count, set bullets_to_fire appropriately
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# Per-shot budget for entity hit particles: only the first 3 entities hit by this shot
# (all pellets included) emit blood particles, to avoid lag when piercing a whole horde
scoreboard players set #hit_particles_left mgs.data 3

# If weapon is a grenade, throw it instead
execute if data storage mgs:gun all.stats.grenade_type run return run function mgs:v5.0.1/grenade/throw

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.0.1/projectile/summon_loop

# Shoot with hitscan raycast
function mgs:v5.0.1/player/shoot

