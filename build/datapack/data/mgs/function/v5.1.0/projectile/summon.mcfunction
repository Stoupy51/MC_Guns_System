
#> mgs:v5.1.0/projectile/summon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/projectile/summon_loop
#

# Spread from the accuracy value.
function mgs:v5.1.0/raycast/accuracy/get_value

data modify storage mgs:temp proj set value {}
data modify storage mgs:temp proj.expl_damage set from storage mgs:gun all.stats.expl_damage
data modify storage mgs:temp proj.expl_decay set from storage mgs:gun all.stats.expl_decay
data modify storage mgs:temp proj.expl_radius set from storage mgs:gun all.stats.expl_radius
data modify storage mgs:temp proj.damage set from storage mgs:gun all.stats.damage
data modify storage mgs:temp proj.proj_gravity set from storage mgs:gun all.stats.proj_gravity
data modify storage mgs:temp proj.proj_speed set from storage mgs:gun all.stats.proj_speed
data modify storage mgs:temp proj.proj_lifetime set from storage mgs:gun all.stats.proj_lifetime
data modify storage mgs:temp proj.proj_model set from storage mgs:gun all.stats.proj_model
data modify storage mgs:temp proj.base_weapon set from storage mgs:gun all.stats.base_weapon
data modify storage mgs:temp proj.pap_level set from storage mgs:gun all.stats.pap_level

# At the muzzle, 0.69 ahead of the eyes, only when that spot is open, else at the eyes: flush against a wall the muzzle is inside it,
# and a projectile starting inside a block never registers an entry collision (bs.move sees it leave), so it went through thick walls.
execute anchored eyes positioned ^ ^ ^0.69 store success score #proj_muzzle_free mgs.data if block ~ ~ ~ #mgs:v5.1.0/projectile_pass_through
execute if score #proj_muzzle_free mgs.data matches 1 anchored eyes positioned ^ ^ ^0.69 summon item_display run function mgs:v5.1.0/projectile/init
execute if score #proj_muzzle_free mgs.data matches 0 anchored eyes positioned ^ ^ ^0 summon item_display run function mgs:v5.1.0/projectile/init

scoreboard players add #slow_bullet_count mgs.data 1

