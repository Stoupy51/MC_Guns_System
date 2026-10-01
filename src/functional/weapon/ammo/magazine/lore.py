""" The generic ammo-in-lore rewriter, instantiated once per item kind. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import CAPACITY, REMAINING_BULLETS


def create_lore_functions(type_name: str, tag: str, remaining_source: str, capacity_source: str) -> None:
	""" Create lore modification functions for weapons or magazines.

	Args:
		type_name: Type name for the lore functions (e.g., "lore" or "mag_lore").
		tag: Temporary tag to identify the item being modified.
		remaining_source: Source to get the remaining bullets value.
		capacity_source: Source to get the capacity value.
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function(f"ammo/modify_{type_name}", f"""
# Target of the item_display.
tag @s add {tag}

$execute summon item_display run function {ns}:v{version}/ammo/get_current_{type_name} {{"slot":"$(slot)"}}

scoreboard players set #index {ns}.data 0
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_{type_name}_loop {{"slot":"$(slot)"}}

tag @s remove {tag}
""")

	write_versioned_function(f"ammo/get_current_{type_name}", f"""
$item replace entity @s contents from entity @p[tag={tag}] $(slot)

data modify storage {ns}:temp components set from entity @s item.components
data modify storage {ns}:temp lore set from storage {ns}:temp components."minecraft:lore"
data modify storage {ns}:temp copy set from storage {ns}:temp lore

kill @s
""")

	write_versioned_function(f"ammo/search_{type_name}_loop", f"""
# An ammo line reads number/number.
scoreboard players set #success {ns}.data 0
data modify storage {ns}:temp lore_extra set from storage {ns}:temp copy[0].extra
data modify storage {ns}:temp lore_slash set from storage {ns}:temp lore_extra[-2]
execute if data storage {ns}:temp lore_slash{{"text":"/"}} unless data storage {ns}:temp lore_extra[-3].text unless data storage {ns}:temp lore_extra[-1].text run scoreboard players set #success {ns}.data 1

execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with set value {{}}
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.index int 1 run scoreboard players get #index {ns}.data
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.{REMAINING_BULLETS} int 1 run scoreboard players get {remaining_source}
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.{CAPACITY} set from {capacity_source}
$execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.slot set value "$(slot)"
execute if score #success {ns}.data matches 1 summon item_display run return run function {ns}:v{version}/ammo/found_{type_name}_line with storage {ns}:input with

data remove storage {ns}:temp copy[0]
scoreboard players add #index {ns}.data 1
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_{type_name}_loop {{"slot":"$(slot)"}}
""")

	write_versioned_function(f"ammo/found_{type_name}_line", f"""
$item replace entity @s contents from entity @p[tag={tag}] $(slot)

$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-1] set value "$({CAPACITY})"
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-3] set value "$({REMAINING_BULLETS})"

$item replace entity @p[tag={tag}] $(slot) from entity @s contents

kill @s
""")

