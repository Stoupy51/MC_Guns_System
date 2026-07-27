""" The starting and respawn loadouts, and restoring a saved inventory slot by slot. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers.content import SharedContent


# Functions
def write_zombies_loadout() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Zombies keeps vanilla reach: its knife is the fallback weapon once ammo runs out
	knife_item = SharedContent.knife_item_snbt(ns)

	write_versioned_function("zombies/inventory/give_starting_loadout", f"""
clear @s

# hotbar.0: knife
item replace entity @s hotbar.0 with {knife_item}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.0",group:"hotbar",index:0}}

# hotbar.1 + inventory.1: starting weapon and scaled magazine
loot replace entity @s hotbar.1 loot {ns}:i/m1911
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.1",group:"hotbar",index:1}}

loot replace entity @s inventory.1 loot {ns}:i/m1911_mag
function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.1",index:1,remaining_multiplier:0.5}}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.1",group:"inventory",index:1}}

# hotbar.7: main equipment (frag by default). Record the lethal type so an empty slot later
# refills with frag (index 0), not some stale value from a previous life.
loot replace entity @s hotbar.7 loot {ns}:i/frag_grenade
item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_4
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}
scoreboard players set @s {ns}.zb.lethal_type 0

# hotbar.8: info item
function {ns}:v{version}/zombies/inventory/refresh_info_item

# hotbar.4: only for manual abilities (automatic abilities must not show this item)
execute if score @s {ns}.zb.ability matches 3.. run function {ns}:v{version}/zombies/inventory/give_ability_item
""")

	write_versioned_function("zombies/inventory/give_respawn_loadout", f"""
function {ns}:v{version}/zombies/inventory/give_starting_loadout

# Bleed-out respawns come back lighter than a fresh game start: knife + M1911 + only 2 frags.
# The starting-loadout clear also strips any bought knife/grenade-type/tactical (intended).
item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_2
""")

	# Inventory snapshot restore, used by the Who's Who body revive and Tombstone recovery.
	# Players cannot be data-modified, so a stored Inventory snapshot is given back one stack at a time.
	# Each entry is loaded into a single-slot shuttle item_display, then `item replace`d into its ORIGINAL slot.
	# Hotbar and main go through a container.N macro; armor and offhand use their named slots.
	# Entry point: @s = the player (executed at them).
	# Caller fills storage {ns}:temp _restore.items with a copied player Inventory NBT list.
	# Replaces the whole inventory (clear first).
	write_versioned_function("zombies/inventory/restore_inventory", f"""
clear @s
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.inv_restore","{ns}.gm_entity"]}}
execute if data storage {ns}:temp _restore.items[0] run function {ns}:v{version}/zombies/inventory/restore_loop
kill @e[type=minecraft:item_display,tag={ns}.inv_restore]
data remove storage {ns}:temp _restore
""")

	## One snapshot entry per pass: load it into the shuttle, place it into its slot, pop, recurse.
	write_versioned_function("zombies/inventory/restore_loop", f"""
data modify storage {ns}:temp _restore.item set from storage {ns}:temp _restore.items[0]
execute store result score #inv_slot {ns}.data run data get storage {ns}:temp _restore.item.Slot
data remove storage {ns}:temp _restore.item.Slot
data modify entity @n[type=minecraft:item_display,tag={ns}.inv_restore] item set from storage {ns}:temp _restore.item

# Slot mapping: 0..35 = container.N (hotbar + main inventory), 100..103 = armor, -106 = offhand
execute if score #inv_slot {ns}.data matches 0..35 store result storage {ns}:temp _restore.slot int 1 run scoreboard players get #inv_slot {ns}.data
execute if score #inv_slot {ns}.data matches 0..35 run function {ns}:v{version}/zombies/inventory/restore_slot with storage {ns}:temp _restore
execute if score #inv_slot {ns}.data matches 100 run item replace entity @s armor.feet from entity @n[type=minecraft:item_display,tag={ns}.inv_restore] contents
execute if score #inv_slot {ns}.data matches 101 run item replace entity @s armor.legs from entity @n[type=minecraft:item_display,tag={ns}.inv_restore] contents
execute if score #inv_slot {ns}.data matches 102 run item replace entity @s armor.chest from entity @n[type=minecraft:item_display,tag={ns}.inv_restore] contents
execute if score #inv_slot {ns}.data matches 103 run item replace entity @s armor.head from entity @n[type=minecraft:item_display,tag={ns}.inv_restore] contents
execute if score #inv_slot {ns}.data matches -106 run item replace entity @s weapon.offhand from entity @n[type=minecraft:item_display,tag={ns}.inv_restore] contents

data remove storage {ns}:temp _restore.items[0]
execute if data storage {ns}:temp _restore.items[0] run function {ns}:v{version}/zombies/inventory/restore_loop
""")

	## Macro: place the shuttle item into a numeric container slot (rare event — macro cost is fine).
	write_versioned_function("zombies/inventory/restore_slot", f"""
$item replace entity @s container.$(slot) from entity @n[type=minecraft:item_display,tag={ns}.inv_restore] contents
""")

