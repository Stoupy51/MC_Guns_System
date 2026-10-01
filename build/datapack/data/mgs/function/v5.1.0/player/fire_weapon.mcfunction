
#> mgs:v5.1.0/player/fire_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/right_click
#

# Shader: muzzle flash for everyone who can see the shooter - skip for grenades
execute store success score #has_pap_level mgs.data if data storage mgs:gun all.stats.pap_level
execute if score #has_pap_level mgs.data matches 1 unless data storage mgs:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function mgs:v5.1.0/player/apply_pap_flash_if_can_see
execute if score #has_pap_level mgs.data matches 0 unless data storage mgs:gun all.stats.grenade_type at @s anchored eyes positioned ^ ^ ^0.001 as @a[distance=..16] run function mgs:v5.1.0/player/apply_flash_if_can_see

execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# Only the first 3 entities hit by a shot (all pellets) bleed, against lag when piercing a horde.
scoreboard players set #hit_particles_left mgs.data 3

execute if data storage mgs:gun all.stats.grenade_type run return run function mgs:v5.1.0/grenade/throw

# Weapons with projectile config fire slow projectiles instead of a raycast.
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.1.0/projectile/summon_loop

function mgs:v5.1.0/player/shoot

