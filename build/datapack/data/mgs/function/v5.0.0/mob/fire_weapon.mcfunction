
#> mgs:v5.0.0/mob/fire_weapon
#
# @executed	anchored eyes & facing entity @n[tag=mgs.target] feet
#
# @within	mgs:v5.0.0/mob/tick [ anchored eyes & facing entity @n[tag=mgs.target] feet ]
#

# Rotate to face the target eyes
rotate @s facing entity @n[tag=mgs.target] eyes

# Apply random inaccuracy (skip for level 5 mobs with perfect aim)
execute unless entity @s[tag=mgs.mob_lv5] run function mgs:v5.0.0/mob/apply_inaccuracy

# Set cooldown from weapon stats
execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.cooldown

# For weapons with pellet count, set bullets_to_fire appropriately
scoreboard players set #bullets_to_fire mgs.data 1
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count

# If weapon is a grenade, throw it instead
execute if data storage mgs:gun all.stats.grenade_type run return run function mgs:v5.0.0/grenade/throw

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage mgs:gun all.stats.proj_speed run return run function mgs:v5.0.0/projectile/summon_loop

# Shoot with hitscan raycast
function mgs:v5.0.0/mob/shoot

# Play fire sound to nearby players
execute if data storage mgs:gun all.sounds.fire run function mgs:v5.0.0/mob/fire_sound with storage mgs:gun all.sounds

# Signal: on_shoot (weapon data available in mgs:signals)
data modify storage mgs:signals on_shoot set value {}
data modify storage mgs:signals on_shoot.weapon set from storage mgs:gun all
function #mgs:signals/on_shoot

