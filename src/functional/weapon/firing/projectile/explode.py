""" The explosion: particles, block damage and finding the shooter to credit. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import BASE_WEAPON, DAMAGE
from ...explosion import Explosion


# Functions
def write_projectile_explosion() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("projectile/explode", f"""
scoreboard players set #ray_gun {ns}.data 0
execute if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}} run scoreboard players set #ray_gun {ns}.data 1
execute if score #ray_gun {ns}.data matches 1 if data entity @s data.config.pap_level run scoreboard players set #ray_gun {ns}.data 2
## Pack-a-Punched Ray Gun: red burst.
execute if score #ray_gun {ns}.data matches 2 run particle flash{{color:[0.8,0.0,0.0,1.0]}} ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 2 run particle dust_color_transition{{from_color:[1.0,0.0,0.0],to_color:[0.3,0.0,0.0],scale:1.8}} ~ ~ ~ 0.6 0.6 0.6 0 200 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 2 run particle crimson_spore ~ ~ ~ 0.5 0.5 0.5 0.05 100 force @a[distance=..128]
## Ray Gun: green burst.
execute if score #ray_gun {ns}.data matches 1 run particle flash{{color:[0.0,0.8,0.0,1.0]}} ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle dust{{color:[0.0,0.8,0.0],scale:1.5}} ~ ~ ~ 0.5 0.5 0.5 0 200 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle glow ~ ~ ~ 0.5 0.5 0.5 0.1 80 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 1 run particle electric_spark ~ ~ ~ 0.5 0.5 0.5 0.05 100 force @a[distance=..128]
## Other weapons: fire and smoke.
execute if score #ray_gun {ns}.data matches 0 run particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle large_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 50 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
execute if score #ray_gun {ns}.data matches 0 run particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

# The Ray Gun is silent.
execute if score #ray_gun {ns}.data matches 0 run playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# RealisticExplosionLibrary, when projectile_explosion_power > 0.
execute if score #projectile_explosion_power {ns}.config matches 1.. run function {ns}:v{version}/projectile/realistic_explosion

{Explosion.setup_lines(ns, version)}

# Direct hit on the entity tagged in on_collision; the shooter gets ticking so the DPS signal finds them.
tag @n[tag={ns}.temp_shooter] add {ns}.ticking

# One decimal.
execute store result score #direct_dmg {ns}.data run data get entity @s data.config.{DAMAGE} 10

# In a zombies game: 5x against zombies, players capped at 6 HP (3 hearts).
execute if data storage {ns}:zombies game{{state:"active"}} if entity @n[tag={ns}.direct_hit,type=!player] run scoreboard players operation #direct_dmg {ns}.data *= #5 {ns}.data
execute if data storage {ns}:zombies game{{state:"active"}} if entity @n[tag={ns}.direct_hit,type=player] if score #direct_dmg {ns}.data matches 60.. run scoreboard players set #direct_dmg {ns}.data 60

# Flak Jacket (MP): half direct-hit damage.
execute if entity @n[tag={ns}.direct_hit,type=player,scores={{{ns}.mp.in_game=1,{ns}.special.flak_jacket=1}}] run scoreboard players operation #direct_dmg {ns}.data /= #2 {ns}.data

# PhD Flopper (zombies): no direct-hit damage.
execute if entity @n[tag={ns}.direct_hit,type=player,scores={{{ns}.special.phd_flopper=1}}] run scoreboard players set #direct_dmg {ns}.data 0

# Instant kill, as on the area path, so small-blast explosives and direct strikes can instant-kill; never players during a zombies game.
execute if entity @n[tag={ns}.direct_hit,tag=!{ns}.no_instant_kill,type=!player] if score @n[tag={ns}.temp_shooter] {ns}.special.instant_kill matches 1.. run scoreboard players set #direct_dmg {ns}.data 99999
execute unless data storage {ns}:zombies game{{state:"active"}} if entity @n[tag={ns}.direct_hit,tag=!{ns}.no_instant_kill,type=player] if score @n[tag={ns}.temp_shooter] {ns}.special.instant_kill matches 1.. run scoreboard players set #direct_dmg {ns}.data 99999

data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@n[tag={ns}.temp_shooter]"}}
execute store result storage {ns}:input with.amount float 0.1 run scoreboard players get #direct_dmg {ns}.data
data modify storage {ns}:input with.weapon set from storage {ns}:gun all
execute as @n[tag={ns}.direct_hit,tag=!{ns}.temp_shooter] run function {ns}:v{version}/utils/signal_and_damage
tag @e[tag={ns}.direct_hit] remove {ns}.direct_hit
tag @n[tag={ns}.temp_shooter] remove {ns}.ticking

# Macro, for the configurable radius.
{Explosion.area_damage_lines(ns, version)}

# Run as the projectile; explosion data in mgs:signals.
data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
function #{ns}:signals/on_explosion

tag @e[tag={ns}.temp_shooter] remove {ns}.temp_shooter

function {ns}:v{version}/projectile/delete
""")

	write_versioned_function("projectile/realistic_explosion", f"""
scoreboard players operation #explosion_power realistic_explosion.data = #projectile_explosion_power {ns}.config
execute if score #projectile_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 1
execute unless score #projectile_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 0
function realistic_explosion:explode
""")

	write_versioned_function("projectile/match_shooter", f"""
# `data modify ... set` succeeds only when the value changes, so 0 means the same UUID.
data modify storage {ns}:temp copy_uuid set from entity @s UUID
execute store success score #is_match {ns}.data run data modify storage {ns}:temp copy_uuid set from storage {ns}:temp expl.shooter_uuid

execute if score #is_match {ns}.data matches 0 run scoreboard players set #found {ns}.data 1
execute if score #is_match {ns}.data matches 0 run tag @s add {ns}.temp_shooter
""")

