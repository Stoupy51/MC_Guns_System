""" Finding a magazine in the inventory and spending it, whole or partially. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import (
	BASE_WEAPON,
	CAPACITY,
	REMAINING_BULLETS,
	SINGLE_RELOAD,
)


# Functions
def write_magazine_consumption() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	magazine_custom_data: str = f"""{{{ns}:{{"magazine":true,"weapon":"$({BASE_WEAPON})"}}}}"""
	slot_checks: str = ""
	for slot in ItemBuilder.ALL_SLOTS:
		slot_checks += (
			f"$execute if score #found_ammo {ns}.data < #capacity {ns}.data if items entity @s {slot} *[custom_data~{magazine_custom_data}] run "
			f"""function {ns}:v{version}/ammo/inventory/process_slot {{slot:"{slot}",{BASE_WEAPON}:"$({BASE_WEAPON})"}}\n"""
		)
	write_versioned_function("ammo/inventory/find", f"""
# Found ammo starts at the remaining bullets.
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute store result score #initial_ammo {ns}.data run scoreboard players get @s {ns}.{REMAINING_BULLETS}
scoreboard players operation #found_ammo {ns}.data = #initial_ammo {ns}.data

# Single-shell reload: one bullet per cycle.
execute if data storage {ns}:gun all.stats.{SINGLE_RELOAD} run scoreboard players operation #single_target {ns}.data = #initial_ammo {ns}.data
execute if data storage {ns}:gun all.stats.{SINGLE_RELOAD} run scoreboard players add #single_target {ns}.data 1
execute if data storage {ns}:gun all.stats.{SINGLE_RELOAD} if score #capacity {ns}.data > #single_target {ns}.data run scoreboard players operation #capacity {ns}.data = #single_target {ns}.data

{slot_checks}

# Ammo found: compute the reserve and succeed.
execute unless score @s {ns}.{REMAINING_BULLETS} = #initial_ammo {ns}.data run return run function {ns}:v{version}/ammo/compute_reserve
return fail
""")

	write_versioned_function("ammo/inventory/process_slot", f"""
tag @s add {ns}.extracting_bullets
$execute summon item_display run function {ns}:v{version}/ammo/extract_bullets {{slot:"$(slot)"}}
tag @s remove {ns}.extracting_bullets
execute if score #bullets {ns}.data matches 0 run return 0

# to_take = min(bullets, capacity - found_ammo)
scoreboard players operation #to_take {ns}.data = #capacity {ns}.data
scoreboard players operation #to_take {ns}.data -= #found_ammo {ns}.data
execute if score #bullets {ns}.data < #to_take {ns}.data run scoreboard players operation #to_take {ns}.data = #bullets {ns}.data

scoreboard players operation #found_ammo {ns}.data += #to_take {ns}.data

scoreboard players operation #bullets {ns}.data -= #to_take {ns}.data

# Consumables: an emptied stack clears the slot, otherwise the stack count drops.
$execute if score #bullets {ns}.data matches ..0 if items entity @s $(slot) *[custom_data~{{{ns}:{{consumable:true}}}}] run return run function {ns}:v{version}/ammo/inventory/consume_slot {{slot:"$(slot)"}}
$execute if score #bullets {ns}.data matches 1.. if items entity @s $(slot) *[custom_data~{{{ns}:{{consumable:true}}}}] run return run function {ns}:v{version}/ammo/inventory/consume_partial {{slot:"$(slot)"}}

$execute if score #bullets {ns}.data matches ..0 run function {ns}:v{version}/ammo/inventory/set_item_model {{slot:"$(slot)",{BASE_WEAPON}:"$({BASE_WEAPON})"}}
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run scoreboard players get #bullets {ns}.data
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

$function {ns}:v{version}/ammo/modify_mag_lore {{slot:"$(slot)"}}

scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #found_ammo {ns}.data
""")
	write_versioned_function("ammo/inventory/set_item_model", f"""
$item modify entity @s $(slot) {{type:"minecraft:set_components", components:{{"minecraft:item_model":"{ns}:$({BASE_WEAPON})_mag_empty"}}}}
""")

	write_versioned_function("ammo/inventory/consume_slot", f"""
$item replace entity @s $(slot) with air

scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #found_ammo {ns}.data
""")

	write_versioned_function("ammo/inventory/consume_partial", f"""
# #bullets is the items left in the stack.
$item modify entity @s $(slot) {ns}:v{version}/set_consumable_count

scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #found_ammo {ns}.data
""")

	write_versioned_function("ammo/extract_bullets", f"""
$item replace entity @s contents from entity @p[tag={ns}.extracting_bullets] $(slot)

# A consumable (1b) counts one bullet per item; regular and converted magazines read remaining_bullets.
execute if data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}} store result score #bullets {ns}.data run data get entity @s item.count
execute unless data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}} store result score #bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS}

execute store result storage {ns}:temp {CAPACITY} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}

kill @s
""")

	write_versioned_function("ammo/end_reload", f"""
# The reload is complete: consume magazines now (single-shell weapons load one bullet per cycle, even with no_magazine).
execute if data storage {ns}:config no_magazine unless data storage {ns}:gun all.stats.{SINGLE_RELOAD} store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{CAPACITY}
execute if data storage {ns}:config no_magazine if data storage {ns}:gun all.stats.{SINGLE_RELOAD} run function {ns}:v{version}/ammo/single_reload_add_one
execute unless data storage {ns}:config no_magazine run function {ns}:v{version}/ammo/inventory/find with storage {ns}:gun all.stats

execute if data storage {ns}:gun all.gun run function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}

tag @s remove {ns}.reloading

# Next shell unless full, out of ammo, or firing.
execute if data storage {ns}:gun all.stats.{SINGLE_RELOAD} run function {ns}:v{version}/ammo/single_reload_continue
""")

