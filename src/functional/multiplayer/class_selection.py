
# ruff: noqa: E501
# Imports
import json

from stewbeet import JsonDict, Mem, write_load_file, write_versioned_function

from .classes import CLASS_IDS, CLASSES, get_class_description


def generate_class_selection() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Scoreboards for class selection
	## ============================
	write_load_file(
f"""
# Class selection scoreboard (1-10 = class id, 0 = none)
scoreboard objectives add {ns}.mp.class dummy

# Death detection for respawn
scoreboard objectives add {ns}.mp.death_count deathCount
""")

	## ============================
	## set_class macro (used by menus, triggers, and inventory selection)
	## ============================
	write_versioned_function("multiplayer/set_class",
f"""
$scoreboard players set @s {ns}.mp.class $(class_num)

# If game active: queue for next respawn
$execute if data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Class set to ","color":"white"}},{{"text":"$(class_name)","color":"green","bold":true}},{{"text":" — will apply on respawn","color":"yellow"}}]

# If game not active: apply immediately and notify
$execute unless data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Class set to ","color":"white"}},{{"text":"$(class_name)","color":"green","bold":true}}]
execute unless data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/apply_class
""")

	## ============================
	## Give class selector items (initial selection: in hotbar)
	## ============================
	give_initial_commands: str = "# Give class selector items for initial class pick\nclear @s\n"
	for idx, (class_id, class_data) in enumerate(CLASSES.items()):
		# Hotbar 0-8, then overflow to inventory.0+
		slot: str = f"hotbar.{idx}" if idx < 9 else f"inventory.{idx - 9}"
		give_initial_commands += _class_item_command(slot, class_id, class_data)

	write_versioned_function("multiplayer/give_class_selectors", give_initial_commands)

	## ============================
	## Give class selectors in bottom inventory row (during gameplay)
	## ============================
	give_gameplay_commands: str = "# Give class selector items in bottom inventory row\n"
	for idx, (class_id, class_data) in enumerate(CLASSES.items()):
		inv_slot: int = 17 + idx  # inventory.17 through inventory.26
		give_gameplay_commands += _class_item_command(f"inventory.{inv_slot}", class_id, class_data)

	write_versioned_function("multiplayer/give_class_selectors_gameplay", give_gameplay_commands)

	## ============================
	## Detect class selection (holding selector in mainhand)
	## ============================
	detect_commands: str = ""
	for class_id in CLASS_IDS:
		class_num: int = CLASS_IDS[class_id]
		detect_commands += f'execute if items entity @s weapon.mainhand *[custom_data~{{mgs:{{class_selector:"{class_id}"}}}}] run scoreboard players set @s {ns}.mp.class {class_num}\n'

	detect_commands += f"""
# Clear all class selector items from inventory
clear @s minecraft:poisonous_potato[custom_data~{{mgs:{{class_selector:{{}}}}}}]

# If game active: queue for next respawn, keep selectors in inventory for future
execute if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/give_class_selectors_gameplay
"""
	for class_id, class_data in CLASSES.items():
		class_num = CLASS_IDS[class_id]
		name: str = class_data["name"]
		detect_commands += f'execute if score @s {ns}.mp.class matches {class_num} if data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Class set to ","color":"white"}},{{"text":"{name}","color":"green","bold":true}},{{"text":" — will apply on respawn","color":"yellow"}}]\n'

	detect_commands += f"""
# If game not active: apply immediately
execute unless data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/apply_class
"""
	for class_id, class_data in CLASSES.items():
		class_num = CLASS_IDS[class_id]
		name = class_data["name"]
		detect_commands += f'execute if score @s {ns}.mp.class matches {class_num} unless data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Class selected: ","color":"white"}},{{"text":"{name}","color":"green","bold":true}}]\n'

	write_versioned_function("multiplayer/detect_class_selection", detect_commands)

	## ============================
	## Apply class loadout based on score
	## ============================
	apply_commands: str = ""
	for class_id, class_num in CLASS_IDS.items():
		apply_commands += f"execute if score @s {ns}.mp.class matches {class_num} run function {ns}:v{version}/multiplayer/class/{class_id}\n"

	# After loadout, give class selectors in bottom inventory row
	apply_commands += f"\n# Give class selectors in bottom inventory row for future changes\nfunction {ns}:v{version}/multiplayer/give_class_selectors_gameplay\n"

	write_versioned_function("multiplayer/apply_class", apply_commands)

	## ============================
	## On respawn (called from player tick when death detected)
	## ============================
	write_versioned_function("multiplayer/on_respawn",
f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Increment death stats
scoreboard players add @s {ns}.mp.deaths 1

# Apply current class (auto-equip with loadout + bottom row selectors)
execute if score @s {ns}.mp.class matches 1.. run function {ns}:v{version}/multiplayer/apply_class

# If no class selected yet, give full selectors
execute unless score @s {ns}.mp.class matches 1.. run function {ns}:v{version}/multiplayer/give_class_selectors
""")

	## ============================
	## Player tick hooks (appended to player/tick)
	## ============================
	write_versioned_function("player/tick",
f"""
# Multiplayer: detect class selection from inventory
execute if items entity @s weapon.mainhand *[custom_data~{{mgs:{{class_selector:{{}}}}}}] run function {ns}:v{version}/multiplayer/detect_class_selection

# Multiplayer: detect respawn (death_count incremented by deathCount criterion)
execute if data storage {ns}:multiplayer game{{state:"active"}} if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/multiplayer/on_respawn
""")


def _class_item_command(slot: str, class_id: str, class_data: JsonDict) -> str:
	""" Generate an 'item replace' command for a class selector item. """
	gun: str = class_data["main"]["gun"]
	name: str = class_data["name"]
	description: str = get_class_description(class_id)

	# Build lore lines from class description (split on newlines)
	# Use SNBT compound notation (no surrounding quotes) so Minecraft parses them as text components
	lore_lines: list[str] = []
	for line in description.split("\n"):
		lore_lines.append(json.dumps({"text": line, "color": "gray", "italic": False}))
	lore_snbt: str = ",".join(lore_lines)

	# Build item name as SNBT compound (no surrounding quotes)
	name_snbt: str = json.dumps({"text": name, "color": "green", "bold": True, "italic": False})

	return f'item replace entity @s {slot} with minecraft:poisonous_potato[item_model="mgs:{gun}",custom_data={{mgs:{{class_selector:"{class_id}"}}}},item_name={name_snbt},lore=[{lore_snbt}],max_stack_size=1]\n'

