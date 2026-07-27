""" The explosion: particles, block damage and finding the shooter to credit. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import BASE_WEAPON, DAMAGE, EXPLOSION_DAMAGE, EXPLOSION_DECAY, EXPLOSION_RADIUS


# Functions
def write_projectile_explosion() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Explosion effect
	write_versioned_function("projectile/explode", f"""
# Explosion particles
scoreboard players set #ray_gun {ns}.data 0
execute if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}} run scoreboard players set #ray_gun {ns}.data 1
execute if score #ray_gun {ns}.data matches 1 if data entity @s data.config.pap_level run scoreboard players set #ray_gun {ns}.data 2
## Upgraded ray_gun explosion: red energy burst
execute if score #ray_gun {ns}.data matches 2 run particle flash{{color:[0.8,0.0,0.0,1.0]}} ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 2 run particle dust_color_transition{{from_color:[1.0,0.0,0.0],to_color:[0.3,0.0,0.0],scale:1.8}} ~ ~ ~ 0.6 0.6 0.6 0 200 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 2 run particle crimson_spore ~ ~ ~ 0.5 0.5 0.5 0.05 100 force @a[distance=..128]
## Normal ray_gun: green energy burst
execute if score #ray_gun {ns}.data matches 1 run particle flash{{color:[0.0,0.8,0.0,1.0]}} ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle dust{{color:[0.0,0.8,0.0],scale:1.5}} ~ ~ ~ 0.5 0.5 0.5 0 200 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle glow ~ ~ ~ 0.5 0.5 0.5 0.1 80 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle electric_spark ~ ~ ~ 0.5 0.5 0.5 0.05 100 force @a[distance=..128]
## Explosion particles - standard weapons: fire + smoke
execute if score #ray_gun {ns}.data matches 0 run particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle large_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 50 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

# Explosion sound - ray_gun is silent (no explosion sound)
execute if score #ray_gun {ns}.data matches 0 run playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# Block destruction via RealisticExplosionLibrary (if RPG_EXPLOSION_POWER > 0)
execute if score #projectile_explosion_power {ns}.config matches 1.. run function {ns}:v{version}/projectile/realistic_explosion

# Store explosion center position for damage calculation
execute store result score #ctr_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #ctr_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #ctr_z {ns}.data run data get entity @s Pos[2] 1000

# Copy explosion config from entity data to temp storage
data modify storage {ns}:temp expl.{EXPLOSION_DAMAGE} set from entity @s data.config.{EXPLOSION_DAMAGE}
data modify storage {ns}:temp expl.{EXPLOSION_DECAY} set from entity @s data.config.{EXPLOSION_DECAY}
data modify storage {ns}:temp expl.{EXPLOSION_RADIUS} set from entity @s data.config.{EXPLOSION_RADIUS}

# Resolve shooter: copy UUID to storage, then find matching player
data modify storage {ns}:temp expl.shooter_uuid set from entity @s data.shooter

# Tag the matching shooter for damage attribution
scoreboard players set #found {ns}.data 0
execute as @a run function {ns}:v{version}/projectile/match_shooter
execute if score #found {ns}.data matches 0 as @e[tag={ns}.armed] run function {ns}:v{version}/projectile/match_shooter

# Apply bullet direct-hit damage to the entity tagged in on_collision (if entity was hit, not just a block)
# Give shooter ticking tag so DPS signal can find them
tag @n[tag={ns}.temp_shooter] add {ns}.ticking

# Get direct-hit damage amount (with 1 decimal)
execute store result score #direct_dmg {ns}.data run data get entity @s data.config.{DAMAGE} 10

# If zombie game is active: multiply by 5 for zombies, cap for players (6 hp = 3 hearts)
execute if data storage {ns}:zombies game{{state:"active"}} if entity @n[tag={ns}.direct_hit,type=!player] run scoreboard players operation #direct_dmg {ns}.data *= #5 {ns}.data
execute if data storage {ns}:zombies game{{state:"active"}} if entity @n[tag={ns}.direct_hit,type=player] if score #direct_dmg {ns}.data matches 60.. run scoreboard players set #direct_dmg {ns}.data 60

# Flak Jacket perk: halve explosive direct-hit damage to a perked MP player
execute if entity @n[tag={ns}.direct_hit,type=player,scores={{{ns}.mp.in_game=1,{ns}.special.flak_jacket=1}}] run scoreboard players operation #direct_dmg {ns}.data /= #2 {ns}.data

# PhD Flopper perk: a perked (zombies) player takes no explosive direct-hit damage
execute if entity @n[tag={ns}.direct_hit,type=player,scores={{{ns}.special.phd_flopper=1}}] run scoreboard players set #direct_dmg {ns}.data 0

# Instant kill: one-shot a non-immune victim when the shooter has it active (mirrors the area path).
# Without this, explosives with little/no blast radius (or a direct projectile strike) never instant-kill.
# Never applied to players while a zombies game is active (would bypass the explosion cap above).
execute if entity @n[tag={ns}.direct_hit,tag=!{ns}.no_instant_kill,type=!player] if score @n[tag={ns}.temp_shooter] {ns}.special.instant_kill matches 1.. run scoreboard players set #direct_dmg {ns}.data 99999
execute unless data storage {ns}:zombies game{{state:"active"}} if entity @n[tag={ns}.direct_hit,tag=!{ns}.no_instant_kill,type=player] if score @n[tag={ns}.temp_shooter] {ns}.special.instant_kill matches 1.. run scoreboard players set #direct_dmg {ns}.data 99999

# Apply direct hit damage using the existing damage utility
data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@n[tag={ns}.temp_shooter]"}}
execute store result storage {ns}:input with.amount float 0.1 run scoreboard players get #direct_dmg {ns}.data
data modify storage {ns}:input with.weapon set from storage {ns}:gun all
execute as @n[tag={ns}.direct_hit,tag=!{ns}.temp_shooter] run function {ns}:v{version}/utils/signal_and_damage
tag @e[tag={ns}.direct_hit] remove {ns}.direct_hit
tag @n[tag={ns}.temp_shooter] remove {ns}.ticking

# Apply area damage to nearby entities (macro for configurable radius)
execute store result storage {ns}:temp expl.radius_float float 1 run data get entity @s data.config.{EXPLOSION_RADIUS}
function {ns}:v{version}/projectile/damage_area with storage {ns}:temp expl

# Signal: on_explosion (@s = projectile entity, explosion data in mgs:signals)
data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
function #{ns}:signals/on_explosion

# Clean up shooter tag
tag @e[tag={ns}.temp_shooter] remove {ns}.temp_shooter

# Delete the projectile
function {ns}:v{version}/projectile/delete
""")  # noqa: E501

	## Realistic block destruction (calls RealisticExplosionLibrary)
	write_versioned_function("projectile/realistic_explosion", f"""
# Set explosion power from config and call the library
scoreboard players operation #explosion_power realistic_explosion.data = #projectile_explosion_power {ns}.config
execute if score #projectile_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 1
execute unless score #projectile_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 0
function realistic_explosion:explode
""")

	## Match shooter by UUID comparison
	write_versioned_function("projectile/match_shooter", f"""
# Compare this player's UUID with the stored shooter UUID
# data modify returns 0 (no change) when values are identical, 1 when modified
data modify storage {ns}:temp copy_uuid set from entity @s UUID
execute store success score #is_match {ns}.data run data modify storage {ns}:temp copy_uuid set from storage {ns}:temp expl.shooter_uuid

# If #is_match is 0, the UUIDs were identical (no change was made), so this is the shooter
execute if score #is_match {ns}.data matches 0 run scoreboard players set #found {ns}.data 1
execute if score #is_match {ns}.data matches 0 run tag @s add {ns}.temp_shooter
""")

