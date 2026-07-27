""" Finding a magazine in the inventory and spending it, whole or partially. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import BASE_WEAPON, CAPACITY, REMAINING_BULLETS, SINGLE_RELOAD


# Functions
def write_magazine_consumption() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Find and consume magazines from inventory
	magazine_custom_data: str = f"""{{{ns}:{{"magazine":true,"weapon":"$({BASE_WEAPON})"}}}}"""
	slot_checks: str = ""
	for slot in ItemBuilder.ALL_SLOTS:
		slot_checks += (
			f"$execute if score #found_ammo {ns}.data < #capacity {ns}.data if items entity @s {slot} *[custom_data~{magazine_custom_data}] run "
			f"""function {ns}:v{version}/ammo/inventory/process_slot {{slot:"{slot}",{BASE_WEAPON}:"$({BASE_WEAPON})"}}\n"""
		)
	write_versioned_function("ammo/inventory/find", f"""
# Get capacity and initialize found ammo to current remaining bullets
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute store result score #initial_ammo {ns}.data run scoreboard players get @s {ns}.{REMAINING_BULLETS}
scoreboard players operation #found_ammo {ns}.data = #initial_ammo {ns}.data

# Single-shell reload: cap the fill target to current + 1 so only one bullet is loaded per cycle
execute if data storage {ns}:gun all.stats.{SINGLE_RELOAD} run scoreboard players operation #single_target {ns}.data = #initial_ammo {ns}.data
execute if data storage {ns}:gun all.stats.{SINGLE_RELOAD} run scoreboard players add #single_target {ns}.data 1
execute if data storage {ns}:gun all.stats.{SINGLE_RELOAD} if score #capacity {ns}.data > #single_target {ns}.data run scoreboard players operation #capacity {ns}.data = #single_target {ns}.data

# Check all slots for magazines
{slot_checks}

# If found ammo, compute reserve ammo and return success, else return fail
execute unless score @s {ns}.{REMAINING_BULLETS} = #initial_ammo {ns}.data run return run function {ns}:v{version}/ammo/compute_reserve
return fail
""")

	write_versioned_function("ammo/inventory/process_slot", f"""
# Get bullets from the magazine
tag @s add {ns}.extracting_bullets
$execute summon item_display run function {ns}:v{version}/ammo/extract_bullets {{slot:"$(slot)"}}
tag @s remove {ns}.extracting_bullets
execute if score #bullets {ns}.data matches 0 run return 0

# Calculate to_take = min(bullets, capacity - found_ammo)
scoreboard players operation #to_take {ns}.data = #capacity {ns}.data
scoreboard players operation #to_take {ns}.data -= #found_ammo {ns}.data
execute if score #bullets {ns}.data < #to_take {ns}.data run scoreboard players operation #to_take {ns}.data = #bullets {ns}.data

# Add to found_ammo
scoreboard players operation #found_ammo {ns}.data += #to_take {ns}.data

# Subtract from bullets
scoreboard players operation #bullets {ns}.data -= #to_take {ns}.data

# If the magazine is consumable and fully depleted, clear the slot and return
# If the magazine is consumable but still has items, update the stack count and return
$execute if score #bullets {ns}.data matches ..0 if items entity @s $(slot) *[custom_data~{{{ns}:{{consumable:true}}}}] run return run function {ns}:v{version}/ammo/inventory/consume_slot {{slot:"$(slot)"}}
$execute if score #bullets {ns}.data matches 1.. if items entity @s $(slot) *[custom_data~{{{ns}:{{consumable:true}}}}] run return run function {ns}:v{version}/ammo/inventory/consume_partial {{slot:"$(slot)"}}

# Modify the magazine item
$execute if score #bullets {ns}.data matches ..0 run function {ns}:v{version}/ammo/inventory/set_item_model {{slot:"$(slot)",{BASE_WEAPON}:"$({BASE_WEAPON})"}}
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run scoreboard players get #bullets {ns}.data
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

# Update magazine lore
$function {ns}:v{version}/ammo/modify_mag_lore {{slot:"$(slot)"}}

# Update player's ammo count
scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #found_ammo {ns}.data
""")
	write_versioned_function("ammo/inventory/set_item_model", f"""
$item modify entity @s $(slot) {{function:"minecraft:set_components", components:{{"minecraft:item_model":"{ns}:$({BASE_WEAPON})_mag_empty"}}}}
""")

	# Consume a consumable magazine fully (clear it from inventory)
	write_versioned_function("ammo/inventory/consume_slot", f"""
# Clear the fully depleted consumable magazine from the slot
$item replace entity @s $(slot) with air

# Update player's ammo count
scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #found_ammo {ns}.data
""")

	# Partially consume a consumable magazine stack (reduce count, keep remaining)
	write_versioned_function("ammo/inventory/consume_partial", f"""
# Set the stack count to the remaining bullets (#bullets = remaining items in stack)
$item modify entity @s $(slot) {ns}:v{version}/set_consumable_count

# Update player's ammo count
scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #found_ammo {ns}.data
""")

	write_versioned_function("ammo/extract_bullets", f"""
# Copy item to entity
$item replace entity @s contents from entity @p[tag={ns}.extracting_bullets] $(slot)

# For consumable magazines (1b = true consumable), the stack count IS the bullet count (each item = 1 bullet)
# For regular/converted magazines, read remaining_bullets from custom data
execute if data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}} store result score #bullets {ns}.data run data get entity @s item.count
execute unless data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}} store result score #bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS}

# Get magazine capacity
execute store result storage {ns}:temp {CAPACITY} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}

# Kill entity
kill @s
""")

	write_versioned_function("ammo/end_reload", f"""
# Actually consume magazines and update ammo now that reload is complete
# (single-shell weapons only load one bullet per cycle, even in no_magazine mode)
execute if data storage {ns}:config no_magazine unless data storage {ns}:gun all.stats.{SINGLE_RELOAD} store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{CAPACITY}
execute if data storage {ns}:config no_magazine if data storage {ns}:gun all.stats.{SINGLE_RELOAD} run function {ns}:v{version}/ammo/single_reload_add_one
execute unless data storage {ns}:config no_magazine run function {ns}:v{version}/ammo/inventory/find with storage {ns}:gun all.stats

# Update weapon lore (if still holding weapon)
execute if data storage {ns}:gun all.gun run function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}

# Remove reloading tag
tag @s remove {ns}.reloading

# Single-shell reload: chain into the next shell unless full, out of ammo, or the player is firing
execute if data storage {ns}:gun all.stats.{SINGLE_RELOAD} run function {ns}:v{version}/ammo/single_reload_continue
""")

