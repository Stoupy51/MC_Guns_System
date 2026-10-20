
#> mgs:v5.2.0/player/fire_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/player/right_click
#

# Shader: muzzle flash, skipped for grenades. The post effect lights the scene from its viewer's camera,
# so only the shooter gets it; other players see a flash particle at the muzzle.
execute store success score #has_pap_level mgs.data if data storage mgs:gun all.stats.pap_level
execute if score #has_pap_level mgs.data matches 1 unless data storage mgs:gun all.stats.grenade_type run function mgs:v5.2.0/player/apply_pap_flash
execute if score #has_pap_level mgs.data matches 0 unless data storage mgs:gun all.stats.grenade_type run function mgs:v5.2.0/player/apply_flash
execute if score #has_pap_level mgs.data matches 1 unless data storage mgs:gun all.stats.grenade_type at @s anchored eyes run particle flash{color:[0.6, 0.0, 1.0, 0.15]} ^-0.35 ^-0.3 ^1 0 0 0 0 1 force @a[distance=0.01..48]
execute if score #has_pap_level mgs.data matches 0 unless data storage mgs:gun all.stats.grenade_type at @s anchored eyes run particle flash{color:[1.0, 0.8, 0.5, 1.0]} ^-0.35 ^-0.3 ^1 0 0 0 0 1 force @a[distance=0.01..48]

execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# Only the first 3 entities hit by a shot (all pellets) bleed, against lag when piercing a horde.
scoreboard players set #hit_particles_left mgs.data 3

execute if data storage mgs:gun all.stats.grenade_type run return run function mgs:v5.2.0/grenade/throw

# Weapons with projectile config fire slow projectiles instead of a raycast.
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.2.0/projectile/summon_loop

function mgs:v5.2.0/player/shoot

