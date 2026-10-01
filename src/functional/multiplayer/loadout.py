""" Applies a loadout to a player, slot by slot. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .classes import MultiplayerClasses


# Functions
def generate_loadouts() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Default classes, as an ordered list in storage.
	class_entries: list[str] = []
	for class_id, class_data in MultiplayerClasses.CLASSES.items():
		class_num: int = MultiplayerClasses.CLASS_IDS[class_id]
		class_entries.append(MultiplayerClasses.build_class_snbt(ns, class_id, class_data, class_num))

	classes_snbt: str = ",".join(class_entries)
	write_load_file(f"data modify storage {ns}:multiplayer classes_list set value [{classes_snbt}]")

	## Loadouts are applied by recursing over their slots.

	write_versioned_function("multiplayer/apply_slot_loot", "$loot replace entity @s $(slot) loot $(loot)")

	# Equipment stacks (2 grenades).
	write_versioned_function("multiplayer/apply_slot_count", """$item modify entity @s $(slot) {"type":"minecraft:set_count","count":$(count),"add":false}""")

	# From the #bullets score.
	write_versioned_function("multiplayer/apply_slot_consumable", f"""
$scoreboard players set #bullets {ns}.data $(bullets)
$item modify entity @s $(slot) {ns}:v{version}/set_consumable_count
""")

	# The loadout's camo suffix ("" for none).
	write_versioned_function("multiplayer/apply_knife", f"""$loot replace entity @s hotbar.0 loot {ns}:i/combat_knife$(camo)
""")

	write_versioned_function("multiplayer/apply_next_slot", f"""
data modify storage {ns}:temp current_slot set from storage {ns}:temp slots[0]
function {ns}:v{version}/multiplayer/apply_slot_loot with storage {ns}:temp current_slot

execute unless data storage {ns}:temp current_slot{{count:1}} run function {ns}:v{version}/multiplayer/apply_slot_count with storage {ns}:temp current_slot

execute if data storage {ns}:temp current_slot{{consumable:true}} run function {ns}:v{version}/multiplayer/apply_slot_consumable with storage {ns}:temp current_slot

data remove storage {ns}:temp slots[0]
execute if data storage {ns}:temp slots[0] run function {ns}:v{version}/multiplayer/apply_next_slot
""")

	## Run after copying the class into {ns}:temp current_class.
	write_versioned_function("multiplayer/apply_class_dynamic", f"""
clear @s

item replace entity @s armor.head with air
item replace entity @s armor.chest with leather_chestplate[dyed_color=10263702,unbreakable={{}}]
item replace entity @s armor.legs with chainmail_leggings[unbreakable={{}}]
item replace entity @s armor.feet with iron_boots[unbreakable={{}}]

# The knife is always given in hotbar.0, so weapons start at hotbar.1 and hotbar.2. The camo defaults to "":
# standard classes never set it, and older loadouts have no field, which would fail the macro.
data modify storage {ns}:temp _knife set value {{camo:""}}
execute if data storage {ns}:temp current_class.knife_camo run data modify storage {ns}:temp _knife.camo set from storage {ns}:temp current_class.knife_camo
function {ns}:v{version}/multiplayer/apply_knife with storage {ns}:temp _knife

data modify storage {ns}:temp slots set from storage {ns}:temp current_class.slots

execute if data storage {ns}:temp slots[0] run function {ns}:v{version}/multiplayer/apply_next_slot

function {ns}:v{version}/multiplayer/apply_perks

# Multiplayer only.
execute if entity @s[tag={ns}.give_class_menu] run loot replace entity @s hotbar.4 loot {ns}:i/class_menu
""")

	## Shared by standard classes and custom loadouts: every perk not on the loadout is reset.
	write_versioned_function("multiplayer/apply_perks", f"""
# Sleight of Hand, Fast Hands: percentages (50 = 50% faster), 0 when absent.
execute if data storage {ns}:temp current_class{{perks:["quick_reload"]}} run scoreboard players set @s {ns}.special.quick_reload 50
execute unless data storage {ns}:temp current_class{{perks:["quick_reload"]}} run scoreboard players set @s {ns}.special.quick_reload 0
execute if data storage {ns}:temp current_class{{perks:["quick_swap"]}} run scoreboard players set @s {ns}.special.quick_swap 50
execute unless data storage {ns}:temp current_class{{perks:["quick_swap"]}} run scoreboard players set @s {ns}.special.quick_swap 0

# Flags read by the systems they affect.
execute store success score #has_perk {ns}.data if data storage {ns}:temp current_class{{perks:["scavenger"]}}
scoreboard players operation @s {ns}.special.scavenger = #has_perk {ns}.data
execute store success score #has_perk {ns}.data if data storage {ns}:temp current_class{{perks:["flak_jacket"]}}
scoreboard players operation @s {ns}.special.flak_jacket = #has_perk {ns}.data
execute store success score #has_perk {ns}.data if data storage {ns}:temp current_class{{perks:["tracker"]}}
scoreboard players operation @s {ns}.special.tracker = #has_perk {ns}.data
execute store success score #has_perk {ns}.data if data storage {ns}:temp current_class{{perks:["tactical_mask"]}}
scoreboard players operation @s {ns}.special.tactical_mask = #has_perk {ns}.data
execute store success score #has_perk {ns}.data if data storage {ns}:temp current_class{{perks:["overkill"]}}
scoreboard players operation @s {ns}.special.overkill = #has_perk {ns}.data
execute store success score #has_perk {ns}.data if data storage {ns}:temp current_class{{perks:["quick_fix"]}}
scoreboard players operation @s {ns}.special.quick_fix = #has_perk {ns}.data

# Juggernaut: flag and 24 HP max health, back to 20 otherwise.
execute store success score #has_perk {ns}.data if data storage {ns}:temp current_class{{perks:["juggernaut"]}}
scoreboard players operation @s {ns}.special.juggernaut = #has_perk {ns}.data
execute if score #has_perk {ns}.data matches 1 run attribute @s minecraft:max_health base set 24
execute if score #has_perk {ns}.data matches 0 run attribute @s minecraft:max_health base reset

# Loadouts never grant admin or power-up buffs.
scoreboard players set @s {ns}.special.infinite_ammo 0
scoreboard players set @s {ns}.special.instant_kill 0
""")

