""" The gradient stat labels and the entry point rebuilding a weapon's whole lore. """
# Imports
import json

from stewbeet import Mem, write_load_file, write_versioned_function
from stewbeet import create_gradient_text as new_hex

from .....config.stats.colors import END_HEX, START_HEX


# Functions
def write_lore_templates() -> None:
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

	# Main entry point: utils/update_all_lore {slot:"weapon.mainhand"} Rebuilds ALL lore lines from the weapon's current stats in custom_data
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

