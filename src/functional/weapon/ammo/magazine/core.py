""" Consuming a bullet, the infinite-ammo refill and reading ammo back on a weapon switch. """
# Imports
from stewbeet import (
	ItemModifier,
	JsonDict,
	Mem,
	set_json_encoder,
	write_versioned_function,
)

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import CAPACITY, REMAINING_BULLETS
from .lore import create_lore_functions


# Functions
def write_ammo_core() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	create_lore_functions(
		type_name="lore",
		tag=f"{ns}.modify_lore",
		remaining_source=f"@s {ns}.{REMAINING_BULLETS}",
		capacity_source=f"storage {ns}:temp components.\"minecraft:custom_data\".{ns}.stats.{CAPACITY}"
	)

	create_lore_functions(
		type_name="mag_lore",
		tag=f"{ns}.modify_mag_lore",
		remaining_source=f"#bullets {ns}.data",
		capacity_source=f"storage {ns}:temp {CAPACITY}"
	)

	write_versioned_function("player/right_click", f"""
function {ns}:v{version}/ammo/decrease
""")

	write_versioned_function("ammo/decrease", f"""
# Infinite ammo refills to capacity and consumes nothing.
execute if score @s {ns}.special.infinite_ammo matches 1.. run return run function {ns}:v{version}/ammo/infinite_refill

scoreboard players remove @s {ns}.{REMAINING_BULLETS} 1
execute if score @s {ns}.{REMAINING_BULLETS} matches ..0 run function {ns}:v{version}/ammo/reload

# Read by the mid-cooldown sound check.
execute if data storage {ns}:gun all.sounds.pump run tag @s add {ns}.pump_sound

# Read by the mid-reload sound check.
execute if data storage {ns}:gun all.sounds.playermid run tag @s add {ns}.reload_mid_sound
""")

	write_versioned_function("ammo/infinite_refill", f"""
execute store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{CAPACITY}
""")

	write_versioned_function("switch/on_weapon_switch", f"""
# Unequipping: the previous weapon (remaining bullets -1) gets the player's ammo count back into its stats.
execute if score @s {ns}.last_selected matches 1.. run function {ns}:v{version}/ammo/update_old_weapon

# Equipping: its ammo count goes to the player's score, and the item is marked -1 (live in the score).
execute if score #current_id {ns}.data matches 1.. run function {ns}:v{version}/ammo/copy_data
""")

	custom_data = f"{{{ns}:{{stats:{{{REMAINING_BULLETS}:-1}}}}}}"
	content: str = f"""
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}

"""
	for slot in ItemBuilder.ALL_SLOTS:
		content += f"""execute if items entity @s {slot} *[custom_data~{custom_data}] run return run function {ns}:v{version}/ammo/set_count {{slot:"{slot}"}}\n"""
	write_versioned_function("ammo/update_old_weapon", content)

	modifier: JsonDict = {
		"type":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:temp"},
		"ops":[{"source":REMAINING_BULLETS,"target":f"{ns}.stats.{REMAINING_BULLETS}","op":"replace"}]
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/update_ammo"] = set_json_encoder(ItemModifier(modifier), max_level=-1)

	# Stack count from the #bullets score.
	consumable_count_modifier: JsonDict = {
		"type": "minecraft:set_count",
		"count": {"type": "minecraft:score", "target": {"type": "fixed", "name": "#bullets"}, "score": f"{ns}.data"},
		"add": False
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/set_consumable_count"] = set_json_encoder(ItemModifier(consumable_count_modifier), max_level=-1)

	write_versioned_function("ammo/set_count", f"""
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

$function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}
""")

	write_versioned_function("ammo/copy_data", f"""
# Unless it is already -1.
execute store result score #count {ns}.data run data get storage {ns}:gun all.stats.{REMAINING_BULLETS}
execute unless score #count {ns}.data matches -1 run scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #count {ns}.data

data modify storage {ns}:gun all.stats.{REMAINING_BULLETS} set value -1
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats
""")

	# ammo/modify_lore and its helpers come from create_lore_functions("lore", ...) above.

