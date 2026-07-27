""" The generic ammo-in-lore rewriter, instantiated once per item kind. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import CAPACITY, REMAINING_BULLETS


def create_lore_functions(type_name: str, tag: str, remaining_source: str, capacity_source: str) -> None:
	""" Create lore modification functions for weapons or magazines.

	Args:
		type_name        (str): Type name for the lore functions (e.g., "lore" or "mag_lore").
		tag              (str): Temporary tag to identify the item being modified.
		remaining_source (str): Source to get the remaining bullets value.
		capacity_source  (str): Source to get the capacity value.
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Modify lore function
	write_versioned_function(f"ammo/modify_{type_name}", f"""
# Add temporary tag for item display targeting
tag @s add {tag}

# Get current item lore
$execute summon item_display run function {ns}:v{version}/ammo/get_current_{type_name} {{"slot":"$(slot)"}}

# Find and update ammo count in lore
scoreboard players set #index {ns}.data 0
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_{type_name}_loop {{"slot":"$(slot)"}}

# Clean up temporary tag
tag @s remove {tag}
""")

	# Get current item lore
	write_versioned_function(f"ammo/get_current_{type_name}", f"""
# Copy item to item display entity
$item replace entity @s contents from entity @p[tag={tag}] $(slot)

# Extract lore data
data modify storage {ns}:temp components set from entity @s item.components
data modify storage {ns}:temp lore set from storage {ns}:temp components."minecraft:lore"
data modify storage {ns}:temp copy set from storage {ns}:temp lore

# Clean up item display
kill @s
""")

	# Search for ammo line in lore
	write_versioned_function(f"ammo/search_{type_name}_loop", f"""
# Check if current lore line matches ammo format (number/number)
scoreboard players set #success {ns}.data 0
data modify storage {ns}:temp lore_extra set from storage {ns}:temp copy[0].extra
data modify storage {ns}:temp lore_slash set from storage {ns}:temp lore_extra[-2]
execute if data storage {ns}:temp lore_slash{{"text":"/"}} unless data storage {ns}:temp lore_extra[-3].text unless data storage {ns}:temp lore_extra[-1].text run scoreboard players set #success {ns}.data 1

# If ammo line found, prepare data for modification
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with set value {{}}
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.index int 1 run scoreboard players get #index {ns}.data
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.{REMAINING_BULLETS} int 1 run scoreboard players get {remaining_source}
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.{CAPACITY} set from {capacity_source}
$execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.slot set value "$(slot)"
execute if score #success {ns}.data matches 1 summon item_display run return run function {ns}:v{version}/ammo/found_{type_name}_line with storage {ns}:input with

# Continue searching if not found
data remove storage {ns}:temp copy[0]
scoreboard players add #index {ns}.data 1
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_{type_name}_loop {{"slot":"$(slot)"}}
""")

	# Update ammo count in item lore
	write_versioned_function(f"ammo/found_{type_name}_line", f"""
# Copy item to item display for modification
$item replace entity @s contents from entity @p[tag={tag}] $(slot)

# Update ammo count in lore
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-1] set value "$({CAPACITY})"
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-3] set value "$({REMAINING_BULLETS})"

# Copy modified item back to player
$item replace entity @p[tag={tag}] $(slot) from entity @s contents

# Clean up item display
kill @s
""")

