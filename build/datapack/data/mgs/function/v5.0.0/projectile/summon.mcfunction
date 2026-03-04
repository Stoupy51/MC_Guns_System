
#> mgs:v5.0.0/projectile/summon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/projectile/summon_loop
#

# Get accuracy value and apply spread
function mgs:v5.0.0/raycast/accuracy/get_value

# Prepare projectile data in storage before summoning
data modify storage mgs:temp proj set value {}
data modify storage mgs:temp proj.expl_damage set from storage mgs:gun all.stats.expl_damage
data modify storage mgs:temp proj.expl_decay set from storage mgs:gun all.stats.expl_decay
data modify storage mgs:temp proj.expl_radius set from storage mgs:gun all.stats.expl_radius
data modify storage mgs:temp proj.proj_gravity set from storage mgs:gun all.stats.proj_gravity
data modify storage mgs:temp proj.proj_speed set from storage mgs:gun all.stats.proj_speed
data modify storage mgs:temp proj.proj_lifetime set from storage mgs:gun all.stats.proj_lifetime
data modify storage mgs:temp proj.proj_model set from storage mgs:gun all.stats.proj_model
data modify storage mgs:temp proj.base_weapon set from storage mgs:gun all.stats.base_weapon

# Summon the projectile entity at the player's eye position
execute anchored eyes positioned ^ ^ ^0.5 summon item_display run function mgs:v5.0.0/projectile/init

# Increment slow bullet counter
scoreboard players add #slow_bullet_count mgs.data 1

