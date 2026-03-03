
# Imports
import json

from stewbeet import Mem, write_load_file, write_versioned_function

from .classes import CLASSES

# Consumable magazine item IDs (stack count = bullet count, uses set_consumable_count modifier)
CONSUMABLE_MAGS: set[str] = {"rpg7_rocket", "mosin_bullet", "m24_bullet", "spas12_shell", "m500_shell", "m590_shell"}


def generate_loadouts() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Default Class Registration
	## ============================
	for class_id, class_data in CLASSES.items():
		class_json: str = json.dumps(class_data)
		write_load_file(f"data modify storage {ns}:multiplayer classes.{class_id} set value {class_json}")

	## ============================
	## Per-class loadout functions
	## ============================
	for class_id, class_data in CLASSES.items():
		commands: str = f"""
# Apply class: {class_data['name']} - {class_data['lore']}
clear @s
"""

		# Primary weapon → hotbar.0
		commands += f"# Primary weapon → hotbar.0\nloot replace entity @s hotbar.0 loot {ns}:i/{class_data['main']['gun']}\n"

		# Secondary weapon → hotbar.1
		if "secondary" in class_data:
			commands += f"\n# Secondary weapon → hotbar.1\nloot replace entity @s hotbar.1 loot {ns}:i/{class_data['secondary']['gun']}\n"

		# Equipment (grenades) → hotbar.8, hotbar.7 (one slot per type, count via modifier)
		if "equipment" in class_data:
			equip_slot: int = 8
			commands += "\n# Equipment → hotbar.8, hotbar.7, ...\n"
			for item_id, count in class_data["equipment"].items():
				commands += f"loot replace entity @s hotbar.{equip_slot} loot {ns}:i/{item_id}\n"
				if count > 1:
					commands += f'item modify entity @s hotbar.{equip_slot} {{"function":"minecraft:set_count","count":{count},"add":false}}\n'
				equip_slot -= 1

		# Magazines → inventory.0, inventory.1, ...
		inv_slot: int = 0
		commands += "\n# Magazines → inventory.0, inventory.1, ...\n"

		# Primary magazines
		mag_id: str = class_data["main"]["mag"]
		mag_count: int = class_data["main"].get("mag_count", 0)
		if mag_id in CONSUMABLE_MAGS:
			# Consumable: single stack, set count via item modifier
			commands += f"loot replace entity @s inventory.{inv_slot} loot {ns}:i/{mag_id}\n"
			commands += f"scoreboard players set #bullets {ns}.data {mag_count}\n"
			commands += f"item modify entity @s inventory.{inv_slot} {ns}:v{version}/set_consumable_count\n"
			inv_slot += 1
		else:
			# Regular: one magazine per slot
			for _ in range(mag_count):
				commands += f"loot replace entity @s inventory.{inv_slot} loot {ns}:i/{mag_id}\n"
				inv_slot += 1

		# Secondary magazines
		if "secondary" in class_data:
			sec_mag_id: str = class_data["secondary"]["mag"]
			sec_mag_count: int = class_data["secondary"].get("mag_count", 0)
			if sec_mag_id in CONSUMABLE_MAGS:
				commands += f"loot replace entity @s inventory.{inv_slot} loot {ns}:i/{sec_mag_id}\n"
				commands += f"scoreboard players set #bullets {ns}.data {sec_mag_count}\n"
				commands += f"item modify entity @s inventory.{inv_slot} {ns}:v{version}/set_consumable_count\n"
				inv_slot += 1
			else:
				for _ in range(sec_mag_count):
					commands += f"loot replace entity @s inventory.{inv_slot} loot {ns}:i/{sec_mag_id}\n"
					inv_slot += 1

		write_versioned_function(f"multiplayer/class/{class_id}", commands)

