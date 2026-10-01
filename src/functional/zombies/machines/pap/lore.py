""" The upgraded item's name and the per-stat deltas annotated onto its lore. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_pap_lore() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# [name, " (PaP N/M)"]
	write_versioned_function("zombies/pap/set_item_name_with_level", """
$item modify entity @s $(slot) {"type":"minecraft:set_components","components":{"minecraft:item_name":[{"text":"$(name)","color":"gold","italic":false},{"text":" (PaP $(level)/$(max))","color":"aqua","italic":false}]}}
""")

	# Annotate lore lines with PAP deltas: old stats in _pap_old_stats, new ones in _pap_extract.stats, #pap_li is the line index.
	annotate_lore_lines: list[str] = [f'scoreboard players set #pap_li {ns}.data 0']

	# Line 0: damage
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.damage',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.damage',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_int_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Line 1: ammo capacity
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.capacity',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.capacity',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_int_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Line 2: reload time (ticks to seconds)
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.reload_time',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.reload_time',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_time_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Optional fire rate line, gated on the old stats: the lore only has it if the weapon had a cooldown before.
	# pap_stats can add one (m1911), which would annotate a missing line and shift the ones below.
	annotate_lore_lines.append(
		f'execute if data storage {ns}:temp _pap_old_stats.cooldown run function {ns}:v{version}/zombies/pap/annotate_fire_rate_line'
	)

	# Optional pellets line, gated the same way.
	annotate_lore_lines.append(
		f'execute if data storage {ns}:temp _pap_old_stats.pellet_count run function {ns}:v{version}/zombies/pap/annotate_pellets_line'
	)

	# Damage decay (percentage, x100)
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.decay 100',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.decay 100',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_pct_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Switch time (ticks to seconds)
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.switch',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.switch',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_time_delta',
	])
	write_versioned_function("zombies/pap/annotate_lore", "\n".join(annotate_lore_lines))

	write_versioned_function("zombies/pap/annotate_int_delta", f"""
execute store result storage {ns}:temp _pap_ann.index int 1 run scoreboard players get #pap_li {ns}.data
data modify storage {ns}:temp _pap_ann.suffix set value ""
execute store result storage {ns}:temp _pap_ann.value int 1 run scoreboard players get #pap_new {ns}.data
function {ns}:v{version}/zombies/pap/annotate_append_int with storage {ns}:temp _pap_ann
""")

	# #pap_new is already x100.
	write_versioned_function("zombies/pap/annotate_pct_delta", f"""
execute store result storage {ns}:temp _pap_ann.index int 1 run scoreboard players get #pap_li {ns}.data
data modify storage {ns}:temp _pap_ann.suffix set value "%"
execute store result storage {ns}:temp _pap_ann.value int 1 run scoreboard players get #pap_new {ns}.data
function {ns}:v{version}/zombies/pap/annotate_append_int with storage {ns}:temp _pap_ann
""")

	# Ticks to X.Y s.
	write_versioned_function("zombies/pap/annotate_time_delta", f"""
execute store result storage {ns}:temp _pap_ann.index int 1 run scoreboard players get #pap_li {ns}.data
data modify storage {ns}:temp _pap_ann.suffix set value "s"

# Tenths = ticks x 10 / 20.
scoreboard players operation #pap_tenths {ns}.data = #pap_new {ns}.data
scoreboard players operation #pap_tenths {ns}.data *= #10 {ns}.data
scoreboard players operation #pap_tenths {ns}.data /= #20 {ns}.data

scoreboard players operation #pap_whole {ns}.data = #pap_tenths {ns}.data
scoreboard players operation #pap_whole {ns}.data /= #10 {ns}.data
scoreboard players operation #pap_dec {ns}.data = #pap_tenths {ns}.data
scoreboard players operation #pap_dec {ns}.data %= #10 {ns}.data

execute store result storage {ns}:temp _pap_ann.whole int 1 run scoreboard players get #pap_whole {ns}.data
execute store result storage {ns}:temp _pap_ann.dec int 1 run scoreboard players get #pap_dec {ns}.data
function {ns}:v{version}/zombies/pap/annotate_append_dec with storage {ns}:temp _pap_ann
""")

	# Rate in tenths = 200 / cooldown.
	write_versioned_function("zombies/pap/annotate_fire_rate_line", f"""
execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.cooldown
execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.cooldown

scoreboard players operation #pap_rate_old {ns}.data = #200 {ns}.data
scoreboard players operation #pap_rate_old {ns}.data /= #pap_old {ns}.data
scoreboard players operation #pap_rate_new {ns}.data = #200 {ns}.data
scoreboard players operation #pap_rate_new {ns}.data /= #pap_new {ns}.data

scoreboard players operation #pap_delta {ns}.data = #pap_rate_new {ns}.data
scoreboard players operation #pap_delta {ns}.data -= #pap_rate_old {ns}.data

execute store result storage {ns}:temp _pap_ann.index int 1 run scoreboard players get #pap_li {ns}.data
execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_rate_delta
scoreboard players add #pap_li {ns}.data 1
""")

	# #pap_rate_new is in tenths.
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

	write_versioned_function("zombies/pap/annotate_pellets_line", f"""
execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.pellet_count
execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.pellet_count
scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data
scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data
execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_int_delta
scoreboard players add #pap_li {ns}.data 1
""")

	# Appends " > $(value)$(suffix)" and never removes an earlier one.
	write_versioned_function("zombies/pap/annotate_append_int", f"""
$data modify storage {ns}:temp _pap_extract.lore[$(index)].extra append value {{"text":" > $(value)$(suffix)","color":"aqua","italic":false}}
""")

	# Appends " > $(whole).$(dec)$(suffix)" and never removes an earlier one.
	write_versioned_function("zombies/pap/annotate_append_dec", f"""
$data modify storage {ns}:temp _pap_extract.lore[$(index)].extra append value {{"text":" > $(whole).$(dec)$(suffix)","color":"aqua","italic":false}}
""")

	write_versioned_function("zombies/pap/set_item_lore", """
$item modify entity @s $(slot) {"type":"minecraft:set_components","components":{"minecraft:lore":$(lore)}}
	""")

	write_versioned_function("zombies/pap/apply_to_slot", f"""
$item modify entity @s $(slot) {ns}:v{version}/zb_pap_apply_stats
$data modify storage {ns}:temp _pap_name_data.slot set value "$(slot)"
function {ns}:v{version}/zombies/pap/set_item_name_with_level with storage {ns}:temp _pap_name_data
$execute if data storage {ns}:temp _pap_extract.lore[0] run data modify storage {ns}:temp _pap_apply_lore.slot set value "$(slot)"
execute if data storage {ns}:temp _pap_extract.lore[0] run data modify storage {ns}:temp _pap_apply_lore.lore set from storage {ns}:temp _pap_extract.lore
execute if data storage {ns}:temp _pap_extract.lore[0] run function {ns}:v{version}/zombies/pap/set_item_lore with storage {ns}:temp _pap_apply_lore

$data modify storage {ns}:temp _pap_scope_model.slot set value "$(slot)"
data modify storage {ns}:temp _pap_scope_model.model set from storage {ns}:temp _pap_extract.stats.models.normal
function {ns}:v{version}/zombies/pap/set_item_model_from_scope with storage {ns}:temp _pap_scope_model

$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"$(slot)"}}
""")

