""" Building the loadout entry from the editor state and writing it back to storage. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ....helpers import MGS_TAG
from ...classes import MultiplayerClasses
from ..catalogs import GRENADE_TYPES, PICK10_TOTAL, PRIMARY_WEAPONS, SECONDARY_WEAPONS, TRIG_SAVE_PUBLIC
from .shared import editor_fn


# Functions
def write_editor_save() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## SAVE — build the loadout entry from the editor state Pre-generate weapon slot lookup tables
	primary_slot_entries: list[str] = []
	for wp in PRIMARY_WEAPONS:
		gun_id, mag_id, mag_count = wp.item_id, wp.magazine_id, wp.default_mag_count
		gun_slot = f'{{slot:"hotbar.1",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}'
		is_consumable = "1b" if mag_id in MultiplayerClasses.CONSUMABLE_MAGS else "0b"
		bullets = mag_count if mag_id in MultiplayerClasses.CONSUMABLE_MAGS else 0
		primary_slot_entries.append(
			f'{{id:"{gun_id}",gun_slot:{gun_slot},mag_id:"{mag_id}",mag_consumable:{is_consumable},mag_bullets:{bullets}}}'
		)
	secondary_slot_entries: list[str] = []
	for wp in (w for w in SECONDARY_WEAPONS if w.in_loadout):
		gun_id, mag_id, mag_count = wp.item_id, wp.magazine_id, wp.default_mag_count
		gun_slot = f'{{slot:"hotbar.2",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}'
		is_consumable = "1b" if mag_id in MultiplayerClasses.CONSUMABLE_MAGS else "0b"
		bullets = mag_count if mag_id in MultiplayerClasses.CONSUMABLE_MAGS else 0
		secondary_slot_entries.append(
			f'{{id:"{gun_id}",gun_slot:{gun_slot},mag_id:"{mag_id}",mag_consumable:{is_consumable},mag_bullets:{bullets}}}'
		)

	write_load_file(f"""
# Slot lookup tables for custom loadout editor (pre-computed at build time)
data modify storage {ns}:multiplayer primary_slot_table set value [{",".join(primary_slot_entries)}]
data modify storage {ns}:multiplayer secondary_slot_table set value [{",".join(secondary_slot_entries)}]
""")

	save_primary_dispatch = ""
	for idx, wp in enumerate(PRIMARY_WEAPONS):
		gun_id = wp.item_id
		save_primary_dispatch += (
			f'execute if data storage {ns}:temp editor{{primary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.primary_data set from storage {ns}:multiplayer primary_slot_table[{idx}]\n'
		)
	save_secondary_dispatch = ""
	for idx, wp in enumerate(w for w in SECONDARY_WEAPONS if w.in_loadout):
		gun_id = wp.item_id
		save_secondary_dispatch += (
			f'execute if data storage {ns}:temp editor{{secondary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.secondary_data set from storage {ns}:multiplayer secondary_slot_table[{idx}]\n'
		)
	# Overkill: the secondary may be a primary weapon — look it up in the primary table instead
	for idx, wp in enumerate(PRIMARY_WEAPONS):
		gun_id = wp.item_id
		save_secondary_dispatch += (
			f'execute if data storage {ns}:temp editor{{secondary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.secondary_data set from storage {ns}:multiplayer primary_slot_table[{idx}]\n'
		)

	equip_name_dispatch: dict[int, str] = {}
	for slot_num, field in [(1, "equip_slot1"), (2, "equip_slot2")]:
		equip_name_dispatch[slot_num] = "\n".join(
			f'execute if data storage {ns}:temp editor{{{field}:"{g.item_id}"}} run data modify storage {ns}:temp _new_loadout.{field}_name set value "{g.display_name}"'
			for g in GRENADE_TYPES if g.item_id
		)

	write_versioned_function("multiplayer/editor/save", f"""
# Guard: a primary weapon is required (hub grays save out, but triggers can be sent manually)
execute if data storage {ns}:temp editor{{primary:""}} run tellraw @s [{MGS_TAG},{{"text":"A primary weapon is required to save!","color":"red"}}]
execute if data storage {ns}:temp editor{{primary:""}} run return run function {fn}/hub

# Refresh the budget so points_used is accurate
function {fn}/recompute_points

# Determine visibility from trigger value
scoreboard players set #cl_public {ns}.data 0
execute if score @s {ns}.player.config matches {TRIG_SAVE_PUBLIC} run scoreboard players set #cl_public {ns}.data 1

# Initialize build workspace
data modify storage {ns}:temp _build set value {{}}

# Look up primary weapon slot data
{save_primary_dispatch}
# Look up secondary weapon slot data
{save_secondary_dispatch}
# Overkill: a primary used as secondary comes from the primary table (slot hotbar.1) — force hotbar.2
execute if data storage {ns}:temp _build.secondary_data run data modify storage {ns}:temp _build.secondary_data.gun_slot.slot set value "hotbar.2"

# Build the new loadout entry (include new Pick-10 fields)
data modify storage {ns}:temp _new_loadout set value {{id:0,owner_pid:0,owner_name:"",name:"",public:0b,likes:0,favorites_count:0,points_used:0,main_gun:"",main_gun_display:"",secondary_gun:"",secondary_gun_display:"None",primary_mag_count:1,secondary_mag_count:0,equip_slot1:"",equip_slot1_name:"None",equip_slot2:"",equip_slot2_name:"None",perks:[],slots:[]}}
# Set loadout ID: from the counter for new loadouts, or keep the edited loadout's id
execute if score @s {ns}.mp.edit_target matches ..0 store result storage {ns}:temp _new_loadout.id int 1 run data get storage {ns}:multiplayer next_loadout_id
execute if score @s {ns}.mp.edit_target matches 1.. store result storage {ns}:temp _new_loadout.id int 1 run scoreboard players get @s {ns}.mp.edit_target

# Increment the counter (new loadouts only)
execute if score @s {ns}.mp.edit_target matches ..0 store result score #temp {ns}.data run data get storage {ns}:multiplayer next_loadout_id
execute if score @s {ns}.mp.edit_target matches ..0 run scoreboard players add #temp {ns}.data 1
execute if score @s {ns}.mp.edit_target matches ..0 store result storage {ns}:multiplayer next_loadout_id int 1 run scoreboard players get #temp {ns}.data

# Set owner info
execute store result storage {ns}:temp _new_loadout.owner_pid int 1 run scoreboard players get @s {ns}.mp.pid

# Capture owner username via player head loot table trick
tag @s add {ns}.username_getter
execute at @s summon item_display run function {ns}:v{version}/multiplayer/get_username
tag @s remove {ns}.username_getter

# Set weapon IDs (scope/camo-modified)
data modify storage {ns}:temp _new_loadout.main_gun set from storage {ns}:temp editor.primary_full
data modify storage {ns}:temp _new_loadout.secondary_gun set from storage {ns}:temp editor.secondary_full

# Copy Pick-10 fields from editor
data modify storage {ns}:temp _new_loadout.primary_mag_count set from storage {ns}:temp editor.primary_mag_count
data modify storage {ns}:temp _new_loadout.secondary_mag_count set from storage {ns}:temp editor.secondary_mag_count
data modify storage {ns}:temp _new_loadout.equip_slot1 set from storage {ns}:temp editor.equip_slot1
data modify storage {ns}:temp _new_loadout.equip_slot2 set from storage {ns}:temp editor.equip_slot2
data modify storage {ns}:temp _new_loadout.perks set from storage {ns}:temp editor.perks

# Embed the full editor state so the loadout can be re-opened for editing later
data modify storage {ns}:temp _new_loadout.editor_state set from storage {ns}:temp editor

# Compute points used = PICK10_TOTAL - remaining
scoreboard players set #pts_used {ns}.data {PICK10_TOTAL}
scoreboard players operation #pts_used {ns}.data -= @s {ns}.mp.edit_points
execute store result storage {ns}:temp _new_loadout.points_used int 1 run scoreboard players get #pts_used {ns}.data

# Set equip slot display names
execute if data storage {ns}:temp editor{{equip_slot1:""}} run data modify storage {ns}:temp _new_loadout.equip_slot1_name set value "None"
{equip_name_dispatch[1]}
execute if data storage {ns}:temp editor{{equip_slot2:""}} run data modify storage {ns}:temp _new_loadout.equip_slot2_name set value "None"
{equip_name_dispatch[2]}

# Set visibility
execute if score #cl_public {ns}.data matches 1 run data modify storage {ns}:temp _new_loadout.public set value 1b

# Override weapon loot entries with scope/camo-modified IDs
function {fn}/fix_primary_loot with storage {ns}:temp editor
execute if data storage {ns}:temp _build.secondary_data run function {fn}/fix_secondary_loot with storage {ns}:temp editor

# Build slot list
# 1. Primary weapon (hotbar.1)
data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.primary_data.gun_slot

# 2. Secondary weapon (hotbar.2) - if selected
execute if data storage {ns}:temp _build.secondary_data run data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.secondary_data.gun_slot

# 3. Equipment slots (hotbar.8 and hotbar.7)
execute unless data storage {ns}:temp editor{{equip_slot1:""}} run function {fn}/append_equip1 with storage {ns}:temp editor
execute unless data storage {ns}:temp editor{{equip_slot2:""}} run function {fn}/append_equip2 with storage {ns}:temp editor

# 4. Primary magazine slots (inventory slots starting at 0)
scoreboard players set #inv_slot {ns}.data 0
data modify storage {ns}:temp _mag_data set from storage {ns}:temp _build.primary_data
execute store result score #pmag_count {ns}.data run data get storage {ns}:temp editor.primary_mag_count
execute if score #pmag_count {ns}.data matches 1.. run function {fn}/append_mag_slots

# 5. Secondary magazine slots (continuing from #inv_slot)
execute if data storage {ns}:temp _build.secondary_data run function {fn}/start_secondary_mags

# Auto-name the loadout and set gun display names
function {fn}/set_name with storage {ns}:temp editor
function {fn}/set_main_gun_display with storage {ns}:temp editor
data modify storage {ns}:temp _new_loadout.secondary_gun_display set value "None"
execute unless data storage {ns}:temp editor{{secondary:""}} run function {fn}/set_sec_gun_display with storage {ns}:temp editor

# Append new loadout, or replace the original when editing
execute if score @s {ns}.mp.edit_target matches ..0 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout
execute if score @s {ns}.mp.edit_target matches 1.. run function {fn}/save_replace

# Reset editor state
scoreboard players set @s {ns}.mp.edit_step 0
scoreboard players set @s {ns}.mp.edit_target 0

# Notify player and show the updated loadout list
function {fn}/notify_saved with storage {ns}:temp editor
function {ns}:v{version}/multiplayer/my_loadouts/browse
""")

	## save_replace - Editing flow: rebuild the list, swapping the original entry (by id + owner) for the freshly built _new_loadout while preserving its social stats.
	write_versioned_function("multiplayer/editor/save_replace", f"""
scoreboard players operation #edit_id {ns}.data = @s {ns}.mp.edit_target
data modify storage {ns}:temp _edit_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
scoreboard players set #edit_replaced {ns}.data 0
execute if data storage {ns}:temp _edit_src[0] run function {fn}/save_replace_iter

# If the original vanished in the meantime (e.g. deleted), append as a new entry
execute if score #edit_replaced {ns}.data matches 0 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout
""")

	write_versioned_function("multiplayer/editor/save_replace_iter", f"""
# Match by id + ownership
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _edit_src[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _edit_src[0].owner_pid
scoreboard players set #edit_match {ns}.data 0
execute if score #entry_id {ns}.data = #edit_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run scoreboard players set #edit_match {ns}.data 1

# On match: carry over social stats, then insert the rebuilt loadout in place of the original
execute if score #edit_match {ns}.data matches 1 if data storage {ns}:temp _edit_src[0].likes run data modify storage {ns}:temp _new_loadout.likes set from storage {ns}:temp _edit_src[0].likes
execute if score #edit_match {ns}.data matches 1 if data storage {ns}:temp _edit_src[0].favorites_count run data modify storage {ns}:temp _new_loadout.favorites_count set from storage {ns}:temp _edit_src[0].favorites_count
execute if score #edit_match {ns}.data matches 1 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout
execute if score #edit_match {ns}.data matches 1 run scoreboard players set #edit_replaced {ns}.data 1
execute unless score #edit_match {ns}.data matches 1 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _edit_src[0]

data remove storage {ns}:temp _edit_src[0]
execute if data storage {ns}:temp _edit_src[0] run function {fn}/save_replace_iter
""")

	## Equip slot append macros (include the camo suffix)
	write_versioned_function("multiplayer/editor/append_equip1", f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"hotbar.8",loot:"{ns}:i/$(equip_slot1)$(equip_slot1_camo)",count:1,consumable:0b,bullets:0}}
""")
	write_versioned_function("multiplayer/editor/append_equip2", f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"hotbar.7",loot:"{ns}:i/$(equip_slot2)$(equip_slot2_camo)",count:1,consumable:0b,bullets:0}}
""")

	## append_mag_slots - Add magazine slots based on type and count
	write_versioned_function("multiplayer/editor/append_mag_slots", f"""
# Flatten mag_id for macro use (macro vars can't use dot-paths)
data modify storage {ns}:temp _mag_id set from storage {ns}:temp _mag_data.mag_id
data modify storage {ns}:temp _mag_bullets set from storage {ns}:temp _mag_data.mag_bullets

# Consumable mag: one slot only (with count and bullets)
execute if data storage {ns}:temp _mag_data{{mag_consumable:1b}} run function {fn}/append_mag_consumable
execute if data storage {ns}:temp _mag_data{{mag_consumable:1b}} run return 0

# Non-consumable: add one slot per count
execute if score #pmag_count {ns}.data matches 1.. run function {fn}/append_mag_loop
""")

	write_versioned_function("multiplayer/editor/append_mag_consumable", f"""
# Total bullets = mag_bullets (capacity) * pmag_count (user's chosen count)
execute store result score #mag_bullets {ns}.data run data get storage {ns}:temp _mag_bullets
scoreboard players operation #mag_bullets {ns}.data *= #pmag_count {ns}.data
execute store result storage {ns}:temp _mag_bullets int 1 run scoreboard players get #mag_bullets {ns}.data
execute store result storage {ns}:temp _inv_n int 1 run scoreboard players get #inv_slot {ns}.data
function {fn}/append_mag_consumable_macro with storage {ns}:temp
scoreboard players add #inv_slot {ns}.data 1
""")

	write_versioned_function("multiplayer/editor/append_mag_consumable_macro", f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"inventory.$(_inv_n)",loot:"{ns}:i/$(_mag_id)",count:1,consumable:1b,bullets:$(_mag_bullets)}}
""")

	write_versioned_function("multiplayer/editor/append_mag_loop", f"""
execute if score #pmag_count {ns}.data matches ..0 run return 0
execute store result storage {ns}:temp _inv_n int 1 run scoreboard players get #inv_slot {ns}.data
function {fn}/append_mag_regular with storage {ns}:temp
scoreboard players add #inv_slot {ns}.data 1
scoreboard players remove #pmag_count {ns}.data 1
return run function {fn}/append_mag_loop
""")

	write_versioned_function("multiplayer/editor/append_mag_regular", f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"inventory.$(_inv_n)",loot:"{ns}:i/$(_mag_id)",count:1,consumable:0b,bullets:0}}
""")

	## start_secondary_mags - setup secondary mag data and loop
	write_versioned_function("multiplayer/editor/start_secondary_mags", f"""
data modify storage {ns}:temp _mag_data set from storage {ns}:temp _build.secondary_data
execute store result score #pmag_count {ns}.data run data get storage {ns}:temp editor.secondary_mag_count
execute if score #pmag_count {ns}.data matches 1.. run function {fn}/append_mag_slots
""")

	## Fix loot macros
	write_versioned_function("multiplayer/editor/fix_primary_loot", f"""$data modify storage {ns}:temp _build.primary_data.gun_slot.loot set value "{ns}:i/$(primary_full)"
""")
	write_versioned_function("multiplayer/editor/fix_secondary_loot", f"""$data modify storage {ns}:temp _build.secondary_data.gun_slot.loot set value "{ns}:i/$(secondary_full)"
""")

	## Name and notification macros
	write_versioned_function("multiplayer/editor/set_name", f"""$data modify storage {ns}:temp _new_loadout.name set value "$(primary_name) + $(secondary_name)"\n""")
	write_versioned_function("multiplayer/editor/set_main_gun_display", f"""$data modify storage {ns}:temp _new_loadout.main_gun_display set value "$(primary_name) ($(primary_scope_name), $(primary_camo_name))"\n""")
	write_versioned_function("multiplayer/editor/set_sec_gun_display", f"""$data modify storage {ns}:temp _new_loadout.secondary_gun_display set value "$(secondary_name) ($(secondary_scope_name), $(secondary_camo_name))"\n""")
	write_versioned_function("multiplayer/editor/notify_saved", '$tellraw @s ["",' + MGS_TAG + ',[{"text":"","color":"white"},{"text":"Loadout saved"},": "],{"text":"$(primary_name) + $(secondary_name)","color":"green","bold":true}]')

