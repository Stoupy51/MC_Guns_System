
#> mgs:v5.0.0/projectile/explode
#
# @executed	as @e[tag=mgs.slow_bullet] & at @s
#
# @within	mgs:v5.0.0/projectile/tick
#

# Explosion particles - ray_gun: green energy burst (no smoke)
execute store success score #is_ray_gun mgs.data if data entity @s data.config{base_weapon:"ray_gun"}
execute if score #is_ray_gun mgs.data matches 1 run particle flash{color:[0.0,0.8,0.0,1.0]} ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 1 run particle dust{color:[0.0,0.8,0.0],scale:1.5} ~ ~ ~ 0.5 0.5 0.5 0 200 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 1 run particle glow ~ ~ ~ 0.5 0.5 0.5 0.1 80 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 1 run particle electric_spark ~ ~ ~ 0.5 0.5 0.5 0.05 100 force @a[distance=..128]
# Explosion particles - standard weapons: fire + smoke
execute if score #is_ray_gun mgs.data matches 0 run particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 0 run particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 0 run particle large_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 50 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 0 run particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
execute if score #is_ray_gun mgs.data matches 0 run particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

# Explosion sound - ray_gun is silent (no explosion sound)
execute if score #is_ray_gun mgs.data matches 0 run playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# Block destruction via RealisticExplosionLibrary (if RPG_EXPLOSION_POWER > 0)
execute if score #rpg_explosion_power mgs.config matches 1.. run function mgs:v5.0.0/projectile/realistic_explosion

# Store explosion center position for damage calculation
execute store result storage mgs:temp expl.center_x int 1 run data get entity @s Pos[0] 1000
execute store result storage mgs:temp expl.center_y int 1 run data get entity @s Pos[1] 1000
execute store result storage mgs:temp expl.center_z int 1 run data get entity @s Pos[2] 1000

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
execute store result storage mgs:temp expl.radius_int int 1 run data get entity @s data.config.expl_radius
function mgs:v5.0.0/projectile/damage_area with storage mgs:temp expl

# Signal: on_explosion (@s = projectile entity, explosion data in mgs:signals)
data modify storage mgs:signals on_explosion set value {}
data modify storage mgs:signals on_explosion.config set from entity @s data.config
data modify storage mgs:signals on_explosion.position set from entity @s Pos
function #mgs:signals/on_explosion

# Clean up shooter tag
tag @e[tag=mgs.temp_shooter] remove mgs.temp_shooter

# Delete the projectile
function mgs:v5.0.0/projectile/delete

