""" The upgraded item's name and the per-stat deltas annotated onto its lore. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_pap_lore() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Set item name with PAP level suffix: [name, " (PaP N/M)"]
	write_versioned_function("zombies/pap/set_item_name_with_level", """
$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:item_name":[{"text":"$(name)","color":"gold","italic":false},{"text":" (PaP $(level)/$(max))","color":"aqua","italic":false}]}}
""")

	# Annotate lore lines with runtime-computed PAP deltas.
	# Old stats are in _pap_old_stats (copied before overrides), new stats in _pap_extract.stats.
	# Uses #pap_li to track current lore line index.
	annotate_lore_lines: list[str] = [f'scoreboard players set #pap_li {ns}.data 0']

	# Line 0: Damage (integer)
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.damage',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.damage',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_int_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Line 1: Ammo capacity
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.capacity',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.capacity',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_int_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Line 2: Reload Time (ticks → seconds)
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.reload_time',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.reload_time',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_time_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Line 3 (conditional): Fire Rate.
	# Gate on OLD stats — the extracted lore has a Fire Rate line only if the weapon had a cooldown BEFORE this PAP. pap_stats can add cooldown (e.g. m1911), which would otherwise annotate a line that isn't there and shift decay/switch down one.
	annotate_lore_lines.append(
		f'execute if data storage {ns}:temp _pap_old_stats.cooldown run function {ns}:v{version}/zombies/pap/annotate_fire_rate_line'
	)

	# Line N (conditional): Pellets — same reasoning, gate on old stats
	annotate_lore_lines.append(
		f'execute if data storage {ns}:temp _pap_old_stats.pellet_count run function {ns}:v{version}/zombies/pap/annotate_pellets_line'
	)

	# Line N: Damage Decay (percentage, scaled x100)
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.decay 100',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.decay 100',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_pct_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Line N: Switch Time (ticks → seconds)
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.switch',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.switch',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_time_delta',
	])
	write_versioned_function("zombies/pap/annotate_lore", "\n".join(annotate_lore_lines))

	# Helper: annotate new integer value (damage, pellets)
	write_versioned_function("zombies/pap/annotate_int_delta", f"""
execute store result storage {ns}:temp _pap_ann.index int 1 run scoreboard players get #pap_li {ns}.data
data modify storage {ns}:temp _pap_ann.suffix set value ""
execute store result storage {ns}:temp _pap_ann.value int 1 run scoreboard players get #pap_new {ns}.data
function {ns}:v{version}/zombies/pap/annotate_append_int with storage {ns}:temp _pap_ann
""")

	# Helper: annotate new percentage value (decay — x100 already in #pap_new)
	write_versioned_function("zombies/pap/annotate_pct_delta", f"""
execute store result storage {ns}:temp _pap_ann.index int 1 run scoreboard players get #pap_li {ns}.data
data modify storage {ns}:temp _pap_ann.suffix set value "%"
execute store result storage {ns}:temp _pap_ann.value int 1 run scoreboard players get #pap_new {ns}.data
function {ns}:v{version}/zombies/pap/annotate_append_int with storage {ns}:temp _pap_ann
""")

	# Helper: annotate new time value (reload, switch) — new ticks → X.Ys
	write_versioned_function("zombies/pap/annotate_time_delta", f"""
execute store result storage {ns}:temp _pap_ann.index int 1 run scoreboard players get #pap_li {ns}.data
data modify storage {ns}:temp _pap_ann.suffix set value "s"

# Tenths of seconds: new_ticks * 10 / 20
scoreboard players operation #pap_tenths {ns}.data = #pap_new {ns}.data
scoreboard players operation #pap_tenths {ns}.data *= #10 {ns}.data
scoreboard players operation #pap_tenths {ns}.data /= #20 {ns}.data

# Split into whole.decimal
scoreboard players operation #pap_whole {ns}.data = #pap_tenths {ns}.data
scoreboard players operation #pap_whole {ns}.data /= #10 {ns}.data
scoreboard players operation #pap_dec {ns}.data = #pap_tenths {ns}.data
scoreboard players operation #pap_dec {ns}.data %= #10 {ns}.data

execute store result storage {ns}:temp _pap_ann.whole int 1 run scoreboard players get #pap_whole {ns}.data
execute store result storage {ns}:temp _pap_ann.dec int 1 run scoreboard players get #pap_dec {ns}.data
function {ns}:v{version}/zombies/pap/annotate_append_dec with storage {ns}:temp _pap_ann
""")

	# Helper: fire rate line (conditional) — rate = 200/cooldown (tenths)
	write_versioned_function("zombies/pap/annotate_fire_rate_line", f"""
execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.cooldown
execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.cooldown

# Compute fire rate in tenths: 200 / cooldown
scoreboard players operation #pap_rate_old {ns}.data = #200 {ns}.data
scoreboard players operation #pap_rate_old {ns}.data /= #pap_old {ns}.data
scoreboard players operation #pap_rate_new {ns}.data = #200 {ns}.data
scoreboard players operation #pap_rate_new {ns}.data /= #pap_new {ns}.data

scoreboard players operation #pap_delta {ns}.data = #pap_rate_new {ns}.data
scoreboard players operation #pap_delta {ns}.data -= #pap_rate_old {ns}.data

# Annotate if rate changed
execute store result storage {ns}:temp _pap_ann.index int 1 run scoreboard players get #pap_li {ns}.data
execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_rate_delta
scoreboard players add #pap_li {ns}.data 1
""")

	# Helper: new rate value — #pap_rate_new is in tenths, split whole.dec
	write_versioned_function("zombies/pap/annotate_rate_delta", f"""
data modify storage {ns}:temp _pap_ann.suffix set value ""

scoreboard players operation #pap_whole {ns}.data = #pap_rate_new {ns}.data
scoreboard players operation #pap_whole {ns}.data /= #10 {ns}.data
scoreboard players operation #pap_dec {ns}.data = #pap_rate_new {ns}.data
scoreboard players operation #pap_dec {ns}.data %= #10 {ns}.data

execute store result storage {ns}:temp _pap_ann.whole int 1 run scoreboard players get #pap_whole {ns}.data
execute store result storage {ns}:temp _pap_ann.dec int 1 run scoreboard players get #pap_dec {ns}.data
function {ns}:v{version}/zombies/pap/annotate_append_dec with storage {ns}:temp _pap_ann
""")

	# Helper: pellets line (conditional) — integer delta
	write_versioned_function("zombies/pap/annotate_pellets_line", f"""
execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.pellet_count
execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.pellet_count
scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data
scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data
execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_int_delta
scoreboard players add #pap_li {ns}.data 1
""")

	# Macro: append integer annotation " > $(value)$(suffix)" — always appends, never removes previous
	write_versioned_function("zombies/pap/annotate_append_int", f"""
$data modify storage {ns}:temp _pap_extract.lore[$(index)].extra append value {{"text":" > $(value)$(suffix)","color":"aqua","italic":false}}
""")

	# Macro: append decimal annotation " > $(whole).$(dec)$(suffix)" — always appends, never removes previous
	write_versioned_function("zombies/pap/annotate_append_dec", f"""
$data modify storage {ns}:temp _pap_extract.lore[$(index)].extra append value {{"text":" > $(whole).$(dec)$(suffix)","color":"aqua","italic":false}}
""")
	write_versioned_function("zombies/pap/set_item_name", """
$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:item_name":{"text":"$(name)","color":"gold","italic":false}}}
""")

	write_versioned_function("zombies/pap/set_item_lore", """
$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:lore":$(lore)}}
	""")

	write_versioned_function("zombies/pap/apply_to_slot", f"""
$item modify entity @s $(slot) {ns}:v{version}/zb_pap_apply_stats
$data modify storage {ns}:temp _pap_name_data.slot set value "$(slot)"
function {ns}:v{version}/zombies/pap/set_item_name_with_level with storage {ns}:temp _pap_name_data
$execute if data storage {ns}:temp _pap_extract.lore[0] run data modify storage {ns}:temp _pap_apply_lore.slot set value "$(slot)"
execute if data storage {ns}:temp _pap_extract.lore[0] run data modify storage {ns}:temp _pap_apply_lore.lore set from storage {ns}:temp _pap_extract.lore
execute if data storage {ns}:temp _pap_extract.lore[0] run function {ns}:v{version}/zombies/pap/set_item_lore with storage {ns}:temp _pap_apply_lore

# Update item_model to match new scope
$data modify storage {ns}:temp _pap_scope_model.slot set value "$(slot)"
data modify storage {ns}:temp _pap_scope_model.model set from storage {ns}:temp _pap_extract.stats.models.normal
function {ns}:v{version}/zombies/pap/set_item_model_from_scope with storage {ns}:temp _pap_scope_model

$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"$(slot)"}}
""")

