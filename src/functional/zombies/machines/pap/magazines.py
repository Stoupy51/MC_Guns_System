""" Upgrading matching magazines to 8x the weapon's capacity, and refilling them. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import BASE_WEAPON, CAPACITY, REMAINING_BULLETS


# Functions
def write_pap_magazines() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# --- PAP Magazine Capacity Upgrade (8x weapon capacity) ---
	pap_mag_lines: list[str] = [
		f"# Upgrade and refill matching {BASE_WEAPON} magazines to 8x weapon capacity",
		f"execute store result score #pap_mag_cap {ns}.data run data get storage {ns}:temp _pap_extract.stats.capacity 8",
	]
	for slot in ItemBuilder.ALL_SLOTS:
		if slot == "weapon.mainhand":
			continue
		pap_mag_lines.append(
			f'$execute if items entity @s {slot} *[custom_data~{{{ns}:{{magazine:true,weapon:"$({BASE_WEAPON})"}}}}] run function {ns}:v{version}/zombies/pap/upgrade_magazine_slot {{slot:"{slot}"}}'
		)
	write_versioned_function("zombies/pap/pap_upgrade_magazines", "\n".join(pap_mag_lines))

	write_versioned_function("zombies/pap/upgrade_magazine_slot", f"""
# Set magazine capacity and remaining to weapon capacity x 8
execute store result storage {ns}:temp zb_item_stats.{CAPACITY} int 1 run scoreboard players get #pap_mag_cap {ns}.data
execute store result storage {ns}:temp zb_item_stats.{REMAINING_BULLETS} int 1 run scoreboard players get #pap_mag_cap {ns}.data

# Apply new stats to magazine
$item modify entity @s $(slot) {ns}:v{version}/zb_item_stats

# Update magazine lore
data modify storage {ns}:temp {CAPACITY} set from storage {ns}:temp zb_item_stats.{CAPACITY}
scoreboard players operation #bullets {ns}.data = #pap_mag_cap {ns}.data
$function {ns}:v{version}/ammo/modify_mag_lore {{slot:"$(slot)"}}

# Restore full magazine model (read actual item_model from the magazine)
$data modify storage {ns}:temp refill.slot set value "$(slot)"
data modify storage {ns}:temp refill.{BASE_WEAPON} set from storage {ns}:temp _pap_extract.stats.{BASE_WEAPON}
tag @s add {ns}.pap_extracting_mag
$execute summon item_display run function {ns}:v{version}/zombies/pap/extract_mag_model {{slot:"$(slot)"}}
tag @s remove {ns}.pap_extracting_mag
function {ns}:v{version}/zombies/bonus/set_full_mag_model with storage {ns}:temp refill
""")

	# Extract magazine item_model via item_display (@s = item_display, caller = player)
	write_versioned_function("zombies/pap/extract_mag_model", f"""
$item replace entity @s contents from entity @p[tag={ns}.pap_extracting_mag] $(slot)
data modify storage {ns}:temp refill.mag_model set from entity @s item.components."minecraft:item_model"
kill @s
""")

	# Refill all magazine items in inventory that match the PAP'd weapon's base_weapon.
	mag_refill_lines: list[str] = [f"# Refill matching {BASE_WEAPON} magazines — called with storage mgs:temp _pap_extract.stats"]
	for slot in ItemBuilder.ALL_SLOTS:
		if slot == "weapon.mainhand":
			continue
		mag_refill_lines.append(
			f'$execute if items entity @s {slot} *[custom_data~{{{ns}:{{magazine:true,weapon:"$({BASE_WEAPON})"}}}}] run function {ns}:v{version}/zombies/bonus/refill_magazine {{slot:"{slot}"}}'
		)
	write_versioned_function("zombies/pap/refill_matching_magazines", "\n".join(mag_refill_lines))

