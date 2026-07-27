""" Tagging an item with its slot, and putting anything found in the wrong one back. """
# ruff: noqa: E501
# Imports
from stewbeet import ItemModifier, JsonDict, Mem, set_json_encoder, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import CAPACITY, REMAINING_BULLETS


# Functions
def write_slot_enforcement() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	zb_tagged_cd = "{" + ns + ":{zombies:{}}}"
	zb_tagged_match = f"*[custom_data~{zb_tagged_cd}]"

	zb_stats_modifier: JsonDict = {
		"function": "minecraft:copy_custom_data",
		"source": {"type": "minecraft:storage", "source": f"{ns}:temp"},
		"ops": [
			{"source": f"zb_item_stats.{CAPACITY}", "target": f"{ns}.stats.{CAPACITY}", "op": "replace"},
			{"source": f"zb_item_stats.{REMAINING_BULLETS}", "target": f"{ns}.stats.{REMAINING_BULLETS}", "op": "replace"},
		],
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_item_stats"] = set_json_encoder(ItemModifier(zb_stats_modifier), max_level=-1)

	zb_slot_modifier: JsonDict = {
		"function": "minecraft:copy_custom_data",
		"source": {"type": "minecraft:storage", "source": f"{ns}:temp"},
		"ops": [
			{"source": "zb_slot", "target": f"{ns}.zombies", "op": "replace"},
		],
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_slot_tag"] = set_json_encoder(ItemModifier(zb_slot_modifier), max_level=-1)

	# Marks a magazine as zombies-converted by setting consumable to 2b.
	# Value 1b = true consumable (stack count = bullets), 2b = zombies non-consumable (custom_data only).
	zb_mark_converted_modifier: list[JsonDict] = [
		{
			"function": "minecraft:set_custom_data",
			"tag": f'{{{ns}: {{consumable: 2b}}}}',
		},
		{
			"function": "minecraft:set_components",
			"components": {"minecraft:max_stack_size": 1}
		}
	]
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_mark_converted"] = set_json_encoder(ItemModifier(zb_mark_converted_modifier), max_level=-1) # type: ignore

	all_slot_scans: str = ""
	for slot in ItemBuilder.ALL_SLOTS:
		all_slot_scans += (
			f'$execute if score #zb_inv_found {ns}.data matches 0 if items entity @s {slot} $(match) '
			f'run function {ns}:v{version}/zombies/inventory/move_found_slot {{from:"{slot}",to:"$(slot)"}}\n'
		)

	write_versioned_function("zombies/inventory/apply_slot_tag", f"""
data modify storage {ns}:temp zb_slot set value {{}}
$data modify storage {ns}:temp zb_slot.$(group) set value $(index)
$item modify entity @s $(slot) {ns}:v{version}/zb_slot_tag
""")

	write_versioned_function("zombies/inventory/read_capacity", f"""
$item replace entity @s contents from entity @p[tag={ns}.zb_scaling_mag] $(slot)
$execute store result score #zb_cap {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY} $(multiplier)
kill @s
""")

	write_versioned_function("zombies/inventory/scale_magazine_slot", f"""
# Read capacity from the paired weapon at hotbar.$(index) (inventory.N always pairs with hotbar.N)
tag @s add {ns}.zb_scaling_mag
$execute summon item_display run function {ns}:v{version}/zombies/inventory/read_capacity {{slot:"hotbar.$(index)",multiplier:6}}
tag @s remove {ns}.zb_scaling_mag

# Write capacity and starting ammo into custom_data
execute store result storage {ns}:temp zb_item_stats.{CAPACITY} int 1 run scoreboard players get #zb_cap {ns}.data
$execute store result storage {ns}:temp zb_item_stats.{REMAINING_BULLETS} int $(remaining_multiplier) run scoreboard players get #zb_cap {ns}.data
$item modify entity @s $(slot) {ns}:v{version}/zb_item_stats

# Mark as zombies-converted (consumable=2b): ammo.py reads remaining_bullets instead of stack count.
$item modify entity @s $(slot) {ns}:v{version}/zb_mark_converted

# Force count to 1 (consumable magazines used stack count as ammo, now using custom_data)
scoreboard players set #bullets {ns}.data 1
$item modify entity @s $(slot) {ns}:v{version}/set_consumable_count

# Update magazine lore to show new ammo count
data modify storage {ns}:temp {CAPACITY} set from storage {ns}:temp zb_item_stats.{CAPACITY}
execute store result score #bullets {ns}.data run data get storage {ns}:temp zb_item_stats.{REMAINING_BULLETS}
$function {ns}:v{version}/ammo/modify_mag_lore {{slot:"$(slot)"}}
""")

	write_versioned_function("zombies/inventory/enforce_slot", f"""
$execute if items entity @s $(slot) $(match) run return 1

# Scan all inventory slots for the correct item and swap it into place
scoreboard players set #zb_inv_found {ns}.data 0
{all_slot_scans}
execute if score #zb_inv_found {ns}.data matches 1 run return 1

# Not found in any slot: drop wrong zombies item from target slot if present, then try ground pickup
$execute if items entity @s $(slot) {zb_tagged_match} run function {ns}:v{version}/zombies/inventory/drop_wrong_slot_item {{slot:"$(slot)"}}

tag @s add {ns}.inv_slot_owner
$execute as @e[type=item,distance=..8,nbt={{Item:{{components:{{"minecraft:custom_data":$(expected_nbt)}}}}}}] on origin if entity @s[tag={ns}.inv_slot_owner] run function {ns}:v{version}/zombies/inventory/try_pick_dropped_item {{slot:"$(slot)",expected_nbt:$(expected_nbt)}}
tag @s remove {ns}.inv_slot_owner

return 0
""")

	write_versioned_function("zombies/inventory/move_found_slot", f"""
# Swap source and target via temp item_display (handles empty target too)
tag @s add {ns}.inv_swapping
$execute summon item_display run function {ns}:v{version}/zombies/inventory/swap_slots {{from:"$(from)",to:"$(to)"}}
tag @s remove {ns}.inv_swapping
scoreboard players set #zb_inv_found {ns}.data 1
""")

	write_versioned_function("zombies/inventory/swap_slots", f"""
# @s = temp item_display, player = @p[tag={ns}.inv_swapping]
# Save target item to temp display
$item replace entity @s contents from entity @p[tag={ns}.inv_swapping] $(to)
# Move source to target
$item replace entity @p[tag={ns}.inv_swapping] $(to) from entity @p[tag={ns}.inv_swapping] $(from)
# Put old target item (from display) into source, or clear source if target was empty
$execute if items entity @s contents * run item replace entity @p[tag={ns}.inv_swapping] $(from) from entity @s contents
$execute unless items entity @s contents * run item replace entity @p[tag={ns}.inv_swapping] $(from) with air
kill @s
""")

	write_versioned_function("zombies/inventory/drop_wrong_slot_item", f"""
tag @s add {ns}.inv_slot_owner
summon minecraft:item ~ ~ ~ {{Item:{{id:"minecraft:stone",count:1}},Tags:["{ns}.inv_new_drop"]}}
$execute as @n[type=item,tag={ns}.inv_new_drop,distance=..1] run function {ns}:v{version}/zombies/inventory/copy_slot_item_to_drop {{slot:"$(slot)"}}
tag @s remove {ns}.inv_slot_owner
$item replace entity @s $(slot) with air
""")

	write_versioned_function("zombies/inventory/copy_slot_item_to_drop", f"""
$item replace entity @s contents from entity @p[tag={ns}.inv_slot_owner] $(slot)
data modify entity @s PickupDelay set value 0s
data modify entity @s Thrower set from entity @p[tag={ns}.inv_slot_owner] UUID
data modify entity @s Owner set from entity @s Thrower
tag @s remove {ns}.inv_new_drop
""")

	write_versioned_function("zombies/inventory/try_pick_dropped_item", f"""
$execute if score #zb_inv_found {ns}.data matches 0 run item replace entity @p[tag={ns}.inv_slot_owner] $(slot) from entity @n[type=item,distance=..8,nbt={{Item:{{components:{{"minecraft:custom_data":$(expected_nbt)}}}}}}] contents
$execute if score #zb_inv_found {ns}.data matches 0 run kill @n[type=item,distance=..8,nbt={{Item:{{components:{{"minecraft:custom_data":$(expected_nbt)}}}}}}]
scoreboard players set #zb_inv_found {ns}.data 1
""")

