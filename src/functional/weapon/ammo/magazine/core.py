""" Consuming a bullet, the infinite-ammo refill and reading ammo back on a weapon switch. """
# Imports
from stewbeet import ItemModifier, JsonDict, Mem, set_json_encoder, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import CAPACITY, REMAINING_BULLETS
from .lore import create_lore_functions


# Functions
def write_ammo_core() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Create lore functions for weapons
	create_lore_functions(
		type_name="lore",
		tag=f"{ns}.modify_lore",
		remaining_source=f"@s {ns}.{REMAINING_BULLETS}",
		capacity_source=f"storage {ns}:temp components.\"minecraft:custom_data\".{ns}.stats.{CAPACITY}"
	)

	# Create lore functions for magazines
	create_lore_functions(
		type_name="mag_lore",
		tag=f"{ns}.modify_mag_lore",
		remaining_source=f"#bullets {ns}.data",
		capacity_source=f"storage {ns}:temp {CAPACITY}"
	)

	# Handle right click event by decreasing ammo count
	write_versioned_function("player/right_click", f"""
# Decrease bullet count
function {ns}:v{version}/ammo/decrease
""")

	# Decrease ammo count function
	write_versioned_function("ammo/decrease", f"""
# If infinite ammo is active, refill ammo to max capacity and skip consumption
execute if score @s {ns}.special.infinite_ammo matches 1.. run return run function {ns}:v{version}/ammo/infinite_refill

# Remove 1 bullet from player's ammo count
scoreboard players remove @s {ns}.{REMAINING_BULLETS} 1
execute if score @s {ns}.{REMAINING_BULLETS} matches ..0 run function {ns}:v{version}/ammo/reload

# Add mid cooldown sound tag if weapon has pump sound
execute if data storage {ns}:gun all.sounds.pump run tag @s add {ns}.pump_sound

# Add mid reload sound tag if weapon has reload mid sound
execute if data storage {ns}:gun all.sounds.playermid run tag @s add {ns}.reload_mid_sound
""")

	# Infinite ammo refill: set current ammo to weapon's max capacity
	write_versioned_function("ammo/infinite_refill", f"""
# Set player's ammo count to weapon capacity
execute store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{CAPACITY}
""")

	# Handle weapon switching logic
	write_versioned_function("switch/on_weapon_switch", f"""
# When unequipping a weapon (player was holding a weapon):
#   - Find weapon with CURRENT_AMMO = -1 (needs update)
#   - Store current ammo count in weapon's stats
execute if score @s {ns}.last_selected matches 1.. run function {ns}:v{version}/ammo/update_old_weapon

# When equipping a new weapon:
#   - Load ammo count from weapon's stats into player scoreboard
#   - Mark weapon as needing update by setting ammo to -1
execute if score #current_id {ns}.data matches 1.. run function {ns}:v{version}/ammo/copy_data
""")

	# Update ammo count for previously equipped weapon
	custom_data = f"{{{ns}:{{stats:{{{REMAINING_BULLETS}:-1}}}}}}"
	content: str = f"""
# Store player's current ammo count in temporary storage
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}

# Check all inventory slots for weapon needing ammo update (remaining bullets = -1)
"""
	for slot in ItemBuilder.ALL_SLOTS:
		content += f"""execute if items entity @s {slot} *[custom_data~{custom_data}] run return run function {ns}:v{version}/ammo/set_count {{slot:"{slot}"}}\n"""
	write_versioned_function("ammo/update_old_weapon", content)

	# Create item modifier to update weapon's ammo count
	modifier: JsonDict = {
		"function":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:temp"},
		"ops":[{"source":REMAINING_BULLETS,"target":f"{ns}.stats.{REMAINING_BULLETS}","op":"replace"}]
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/update_ammo"] = set_json_encoder(ItemModifier(modifier), max_level=-1)

	# Create item modifier to set consumable stack count from a score (#bullets in mgs.data)
	consumable_count_modifier: JsonDict = {
		"function": "minecraft:set_count",
		"count": {"type": "minecraft:score", "target": {"type": "fixed", "name": "#bullets"}, "score": f"{ns}.data"},
		"add": False
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/set_consumable_count"] = set_json_encoder(ItemModifier(consumable_count_modifier), max_level=-1)

	# Update weapon's ammo count and lore
	write_versioned_function("ammo/set_count", f"""
# Apply new ammo count to weapon
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

# Update weapon's lore to show new ammo count
$function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}
""")

	# Load ammo data from newly equipped weapon
	write_versioned_function("ammo/copy_data", f"""
# Load ammo count from weapon into player's scoreboard (if different from -1)
execute store result score #count {ns}.data run data get storage {ns}:gun all.stats.{REMAINING_BULLETS}
execute unless score #count {ns}.data matches -1 run scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #count {ns}.data

# Mark weapon as needing update
data modify storage {ns}:gun all.stats.{REMAINING_BULLETS} set value -1
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats
""")

	# Note: ammo/modify_lore, ammo/get_current_lore, ammo/search_lore_loop, and ammo/found_lore_line are generated by create_lore_functions("lore", ...) above.

