""" Reading the selected gun, its runtime max level and applying one pap_stats field per stat. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import PAP_STATS, STATS_FIELDS


# Functions
def write_pap_stats() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/pap/extract_selected", f"""
tag @s add {ns}.pap_extracting
$execute summon item_display run function {ns}:v{version}/zombies/pap/extract_selected_item {{slot:"$(slot)"}}
tag @s remove {ns}.pap_extracting
""")

	write_versioned_function("zombies/pap/extract_selected_item", f"""
$item replace entity @s contents from entity @p[tag={ns}.pap_extracting] $(slot)

data modify storage {ns}:temp _pap_extract set value {{}}
data modify storage {ns}:temp _pap_extract.weapon set from entity @s item.components."minecraft:custom_data".{ns}.weapon
data modify storage {ns}:temp _pap_extract.stats set from entity @s item.components."minecraft:custom_data".{ns}.stats
execute if data entity @s item.components."minecraft:item_name"[0].text run data modify storage {ns}:temp _pap_extract.current_name set from entity @s item.components."minecraft:item_name"[0].text
execute if data entity @s item.components."minecraft:lore"[0] run data modify storage {ns}:temp _pap_extract.lore set from entity @s item.components."minecraft:lore"
kill @s
""")

	# Dynamic list picker helpers, with no hardcoded max level.
	#   - _pap_pick.list: the PAP list to resolve
	#   - #pap_next_idx: 0-based requested level index
	#   - _pap_pick.value: resolved value, clamped to the last available entry
	write_versioned_function("zombies/pap/pick_list_value", f"""
scoreboard players set #pap_pick_i {ns}.data 0
data modify storage {ns}:temp _pap_pick.value set from storage {ns}:temp _pap_pick.list[0]
function {ns}:v{version}/zombies/pap/pick_list_value_step
""")

	write_versioned_function("zombies/pap/pick_list_value_step", f"""
execute if score #pap_pick_i {ns}.data < #pap_next_idx {ns}.data if data storage {ns}:temp _pap_pick.list[1] run function {ns}:v{version}/zombies/pap/pick_list_value_advance
""")

	write_versioned_function("zombies/pap/pick_list_value_advance", f"""
data remove storage {ns}:temp _pap_pick.list[0]
scoreboard players add #pap_pick_i {ns}.data 1
data modify storage {ns}:temp _pap_pick.value set from storage {ns}:temp _pap_pick.list[0]
function {ns}:v{version}/zombies/pap/pick_list_value_step
""")

	# Runtime max level from list lengths in pap_stats (defaults to 1 when pap_stats exists).
	compute_max_lines: list[str] = [f"scoreboard players set #pap_max {ns}.data 1"]
	for field in STATS_FIELDS:
		compute_max_lines.append(
			f'execute if data storage {ns}:temp _pap_extract.stats.{PAP_STATS}.{field}[0] store result score #pap_len {ns}.data run data get storage {ns}:temp _pap_extract.stats.{PAP_STATS}.{field}'
		)
		compute_max_lines.append(
			f'execute if score #pap_len {ns}.data > #pap_max {ns}.data run scoreboard players operation #pap_max {ns}.data = #pap_len {ns}.data'
		)
	compute_max_lines.append(
		f'execute if data storage {ns}:temp _pap_extract.stats.{PAP_STATS}.pap_name[0] store result score #pap_len {ns}.data run data get storage {ns}:temp _pap_extract.stats.{PAP_STATS}.pap_name'
	)
	compute_max_lines.append(
		f'execute if score #pap_len {ns}.data > #pap_max {ns}.data run scoreboard players operation #pap_max {ns}.data = #pap_len {ns}.data'
	)
	write_versioned_function("zombies/pap/compute_max_level", "\n".join(compute_max_lines))

	# Apply one PAP field dynamically from stats.pap_stats.$(field) for #pap_next_idx.
	# Macro rather than one function per stat: this is the PaP purchase path (cold), and the arg set is the fixed STATS_FIELDS list, so every variant is compiled once and then cached.
	write_versioned_function("zombies/pap/apply_field", f"""
$data modify storage {ns}:temp _pap_pick.list set from storage {ns}:temp _pap_extract.stats.{PAP_STATS}.$(field)
execute if data storage {ns}:temp _pap_pick.list[0] run function {ns}:v{version}/zombies/pap/pick_list_value
$execute if data storage {ns}:temp _pap_pick.list[0] run data modify storage {ns}:temp _pap_extract.stats.$(field) set from storage {ns}:temp _pap_pick.value
$execute unless data storage {ns}:temp _pap_pick.list[0] run data modify storage {ns}:temp _pap_extract.stats.$(field) set from storage {ns}:temp _pap_extract.stats.{PAP_STATS}.$(field)
""")

	apply_lines: list[str] = []
	for field in STATS_FIELDS:
		apply_lines.append(
			f'execute if data storage {ns}:temp _pap_extract.stats.{PAP_STATS}.{field} run function {ns}:v{version}/zombies/pap/apply_field {{field:"{field}"}}'
		)
	write_versioned_function("zombies/pap/apply_runtime_overrides", "\n".join(apply_lines))

	# Resolve optional pap_name dynamically (scalar or list).
	name_lines: list[str] = [
		f'data modify storage {ns}:temp _pap_pick.list set from storage {ns}:temp _pap_extract.stats.{PAP_STATS}.pap_name',
		f'execute if data storage {ns}:temp _pap_pick.list[0] run function {ns}:v{version}/zombies/pap/pick_list_value',
		f'execute if data storage {ns}:temp _pap_pick.list[0] run data modify storage {ns}:temp _pap_extract.new_name set from storage {ns}:temp _pap_pick.value',
		f'execute unless data storage {ns}:temp _pap_pick.list[0] run data modify storage {ns}:temp _pap_extract.new_name set from storage {ns}:temp _pap_extract.stats.{PAP_STATS}.pap_name',
	]
	write_versioned_function("zombies/pap/resolve_runtime_name", "\n".join(name_lines))

