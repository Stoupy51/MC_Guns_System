
#> mgs:v5.1.0/mob/fire_weapon
#
# @executed	anchored eyes & facing entity @e[tag=mgs.target,limit=1] feet
#
# @within	mgs:v5.1.0/mob/tick [ anchored eyes & facing entity @e[tag=mgs.target,limit=1] feet ]
#

rotate @s facing entity @n[tag=mgs.target] eyes

# Level 5 mobs have perfect aim.
execute unless entity @s[tag=mgs.mob_lv5] run function mgs:v5.1.0/mob/apply_inaccuracy

execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.cooldown

scoreboard players set #bullets_to_fire mgs.data 1
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

execute if data storage mgs:gun all.stats.grenade_type run return run function mgs:v5.1.0/grenade/throw

# Weapons with projectile config fire slow projectiles instead of a raycast.
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.1.0/projectile/summon_loop

function mgs:v5.1.0/mob/shoot

execute if data storage mgs:gun all.sounds.fire run function mgs:v5.1.0/mob/fire_sound with storage mgs:gun all.sounds

# Weapon data in mgs:signals.
data modify storage mgs:signals on_shoot set value {}
data modify storage mgs:signals on_shoot.weapon set from storage mgs:gun all
function #mgs:signals/on_shoot

