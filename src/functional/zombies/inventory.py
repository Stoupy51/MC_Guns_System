
# ruff: noqa: E501
# Zombies Inventory Management
# Handles starting loadouts, slot layout, grenade replenishment, and inventory protection.
from stewbeet import Advancement, ItemModifier, JsonDict, Mem, set_json_encoder, write_versioned_function

from ...config.stats import CAPACITY, REMAINING_BULLETS


def generate_zombies_inventory() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# ── Centralized Item Definitions (easy-edit constants) ────────

	# Custom data match patterns (pre-built to avoid f-string brace issues)
	knife_cd = "{" + ns + ":{knife:true}}"
	gun_cd = "{" + ns + ":{gun:true}}"
	mag_cd = "{" + ns + ":{magazine:true}}"
	info_cd = "{" + ns + ":{zb_info:true}}"
	ability_cd = "{" + ns + ":{zb_ability_item:true}}"
	frag_cd = "{" + ns + ':{gun:true,stats:{grenade_type:"frag"}}}'
	frag_stats_cd = "{" + ns + ':{stats:{grenade_type:"frag"}}}'
	ns_cd = "{" + ns + ":}"

	# Full knife item definition (20 attack damage to one-shot round 1 zombies)
	knife_item = (
		f"minecraft:iron_sword[custom_data={knife_cd},"
		f'item_name={{"text":"Knife","color":"white","italic":false}},'
		f'attribute_modifiers=[{{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"}}]'
		f"]"
	)
	knife_match = f"minecraft:iron_sword[custom_data~{knife_cd}]"

	# Match patterns with wildcard item type
	gun_match = f"*[custom_data~{gun_cd}]"
	mag_match = f"*[custom_data~{mag_cd}]"
	info_match = f"*[custom_data~{info_cd}]"
	ability_match = f"*[custom_data~{ability_cd}]"
	frag_match = f"*[custom_data~{frag_cd}]"
	frag_stats_match = f"*[custom_data~{frag_stats_cd}]"
	ns_match = f"*[custom_data~{ns_cd}]"

	# ── Item Modifiers ────────────────────────────────────────────

	# Modifier to patch capacity and remaining_bullets from storage {ns}:temp zb_item_stats
	zb_stats_modifier: JsonDict = {
		"function": "minecraft:copy_custom_data",
		"source": {"type": "minecraft:storage", "source": f"{ns}:temp"},
		"ops": [
			{"source": f"zb_item_stats.{CAPACITY}", "target": f"{ns}.stats.{CAPACITY}", "op": "replace"},
			{"source": f"zb_item_stats.{REMAINING_BULLETS}", "target": f"{ns}.stats.{REMAINING_BULLETS}", "op": "replace"},
		]
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_item_stats"] = set_json_encoder(ItemModifier(zb_stats_modifier), max_level=-1)

	# Starting Loadout ──────────────────────────────────────────

	write_versioned_function("zombies/inventory/give_starting_loadout", f"""
# Clear existing inventory
clear @s

# hotbar.0: Knife
item replace entity @s hotbar.0 with {knife_item}

# hotbar.1: Starting weapon (M1911)
loot replace entity @s hotbar.1 loot {ns}:i/m1911

# inventory.1: M1911 magazine (dynamically scaled: base capacity * 8, half filled)
loot replace entity @s inventory.1 loot {ns}:i/m1911_mag
execute store result score #zb_cap {ns}.data run data get entity @s Inventory[{{Slot:10b}}].components."minecraft:custom_data".{ns}.stats.{CAPACITY}
scoreboard players set #zb_const {ns}.data 8
scoreboard players operation #zb_cap {ns}.data *= #zb_const {ns}.data
execute store result storage {ns}:temp zb_item_stats.{CAPACITY} int 1 run scoreboard players get #zb_cap {ns}.data
scoreboard players set #zb_const {ns}.data 2
scoreboard players operation #zb_cap {ns}.data /= #zb_const {ns}.data
execute store result storage {ns}:temp zb_item_stats.{REMAINING_BULLETS} int 1 run scoreboard players get #zb_cap {ns}.data
item modify entity @s inventory.1 {ns}:v{version}/zb_item_stats

# hotbar.7: Frag grenade (4 uses)
data modify storage {ns}:temp zb_item_stats set value {{{CAPACITY}:4,{REMAINING_BULLETS}:4}}
loot replace entity @s hotbar.7 loot {ns}:i/frag_grenade
item modify entity @s hotbar.7 {ns}:v{version}/zb_item_stats

# hotbar.8: Player info item
function {ns}:v{version}/zombies/inventory/refresh_info_item

# hotbar.4: Ability item (if ability is set)
execute if score @s {ns}.zb.ability matches 1.. run function {ns}:v{version}/zombies/inventory/give_ability_item
""")

	# Respawn Loadout ───────────────────────────────────────────

	write_versioned_function("zombies/inventory/give_respawn_loadout", f"""
function {ns}:v{version}/zombies/inventory/give_starting_loadout
""")

	# Player Info Item ──────────────────────────────────────────

	write_versioned_function("zombies/inventory/refresh_info_item", f"""
# Build a player info item with current stats in lore
item replace entity @s hotbar.8 with minecraft:paper[custom_data={{{ns}:{{zb_info:true}}}},item_name={{"text":"\\u2139 Player Info","color":"gold","italic":false}},lore=[{{"text":"Round: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold"}}]}},{{"text":"Points: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"gold"}}]}},{{"text":"Kills: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.kills"}},"color":"green"}}]}},{{"text":"Downs: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.downs"}},"color":"red"}}]}},{{"text":"","italic":false}},{{"text":"Passive: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.passive"}},"color":"aqua"}}]}},{{"text":"Ability: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.ability"}},"color":"green"}}]}}]]
""")

	# Ability Item ──────────────────────────────────────────────

	write_versioned_function("zombies/inventory/give_ability_item", f"""
# Place ability use item in hotbar.4
item replace entity @s hotbar.4 with minecraft:paper[custom_data={{{ns}:{{zb_ability_item:true}}}},consumable={{consume_seconds:1000000,animation:"spear",sound:"minecraft:intentionally_empty",has_consume_particles:false}},food={{saturation:0,nutrition:0,can_always_eat:true}},use_effects={{can_sprint:true,speed_multiplier:1.0,interact_vibrations:false}},item_name={{"text":"\\u2b50 Use Ability","color":"green","italic":false}},lore=[{{"text":"Right-click to activate","color":"gray","italic":false}}]]
""")

	# Grenade Replenishment (called per-player at round start)

	write_versioned_function("zombies/inventory/replenish_grenades", f"""
# Only if player has a grenade in hotbar.7
execute unless items entity @s hotbar.7 {gun_match} run return fail

# Read current remaining bullets from grenade (hotbar.7 = Slot 7b in player NBT)
execute store result score #nade_rem {ns}.data run data get entity @s Inventory[{{Slot:7b}}].components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS}

# Add 2, cap at 4
scoreboard players add #nade_rem {ns}.data 2
execute if score #nade_rem {ns}.data matches 5.. run scoreboard players set #nade_rem {ns}.data 4

# Apply via item modifier
execute store result storage {ns}:temp zb_item_stats.{REMAINING_BULLETS} int 1 run scoreboard players get #nade_rem {ns}.data
data modify storage {ns}:temp zb_item_stats.{CAPACITY} set value 4
item modify entity @s hotbar.7 {ns}:v{version}/zb_item_stats
""")

	# Inventory Protection ──────────────────────────────────────

	# Advancement: detect inventory change during zombies
	inv_changed_adv: JsonDict = {
		"criteria": {
			"change": {
				"trigger": "minecraft:inventory_changed"
			}
		},
		"rewards": {
			"function": f"{ns}:v{version}/zombies/inventory/on_change"
		}
	}
	Mem.ctx.data[ns].advancements[f"v{version}/zombies/inventory_changed"] = set_json_encoder(Advancement(inv_changed_adv), max_level=-1)

	## On inventory change: validate layout
	write_versioned_function("zombies/inventory/on_change", f"""
# Only process during active zombies game
execute unless score @s {ns}.zb.in_game matches 1 run return fail
execute if data storage {ns}:zombies game{{state:"lobby"}} run return fail
execute if data storage {ns}:zombies game{{state:"ended"}} run return fail

# Revoke advancement to re-detect
advancement revoke @s only {ns}:v{version}/zombies/inventory_changed

# Check & fix slot integrity
function {ns}:v{version}/zombies/inventory/check_slots
""")

	## Kill dropped items via Common Signals (executes as new item entity)
	write_versioned_function("zombies/inventory/on_new_item", f"""
# Kill any {ns} item dropped by a player in a zombies game
execute if data entity @s Item.components."minecraft:custom_data".{ns} on origin if score @s {ns}.zb.in_game matches 1 run kill @s
""", tags=["common_signals:signals/on_new_item"])

	## Check slot integrity — ensure protected items are in correct slots
	write_versioned_function("zombies/inventory/check_slots", f"""
# Knife must be in hotbar.0
execute unless items entity @s hotbar.0 {knife_match} run function {ns}:v{version}/zombies/inventory/fix_knife

# Info item must be in hotbar.8
execute unless items entity @s hotbar.8 {info_match} run function {ns}:v{version}/zombies/inventory/fix_info

# Grenade must be in hotbar.7
execute unless items entity @s hotbar.7 {frag_match} run function {ns}:v{version}/zombies/inventory/fix_grenade

# Ability item must be in hotbar.4 (if player has ability)
execute if score @s {ns}.zb.ability matches 1.. unless items entity @s hotbar.4 {ability_match} run function {ns}:v{version}/zombies/inventory/give_ability_item

# Weapon in hotbar.1 must be a gun
execute unless items entity @s hotbar.1 {gun_match} run function {ns}:v{version}/zombies/inventory/fix_weapon_1

# Magazine in inventory.1 should exist if weapon 1 exists
execute if items entity @s hotbar.1 {gun_match} unless items entity @s inventory.1 {mag_match} run function {ns}:v{version}/zombies/inventory/fix_mag_1

# Prevent items in forbidden slots
item replace entity @s hotbar.5 with air

# Clear cursor (prevent holding mgs items outside inventory)
execute if items entity @s player.cursor {ns_match} run item replace entity @s player.cursor with air
""")

	## Fix: knife not in hotbar.0
	write_versioned_function("zombies/inventory/fix_knife", f"""
# Re-give any knife from wrong slots
clear @s {knife_match}
item replace entity @s hotbar.0 with {knife_item}
""")

	## Fix: info item not in hotbar.8
	write_versioned_function("zombies/inventory/fix_info", f"""
clear @s {info_match}
function {ns}:v{version}/zombies/inventory/refresh_info_item
""")

	## Fix: grenade not in hotbar.7
	write_versioned_function("zombies/inventory/fix_grenade", f"""
clear @s {frag_match}
data modify storage {ns}:temp zb_item_stats set value {{{CAPACITY}:4,{REMAINING_BULLETS}:0}}
loot replace entity @s hotbar.7 loot {ns}:i/frag_grenade
item modify entity @s hotbar.7 {ns}:v{version}/zb_item_stats
""")

	## Fix: weapon 1 not in hotbar.1
	write_versioned_function("zombies/inventory/fix_weapon_1", f"""
# Search for a non-grenade gun in other hotbar slots and swap it back to hotbar.1
execute if items entity @s hotbar.0 {gun_match} unless items entity @s hotbar.0 {frag_stats_match} run return run function {ns}:v{version}/zombies/inventory/swap_to_1 {{from:"hotbar.0"}}
execute if items entity @s hotbar.2 {gun_match} unless items entity @s hotbar.2 {frag_stats_match} run return run function {ns}:v{version}/zombies/inventory/swap_to_1 {{from:"hotbar.2"}}
execute if items entity @s hotbar.3 {gun_match} unless items entity @s hotbar.3 {frag_stats_match} run return run function {ns}:v{version}/zombies/inventory/swap_to_1 {{from:"hotbar.3"}}
execute if items entity @s hotbar.4 {gun_match} unless items entity @s hotbar.4 {frag_stats_match} run return run function {ns}:v{version}/zombies/inventory/swap_to_1 {{from:"hotbar.4"}}
execute if items entity @s hotbar.5 {gun_match} unless items entity @s hotbar.5 {frag_stats_match} run return run function {ns}:v{version}/zombies/inventory/swap_to_1 {{from:"hotbar.5"}}
execute if items entity @s hotbar.6 {gun_match} unless items entity @s hotbar.6 {frag_stats_match} run return run function {ns}:v{version}/zombies/inventory/swap_to_1 {{from:"hotbar.6"}}
execute if items entity @s hotbar.8 {gun_match} unless items entity @s hotbar.8 {frag_stats_match} run return run function {ns}:v{version}/zombies/inventory/swap_to_1 {{from:"hotbar.8"}}
""")

	## Swap item from source slot to hotbar.1 using item_display intermediary
	write_versioned_function("zombies/inventory/swap_to_1", f"""
tag @s add {ns}.inv_fix
$execute summon item_display run function {ns}:v{version}/zombies/inventory/do_swap_1 {{from:"$(from)"}}
tag @s remove {ns}.inv_fix
""")

	write_versioned_function("zombies/inventory/do_swap_1", f"""
# Copy the weapon from source slot to item_display
$item replace entity @s contents from entity @p[tag={ns}.inv_fix] $(from)
# Move whatever is in hotbar.1 to source slot
$item replace entity @p[tag={ns}.inv_fix] $(from) from entity @p[tag={ns}.inv_fix] hotbar.1
# Move weapon from item_display to hotbar.1
item replace entity @p[tag={ns}.inv_fix] hotbar.1 from entity @s contents
kill @s
""")

	## Fix: magazine 1 not in inventory.1
	write_versioned_function("zombies/inventory/fix_mag_1", f"""
execute if items entity @s hotbar.0 {mag_match} run return run function {ns}:v{version}/zombies/inventory/move_mag_to_inv1 {{from:"hotbar.0"}}
execute if items entity @s hotbar.1 {mag_match} run return run function {ns}:v{version}/zombies/inventory/move_mag_to_inv1 {{from:"hotbar.1"}}
execute if items entity @s hotbar.2 {mag_match} run return run function {ns}:v{version}/zombies/inventory/move_mag_to_inv1 {{from:"hotbar.2"}}
execute if items entity @s inventory.0 {mag_match} run return run function {ns}:v{version}/zombies/inventory/move_mag_to_inv1 {{from:"inventory.0"}}
execute if items entity @s inventory.2 {mag_match} run return run function {ns}:v{version}/zombies/inventory/move_mag_to_inv1 {{from:"inventory.2"}}
""")

	write_versioned_function("zombies/inventory/move_mag_to_inv1", """
$item replace entity @s inventory.1 from entity @s $(from)
$item replace entity @s $(from) with air
""")

