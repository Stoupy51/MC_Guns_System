
#> mgs:v5.0.1/projectile/explode
#
# @executed	at @s
#
# @within	mgs:v5.0.1/projectile/post_vel
#

# Explosion particles
scoreboard players set #ray_gun mgs.data 0
execute if data entity @s data.config{base_weapon:"ray_gun"} run scoreboard players set #ray_gun mgs.data 1
execute if score #ray_gun mgs.data matches 1 if data entity @s data.config.pap_level run scoreboard players set #ray_gun mgs.data 2
## Upgraded ray_gun explosion: red energy burst
execute if score #ray_gun mgs.data matches 2 run particle flash{color:[0.8,0.0,0.0,1.0]} ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 2 run particle dust_color_transition{from_color:[1.0,0.0,0.0],to_color:[0.3,0.0,0.0],scale:1.8} ~ ~ ~ 0.6 0.6 0.6 0 200 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 2 run particle crimson_spore ~ ~ ~ 0.5 0.5 0.5 0.05 100 force @a[distance=..128]
## Normal ray_gun: green energy burst
execute if score #ray_gun mgs.data matches 1 run particle flash{color:[0.0,0.8,0.0,1.0]} ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 1 run particle dust{color:[0.0,0.8,0.0],scale:1.5} ~ ~ ~ 0.5 0.5 0.5 0 200 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 1 run particle glow ~ ~ ~ 0.5 0.5 0.5 0.1 80 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 1 run particle electric_spark ~ ~ ~ 0.5 0.5 0.5 0.05 100 force @a[distance=..128]
## Explosion particles - standard weapons: fire + smoke
execute if score #ray_gun mgs.data matches 0 run particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 0 run particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 0 run particle large_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 50 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 0 run particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
execute if score #ray_gun mgs.data matches 0 run particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

# Explosion sound - ray_gun is silent (no explosion sound)
execute if score #ray_gun mgs.data matches 0 run playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# Block destruction via RealisticExplosionLibrary (if RPG_EXPLOSION_POWER > 0)
execute if score #projectile_explosion_power mgs.config matches 1.. run function mgs:v5.0.1/projectile/realistic_explosion

# Store explosion center position for damage calculation
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
execute as @a run function mgs:v5.0.1/projectile/match_shooter
execute if score #found mgs.data matches 0 as @e[tag=mgs.armed] run function mgs:v5.0.1/projectile/match_shooter

# Apply bullet direct-hit damage to the entity tagged in on_collision (if entity was hit, not just a block)
# Give shooter ticking tag so DPS signal can find them
tag @n[tag=mgs.temp_shooter] add mgs.ticking

# Get direct-hit damage amount (with 1 decimal)
execute store result score #direct_dmg mgs.data run data get entity @s data.config.damage 10

# If zombie game is active: multiply by 5 for zombies, cap for players (15 hp)
execute if data storage mgs:zombies game{state:"active"} if entity @n[tag=mgs.direct_hit,type=!player] run scoreboard players operation #direct_dmg mgs.data *= #5 mgs.data
execute if data storage mgs:zombies game{state:"active"} if entity @n[tag=mgs.direct_hit,type=player] if score #direct_dmg mgs.data matches 150.. run scoreboard players set #direct_dmg mgs.data 150

# Apply direct hit damage using the existing damage utility
data modify storage mgs:input with set value {target:"@s", amount:0.0f, attacker:"@n[tag=mgs.temp_shooter]"}
execute store result storage mgs:input with.amount float 0.1 run scoreboard players get #direct_dmg mgs.data
data modify storage mgs:input with.weapon set from storage mgs:gun all
execute as @n[tag=mgs.direct_hit,tag=!mgs.temp_shooter] run function mgs:v5.0.1/utils/signal_and_damage
tag @e[tag=mgs.direct_hit] remove mgs.direct_hit
tag @n[tag=mgs.temp_shooter] remove mgs.ticking

# Apply area damage to nearby entities (macro for configurable radius)
execute store result storage mgs:temp expl.radius_float float 1 run data get entity @s data.config.expl_radius
function mgs:v5.0.1/projectile/damage_area with storage mgs:temp expl

# Signal: on_explosion (@s = projectile entity, explosion data in mgs:signals)
data modify storage mgs:signals on_explosion set value {}
data modify storage mgs:signals on_explosion.config set from entity @s data.config
data modify storage mgs:signals on_explosion.position set from entity @s Pos
function #mgs:signals/on_explosion

# Clean up shooter tag
tag @e[tag=mgs.temp_shooter] remove mgs.temp_shooter

# Delete the projectile
function mgs:v5.0.1/projectile/delete

