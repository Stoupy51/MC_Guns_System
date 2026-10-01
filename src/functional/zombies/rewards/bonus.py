""" Bonus effects granted by power-ups, such as Max Ammo refills. """
# Imports
from stewbeet import Mem, write_function, write_versioned_function

from ....config.stats.items import ItemBuilder
from ....config.stats.keys import BASE_WEAPON, CAPACITY, REMAINING_BULLETS


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Max Ammo: refill every magazine to capacity.

	magazine_custom_data: str = f"{{{ns}:{{magazine:true}}}}"
	slot_checks: str = ""
	for slot in ItemBuilder.ALL_SLOTS:
		slot_checks += f'execute if items entity @s {slot} *[custom_data~{magazine_custom_data}] run function {ns}:v{version}/zombies/bonus/refill_magazine {{slot:"{slot}"}}\n'

	gun_custom_data: str = f"{{{ns}:{{gun:true}}}}"
	weapon_slot_checks: str = ""
	for slot in ItemBuilder.ALL_SLOTS:
		weapon_slot_checks += f'execute if items entity @s {slot} *[custom_data~{gun_custom_data}] run function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"{slot}"}}\n'

	# Entry point: /execute as <player> run function mgs:zombies/bonus/max_ammo
	write_function(f"{ns}:zombies/bonus/max_ammo", f"""
# Needed for the ammo score sync.
function {ns}:v{version}/utils/copy_gun_data

{slot_checks}
# #max_ammo_reload_weapons: 1 also reloads weapons (recent zombies), 0 only refills magazines (OG).
execute if score #max_ammo_reload_weapons {ns}.config matches 1.. run function {ns}:v{version}/zombies/bonus/max_ammo_reload_weapons

function {ns}:v{version}/zombies/bonus/max_ammo_grenades

function {ns}:v{version}/ammo/compute_reserve
""")

	# Grenades use the item count, not a magazine, so the passes above never refill them.
	write_versioned_function("zombies/bonus/max_ammo_grenades", f"""
# Tactical slot (hotbar.6, Monkey Bombs): back to 3, never granted from an empty slot (tacticals only come from the Mystery Box or a wall-buy).
execute if items entity @s hotbar.6 *[custom_data~{{{ns}:{{gun:true}}}}] run item modify entity @s hotbar.6 {ns}:v{version}/grenade/set_count_3

# Lethal slot (hotbar.7): back to 4.
execute if items entity @s hotbar.7 *[custom_data~{{{ns}:{{gun:true}}}}] run return run item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_4

# Empty lethal slot: 4 of the bought lethal type (semtex stays semtex); give_lethal_type re-tags the slot.
execute unless items entity @s hotbar.7 * run function {ns}:v{version}/zombies/inventory/give_lethal_type {{count:4}}
""")

	write_versioned_function("zombies/bonus/max_ammo_reload_weapons", f"""
{weapon_slot_checks}
execute if data storage {ns}:gun all.gun store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{CAPACITY}
""")

	write_versioned_function("zombies/bonus/reload_weapon_slot", f"""
tag @s add {ns}.reloading_weapon
$execute summon item_display run function {ns}:v{version}/zombies/bonus/extract_weapon_capacity {{slot:"$(slot)"}}
tag @s remove {ns}.reloading_weapon

# Saved so reloading a slot that is not in hand leaves the HUD of the held weapon alone.
scoreboard players operation #rws_save {ns}.data = @s {ns}.{REMAINING_BULLETS}

# modify_lore reads this score.
scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #bullets {ns}.data

# The held weapon (remaining_bullets -1) keeps its ammo in the score, so only its lore changes.
$execute if items entity @s $(slot) *[custom_data~{{{ns}:{{stats:{{{REMAINING_BULLETS}:-1}}}}}}] run return run function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}

$item modify entity @s $(slot) {ns}:v{version}/update_ammo

$function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}

scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #rws_save {ns}.data
""")

	# Run as a temporary item_display.
	write_versioned_function("zombies/bonus/extract_weapon_capacity", f"""
$item replace entity @s contents from entity @p[tag={ns}.reloading_weapon] $(slot)

execute store result score #bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}

data modify storage {ns}:temp components set from entity @s item.components

kill @s
""")

	write_versioned_function("zombies/bonus/refill_magazine", f"""
tag @s add {ns}.refilling_mag
scoreboard players set #stack_size {ns}.data 1
$execute summon item_display run function {ns}:v{version}/zombies/bonus/extract_mag_data {{slot:"$(slot)"}}
tag @s remove {ns}.refilling_mag

# Consumable magazines hold their ammo as the stack count.
execute if score #stack_size {ns}.data matches 2.. run scoreboard players operation #bullets {ns}.data = #stack_size {ns}.data
$execute if score #stack_size {ns}.data matches 2.. run return run item modify entity @s $(slot) {ns}:v{version}/set_consumable_count
execute if score #stack_size {ns}.data matches 2.. run scoreboard players set #bullets {ns}.data 1

$item modify entity @s $(slot) {ns}:v{version}/update_ammo
execute if score #stack_size {ns}.data matches 1 run function {ns}:v{version}/zombies/bonus/set_full_mag_model with storage {ns}:temp refill
$function {ns}:v{version}/ammo/modify_mag_lore {{slot:"$(slot)"}}
""")

	# Run as a temporary item_display.
	write_versioned_function("zombies/bonus/extract_mag_data", f"""
$item replace entity @s contents from entity @p[tag={ns}.refilling_mag] $(slot)

# Consumables read their max_stack_size (64 by default).
execute store success score #is_consumable {ns}.data if data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}}
execute if score #is_consumable {ns}.data matches 1 run scoreboard players set #stack_size {ns}.data 64
execute if score #is_consumable {ns}.data matches 1 if data entity @s item.components."minecraft:max_stack_size" store result score #stack_size {ns}.data run data get entity @s item.components."minecraft:max_stack_size"

execute store result score #bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
execute store result storage {ns}:temp {CAPACITY} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}

# For the model update macro.
data modify storage {ns}:temp refill set value {{}}
$data modify storage {ns}:temp refill.slot set value "$(slot)"
data modify storage {ns}:temp refill.{BASE_WEAPON} set from entity @s item.components."minecraft:custom_data".{ns}.weapon
data modify storage {ns}:temp refill.mag_model set from entity @s item.components."minecraft:item_model"

kill @s
""")

	write_versioned_function("zombies/bonus/set_full_mag_model", r"""
$item modify entity @s $(slot) {"type":"minecraft:set_components", "components":{"minecraft:item_model":"$(mag_model)"}}
""")

	## Nuke: kill every nukable entity, one per tick.

	# Entry point: /function mgs:zombies/bonus/nuke. It needs no executor, so a nuke grabbed by a downed (spectating) player still clears the map.
	write_function(f"{ns}:zombies/bonus/nuke", f"""
# Marked entities lose their attack damage at once, so those waiting in the loop can no longer hurt anyone.
execute as @e[tag={ns}.nukable] run function {ns}:v{version}/zombies/bonus/nuke_mark_one

function {ns}:v{version}/zombies/bonus/nuke_loop
""")

	# Run as a nukable entity.
	write_versioned_function("zombies/bonus/nuke_mark_one", f"""
tag @s add {ns}.nuked
attribute @s minecraft:attack_damage modifier add {ns}:nuke_zero_damage -1 add_multiplied_total
""")

	write_versioned_function("zombies/bonus/nuke_loop", f"""
execute as @n[tag={ns}.nuked,sort=random] at @s run function {ns}:v{version}/zombies/bonus/nuke_damage_one

execute if entity @e[tag={ns}.nuked] run schedule function {ns}:v{version}/zombies/bonus/nuke_loop 1t
""")

	# Run as a nuked entity, at it.
	write_versioned_function("zombies/bonus/nuke_damage_one", f"""
tag @s remove {ns}.nuked

attribute @s minecraft:attack_damage modifier remove {ns}:nuke_zero_damage

# No player attacker, so nuke kills do not pay kill points (the Nuke pays a flat bonus).
damage @s 999999 {ns}:bullet
""")

