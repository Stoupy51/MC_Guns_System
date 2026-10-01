""" Area damage, the per-entity falloff behind it and removing the projectile. """
# Imports
from stewbeet import Conventions, Mem, write_tick_file, write_versioned_function

from .....config.stats.keys import EXPLOSION_DAMAGE, EXPLOSION_DECAY


# Functions
def write_projectile_damage() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("projectile/damage_area", f"""
$execute as @e[type=!#{ns}:ignore,distance=..$(radius_float),{Conventions.GLOBAL_KILL.avoid},nbt=!{{Invulnerable:true}}] run function {ns}:v{version}/projectile/damage_entity
""")

	## Damage falls off with distance.
	write_versioned_function("projectile/damage_entity", f"""
# Not living entities or other projectiles.
execute if entity @s[tag={ns}.slow_bullet] run return fail

# Teammates are skipped, the shooter is not.
execute if entity @s[type=player] unless entity @s[tag={ns}.temp_shooter] store result score #shooter_team {ns}.data run scoreboard players get @n[tag={ns}.temp_shooter] {ns}.mp.team
execute if entity @s[type=player] unless entity @s[tag={ns}.temp_shooter] if score #shooter_team {ns}.data matches 1.. if score @s {ns}.mp.team = #shooter_team {ns}.data run return fail

execute store result score #ent_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #ent_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #ent_z {ns}.data run data get entity @s Pos[2] 1000

# Squared distance, in millionths of a block squared.
scoreboard players operation #dx {ns}.data = #ent_x {ns}.data
scoreboard players operation #dx {ns}.data -= #ctr_x {ns}.data
scoreboard players operation #dy {ns}.data = #ent_y {ns}.data
scoreboard players operation #dy {ns}.data -= #ctr_y {ns}.data
scoreboard players operation #dz {ns}.data = #ent_z {ns}.data
scoreboard players operation #dz {ns}.data -= #ctr_z {ns}.data

scoreboard players operation #dx2 {ns}.data = #dx {ns}.data
scoreboard players operation #dx2 {ns}.data *= #dx {ns}.data
scoreboard players operation #dy2 {ns}.data = #dy {ns}.data
scoreboard players operation #dy2 {ns}.data *= #dy {ns}.data
scoreboard players operation #dz2 {ns}.data = #dz {ns}.data
scoreboard players operation #dz2 {ns}.data *= #dz {ns}.data

scoreboard players operation #dist_sq {ns}.data = #dx2 {ns}.data
scoreboard players operation #dist_sq {ns}.data += #dy2 {ns}.data
scoreboard players operation #dist_sq {ns}.data += #dz2 {ns}.data

# https://docs.mcbookshelf.dev/en/latest/modules/math.html#square-root
execute store result storage bs:in math.sqrt.x double 0.000001 run scoreboard players get #dist_sq {ns}.data
function #bs.math:sqrt
# In tenths of a block, for decay precision.
execute store result score #distance {ns}.data run data get storage bs:out math.sqrt 10

# damage *= pow(decay, distance)
data modify storage bs:in math.pow.x set from storage {ns}:temp expl.{EXPLOSION_DECAY}

# Tenths x 0.1: the distance in blocks.
execute store result storage bs:in math.pow.y float 0.1 run scoreboard players get #distance {ns}.data

function #bs.math:pow

execute store result score #expl_dmg {ns}.data run data get storage {ns}:temp expl.{EXPLOSION_DAMAGE} 10
execute store result score #decay_factor {ns}.data run data get storage bs:out math.pow 1000000

scoreboard players operation #expl_dmg {ns}.data *= #decay_factor {ns}.data
scoreboard players operation #expl_dmg {ns}.data /= #1000000 {ns}.data

# In a zombies game: 5x against zombies, players capped at 6 HP (3 hearts).
execute if data storage {ns}:zombies game{{state:"active"}} if entity @s[type=!player] run scoreboard players operation #expl_dmg {ns}.data *= #5 {ns}.data
execute if data storage {ns}:zombies game{{state:"active"}} if entity @s[type=player] if score #expl_dmg {ns}.data matches 60.. run scoreboard players set #expl_dmg {ns}.data 60

# Flak Jacket (MP): half explosive damage.
execute if entity @s[type=player,scores={{{ns}.mp.in_game=1,{ns}.special.flak_jacket=1}}] run scoreboard players operation #expl_dmg {ns}.data /= #2 {ns}.data

# PhD Flopper (zombies): no explosive damage.
execute if entity @s[type=player,scores={{{ns}.special.phd_flopper=1}}] run scoreboard players set #expl_dmg {ns}.data 0

# Below 0.1 damage.
execute if score #expl_dmg {ns}.data matches ..0 run return fail

# Instant kill sets 99999, except on players during a zombies game (it would bypass the cap above).
tag @n[tag={ns}.temp_shooter] add {ns}.ticking
execute if entity @s[tag=!{ns}.no_instant_kill,type=!player] as @n[tag={ns}.temp_shooter] if score @s {ns}.special.instant_kill matches 1.. run scoreboard players set #expl_dmg {ns}.data 99999
execute unless data storage {ns}:zombies game{{state:"active"}} if entity @s[tag=!{ns}.no_instant_kill,type=player] as @n[tag={ns}.temp_shooter] if score @s {ns}.special.instant_kill matches 1.. run scoreboard players set #expl_dmg {ns}.data 99999

# With the damage signal, weapon info included.
data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@n[tag={ns}.temp_shooter]"}}
execute if entity @n[tag={ns}.temp_shooter,type=player] run data modify storage {ns}:input with.attacker set value "@p[tag={ns}.temp_shooter]"
execute store result storage {ns}:input with.amount float 0.1 run scoreboard players get #expl_dmg {ns}.data
data modify storage {ns}:input with.weapon set from storage {ns}:gun all

# A self-attributed hit is cancelled by friendlyFire=false, so the shooter takes plain, unattributed damage from their own blast.
execute if entity @s[tag={ns}.temp_shooter] run function {ns}:v{version}/utils/signal_and_damage_plain
execute unless entity @s[tag={ns}.temp_shooter] run function {ns}:v{version}/utils/signal_and_damage

# Score 0 means dead, which also covers an entity that no longer exists; guarded against firing twice.
scoreboard players set #victim_hp {ns}.data 0
execute store result score #victim_hp {ns}.data run data get entity @s Health 100
scoreboard players set #is_new_kill {ns}.data 0
execute if score #victim_hp {ns}.data matches ..0 unless entity @s[tag={ns}.already_killed] run scoreboard players set #is_new_kill {ns}.data 1
execute if score #victim_hp {ns}.data matches ..0 unless entity @s[tag={ns}.already_killed] run tag @s add {ns}.already_killed

# Same drop as raycast/apply_damage, for an explosion kill.
execute if score #is_new_kill {ns}.data matches 1 if entity @s[tag={ns}.mission_enemy] at @s run function {ns}:v{version}/missions/drop_enemy_weapon

execute if score #is_new_kill {ns}.data matches 1 run data modify storage {ns}:signals on_kill set value {{}}
execute if score #is_new_kill {ns}.data matches 1 run data modify storage {ns}:signals on_kill.explosion set value true
execute if score #is_new_kill {ns}.data matches 1 as @n[tag={ns}.temp_shooter] run function #{ns}:signals/on_kill

tag @n[tag={ns}.temp_shooter] remove {ns}.ticking
""")

	write_versioned_function("projectile/delete", f"""
scoreboard players remove #slow_bullet_count {ns}.data 1
kill @s
""")

	write_tick_file(f"""
execute if score #slow_bullet_count {ns}.data matches 1.. as @e[type=minecraft:item_display,tag={ns}.slow_bullet] at @s run function {ns}:v{version}/projectile/tick
""")

