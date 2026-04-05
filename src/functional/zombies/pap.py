# ruff: noqa: E501
# Pack-a-Punch machine system for zombies mode.
# Resolves PAP upgrades at runtime from the selected gun's own stats.pap_stats.
from stewbeet import ItemModifier, JsonDict, Mem, set_json_encoder, write_load_file, write_versioned_function

from ...config.stats import ALL_SLOTS, BASE_WEAPON, REMAINING_BULLETS
from ..helpers import MGS_TAG
from .common import deny_not_enough_points_body, deny_requires_power_body, game_active_guard_cmd

# Fields resolved dynamically from stats.pap_stats at runtime.
# No weapon IDs are hardcoded: only key names are used.
PAP_RUNTIME_FIELDS: tuple[str, ...] = (
	"capacity",
	"remaining_bullets",
	"reload_time",
	"reload_end",
	"reload_mid",
	"cooldown",
	"burst",
	"pellet_count",
	"damage",
	"decay",
	"acc_base",
	"acc_sneak",
	"acc_walk",
	"acc_sprint",
	"acc_jump",
	"switch",
	"kick",
	"proj_speed",
	"proj_gravity",
	"proj_lifetime",
	"expl_radius",
	"expl_damage",
	"expl_decay",
)


def generate_pap() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	gun_cd = "{" + ns + ":{gun:true}}"

	# Item modifier: copy upgraded stats from temp storage back into selected gun item.
	pap_stats_modifier: JsonDict = {
		"function": "minecraft:copy_custom_data",
		"source": {"type": "minecraft:storage", "source": f"{ns}:temp"},
		"ops": [
			{"source": "_pap_extract.stats", "target": f"{ns}.stats", "op": "replace"},
		],
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_pap_apply_stats"] = set_json_encoder(ItemModifier(pap_stats_modifier), max_level=-1)

	# Entity scoreboards for PAP machines.
	write_load_file(f"""
# Pack-a-Punch machine scoreboards
scoreboard objectives add {ns}.zb.pap.id dummy
scoreboard objectives add {ns}.zb.pap.price dummy
scoreboard objectives add {ns}.zb.pap.power dummy
scoreboard objectives add {ns}.pap_anim dummy
""")

	# Setup: iterate map compounds and summon interaction entities.
	write_versioned_function("zombies/pap/setup", f"""
scoreboard players set #pap_counter {ns}.data 0
data modify storage {ns}:zombies pap_data set value {{}}
data modify storage {ns}:temp _pap_iter set from storage {ns}:zombies game.map.pap_machines
execute if data storage {ns}:temp _pap_iter[0] run function {ns}:v{version}/zombies/pap/setup_iter
""")

	write_versioned_function("zombies/pap/setup_iter", f"""
# Assign incrementing machine id
scoreboard players add #pap_counter {ns}.data 1

# Convert relative map coords to absolute world coords
execute store result score #papx {ns}.data run data get storage {ns}:temp _pap_iter[0].pos[0]
execute store result score #papy {ns}.data run data get storage {ns}:temp _pap_iter[0].pos[1]
execute store result score #papz {ns}.data run data get storage {ns}:temp _pap_iter[0].pos[2]
scoreboard players operation #papx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #papy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #papz {ns}.data += #gm_base_z {ns}.data

# Store absolute coords for summon macro
execute store result storage {ns}:temp _pap_place.x int 1 run scoreboard players get #papx {ns}.data
execute store result storage {ns}:temp _pap_place.y int 1 run scoreboard players get #papy {ns}.data
execute store result storage {ns}:temp _pap_place.z int 1 run scoreboard players get #papz {ns}.data

# Summon interaction entity
function {ns}:v{version}/zombies/pap/place_at with storage {ns}:temp _pap_place

# Set machine metadata
scoreboard players operation @n[tag={ns}.pap_new] {ns}.zb.pap.id = #pap_counter {ns}.data
execute store result score @n[tag={ns}.pap_new] {ns}.zb.pap.price run data get storage {ns}:temp _pap_iter[0].price
execute store result score @n[tag={ns}.pap_new] {ns}.zb.pap.power run data get storage {ns}:temp _pap_iter[0].power

# Register Bookshelf interaction callbacks
execute as @n[tag={ns}.pap_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/pap/on_right_click",executor:"source"}}
execute as @n[tag={ns}.pap_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/pap/on_hover",executor:"source"}}

# Initialize animation state: -1 = idle
scoreboard players set @n[tag={ns}.pap_new] {ns}.pap_anim -1

# Spawn visual item_display at machine position (default: netherite_block; overridable via display_item + item_model map fields)
data modify storage {ns}:temp _pap_disp.tag set value "{ns}.pap_display"
data modify storage {ns}:temp _pap_disp.item_id set value "minecraft:netherite_block"
data modify storage {ns}:temp _pap_disp.item_model set value "minecraft:netherite_block"
execute if data storage {ns}:temp _pap_iter[0].display_item run data modify storage {ns}:temp _pap_disp.item_id set from storage {ns}:temp _pap_iter[0].display_item
execute if data storage {ns}:temp _pap_iter[0].item_model run data modify storage {ns}:temp _pap_disp.item_model set from storage {ns}:temp _pap_iter[0].item_model
execute as @n[tag={ns}.pap_new] at @s run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pap_disp

# Store display metadata for lookup (reuse the computed _pap_disp fields)
execute store result storage {ns}:temp _pap_store.id int 1 run scoreboard players get #pap_counter {ns}.data
data modify storage {ns}:temp _pap_store.name set value "Pack-a-Punch"
execute if data storage {ns}:temp _pap_iter[0].name run data modify storage {ns}:temp _pap_store.name set from storage {ns}:temp _pap_iter[0].name
data modify storage {ns}:temp _pap_store.display_tag set from storage {ns}:temp _pap_disp.tag
data modify storage {ns}:temp _pap_store.display_item_id set from storage {ns}:temp _pap_disp.item_id
data modify storage {ns}:temp _pap_store.display_item_model set from storage {ns}:temp _pap_disp.item_model
function {ns}:v{version}/zombies/pap/store_data with storage {ns}:temp _pap_store

tag @n[tag={ns}.pap_new] remove {ns}.pap_new

# Continue iteration
data remove storage {ns}:temp _pap_iter[0]
execute if data storage {ns}:temp _pap_iter[0] run function {ns}:v{version}/zombies/pap/setup_iter
""")

	write_versioned_function("zombies/pap/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.2f,height:2.2f,response:true,Tags:["{ns}.pap_machine","{ns}.gm_entity","bs.entity.interaction","{ns}.pap_new"]}}
""")

	write_versioned_function("zombies/pap/store_data", f"""
$data modify storage {ns}:zombies pap_data."$(id)" set value {{name:"$(name)",display_tag:"$(display_tag)",display_item_id:"$(display_item_id)",display_item_model:"$(display_item_model)"}}
""")

	write_versioned_function("zombies/pap/lookup_machine", f"""
$data modify storage {ns}:temp _pap_machine set from storage {ns}:zombies pap_data."$(id)"
""")

	write_versioned_function("zombies/pap/on_hover", f"""
execute store result score #pap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.price
execute store result storage {ns}:temp _pap_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/lookup_machine with storage {ns}:temp _pap_hover
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚙ ","color":"dark_red"}},{{"storage":"{ns}:temp","nbt":"_pap_machine.name","color":"gold","interpret":true}},{{"text":" - Cost: ","color":"gray"}},{{"score":{{"name":"#pap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}],priority:'notification',freeze:5}}
function #smithed.actionbar:message
""")

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

	# Dynamic list picker helpers (no hardcoded max level).
	# _pap_pick.list: the PAP list to resolve
	# #pap_next_idx: 0-based requested level index
	# _pap_pick.value: resolved value (clamped to last available entry)
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
	for field in PAP_RUNTIME_FIELDS:
		compute_max_lines.append(
			f'execute if data storage {ns}:temp _pap_extract.stats.pap_stats.{field}[0] store result score #pap_len {ns}.data run data get storage {ns}:temp _pap_extract.stats.pap_stats.{field}'
		)
		compute_max_lines.append(
			f'execute if score #pap_len {ns}.data > #pap_max {ns}.data run scoreboard players operation #pap_max {ns}.data = #pap_len {ns}.data'
		)
	compute_max_lines.append(
		f'execute if data storage {ns}:temp _pap_extract.stats.pap_stats.pap_name[0] store result score #pap_len {ns}.data run data get storage {ns}:temp _pap_extract.stats.pap_stats.pap_name'
	)
	compute_max_lines.append(
		f'execute if score #pap_len {ns}.data > #pap_max {ns}.data run scoreboard players operation #pap_max {ns}.data = #pap_len {ns}.data'
	)
	write_versioned_function("zombies/pap/compute_max_level", "\n".join(compute_max_lines))

	# Apply one PAP field dynamically from stats.pap_stats.<field> for #pap_next_idx.
	for field in PAP_RUNTIME_FIELDS:
		field_lines: list[str] = [
			f'data modify storage {ns}:temp _pap_pick.list set from storage {ns}:temp _pap_extract.stats.pap_stats.{field}',
			f'execute if data storage {ns}:temp _pap_pick.list[0] run function {ns}:v{version}/zombies/pap/pick_list_value',
			f'execute if data storage {ns}:temp _pap_pick.list[0] run data modify storage {ns}:temp _pap_extract.stats.{field} set from storage {ns}:temp _pap_pick.value',
			f'execute unless data storage {ns}:temp _pap_pick.list[0] run data modify storage {ns}:temp _pap_extract.stats.{field} set from storage {ns}:temp _pap_extract.stats.pap_stats.{field}',
		]
		write_versioned_function(f"zombies/pap/apply_field/{field}", "\n".join(field_lines))

	apply_lines: list[str] = []
	for field in PAP_RUNTIME_FIELDS:
		apply_lines.append(
			f'execute if data storage {ns}:temp _pap_extract.stats.pap_stats.{field} run function {ns}:v{version}/zombies/pap/apply_field/{field}'
		)
	write_versioned_function("zombies/pap/apply_runtime_overrides", "\n".join(apply_lines))

	# Resolve optional pap_name dynamically (scalar or list).
	name_lines: list[str] = [
		f'data modify storage {ns}:temp _pap_pick.list set from storage {ns}:temp _pap_extract.stats.pap_stats.pap_name',
		f'execute if data storage {ns}:temp _pap_pick.list[0] run function {ns}:v{version}/zombies/pap/pick_list_value',
		f'execute if data storage {ns}:temp _pap_pick.list[0] run data modify storage {ns}:temp _pap_extract.new_name set from storage {ns}:temp _pap_pick.value',
		f'execute unless data storage {ns}:temp _pap_pick.list[0] run data modify storage {ns}:temp _pap_extract.new_name set from storage {ns}:temp _pap_extract.stats.pap_stats.pap_name',
	]
	write_versioned_function("zombies/pap/resolve_runtime_name", "\n".join(name_lines))

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

	# Line 1: Ammo (skip — updated by ammo.py)
	annotate_lore_lines.append(f'scoreboard players add #pap_li {ns}.data 1')

	# Line 2: Reload Time (ticks → seconds)
	annotate_lore_lines.extend([
		f'execute store result score #pap_old {ns}.data run data get storage {ns}:temp _pap_old_stats.reload_time',
		f'execute store result score #pap_new {ns}.data run data get storage {ns}:temp _pap_extract.stats.reload_time',
		f'scoreboard players operation #pap_delta {ns}.data = #pap_new {ns}.data',
		f'scoreboard players operation #pap_delta {ns}.data -= #pap_old {ns}.data',
		f'execute unless score #pap_delta {ns}.data matches 0 run function {ns}:v{version}/zombies/pap/annotate_time_delta',
		f'scoreboard players add #pap_li {ns}.data 1',
	])

	# Line 3 (conditional): Fire Rate — only if weapon has cooldown
	annotate_lore_lines.append(
		f'execute if data storage {ns}:temp _pap_extract.stats.cooldown run function {ns}:v{version}/zombies/pap/annotate_fire_rate_line'
	)

	# Line N (conditional): Pellets — only if weapon has pellet_count
	annotate_lore_lines.append(
		f'execute if data storage {ns}:temp _pap_extract.stats.pellet_count run function {ns}:v{version}/zombies/pap/annotate_pellets_line'
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
$function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"$(slot)"}}
""")

	write_versioned_function("zombies/pap/deny_requires_power", f"""
{deny_requires_power_body(ns, version, "Pack-a-Punch machine")}
""")

	write_versioned_function("zombies/pap/deny_not_enough_points", f"""
{deny_not_enough_points_body(ns, version, "#pap_price")}
""")

	write_versioned_function("zombies/pap/deny_hold_weapon_slot", f"""
tellraw @s [{MGS_TAG},{{"text":"Hold weapon slot 1, 2, or 3 to use Pack-a-Punch.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/pap/deny_not_gun", f"""
tellraw @s [{MGS_TAG},{{"text":"Selected slot does not contain a weapon.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/pap/deny_not_supported", f"""
tellraw @s [{MGS_TAG},{{"text":"This weapon cannot be Pack-a-Punched.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/pap/deny_max_level", f"""
tellraw @s [{MGS_TAG},{{"text":"This weapon is already at max Pack-a-Punch level.","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/pap/on_right_click", f"""
# Guard: game must be active
{game_active_guard_cmd(ns)}

# If weapon is coming-out (100..129) or retreating (-61..-2): allow collection
execute if score @n[tag=bs.interaction.target] {ns}.pap_anim matches 100..129 run return run function {ns}:v{version}/zombies/pap/anim_collect
execute if score @n[tag=bs.interaction.target] {ns}.pap_anim matches -61..-2 run return run function {ns}:v{version}/zombies/pap/anim_collect
# If machine is going-in or inside (not yet collectible), deny
execute if score @n[tag=bs.interaction.target] {ns}.pap_anim matches 130.. run return run function {ns}:v{version}/zombies/pap/anim_deny_processing

# Guard: power requirement
execute store result score #pap_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.power
execute if score #pap_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run function {ns}:v{version}/zombies/pap/deny_requires_power

# Guard: player has enough points
execute store result score #pap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.price
execute unless score @s {ns}.zb.points >= #pap_price {ns}.data run return run function {ns}:v{version}/zombies/pap/deny_not_enough_points

# Determine selected zombies weapon slot (must be hotbar.1/2/3)
execute store result score #pap_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #pap_sel {ns}.data matches 1..3 run return run function {ns}:v{version}/zombies/pap/deny_hold_weapon_slot

data modify storage {ns}:temp _pap.slot set value "hotbar.1"
execute if score #pap_sel {ns}.data matches 2 run data modify storage {ns}:temp _pap.slot set value "hotbar.2"
execute if score #pap_sel {ns}.data matches 3 run data modify storage {ns}:temp _pap.slot set value "hotbar.3"

# Guard: selected slot must contain a gun item
scoreboard players set #pap_is_gun {ns}.data 0
execute if score #pap_sel {ns}.data matches 1 if items entity @s hotbar.1 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute if score #pap_sel {ns}.data matches 2 if items entity @s hotbar.2 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute if score #pap_sel {ns}.data matches 3 if items entity @s hotbar.3 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute unless score #pap_is_gun {ns}.data matches 1 run return run function {ns}:v{version}/zombies/pap/deny_not_gun

# Extract selected item data
function {ns}:v{version}/zombies/pap/extract_selected with storage {ns}:temp _pap

# Guard: selected weapon must provide PAP data in its own stats
execute unless data storage {ns}:temp _pap_extract.stats.pap_stats run return run function {ns}:v{version}/zombies/pap/deny_not_supported

# Compute current and next PAP levels
scoreboard players set #pap_level {ns}.data 0
execute if data storage {ns}:temp _pap_extract.stats.pap_level store result score #pap_level {ns}.data run data get storage {ns}:temp _pap_extract.stats.pap_level
scoreboard players operation #pap_next {ns}.data = #pap_level {ns}.data
scoreboard players add #pap_next {ns}.data 1
scoreboard players operation #pap_next_idx {ns}.data = #pap_next {ns}.data
scoreboard players remove #pap_next_idx {ns}.data 1

# Guard: next level must be <= runtime max derived from pap_stats lists
function {ns}:v{version}/zombies/pap/compute_max_level
execute if score #pap_next {ns}.data > #pap_max {ns}.data run return run function {ns}:v{version}/zombies/pap/deny_max_level

# Backup visible stats for lore annotation before overrides
data modify storage {ns}:temp _pap_old_stats set from storage {ns}:temp _pap_extract.stats

# Deduct points and apply runtime overrides from pap_stats
scoreboard players operation @s {ns}.zb.points -= #pap_price {ns}.data
function {ns}:v{version}/zombies/pap/apply_runtime_overrides

# Keep level tracking in the weapon data itself
execute store result storage {ns}:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next {ns}.data

# Resolve pre-built PAP display name with level suffix
execute if data storage {ns}:temp _pap_extract.stats.pap_stats.pap_name run function {ns}:v{version}/zombies/pap/resolve_runtime_name

# Prepare name data: use PAP name if available, otherwise keep original
execute if data storage {ns}:temp _pap_extract.new_name run data modify storage {ns}:temp _pap_name_data.name set from storage {ns}:temp _pap_extract.new_name
execute unless data storage {ns}:temp _pap_extract.new_name run data modify storage {ns}:temp _pap_name_data.name set from storage {ns}:temp _pap_extract.current_name
execute store result storage {ns}:temp _pap_name_data.level int 1 run scoreboard players get #pap_next {ns}.data
execute store result storage {ns}:temp _pap_name_data.max int 1 run scoreboard players get #pap_max {ns}.data

# Annotate lore lines with runtime-computed PAP deltas
execute if data storage {ns}:temp _pap_extract.lore[0] run function {ns}:v{version}/zombies/pap/annotate_lore

# Always refill gun ammo to max capacity on PAP
data modify storage {ns}:temp _pap_extract.stats.{REMAINING_BULLETS} set from storage {ns}:temp _pap_extract.stats.capacity

# Apply to item, refill matching magazines, and refresh ammo display
function {ns}:v{version}/zombies/pap/apply_to_slot with storage {ns}:temp _pap
function {ns}:v{version}/zombies/pap/refill_matching_magazines with storage {ns}:temp _pap_extract.stats
function {ns}:v{version}/ammo/compute_reserve

# Message and feedback
execute store result storage {ns}:temp _pap_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/lookup_machine with storage {ns}:temp _pap_buy
function {ns}:v{version}/zombies/pap/pap_chat_message
function {ns}:v{version}/zombies/feedback/sound_success

# Take weapon from player and start PAP animation
tag @s add {ns}.pap_owner
execute as @n[tag=bs.interaction.target] at @s run function {ns}:v{version}/zombies/pap/anim_start with storage {ns}:temp _pap
tag @s remove {ns}.pap_owner
""")

	# Refill all magazine items in inventory that match the PAP'd weapon's base_weapon.
	mag_refill_lines: list[str] = [f"# Refill matching {BASE_WEAPON} magazines — called with storage mgs:temp _pap_extract.stats"]
	for slot in ALL_SLOTS:
		if slot == "weapon.mainhand":
			continue
		mag_refill_lines.append(
			f'$execute if items entity @s {slot} *[custom_data~{{{ns}:{{magazine:true,weapon:"$({BASE_WEAPON})"}}}}] run function {ns}:v{version}/zombies/bonus/refill_magazine {{slot:"{slot}"}}'
		)
	write_versioned_function("zombies/pap/refill_matching_magazines", "\n".join(mag_refill_lines))

	# Macro: send one lore-line compound as a tellraw text component (with prefix).
	write_versioned_function("zombies/pap/pap_chat_lore_line", """$tellraw @s [{"text":"- ","color":"gray"},$(line)]\n""")

	# Macro: copy lore[$(index)] to _pap_lore_line.line and display if non-empty.
	write_versioned_function("zombies/pap/pap_chat_lore_iter", f"""
$data modify storage {ns}:temp _pap_lore_line.line set from storage {ns}:temp _pap_extract.lore[$(index)]
execute if data storage {ns}:temp _pap_lore_line.line unless data storage {ns}:temp _pap_lore_line.line{{text:""}} run function {ns}:v{version}/zombies/pap/pap_chat_lore_line with storage {ns}:temp _pap_lore_line
""")

	# Loop: iterates indices 0 .. #pap_lore_len-1, calling pap_chat_lore_iter each step.
	write_versioned_function("zombies/pap/pap_chat_lore_loop", f"""
execute store result storage {ns}:temp _pap_lore_idx.index int 1 run scoreboard players get #pap_li {ns}.data
function {ns}:v{version}/zombies/pap/pap_chat_lore_iter with storage {ns}:temp _pap_lore_idx
scoreboard players add #pap_li {ns}.data 1
execute if score #pap_li {ns}.data < #pap_lore_len {ns}.data run function {ns}:v{version}/zombies/pap/pap_chat_lore_loop
""")

	# Detailed PAP upgrade chat message.
	pap_chat_lines: list[str] = [
		f'tellraw @s [{MGS_TAG},{{"text":"Machine: ","color":"gray"}},{{"storage":"{ns}:temp","nbt":"_pap_machine.name","color":"gold","italic":false,"interpret":true}},{{"text":"\\nLevel: ","color":"gray"}},{{"score":{{"name":"#pap_next","objective":"{ns}.data"}},"color":"aqua"}},{{"text":"/","color":"dark_gray"}},{{"score":{{"name":"#pap_max","objective":"{ns}.data"}},"color":"aqua"}},{{"text":"  Cost: -","color":"gray"}},{{"score":{{"name":"#pap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}]',
		'tellraw @s [{"text":"Weapon stats:","color":"gray","italic":true}]',
		# Compute (len - 2) to skip the last 2 entries (switch time + empty separator)
		f'execute store result score #pap_lore_len {ns}.data run data get storage {ns}:temp _pap_extract.lore',
		f'scoreboard players remove #pap_lore_len {ns}.data 2',
		f'scoreboard players set #pap_li {ns}.data 0',
		f'execute if score #pap_li {ns}.data < #pap_lore_len {ns}.data run function {ns}:v{version}/zombies/pap/pap_chat_lore_loop',
	]
	write_versioned_function("zombies/pap/pap_chat_message", "\n".join(pap_chat_lines))

	# --- PAP Animation System ---
	# Timeline (200 ticks total):
	#   200→171 (30 t): GOING IN   — weapon slowly enters machine
	#   170→131 (40 t): INSIDE     — processing particles + periodic sound
	#   130→101 (30 t): COMING OUT — weapon ejects upward
	#   100→1   (100 t): COLLECT WAIT / RETREAT — glowing, player clicks to collect

	# Spawn buffer armor_stand + weapon item_display, transfer weapon, start timer.
	write_versioned_function("zombies/pap/anim_start", f"""
# @s = PAP machine entity, AT machine position
# $(slot) = player weapon slot (hotbar.1 / hotbar.2 / hotbar.3)

# Summon weapon item_display (starts 1.5 blocks above machine via Y=+1.0 translation on a ~0.5 spawn)
summon minecraft:item_display ~ ~0.5 ~ {{Tags:["{ns}.pap_weapon_display","{ns}.gm_entity"],billboard:"fixed",item_display:"fixed",Glowing:0b,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,1.0f,0f],scale:[0.8f,0.8f,0.8f]}}}}

# Transfer weapon into display entity via contents slot, then clear player slot
$item replace entity @n[tag={ns}.pap_weapon_display,distance=..2] contents from entity @p[tag={ns}.pap_owner] $(slot)
$item replace entity @p[tag={ns}.pap_owner] $(slot) with minecraft:air

# Start going-in interpolation immediately: Y from +1.0 to -0.5 over 30 ticks
data merge entity @n[tag={ns}.pap_weapon_display,distance=..2] {{interpolation_duration:30,start_interpolation:0,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,-0.5f,0f],scale:[0.8f,0.8f,0.8f]}}}}

# Store this machine's slot for later retrieval when player collects the weapon
execute store result storage {ns}:temp _pap_anim_slot.id int 1 run scoreboard players get @s {ns}.zb.pap.id
$data modify storage {ns}:temp _pap_anim_slot.slot set value "$(slot)"
function {ns}:v{version}/zombies/pap/anim_store_slot with storage {ns}:temp _pap_anim_slot

# Hide the static item_display temporarily (restored on collect or retreat finish)
kill @e[tag={ns}.pap_display,distance=..2]

# Start animation timer: 200 ticks (30 going-in + 40 inside + 30 coming-out; retreat starts immediately after)
scoreboard players set @s {ns}.pap_anim 200

# Sound: machine accepting weapon
playsound minecraft:block.beacon.activate ambient @a[distance=..30] ~ ~ ~ 1.0 0.6
""")

	# Persist weapon slot keyed by machine ID in zombies storage.
	write_versioned_function("zombies/pap/anim_store_slot", f"""
$data modify storage {ns}:zombies pap_anim_slot."$(id)" set value "$(slot)"
""")

	# Main per-machine tick dispatcher (runs as machine when pap_anim >= 1).
	write_versioned_function("zombies/pap/anim_step", f"""
# Decrement timer
scoreboard players remove @s {ns}.pap_anim 1

# Phase: GOING IN (timer 170..199)
execute if score @s {ns}.pap_anim matches 170..199 run function {ns}:v{version}/zombies/pap/anim_going_in

# Phase: INSIDE (timer 130..169)
execute if score @s {ns}.pap_anim matches 130..169 run function {ns}:v{version}/zombies/pap/anim_inside

# Trigger: start coming-out interpolation at timer=129 (first tick of coming-out)
execute if score @s {ns}.pap_anim matches 129 run function {ns}:v{version}/zombies/pap/anim_trigger_coming_out

# Phase: COMING OUT (timer 100..129)
execute if score @s {ns}.pap_anim matches 100..129 run function {ns}:v{version}/zombies/pap/anim_coming_out

# Trigger: weapon fully emerged — immediately start retreat (CoD style, at timer=100)
execute if score @s {ns}.pap_anim matches 100 run function {ns}:v{version}/zombies/pap/anim_trigger_retreat
""")

	# Sparse purple particles during the going-in phase.
	write_versioned_function("zombies/pap/anim_going_in", f"""
# Sparse purple dust every 2 ticks
execute store result score #pap_t {ns}.data run scoreboard players get @s {ns}.pap_anim
scoreboard players operation #pap_t {ns}.data %= #2 {ns}.data
execute if score #pap_t {ns}.data matches 0 run particle dust{{color:[0.565,0.0,1.0],scale:1.5}} ~ ~1.0 ~ 0.3 0.3 0.3 0 4 force
""")

	# Dense particles and sounds while the weapon is being processed inside the machine.
	write_versioned_function("zombies/pap/anim_inside", f"""
# Dense purple dust + end_rod particles every tick
particle dust{{color:[0.565,0.0,1.0],scale:1.5}} ~ ~0.5 ~ 0.4 0.5 0.4 0 6 force
particle end_rod ~ ~0.5 ~ 0.3 0.3 0.3 0.05 4 force

# Periodic processing sound every 10 ticks
execute store result score #pap_t {ns}.data run scoreboard players get @s {ns}.pap_anim
scoreboard players operation #pap_t {ns}.data %= #10 {ns}.data
execute if score #pap_t {ns}.data matches 0 run playsound minecraft:block.enchantment_table.use ambient @a[distance=..30] ~ ~ ~ 0.8 1.2
""")

	# Trigger coming-out interpolation (fires once at the transition tick).
	write_versioned_function("zombies/pap/anim_trigger_coming_out", f"""
# Interpolate weapon display upward: Y from -0.5 to +1.2 over 30 ticks, slight scale increase
data merge entity @n[tag={ns}.pap_weapon_display,distance=..2] {{interpolation_duration:30,start_interpolation:0,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,1.2f,0f],scale:[0.85f,0.85f,0.85f]}}}}
playsound minecraft:block.beacon.activate ambient @a[distance=..30] ~ ~ ~ 1.5 0.8
""")

	# End_rod and purple particles during the coming-out phase.
	write_versioned_function("zombies/pap/anim_coming_out", r"""
particle end_rod ~ ~0.5 ~ 0.3 0.5 0.3 0.05 6 force
particle dust{color:[0.565,0.0,1.0],scale:1.5} ~ ~1.0 ~ 0.4 0.4 0.4 0 5 force
""")

	# Trigger: weapon fully emerged — immediately start slow retreat (CoD BO style).
	write_versioned_function("zombies/pap/anim_trigger_retreat", f"""
# Weapon is out — start slow retreat back into machine (60 ticks = 3s). Collectible until inside.
data merge entity @n[tag={ns}.pap_weapon_display,distance=..2] {{Glowing:1b,interpolation_duration:60,start_interpolation:0,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,-0.5f,0f],scale:[0.8f,0.8f,0.8f]}}}}

# Switch to retreat mode (-2 to -62 over 60 ticks)
scoreboard players set @s {ns}.pap_anim -2

# Sound + particle burst + broadcast
particle end_rod ~ ~1.2 ~ 0.5 0.5 0.5 0.1 20 force
playsound minecraft:ui.toast.challenge_complete ambient @a[distance=..30] ~ ~ ~ 0.8 1.0
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Weapon upgraded! Collect it before it goes back in!","color":"aqua"}}]
""")

	# Timeout: safety net if pap_anim somehow reaches 0 (should not happen with new CoD logic).
	write_versioned_function("zombies/pap/anim_timeout", f"""
# Weapon not collected — retreat slowly into the machine over 60 ticks
data merge entity @n[tag={ns}.pap_weapon_display,distance=..2] {{Glowing:0b,interpolation_duration:60,start_interpolation:0,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,-0.5f,0f],scale:[0.8f,0.8f,0.8f]}}}}

# Enter retreat mode: pap_anim -2 → -62 over 60 ticks
scoreboard players set @s {ns}.pap_anim -2

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The weapon was not collected and is being returned to the machine!","color":"red"}}]
playsound minecraft:block.fire.extinguish ambient @a[distance=..30] ~ ~ ~ 0.8 0.8
""")

	# Per-tick: decrement retreat timer and emit smoke.
	write_versioned_function("zombies/pap/anim_retreat_step", f"""
scoreboard players remove @s {ns}.pap_anim 1
particle smoke ~ ~0.5 ~ 0.2 0.2 0.2 0.05 2 force
""")

	# Retreat finished: spawn dropped weapon item, remove display, restore static display.
	write_versioned_function("zombies/pap/anim_retreat_finish", f"""
# Spawn an item entity and copy the weapon from the display into it (dropping to the ground)
summon minecraft:item ~ ~0.5 ~ {{PickupDelay:40,Tags:["{ns}.pap_drop"],Item:{{id:"minecraft:stone",count:1}}}}
data modify entity @n[tag={ns}.pap_drop,distance=..1] Item set from entity @n[tag={ns}.pap_weapon_display,distance=..2] item
tag @n[tag={ns}.pap_drop,distance=..1] remove {ns}.pap_drop

# Remove weapon display
kill @e[tag={ns}.pap_weapon_display,distance=..2]

# Reset to idle
scoreboard players set @s {ns}.pap_anim -1

# Restore static machine display
function {ns}:v{version}/zombies/pap/anim_restore_display

# Sound
playsound minecraft:entity.generic.extinguish_fire ambient @a[distance=..20] ~ ~ ~ 1.0 0.8
""")

	# Called from on_right_click when machine pap_anim is in collect-wait range (1..100).
	write_versioned_function("zombies/pap/anim_collect", f"""
# Tag the clicking player so machine-context functions can target them precisely
tag @s add {ns}.pap_owner
execute as @n[tag=bs.interaction.target] at @s run function {ns}:v{version}/zombies/pap/anim_collect_at_machine
tag @s remove {ns}.pap_owner
""")

	# Resolve machine ID and call lookup (runs as machine).
	write_versioned_function("zombies/pap/anim_collect_at_machine", f"""
execute store result storage {ns}:temp _pap_c.id int 1 run scoreboard players get @s {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/anim_collect_lookup with storage {ns}:temp _pap_c
""")

	# Macro $(id): fetch stored slot string, then call give.
	write_versioned_function("zombies/pap/anim_collect_lookup", f"""
$data modify storage {ns}:temp _pap_cg.slot set from storage {ns}:zombies pap_anim_slot."$(id)"
function {ns}:v{version}/zombies/pap/anim_collect_give with storage {ns}:temp _pap_cg
""")

	# Macro $(slot): give weapon back, cleanup, restore display, notify.
	# Macro $(slot): give weapon back from display entity's contents slot, cleanup, restore display, notify.
	write_versioned_function("zombies/pap/anim_collect_give", f"""
# Return upgraded weapon directly from the display entity's contents slot
$item replace entity @p[tag={ns}.pap_owner] $(slot) from entity @n[tag={ns}.pap_weapon_display,distance=..2] contents

# Refresh ammo HUD
execute as @p[tag={ns}.pap_owner] run function {ns}:v{version}/ammo/compute_reserve

# Reset animation timer to idle
scoreboard players set @s {ns}.pap_anim -1

# Remove weapon display (item already given back, safe to kill)
kill @e[tag={ns}.pap_weapon_display,distance=..2]

# Restore the static machine display entity
function {ns}:v{version}/zombies/pap/anim_restore_display

# Notify the player
execute as @p[tag={ns}.pap_owner] run tellraw @s [{MGS_TAG},{{"text":"Collect your upgraded weapon!","color":"green","bold":true}}]
execute as @p[tag={ns}.pap_owner] run function {ns}:v{version}/zombies/feedback/sound_success
""")

	# Re-summon the static item_display for the machine (runs as machine).
	write_versioned_function("zombies/pap/anim_restore_display", f"""
execute store result storage {ns}:temp _pap_restore.id int 1 run scoreboard players get @s {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/anim_restore_display_lookup with storage {ns}:temp _pap_restore
""")

	# Macro $(id): fetch stored display metadata and call summon_machine_display.
	write_versioned_function("zombies/pap/anim_restore_display_lookup", f"""
$data modify storage {ns}:temp _pap_restore_disp.tag set from storage {ns}:zombies pap_data."$(id)".display_tag
$data modify storage {ns}:temp _pap_restore_disp.item_id set from storage {ns}:zombies pap_data."$(id)".display_item_id
$data modify storage {ns}:temp _pap_restore_disp.item_model set from storage {ns}:zombies pap_data."$(id)".display_item_model
function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pap_restore_disp
""")

	# Deny message when machine is busy.
	write_versioned_function("zombies/pap/anim_deny_processing", f"""
tellraw @s [{MGS_TAG},{{"text":"The Pack-a-Punch machine is currently processing a weapon...","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	# Hook PAP animation into the game tick loop.
	write_versioned_function("zombies/game_tick", f"""
# PAP animation tick
execute as @e[tag={ns}.pap_machine,scores={{{ns}.pap_anim=1..}}] at @s run function {ns}:v{version}/zombies/pap/anim_step
execute as @e[tag={ns}.pap_machine,scores={{{ns}.pap_anim=0}}] at @s run function {ns}:v{version}/zombies/pap/anim_timeout
execute as @e[tag={ns}.pap_machine,scores={{{ns}.pap_anim=-61..-2}}] at @s run function {ns}:v{version}/zombies/pap/anim_retreat_step
execute as @e[tag={ns}.pap_machine,scores={{{ns}.pap_anim=-62}}] at @s run function {ns}:v{version}/zombies/pap/anim_retreat_finish
""")

	# Hook into preload_complete to spawn PAP machine interactions.
	write_versioned_function("zombies/preload_complete", f"""
# Setup Pack-a-Punch machines
execute if data storage {ns}:zombies game.map.pap_machines[0] run function {ns}:v{version}/zombies/pap/setup
""")

