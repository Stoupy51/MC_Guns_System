""" The inventory-changed advancement, the slot audit it triggers and the game tick. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import FunctionalHelpers
from ...common import ZombiesCommon
from .shared import SlotPredicates, slot_predicates


# Functions
def write_inventory_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	gun_cd: str = ZombiesCommon.gun_cd(ns)
	mag_cd = "{" + ns + ":{magazine:true}}"
	slots: SlotPredicates = slot_predicates(ns)
	# Zombies keeps vanilla reach: its knife is the fallback weapon once ammo runs out
	knife_item = FunctionalHelpers.knife_item_snbt(ns)

	write_versioned_function("zombies/inventory/on_change", f"""
advancement revoke @s only {ns}:v{version}/zombies/inventory_changed
execute unless score @s {ns}.zb.in_game matches 1 run return fail
execute if data storage {ns}:zombies game{{state:"lobby"}} run return fail
execute if data storage {ns}:zombies game{{state:"ended"}} run return fail

# Prevent recursive re-entry (item replace in swap/enforce can re-trigger inventory_changed)
execute if entity @s[tag={ns}.inv_checking] run return fail
tag @s add {ns}.inv_checking
function {ns}:v{version}/zombies/inventory/check_slots
tag @s remove {ns}.inv_checking
""")

	write_versioned_function("zombies/inventory/check_slots", f"""
# hard forbidden slot
execute if items entity @s hotbar.5 * run function {ns}:v{version}/zombies/inventory/drop_wrong_slot_item {{slot:"hotbar.5"}}

# Always-enforced slots
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.8",match:"*[custom_data~{slots.info}]",expected_nbt:{slots.info}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.7",match:"*[custom_data~{slots.equipment_1}]",expected_nbt:{slots.equipment_1}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.6",match:"*[custom_data~{slots.equipment_2}]",expected_nbt:{slots.equipment_2}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.2",match:"*[custom_data~{slots.gun_2}]",expected_nbt:{slots.gun_2}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.1",match:"*[custom_data~{slots.gun_1}]",expected_nbt:{slots.gun_1}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.0",match:"*[custom_data~{slots.knife}]",expected_nbt:{slots.knife}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"inventory.1",match:"*[custom_data~{slots.mag_1}]",expected_nbt:{slots.mag_1}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"inventory.2",match:"*[custom_data~{slots.mag_2}]",expected_nbt:{slots.mag_2}}}

# Mule kick gates the third weapon/magazine slots only.
execute if score @s {ns}.zb.perk.mule_kick matches 1 run function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.3",match:"*[custom_data~{slots.gun_3}]",expected_nbt:{slots.gun_3}}}
execute if score @s {ns}.zb.perk.mule_kick matches 1 run function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"inventory.3",match:"*[custom_data~{slots.mag_3}]",expected_nbt:{slots.mag_3}}}
execute unless score @s {ns}.zb.perk.mule_kick matches 1 run item replace entity @s hotbar.3 with air
execute unless score @s {ns}.zb.perk.mule_kick matches 1 run item replace entity @s inventory.3 with air

# Ability slot is only for manual abilities (automatic abilities such as coward should not show item)
execute if score @s {ns}.zb.ability matches 3.. run function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.4",match:"*[custom_data~{slots.ability}]",expected_nbt:{slots.ability}}}
execute unless score @s {ns}.zb.ability matches 3.. run item replace entity @s hotbar.4 with air

# Clear cursor (prevent dragging tagged items outside managed inventory)
execute if items entity @s player.cursor * run function {ns}:v{version}/zombies/inventory/drop_wrong_slot_item {{slot:"player.cursor"}}

# Clean orphaned magazines (gun lost in PAP but magazine remains) — skip slots actively in PAP
execute unless score @s {ns}.zb.pap_s matches 1 unless items entity @s hotbar.1 *[custom_data~{gun_cd}] if items entity @s inventory.1 *[custom_data~{mag_cd}] run item replace entity @s inventory.1 with air
execute unless score @s {ns}.zb.pap_s matches 2 unless items entity @s hotbar.2 *[custom_data~{gun_cd}] if items entity @s inventory.2 *[custom_data~{mag_cd}] run item replace entity @s inventory.2 with air
execute unless score @s {ns}.zb.pap_s matches 3 unless items entity @s hotbar.3 *[custom_data~{gun_cd}] if items entity @s inventory.3 *[custom_data~{mag_cd}] run item replace entity @s inventory.3 with air
""")

	write_versioned_function("zombies/game_tick", f"""
# Refresh player info item every 5 seconds (100 ticks)
scoreboard players add #zb_info_timer {ns}.data 1
execute if score #zb_info_timer {ns}.data matches 100.. run scoreboard players set #zb_info_timer {ns}.data 0
execute if score #zb_info_timer {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] if items entity @s hotbar.8 *[custom_data~{slots.info}] run function {ns}:v{version}/zombies/inventory/refresh_info_item
""")

	write_versioned_function("zombies/inventory/on_new_item", f"""
# Kill any non-zombies-slot managed drop from zombies players (@s = the item entity).
# Both item checks MUST run before `on origin`: past it @s is the thrower, so a check on @s Item
# always passed and `kill @s` killed the PLAYER instead of the drop (grenade drop = instant death).
execute unless data entity @s Item.components."minecraft:custom_data".{ns} run return 0
execute if data entity @s Item.components."minecraft:custom_data".{ns}.zombies run return 0

# Thrown by an in-game zombies player? -> the drop is unmanaged, remove it
scoreboard players set #zb_drop_kill {ns}.data 0
execute on origin if score @s {ns}.zb.in_game matches 1 run scoreboard players set #zb_drop_kill {ns}.data 1
execute if score #zb_drop_kill {ns}.data matches 1 run kill @s
""", tags=["common_signals:signals/on_new_item"])

	write_versioned_function("zombies/inventory/recreate_critical_items", f"""
execute unless items entity @s hotbar.0 *[custom_data~{slots.knife}] run item replace entity @s hotbar.0 with {knife_item}
execute unless items entity @s hotbar.0 *[custom_data~{slots.knife}] run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.0",group:"hotbar",index:0}}

execute unless items entity @s hotbar.7 *[custom_data~{slots.equipment_1}] run function {ns}:v{version}/zombies/inventory/loot_replace_lethal
execute unless items entity @s hotbar.7 *[custom_data~{slots.equipment_1}] run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}

execute unless items entity @s hotbar.8 *[custom_data~{slots.info}] run function {ns}:v{version}/zombies/inventory/refresh_info_item
""")

