""" Replenishing lethals and remembering which grenade type a player carries. """
# Imports
from stewbeet import Advancement, JsonDict, Mem, set_json_encoder, write_versioned_function

from .....config.stats.weapons.grenades import LETHAL_GRENADE_IDS
from .shared import SlotPredicates, slot_predicates


# Functions
def write_grenade_slots() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	slots: SlotPredicates = slot_predicates(ns)
	equipment_1_match = f"*[custom_data~{slots.equipment_1}]"

	write_versioned_function("zombies/inventory/replenish_grenades", f"""
# Case 1: player already has grenades in slot 7 - add 2, cap at 4
execute if items entity @s hotbar.7 {equipment_1_match} run item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_add_2
execute if items entity @s hotbar.7 {equipment_1_match} store result score #nade_count {ns}.data run data get entity @s Inventory[{{Slot:7b}}].count
execute if items entity @s hotbar.7 {equipment_1_match} if score #nade_count {ns}.data matches 5.. run item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_4
execute if items entity @s hotbar.7 {equipment_1_match} run return 0

# Case 2: slot 7 is empty (used all grenades) - give 2 of the player's BOUGHT lethal type, not a
# hardcoded frag (a player who bought semtex and used them all should get 2 semtex back).
execute unless items entity @s hotbar.7 * run function {ns}:v{version}/zombies/inventory/give_lethal_type {{count:2}}
""")

	# Re-give the player's recorded lethal type (frag / semtex / …) into the empty hotbar.7.
	# The per-player {ns}.zb.lethal_type score is set on give (starting loadout = frag) and on a lethal wall-buy (wallbuys.py). frag is the fallback for an unset/0 score.
	# Widow's Wine owners always get web grenades in the lethal slot, regardless of the recorded lethal type — so every refill path (respawn replenish, Max Ammo, give_lethal_type) hands out webs.
	# `return run` short-circuits the frag/semtex fallback below.
	lethal_loot_lines: str = f"execute if score @s {ns}.special.widows_wine matches 1 run return run loot replace entity @s hotbar.7 loot {ns}:i/web_grenade\n"
	lethal_loot_lines += f"execute unless score @s {ns}.zb.lethal_type matches 1.. run loot replace entity @s hotbar.7 loot {ns}:i/{LETHAL_GRENADE_IDS[0]}\n"
	lethal_loot_lines += "\n".join(
		f"execute if score @s {ns}.zb.lethal_type matches {i} run loot replace entity @s hotbar.7 loot {ns}:i/{gid}"
		for i, gid in enumerate(LETHAL_GRENADE_IDS) if i > 0
	)
	write_versioned_function("zombies/inventory/loot_replace_lethal", lethal_loot_lines)

	# Fill hotbar.7 with $(count) grenades of the player's lethal type, then re-tag the slot.
	write_versioned_function("zombies/inventory/give_lethal_type", f"""
function {ns}:v{version}/zombies/inventory/loot_replace_lethal
$item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_$(count)
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}
""")

	# Record the player's lethal type from a wall-buy (called by wallbuys.py buy_lethal after the new-purchase give).
	# Reads the bought weapon_id out of the {ns}:temp _wb_weapon storage.
	lethal_record_lines: str = "\n".join(
		f'execute if data storage {ns}:temp _wb_weapon{{weapon_id:"{gid}"}} run scoreboard players set @s {ns}.zb.lethal_type {i}'
		for i, gid in enumerate(LETHAL_GRENADE_IDS) if i > 0
	)
	write_versioned_function("zombies/inventory/record_lethal_type", f"""
scoreboard players set @s {ns}.zb.lethal_type 0
{lethal_record_lines}
""")

	inv_changed_adv: JsonDict = {
		"criteria": {
			"change": {
				"trigger": "minecraft:inventory_changed",
			},
		},
		"rewards": {
			"function": f"{ns}:v{version}/zombies/inventory/on_change",
		},
	}
	Mem.ctx.data[ns].advancements[f"v{version}/zombies/inventory_changed"] = set_json_encoder(Advancement(inv_changed_adv), max_level=-1)

