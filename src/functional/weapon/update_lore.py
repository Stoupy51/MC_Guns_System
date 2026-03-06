
# Imports
import json

from stewbeet import Mem, write_load_file, write_versioned_function
from stewbeet import create_gradient_text as new_hex

from ...config.stats import (
	CAPACITY,
	COOLDOWN,
	DAMAGE,
	DECAY,
	END_HEX,
	EXPLOSION_DAMAGE,
	EXPLOSION_RADIUS,
	GRENADE_FUSE,
	GRENADE_TYPE,
	PELLET_COUNT,
	RELOAD_TIME,
	REMAINING_BULLETS,
	START_HEX,
	SWITCH,
)


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Generate gradient text labels for each stat line (stored in load file as templates)
	templates: dict[str, str] = {
		# Regular gun labels
		"damage":           json.dumps([*new_hex("Damage Per Bullet  ➤ ", START_HEX, END_HEX)]),
		"ammo":             json.dumps([*new_hex("Ammo Remaining      ➤ ", START_HEX, END_HEX)]),
		"reload":           json.dumps([*new_hex("Reloading Time       ➤ ", START_HEX, END_HEX)]),
		"fire_rate":        json.dumps([*new_hex("Fire Rate             ➤ ", START_HEX, END_HEX)]),
		"pellets":          json.dumps([*new_hex("Pellets Per Shot    ➤ ", START_HEX, END_HEX)]),
		"decay":            json.dumps([*new_hex("Damage Decay       ➤ ", START_HEX, END_HEX)]),
		"switch_time":      json.dumps([*new_hex("Switch Time           ➤ ", START_HEX, END_HEX)]),
		# Fire rate unit gradients (appended as nested arrays)
		"fire_rate_sps":    json.dumps([*new_hex("shots/s", END_HEX, START_HEX, text_length=10)]),
		"fire_rate_spshot": json.dumps([*new_hex("s/shot", END_HEX, START_HEX, text_length=10)]),
		# Grenade labels
		"grenade_type":     json.dumps([*new_hex("Type                  ➤ ", START_HEX, END_HEX)]),
		"grenade_fuse":     json.dumps([*new_hex("Fuse Time            ➤ ", START_HEX, END_HEX)]),
		"expl_damage":      json.dumps([*new_hex("Explosion Damage  ➤ ", START_HEX, END_HEX)]),
		"expl_radius":      json.dumps([*new_hex("Explosion Radius   ➤ ", START_HEX, END_HEX)]),
	}

	# Store templates in load file
	template_commands: str = "\n".join(
		f"data modify storage {ns}:lore_templates {key} set value {value}"
		for key, value in templates.items()
	)
	write_load_file(f"\n## Lore label templates for utils/update_all_lore\n{template_commands}")

	# Main entry point: utils/update_all_lore {slot:"weapon.mainhand"}
	# Rebuilds ALL lore lines from the weapon's current stats in custom_data
	write_versioned_function("utils/update_all_lore", f"""
# Rebuild all lore lines for the weapon in the given slot from its current stats
# Usage: function {ns}:v{version}/utils/update_all_lore {{slot:"weapon.mainhand"}}

# Tag player for identification
tag @s add {ns}.update_lore

# Read stats from item into scores
$execute summon item_display run function {ns}:v{version}/lore/extract_stats {{"slot":"$(slot)"}}

# Skip if not a gun
execute if score #is_gun {ns}.data matches 0 run return run tag @s remove {ns}.update_lore

# Compute formatted display values (integer math → storage for macros)
function {ns}:v{version}/lore/compute_values

# Build new lore based on weapon type
execute if score #is_grenade {ns}.data matches 1 run function {ns}:v{version}/lore/build_grenade with storage {ns}:input lore
execute if score #is_grenade {ns}.data matches 0 run function {ns}:v{version}/lore/build_gun with storage {ns}:input lore

# Restore footer (branding line saved during extraction)
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_footer

# Apply new lore to item
$execute summon item_display run function {ns}:v{version}/lore/apply {{"slot":"$(slot)"}}

# Clean up
tag @s remove {ns}.update_lore
""")

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
scoreboard players set #200 {ns}.data 200
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

	# Build gun lore (macro function, called with storage mgs:input lore)
	write_versioned_function("lore/build_gun", f"""
# Initialize new lore array
data modify storage {ns}:temp new_lore set value []

# -- Damage Per Bullet --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates damage
$data modify storage {ns}:temp lore_line append value "$(damage)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Ammo Remaining (X/Y) --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates ammo
$data modify storage {ns}:temp lore_line append value "$(remaining)"
data modify storage {ns}:temp lore_line append value {{"text":"/","color":"#{END_HEX}"}}
$data modify storage {ns}:temp lore_line append value "$(capacity)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Reloading Time --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates reload
$data modify storage {ns}:temp lore_line append value "$(reload_int).$(reload_dec)"
data modify storage {ns}:temp lore_line append value {{"text":"s","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Fire Rate (conditional unit: shots/s or s/shot) --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates fire_rate
$data modify storage {ns}:temp lore_line append value "$(rate_int).$(rate_dec) "
execute if score #fire_rate_tenths {ns}.data matches 10.. run data modify storage {ns}:temp lore_line append from storage {ns}:lore_templates fire_rate_sps
execute if score #fire_rate_tenths {ns}.data matches ..9 run data modify storage {ns}:temp lore_line append from storage {ns}:lore_templates fire_rate_spshot
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Pellets Per Shot (optional, only for shotguns) --
execute if score #has_pellets {ns}.data matches 1 run function {ns}:v{version}/lore/append_pellet_line with storage {ns}:input lore

# -- Damage Decay --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates decay
$data modify storage {ns}:temp lore_line append value "$(decay_pct)"
data modify storage {ns}:temp lore_line append value {{"text":"%","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Switch Time --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates switch_time
$data modify storage {ns}:temp lore_line append value "$(switch_int).$(switch_dec)"
data modify storage {ns}:temp lore_line append value {{"text":"s","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Empty line separator --
data modify storage {ns}:temp new_lore append value ""
""")

	# Append pellet line (separate function for conditional execution)
	write_versioned_function("lore/append_pellet_line", f"""
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates pellets
$data modify storage {ns}:temp lore_line append value "$(pellets)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line
""")

	# Build grenade lore (macro function)
	write_versioned_function("lore/build_grenade", f"""
# Initialize new lore array
data modify storage {ns}:temp new_lore set value []

# -- Type --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates grenade_type
$data modify storage {ns}:temp lore_line append value "$(type_display)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Explosion Damage (optional) --
execute if score #has_expl_damage {ns}.data matches 1 run function {ns}:v{version}/lore/append_expl_damage with storage {ns}:input lore

# -- Explosion Radius (optional) --
execute if score #has_expl_radius {ns}.data matches 1 run function {ns}:v{version}/lore/append_expl_radius with storage {ns}:input lore

# -- Fuse Time --
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates grenade_fuse
$data modify storage {ns}:temp lore_line append value "$(fuse_int).$(fuse_dec)"
data modify storage {ns}:temp lore_line append value {{"text":"s","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line

# -- Empty line separator --
data modify storage {ns}:temp new_lore append value ""
""")

	# Append explosion damage line
	write_versioned_function("lore/append_expl_damage", f"""
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates expl_damage
$data modify storage {ns}:temp lore_line append value "$(expl_damage)"
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line
""")

	# Append explosion radius line
	write_versioned_function("lore/append_expl_radius", f"""
data modify storage {ns}:temp lore_line set from storage {ns}:lore_templates expl_radius
$data modify storage {ns}:temp lore_line append value "$(expl_radius)"
data modify storage {ns}:temp lore_line append value {{"text":" blocks","color":"#{END_HEX}"}}
data modify storage {ns}:temp new_lore append from storage {ns}:temp lore_line
""")

	# Apply new lore to item
	write_versioned_function("lore/apply", f"""
# Copy item from player to item_display
$item replace entity @s contents from entity @p[tag={ns}.update_lore] $(slot)

# Replace lore with rebuilt version
data modify entity @s item.components."minecraft:lore" set from storage {ns}:temp new_lore

# Copy modified item back to player
$item replace entity @p[tag={ns}.update_lore] $(slot) from entity @s contents

# Clean up
kill @s
""")
