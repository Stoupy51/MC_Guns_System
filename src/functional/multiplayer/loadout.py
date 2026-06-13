
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .classes import CLASS_IDS, CLASSES, build_class_snbt


def generate_loadouts() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Initialize default classes in storage as an ordered list
	class_entries: list[str] = []
	for class_id, class_data in CLASSES.items():
		class_num: int = CLASS_IDS[class_id]
		class_entries.append(build_class_snbt(ns, class_id, class_data, class_num))

	classes_snbt: str = ",".join(class_entries)
	write_load_file(f"data modify storage {ns}:multiplayer classes_list set value [{classes_snbt}]")

	## Dynamic loadout application (recursive slot iteration)

	# apply_slot_loot: give the loot table item to the slot (macro)
	write_versioned_function("multiplayer/apply_slot_loot", "$loot replace entity @s $(slot) loot $(loot)")

	# apply_slot_count: set item count (for equipment stacking, e.g. 2 grenades)
	write_versioned_function("multiplayer/apply_slot_count", """$item modify entity @s $(slot) {"function":"minecraft:set_count","count":$(count),"add":false}""")

	# apply_slot_consumable: set consumable magazine stack count from #bullets score
	write_versioned_function("multiplayer/apply_slot_consumable", f"""
$scoreboard players set #bullets {ns}.data $(bullets)
$item modify entity @s $(slot) {ns}:v{version}/set_consumable_count
""")

	# apply_next_slot: recursive function that processes slots[0] then continues
	write_versioned_function("multiplayer/apply_next_slot", f"""
# Apply loot to slot
data modify storage {ns}:temp current_slot set from storage {ns}:temp slots[0]
function {ns}:v{version}/multiplayer/apply_slot_loot with storage {ns}:temp current_slot

# If count > 1, apply set_count modifier
execute unless data storage {ns}:temp current_slot{{count:1}} run function {ns}:v{version}/multiplayer/apply_slot_count with storage {ns}:temp current_slot

# If consumable, apply consumable count modifier
execute if data storage {ns}:temp current_slot{{consumable:true}} run function {ns}:v{version}/multiplayer/apply_slot_consumable with storage {ns}:temp current_slot

# Remove processed slot and recurse
data remove storage {ns}:temp slots[0]
execute if data storage {ns}:temp slots[0] run function {ns}:v{version}/multiplayer/apply_next_slot
""")

	## apply_class_dynamic: reads class from temp storage and applies loadout
	## Called after copying the target class data to mgs:temp
	write_versioned_function("multiplayer/apply_class_dynamic", f"""
# Clear player inventory
clear @s

# Apply armor
item replace entity @s armor.head with air
item replace entity @s armor.chest with leather_chestplate[dyed_color=10263702,unbreakable={{}}]
item replace entity @s armor.legs with chainmail_leggings[unbreakable={{}}]
item replace entity @s armor.feet with iron_boots[unbreakable={{}}]

# Copy class slots to iteration temp
data modify storage {ns}:temp slots set from storage {ns}:temp current_class.slots

# Recursively apply all slots
execute if data storage {ns}:temp slots[0] run function {ns}:v{version}/multiplayer/apply_next_slot

# Apply perks from the selected loadout (standard class or custom)
function {ns}:v{version}/multiplayer/apply_perks

# Give class menu item (only in multiplayer)
execute if entity @s[tag={ns}.give_class_menu] run loot replace entity @s hotbar.4 loot {ns}:i/class_menu
""")

	## apply_perks: reads the perks list from temp current_class and sets the special.* flags.
	## Shared by both standard classes and custom loadouts so every loadout starts from a clean
	## perk state (any perk not on the loadout is reset to 0 / defaults).
	write_versioned_function("multiplayer/apply_perks", f"""
# Sleight of Hand / Fast Hands: percentages (50 = 50% faster), 0 when absent
execute if data storage {ns}:temp current_class{{perks:["quick_reload"]}} run scoreboard players set @s {ns}.special.quick_reload 50
execute unless data storage {ns}:temp current_class{{perks:["quick_reload"]}} run scoreboard players set @s {ns}.special.quick_reload 0
execute if data storage {ns}:temp current_class{{perks:["quick_swap"]}} run scoreboard players set @s {ns}.special.quick_swap 50
execute unless data storage {ns}:temp current_class{{perks:["quick_swap"]}} run scoreboard players set @s {ns}.special.quick_swap 0

# Flag perks (0/1), read by the systems they affect
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

# Juggernaut: flag + raised max health (24 HP), reset to default 20 otherwise
execute store success score #has_perk {ns}.data if data storage {ns}:temp current_class{{perks:["juggernaut"]}}
scoreboard players operation @s {ns}.special.juggernaut = #has_perk {ns}.data
execute if score #has_perk {ns}.data matches 1 run attribute @s minecraft:max_health base set 24
execute if score #has_perk {ns}.data matches 0 run attribute @s minecraft:max_health base reset

# Loadouts never grant the admin/powerup buffs — clear any leftovers
scoreboard players set @s {ns}.special.infinite_ammo 0
scoreboard players set @s {ns}.special.instant_kill 0
""")

