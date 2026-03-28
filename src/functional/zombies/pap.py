# ruff: noqa: E501
# Pack-a-Punch machine system for zombies mode.
# Resolves PAP upgrades at runtime from the selected gun's own stats.pap_stats.
from stewbeet import ItemModifier, JsonDict, Mem, set_json_encoder, write_load_file, write_versioned_function

from ...config.stats import REMAINING_BULLETS
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

# Store display metadata for lookup
execute store result storage {ns}:temp _pap_store.id int 1 run scoreboard players get #pap_counter {ns}.data
data modify storage {ns}:temp _pap_store.name set value "Pack-a-Punch"
execute if data storage {ns}:temp _pap_iter[0].name run data modify storage {ns}:temp _pap_store.name set from storage {ns}:temp _pap_iter[0].name
function {ns}:v{version}/zombies/pap/store_data with storage {ns}:temp _pap_store

# Register Bookshelf interaction callbacks
execute as @n[tag={ns}.pap_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/pap/on_right_click",executor:"source"}}
execute as @n[tag={ns}.pap_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/pap/on_hover",executor:"source"}}
tag @n[tag={ns}.pap_new] remove {ns}.pap_new

# Continue iteration
data remove storage {ns}:temp _pap_iter[0]
execute if data storage {ns}:temp _pap_iter[0] run function {ns}:v{version}/zombies/pap/setup_iter
""")

	write_versioned_function("zombies/pap/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.2f,height:2.2f,response:true,Tags:["{ns}.pap_machine","{ns}.gm_entity","bs.entity.interaction","{ns}.pap_new"]}}
""")

	write_versioned_function("zombies/pap/store_data", f"""
$data modify storage {ns}:zombies pap_data."$(id)" set value {{name:"$(name)"}}
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

	# Append " +X" to each lore line's text-component list for current PAP level.
	write_versioned_function("zombies/pap/append_level_to_lore", f"""
	data modify storage {ns}:temp _pap_lore.in set from storage {ns}:temp _pap_extract.lore
	data modify storage {ns}:temp _pap_lore.out set value []
	execute store result storage {ns}:temp _pap_lore.level int 1 run scoreboard players get #pap_next {ns}.data
	function {ns}:v{version}/zombies/pap/append_level_to_lore_iter
	data modify storage {ns}:temp _pap_extract.lore set from storage {ns}:temp _pap_lore.out
	""")

	write_versioned_function("zombies/pap/append_level_to_lore_iter", f"""
	execute unless data storage {ns}:temp _pap_lore.in[0] run return 0
	data modify storage {ns}:temp _pap_lore.line set from storage {ns}:temp _pap_lore.in[0]
	function {ns}:v{version}/zombies/pap/append_level_to_lore_line with storage {ns}:temp _pap_lore
	data modify storage {ns}:temp _pap_lore.out append from storage {ns}:temp _pap_lore.line
	data remove storage {ns}:temp _pap_lore.in[0]
	function {ns}:v{version}/zombies/pap/append_level_to_lore_iter
	""")

	write_versioned_function("zombies/pap/append_level_to_lore_line", f"""
	$execute if data storage {ns}:temp _pap_lore.line.text unless data storage {ns}:temp _pap_lore.line.extra[0] run data modify storage {ns}:temp _pap_lore.line.extra set value []
	$execute if data storage {ns}:temp _pap_lore.line.text run data modify storage {ns}:temp _pap_lore.line.extra append value {{"text":" +$(level)","color":"dark_green","italic":false}}
	""")

	write_versioned_function("zombies/pap/set_item_name", """
	$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:item_name":{"text":"$(name)","color":"gold","italic":false}}}
""")

	write_versioned_function("zombies/pap/set_item_lore", """
	$item modify entity @s $(slot) {"function":"minecraft:set_components","components":{"minecraft:lore":$(lore)}}
	""")

	write_versioned_function("zombies/pap/apply_to_slot", f"""
$item modify entity @s $(slot) {ns}:v{version}/zb_pap_apply_stats
execute if data storage {ns}:temp _pap_extract.new_name run data modify storage {ns}:temp _pap_apply_name.slot set value "$(slot)"
execute if data storage {ns}:temp _pap_extract.new_name run data modify storage {ns}:temp _pap_apply_name.name set from storage {ns}:temp _pap_extract.new_name
execute if data storage {ns}:temp _pap_extract.new_name run function {ns}:v{version}/zombies/pap/set_item_name with storage {ns}:temp _pap_apply_name
execute if data storage {ns}:temp _pap_extract.lore[0] run data modify storage {ns}:temp _pap_apply_lore.slot set value "$(slot)"
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

# Deduct points and apply runtime overrides from pap_stats
scoreboard players operation @s {ns}.zb.points -= #pap_price {ns}.data
function {ns}:v{version}/zombies/pap/apply_runtime_overrides

# Keep level tracking in the weapon data itself
execute store result storage {ns}:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next {ns}.data

# Optional runtime PAP name override
execute if data storage {ns}:temp _pap_extract.stats.pap_stats.pap_name run function {ns}:v{version}/zombies/pap/resolve_runtime_name

# Lore visual marker for current PAP level
execute if data storage {ns}:temp _pap_extract.lore[0] run function {ns}:v{version}/zombies/pap/append_level_to_lore

# Preserve common refill behavior: if capacity is overridden and no explicit remaining_bullets override,
# refill to the new capacity for this upgrade.
execute if data storage {ns}:temp _pap_extract.stats.pap_stats.capacity unless data storage {ns}:temp _pap_extract.stats.pap_stats.{REMAINING_BULLETS} run data modify storage {ns}:temp _pap_extract.stats.{REMAINING_BULLETS} set from storage {ns}:temp _pap_extract.stats.capacity

# Apply to item and refresh ammo/lore
function {ns}:v{version}/zombies/pap/apply_to_slot with storage {ns}:temp _pap
function {ns}:v{version}/ammo/compute_reserve

# Message and feedback
execute store result storage {ns}:temp _pap_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/lookup_machine with storage {ns}:temp _pap_buy
tellraw @s [{MGS_TAG},{{"text":"Upgraded via ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_pap_machine.name","color":"gold","interpret":true}},{{"text":" to level ","color":"green"}},{{"score":{{"name":"#pap_next","objective":"{ns}.data"}},"color":"yellow"}},{{"text":".","color":"green"}}]
function {ns}:v{version}/zombies/feedback/sound_success
""")

	# Hook into preload_complete to spawn PAP machine interactions.
	write_versioned_function("zombies/preload_complete", f"""
# Setup Pack-a-Punch machines
execute if data storage {ns}:zombies game.map.pap_machines[0] run function {ns}:v{version}/zombies/pap/setup
""")
