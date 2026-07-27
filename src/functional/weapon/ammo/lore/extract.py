""" Reading a weapon's stats out of its custom data and into the values lore shows. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import CAPACITY, COOLDOWN, DAMAGE, DECAY, EXPLOSION_DAMAGE, EXPLOSION_RADIUS, GRENADE_FUSE, GRENADE_TYPE, PELLET_COUNT, RELOAD_TIME, REMAINING_BULLETS, SWITCH


# Functions
def write_lore_extraction() -> None:
	ns: str = Mem.ctx.project_id

	# Extract all stats from item into scores
	cd: str = f'"minecraft:custom_data".{ns}.stats'
	write_versioned_function("lore/extract_stats", f"""
# Copy item from player to item_display
$item replace entity @s contents from entity @p[tag={ns}.update_lore] $(slot)

# Check if item is a gun
execute store result score #is_gun {ns}.data if data entity @s item.components."minecraft:custom_data".{ns}.gun
execute store result score #is_grenade {ns}.data if data entity @s item.components.{cd}.{GRENADE_TYPE}

# Read numeric stats into scores
execute store result score #lore_damage {ns}.data run data get entity @s item.components.{cd}.{DAMAGE}
execute store result score #lore_capacity {ns}.data run data get entity @s item.components.{cd}.{CAPACITY}
execute store result score #lore_remaining {ns}.data run data get entity @s item.components.{cd}.{REMAINING_BULLETS}
execute store result score #lore_reload {ns}.data run data get entity @s item.components.{cd}.{RELOAD_TIME}
execute store result score #lore_cooldown {ns}.data run data get entity @s item.components.{cd}.{COOLDOWN}
execute store result score #lore_pellets {ns}.data run data get entity @s item.components.{cd}.{PELLET_COUNT}
execute store result score #lore_decay {ns}.data run data get entity @s item.components.{cd}.{DECAY} 10000
execute store result score #lore_switch {ns}.data run data get entity @s item.components.{cd}.{SWITCH}
execute store result score #has_pellets {ns}.data if data entity @s item.components.{cd}.{PELLET_COUNT}
execute store result score #has_cooldown {ns}.data if data entity @s item.components.{cd}.{COOLDOWN}

# If remaining_bullets is -1 (weapon-switch marker), use player's scoreboard value instead
execute if score #lore_remaining {ns}.data matches -1 store result score #lore_remaining {ns}.data run scoreboard players get @p[tag={ns}.update_lore] {ns}.{REMAINING_BULLETS}

# Read grenade-specific stats
execute store result score #lore_expl_damage {ns}.data run data get entity @s item.components.{cd}.{EXPLOSION_DAMAGE}
execute store result score #lore_expl_radius {ns}.data run data get entity @s item.components.{cd}.{EXPLOSION_RADIUS}
execute store result score #lore_grenade_fuse {ns}.data run data get entity @s item.components.{cd}.{GRENADE_FUSE}
execute store result score #has_expl_damage {ns}.data if data entity @s item.components.{cd}.{EXPLOSION_DAMAGE}
execute store result score #has_expl_radius {ns}.data if data entity @s item.components.{cd}.{EXPLOSION_RADIUS}

# Read grenade type string into temp storage
data modify storage {ns}:temp grenade_type set from entity @s item.components.{cd}.{GRENADE_TYPE}

# Save footer (last lore line, usually branding/attribution)
data modify storage {ns}:temp lore_footer set from entity @s item.components."minecraft:lore"[-1]

# Clean up item_display
kill @s
""")

	# Compute formatted display values from raw scores
	write_versioned_function("lore/compute_values", f"""
# Initialize input storage for macro functions
data modify storage {ns}:input lore set value {{}}

# --- Damage ---
execute store result storage {ns}:input lore.damage int 1 run scoreboard players get #lore_damage {ns}.data

# --- Ammo ---
execute store result storage {ns}:input lore.remaining int 1 run scoreboard players get #lore_remaining {ns}.data
execute store result storage {ns}:input lore.capacity int 1 run scoreboard players get #lore_capacity {ns}.data

# --- Reload time: ticks → "X.Y" seconds (ticks / 2 gives tenths, then split) ---
scoreboard players operation #half {ns}.data = #lore_reload {ns}.data
scoreboard players operation #half {ns}.data /= #2 {ns}.data
scoreboard players operation #reload_int {ns}.data = #half {ns}.data
scoreboard players operation #reload_int {ns}.data /= #10 {ns}.data
scoreboard players operation #reload_dec {ns}.data = #half {ns}.data
scoreboard players operation #reload_dec {ns}.data %= #10 {ns}.data
execute store result storage {ns}:input lore.reload_int int 1 run scoreboard players get #reload_int {ns}.data
execute store result storage {ns}:input lore.reload_dec int 1 run scoreboard players get #reload_dec {ns}.data

# --- Fire rate: tenths_of_shots_per_second = 200 / cooldown → "X.Y" ---
scoreboard players operation #fire_rate_tenths {ns}.data = #200 {ns}.data
scoreboard players operation #fire_rate_tenths {ns}.data /= #lore_cooldown {ns}.data
scoreboard players operation #rate_int {ns}.data = #fire_rate_tenths {ns}.data
scoreboard players operation #rate_int {ns}.data /= #10 {ns}.data
scoreboard players operation #rate_dec {ns}.data = #fire_rate_tenths {ns}.data
scoreboard players operation #rate_dec {ns}.data %= #10 {ns}.data
execute store result storage {ns}:input lore.rate_int int 1 run scoreboard players get #rate_int {ns}.data
execute store result storage {ns}:input lore.rate_dec int 1 run scoreboard players get #rate_dec {ns}.data

# --- Pellets ---
execute store result storage {ns}:input lore.pellets int 1 run scoreboard players get #lore_pellets {ns}.data

# --- Decay: float*10000, round and divide by 100 for percentage ---
scoreboard players add #lore_decay {ns}.data 50
scoreboard players operation #lore_decay {ns}.data /= #100 {ns}.data
execute store result storage {ns}:input lore.decay_pct int 1 run scoreboard players get #lore_decay {ns}.data

# --- Switch time: ticks → "X.Y" seconds ---
scoreboard players operation #switch_half {ns}.data = #lore_switch {ns}.data
scoreboard players operation #switch_half {ns}.data /= #2 {ns}.data
scoreboard players operation #switch_int {ns}.data = #switch_half {ns}.data
scoreboard players operation #switch_int {ns}.data /= #10 {ns}.data
scoreboard players operation #switch_dec {ns}.data = #switch_half {ns}.data
scoreboard players operation #switch_dec {ns}.data %= #10 {ns}.data
execute store result storage {ns}:input lore.switch_int int 1 run scoreboard players get #switch_int {ns}.data
execute store result storage {ns}:input lore.switch_dec int 1 run scoreboard players get #switch_dec {ns}.data

# --- Grenade stats ---
execute store result storage {ns}:input lore.expl_damage int 1 run scoreboard players get #lore_expl_damage {ns}.data
execute store result storage {ns}:input lore.expl_radius int 1 run scoreboard players get #lore_expl_radius {ns}.data

# --- Grenade fuse time: ticks → "X.Y" seconds ---
scoreboard players operation #fuse_half {ns}.data = #lore_grenade_fuse {ns}.data
scoreboard players operation #fuse_half {ns}.data /= #2 {ns}.data
scoreboard players operation #fuse_int {ns}.data = #fuse_half {ns}.data
scoreboard players operation #fuse_int {ns}.data /= #10 {ns}.data
scoreboard players operation #fuse_dec {ns}.data = #fuse_half {ns}.data
scoreboard players operation #fuse_dec {ns}.data %= #10 {ns}.data
execute store result storage {ns}:input lore.fuse_int int 1 run scoreboard players get #fuse_int {ns}.data
execute store result storage {ns}:input lore.fuse_dec int 1 run scoreboard players get #fuse_dec {ns}.data

# --- Grenade type display name ---
data modify storage {ns}:input lore.type_display set value "Unknown"
execute if data storage {ns}:temp {{grenade_type:"frag"}} run data modify storage {ns}:input lore.type_display set value "Frag"
execute if data storage {ns}:temp {{grenade_type:"semtex"}} run data modify storage {ns}:input lore.type_display set value "Semtex"
execute if data storage {ns}:temp {{grenade_type:"smoke"}} run data modify storage {ns}:input lore.type_display set value "Smoke"
execute if data storage {ns}:temp {{grenade_type:"flash"}} run data modify storage {ns}:input lore.type_display set value "Flash"
""")

