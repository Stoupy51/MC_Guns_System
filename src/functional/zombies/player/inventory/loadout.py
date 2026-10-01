""" The starting and respawn loadouts, and restoring a saved inventory slot by slot. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers.content import SharedContent


# Functions
def write_zombies_loadout() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Zombies keeps vanilla reach: the knife is the fallback once ammo runs out.
	knife_item = SharedContent.knife_item_snbt(ns)

	write_versioned_function("zombies/inventory/give_starting_loadout", f"""
clear @s

item replace entity @s hotbar.0 with {knife_item}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.0",group:"hotbar",index:0}}

# Starting weapon and its scaled magazine.
loot replace entity @s hotbar.1 loot {ns}:i/m1911
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.1",group:"hotbar",index:1}}

loot replace entity @s inventory.1 loot {ns}:i/m1911_mag
function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.1",index:1,remaining_multiplier:0.5}}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.1",group:"inventory",index:1}}

# Main equipment (frag); the lethal type is recorded so an empty slot refills with frag, not a stale value.
loot replace entity @s hotbar.7 loot {ns}:i/frag_grenade
item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_4
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}
scoreboard players set @s {ns}.zb.lethal_type 0

function {ns}:v{version}/zombies/inventory/refresh_info_item

# Only for manual abilities.
execute if score @s {ns}.zb.ability matches 3.. run function {ns}:v{version}/zombies/inventory/give_ability_item
""")

	write_versioned_function("zombies/inventory/give_respawn_loadout", f"""
function {ns}:v{version}/zombies/inventory/give_starting_loadout

# Bleed-out respawns are lighter: knife, M1911 and 2 frags; bought knives, grenade types and tacticals are lost.
item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_2
""")

	# Restore {ns}:temp _restore.items into a cleared inventory (Who's Who revive, Tombstone recovery), run as the player.
	# Players cannot be data-modified, so each entry goes through a one-slot shuttle item_display and `item replace` into its original slot.
	write_versioned_function("zombies/inventory/restore_inventory", f"""
clear @s
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.inv_restore","{ns}.gm_entity"]}}
execute if data storage {ns}:temp _restore.items[0] run function {ns}:v{version}/zombies/inventory/restore_loop
kill @e[type=minecraft:item_display,tag={ns}.inv_restore]
data remove storage {ns}:temp _restore
""")

	## One entry per pass, then recurse.
	write_versioned_function("zombies/inventory/restore_loop", f"""
data modify storage {ns}:temp _restore.item set from storage {ns}:temp _restore.items[0]
execute store result score #inv_slot {ns}.data run data get storage {ns}:temp _restore.item.Slot
data remove storage {ns}:temp _restore.item.Slot
data modify entity @n[type=minecraft:item_display,tag={ns}.inv_restore] item set from storage {ns}:temp _restore.item

# 0..35 container.N (hotbar and main), 100..103 armor, -106 offhand.
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

	## A macro is fine here: restores are rare.
	write_versioned_function("zombies/inventory/restore_slot", f"""
$item replace entity @s container.$(slot) from entity @n[type=minecraft:item_display,tag={ns}.inv_restore] contents
""")

