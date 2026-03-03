
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .classes import CLASS_IDS, CLASSES, build_class_snbt


def generate_loadouts() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Initialize default classes in storage as an ordered list
	## ============================
	class_entries: list[str] = []
	for class_id, class_data in CLASSES.items():
		class_num: int = CLASS_IDS[class_id]
		class_entries.append(build_class_snbt(ns, class_id, class_data, class_num))

	classes_snbt: str = ",".join(class_entries)
	write_load_file(f"data modify storage {ns}:multiplayer classes_list set value [{classes_snbt}]")

	## ============================
	## Dynamic loadout application (recursive slot iteration)
	## ============================

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
	write_versioned_function("multiplayer/apply_next_slot",
f"""
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

	## ============================
	## apply_class_dynamic: reads class from temp storage and applies loadout
	## Called after copying the target class data to mgs:temp
	## ============================
	write_versioned_function("multiplayer/apply_class_dynamic",
f"""
# Clear player inventory
clear @s

# Copy class slots to iteration temp
data modify storage {ns}:temp slots set from storage {ns}:temp current_class.slots

# Recursively apply all slots
execute if data storage {ns}:temp slots[0] run function {ns}:v{version}/multiplayer/apply_next_slot
""")

