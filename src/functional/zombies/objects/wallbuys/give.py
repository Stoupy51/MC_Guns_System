""" Placing the bought item and its magazine into the right slot. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon


# Functions
def write_wallbuy_give() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	gun_cd: str = ZombiesCommon.gun_cd(ns)
	mag_cd: str = "{" + ns + ":{magazine:true}}"

	# Build weapon_id -> magazine_id mapping
	weapon_mag_data: dict[str, str] = {}
	for weapon_id, (mag_id, _, _) in ZombiesCommon.build_weapon_magazine_data().items():
		weapon_mag_data[weapon_id] = mag_id

	# Generate lookup function for weapon -> magazine mapping
	magazine_lookup_cmds = "\n".join([
		f"execute if data storage {ns}:temp _wb_store{{weapon_id:\"{wid}\"}} run data modify storage {ns}:temp _wb_store.magazine_id set value \"{mag_id}\""
		for wid, (mag_id, _, _) in ZombiesCommon.build_weapon_magazine_data().items()
	])

	write_versioned_function("zombies/wallbuys/lookup_magazine_id", magazine_lookup_cmds)

	write_versioned_function("zombies/wallbuys/lookup_weapon", f"""
$data modify storage {ns}:temp _wb_weapon set from storage {ns}:zombies wallbuy_data."$(id)"
""")

	write_versioned_function("zombies/wallbuys/get_display_name", f"""
# Default to localized display item name.
data modify storage {ns}:temp _wb_display_name set from storage {ns}:temp _wb_weapon.item_name

# If a custom map name is set, use it instead.
execute unless data storage {ns}:temp _wb_weapon{{name:""}} if data storage {ns}:temp _wb_weapon.name run data modify storage {ns}:temp _wb_display_name set from storage {ns}:temp _wb_weapon.name
""")

	write_versioned_function("zombies/wallbuys/process_purchase", f"""
scoreboard players set #wb_purchase_done {ns}.data 0
scoreboard players set #wb_purchase_mode {ns}.data 0

# Always prioritize refill of the same weapon to prevent duplicates.
execute if score #wb_purchase_done {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/try_refill_owned with storage {ns}:temp _wb_weapon

# New placement: give to the first empty gun slot (checks each slot individually)
$execute if score #wb_purchase_done {ns}.data matches 0 unless items entity @s hotbar.1 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/give_to_slot {{hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 unless items entity @s hotbar.2 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/give_to_slot {{hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 unless items entity @s hotbar.3 *[custom_data~{gun_cd}] if score @s {ns}.zb.perk.mule_kick matches 1.. run function {ns}:v{version}/zombies/wallbuys/give_to_slot {{hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}

# Otherwise replace the currently selected gun slot (1/2/3 only)
execute if score #wb_purchase_done {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/replace_selected with storage {ns}:temp _wb_weapon
""")

	write_versioned_function("zombies/wallbuys/count_guns", f"""
scoreboard players set #wb_gun_count {ns}.data 0
execute if items entity @s hotbar.1 *[custom_data~{gun_cd}] run scoreboard players add #wb_gun_count {ns}.data 1
execute if items entity @s hotbar.2 *[custom_data~{gun_cd}] run scoreboard players add #wb_gun_count {ns}.data 1
execute if items entity @s hotbar.3 *[custom_data~{gun_cd}] run scoreboard players add #wb_gun_count {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/give_to_slot", f"""
$loot replace entity @s hotbar.$(hotbar) loot {ns}:i/$(weapon_id)

scoreboard players set #wb_mag_given {ns}.data 0
$execute store success score #wb_mag_given {ns}.data run loot replace entity @s inventory.$(inventory) loot {ns}:i/$(magazine_id)
$execute if score #wb_mag_given {ns}.data matches 0 run item replace entity @s inventory.$(inventory) with air

$function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}}
$execute if score #wb_mag_given {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}}
$execute if score #wb_mag_given {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}}

$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"hotbar.$(hotbar)"}}

scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/try_refill_owned", f"""
execute if score #wb_purchase_done {ns}.data matches 1 run return 0

function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.1"}}
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:1,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full

function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.2"}}
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:2,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full

function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.3"}}
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:3,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full
""")

	write_versioned_function("zombies/wallbuys/refill_already_full", f"""
scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 4
""")

	write_versioned_function("zombies/wallbuys/compute_effective_price", f"""
scoreboard players set #wb_price_locked {ns}.data 0
scoreboard players set #wb_price_mode {ns}.data 0

# Slot 1 refill candidate
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:1,weapon_id:"$(weapon_id)"}}
execute if score #wb_same_weapon {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.1"}}
execute if score #wb_price_locked {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run return run function {ns}:v{version}/zombies/wallbuys/select_refill_price {{hotbar:1}}

# Slot 2 refill candidate
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:2,weapon_id:"$(weapon_id)"}}
execute if score #wb_same_weapon {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.2"}}
execute if score #wb_price_locked {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run return run function {ns}:v{version}/zombies/wallbuys/select_refill_price {{hotbar:2}}

# Slot 3 refill candidate
$function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:3,weapon_id:"$(weapon_id)"}}
execute if score #wb_same_weapon {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.3"}}
execute if score #wb_price_locked {ns}.data matches 0 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run return run function {ns}:v{version}/zombies/wallbuys/select_refill_price {{hotbar:3}}
""")

	write_versioned_function("zombies/wallbuys/select_refill_price", f"""
# Default refill price
scoreboard players operation #wb_price {ns}.data = #wb_rfprice {ns}.data
scoreboard players set #wb_price_mode {ns}.data 1

# PAP refill price if weapon in this slot has pap_level > 0
scoreboard players set #wb_pap_level {ns}.data 0
$execute store result score #wb_pap_level {ns}.data run data get entity @s Inventory[{{Slot:$(hotbar)b}}].components."minecraft:custom_data".{ns}.stats.pap_level
execute if score #wb_pap_level {ns}.data matches 1.. run scoreboard players operation #wb_price {ns}.data = #wb_rfpap {ns}.data
execute if score #wb_pap_level {ns}.data matches 1.. run scoreboard players set #wb_price_mode {ns}.data 2

scoreboard players set #wb_price_locked {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/set_hover_price_suffix", f"""
data modify storage {ns}:temp _wb_price_suffix set value ""
execute if score #wb_price_mode {ns}.data matches 1 run data modify storage {ns}:temp _wb_price_suffix set value " (Refill)"
execute if score #wb_price_mode {ns}.data matches 2 run data modify storage {ns}:temp _wb_price_suffix set value " (PAP Refill)"
""")

	write_versioned_function("zombies/wallbuys/check_mag_not_full", f"""
scoreboard players set #wb_mag_not_full {ns}.data 0

# Missing paired mag counts as not full.
$execute unless items entity @s $(slot) *[custom_data~{mag_cd}] run scoreboard players set #wb_mag_not_full {ns}.data 1

tag @s add {ns}.wb_reading_mag
$execute if items entity @s $(slot) *[custom_data~{mag_cd}] summon minecraft:item_display run function {ns}:v{version}/zombies/wallbuys/read_mag_state {{slot:"$(slot)"}}
tag @s remove {ns}.wb_reading_mag

execute if score #wb_mag_rem {ns}.data < #wb_mag_cap {ns}.data run scoreboard players set #wb_mag_not_full {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/check_same_weapon_slot", f"""
scoreboard players set #wb_same_weapon {ns}.data 0
$execute store success score #wb_same_weapon {ns}.data run data get entity @s Inventory[{{Slot:$(slot)b}}].components."minecraft:custom_data".{ns}.$(weapon_id)
""")

	write_versioned_function("zombies/wallbuys/read_mag_state", f"""
$item replace entity @s contents from entity @p[tag={ns}.wb_reading_mag] $(slot)
execute store result score #wb_mag_rem {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.remaining_bullets
execute store result score #wb_mag_cap {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.capacity
kill @s
""")

	write_versioned_function("zombies/wallbuys/reload_pair", f"""
scoreboard players set #wb_new_mag {ns}.data 0
scoreboard players set #wb_mag_created {ns}.data 0
$execute unless items entity @s inventory.$(inventory) *[custom_data~{mag_cd}] run scoreboard players set #wb_new_mag {ns}.data 1
$execute if score #wb_new_mag {ns}.data matches 1 store success score #wb_mag_created {ns}.data run loot replace entity @s inventory.$(inventory) loot {ns}:i/$(magazine_id)
$execute if score #wb_new_mag {ns}.data matches 1 if score #wb_mag_created {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}}

$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"hotbar.$(hotbar)"}}
$execute if items entity @s inventory.$(inventory) *[custom_data~{mag_cd}] run function {ns}:v{version}/zombies/bonus/refill_magazine {{slot:"inventory.$(inventory)"}}

$function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}}
$execute if items entity @s inventory.$(inventory) *[custom_data~{mag_cd}] run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}}

scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 2
""")

	write_versioned_function("zombies/wallbuys/replace_selected", f"""
scoreboard players set #wb_valid_sel {ns}.data 0
execute store result score #wb_sel {ns}.data run data get entity @s SelectedItemSlot

execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.1"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:1,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 1 if items entity @s hotbar.1 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/replace_pair {{hotbar:1,inventory:1,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}

execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.2"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 run function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:2,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 2 if items entity @s hotbar.2 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/replace_pair {{hotbar:2,inventory:2,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}

execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 run function {ns}:v{version}/zombies/wallbuys/check_mag_not_full {{slot:"inventory.3"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 run function {ns}:v{version}/zombies/wallbuys/check_same_weapon_slot {{slot:3,weapon_id:"$(weapon_id)"}}
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/reload_pair {{hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}
execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 if score #wb_same_weapon {ns}.data matches 1 if score #wb_mag_not_full {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/refill_already_full
$execute if score #wb_purchase_done {ns}.data matches 0 if score #wb_sel {ns}.data matches 3 if items entity @s hotbar.3 *[custom_data~{gun_cd}] run function {ns}:v{version}/zombies/wallbuys/replace_pair {{hotbar:3,inventory:3,weapon_id:"$(weapon_id)",magazine_id:"$(magazine_id)"}}

execute if score #wb_purchase_done {ns}.data matches 0 run scoreboard players operation @s {ns}.zb.points += #wb_price {ns}.data
execute if score #wb_purchase_done {ns}.data matches 0 run function {ns}:v{version}/zombies/wallbuys/deny_hold_valid_slot
execute if score #wb_purchase_done {ns}.data matches 0 run scoreboard players set #wb_purchase_mode {ns}.data -1
""")

	write_versioned_function("zombies/wallbuys/deny_hold_valid_slot", f"""
execute if score @s {ns}.zb.perk.mule_kick matches 1.. run tellraw @s [{MGS_TAG},{{"text":"Hold weapon slot 1, 2, or 3 to swap your current gun.","color":"red"}}]
execute unless score @s {ns}.zb.perk.mule_kick matches 1.. run tellraw @s [{MGS_TAG},{{"text":"Hold weapon slot 1 or 2 to swap your current gun.","color":"red"}}]
{ZombiesFeedback.zb_sound('deny')}
""")

	write_versioned_function("zombies/wallbuys/replace_pair", f"""
$loot replace entity @s hotbar.$(hotbar) loot {ns}:i/$(weapon_id)

scoreboard players set #wb_mag_given {ns}.data 0
$execute store success score #wb_mag_given {ns}.data run loot replace entity @s inventory.$(inventory) loot {ns}:i/$(magazine_id)
$execute if score #wb_mag_given {ns}.data matches 0 run item replace entity @s inventory.$(inventory) with air

$function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.$(hotbar)",group:"hotbar",index:$(hotbar)}}
$execute if score #wb_mag_given {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}}
$execute if score #wb_mag_given {ns}.data matches 1 run function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}}

$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"hotbar.$(hotbar)"}}

scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 3
""")

