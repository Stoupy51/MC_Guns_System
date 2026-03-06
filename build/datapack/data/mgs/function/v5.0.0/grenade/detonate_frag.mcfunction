
#> mgs:v5.0.0/grenade/detonate_frag
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/detonate
#

# Explosion particles
particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 100 force @a[distance=..128]
particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

# Explosion sound
playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# Block destruction via RealisticExplosionLibrary (if grenade_explosion_power > 0)
execute if score #grenade_explosion_power mgs.config matches 1.. run function mgs:v5.0.0/grenade/realistic_explosion

# Store explosion center position for damage calculation (scores used by projectile/damage_entity)
execute store result score #ctr_x mgs.data run data get entity @s Pos[0] 1000
execute store result score #ctr_y mgs.data run data get entity @s Pos[1] 1000
execute store result score #ctr_z mgs.data run data get entity @s Pos[2] 1000

# Copy explosion config from entity data to temp storage
data modify storage mgs:temp expl.expl_damage set from entity @s data.config.expl_damage
data modify storage mgs:temp expl.expl_decay set from entity @s data.config.expl_decay
data modify storage mgs:temp expl.expl_radius set from entity @s data.config.expl_radius

# Resolve shooter: copy UUID to storage, then find matching player
data modify storage mgs:temp expl.shooter_uuid set from entity @s data.shooter

# Tag the matching shooter for damage attribution
scoreboard players set #found mgs.data 0
execute as @a run function mgs:v5.0.0/projectile/match_shooter
execute if score #found mgs.data matches 0 as @e[tag=mgs.armed] run function mgs:v5.0.0/projectile/match_shooter

# Apply area damage to nearby entities (macro for configurable radius)
execute store result storage mgs:temp expl.radius_float float 1 run data get entity @s data.config.expl_radius
function mgs:v5.0.0/projectile/damage_area with storage mgs:temp expl

# Signal: on_explosion
data modify storage mgs:signals on_explosion set value {}
data modify storage mgs:signals on_explosion.config set from entity @s data.config
data modify storage mgs:signals on_explosion.position set from entity @s Pos
data modify storage mgs:signals on_explosion.grenade set value true
function #mgs:signals/on_explosion

# Clean up shooter tag
tag @e[tag=mgs.temp_shooter] remove mgs.temp_shooter

# Delete the grenade
function mgs:v5.0.0/grenade/delete

