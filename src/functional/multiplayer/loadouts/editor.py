
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ..classes import CONSUMABLE_MAGS
from .catalogs import (
	ALL_SCOPE_SUFFIXES,
	EQUIPMENT_PRESETS,
	PRIMARY_WEAPONS,
	SCOPE_NAMES,
	SCOPE_VARIANTS,
	SECONDARY_WEAPONS,
	TRIG_EQUIPMENT_BASE,
	TRIG_PRIMARY_BASE,
	TRIG_PRIMARY_SCOPE_BASE,
	TRIG_SAVE_PRIVATE,
	TRIG_SAVE_PUBLIC,
	TRIG_SECONDARY_BASE,
	TRIG_SECONDARY_NONE,
	TRIG_SECONDARY_SCOPE_BASE,
)


def generate_editor() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ====================================================================
	## LOADOUT EDITOR — 4-step dialog flow
	## ====================================================================

	## ============================
	## Step 1: editor/start — Build and show primary weapon selection dialog
	## ============================
	# Build the dialog statically since the weapon list is fixed at build time
	primary_actions: list[str] = []
	for idx, (gun_id, display, category, _mag, _mc) in enumerate(PRIMARY_WEAPONS):
		trig = TRIG_PRIMARY_BASE + idx
		primary_actions.append(
			f'{{label:{{text:"{display}",color:"green"}},'
			f'tooltip:{{text:"{category}"}},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	primary_actions_snbt = ",".join(primary_actions)

	write_versioned_function("multiplayer/editor/start",
f"""
# Mark editor as active (step 1 = picking primary)
scoreboard players set @s {ns}.mp.edit_step 1

# Build primary weapon selection dialog
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Primary",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your primary weapon.",color:"gray"}}}}],\
actions:[{primary_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## Step 2: editor/pick_primary — Store primary choice, route to scope or secondary
	## ============================
	# For each primary weapon, generate a dispatch line that stores the choice in temp
	# Include scope defaults: primary_scope="", primary_scope_name="Iron Sights", primary_full=gun_id
	pick_primary_lines = ""
	for idx, (gun_id, display, category, mag_id, mag_count) in enumerate(PRIMARY_WEAPONS):
		trig = TRIG_PRIMARY_BASE + idx
		pick_primary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor set value '
			f'{{primary:"{gun_id}",primary_name:"{display}",primary_mag:"{mag_id}",primary_mag_count:{mag_count},'
			f'primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"{gun_id}"}}\n'
		)

	# Build scope routing: weapons with scope variants → scope dialog, others → secondary dialog
	scope_route_lines = ""
	# Group weapons by their scope variant set for routing
	scope_set_func: dict[tuple[str, ...], str] = {
		("", "_1", "_2", "_3", "_4"): "scope/primary_full",
		("", "_1", "_2", "_3"):       "scope/primary_no4",
		("", "_1"):                   "scope/primary_1only",
	}
	for gun_id, *_ in PRIMARY_WEAPONS:
		if gun_id in SCOPE_VARIANTS:
			variants = SCOPE_VARIANTS[gun_id]
			func_name = scope_set_func[variants]
			scope_route_lines += (
				f'execute if data storage {ns}:temp editor{{primary:"{gun_id}"}} run '
				f'return run function {ns}:v{version}/multiplayer/editor/{func_name}\n'
			)

	write_versioned_function("multiplayer/editor/pick_primary",
f"""
# Store primary weapon choice based on trigger value
{pick_primary_lines}
# Route: weapons with scope variants go to scope dialog, others skip to secondary
{scope_route_lines}
# No scope variants: go directly to secondary selection
function {ns}:v{version}/multiplayer/editor/show_secondary_dialog
""")

	## ============================
	## Scope dialogs for primary weapon (one per unique scope variant set)
	## ============================
	# Helper: build scope action buttons SNBT
	def scope_actions_snbt(trig_base: int, variants: tuple[str, ...]) -> str:
		actions: list[str] = []
		for suffix in variants:
			idx = ALL_SCOPE_SUFFIXES.index(suffix)
			trig = trig_base + idx
			name = SCOPE_NAMES[suffix]
			actions.append(
				f'{{label:{{text:"{name}",color:"green"}},'
				f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
			)
		return ",".join(actions)

	# Full scope set: Iron Sights, Red Dot, Holographic, 3x Scope, 4x Scope
	full_scope_snbt = scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, ("", "_1", "_2", "_3", "_4"))
	write_versioned_function("multiplayer/editor/scope/primary_full",
f"""
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your optic attachment.",color:"gray"}}}}],\
actions:[{full_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	# No _4 set: Iron Sights, Red Dot, Holographic, 3x Scope
	no4_scope_snbt = scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, ("", "_1", "_2", "_3"))
	write_versioned_function("multiplayer/editor/scope/primary_no4",
f"""
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your optic attachment.",color:"gray"}}}}],\
actions:[{no4_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	# Mosin: Iron Sights, Red Dot only
	mosin_scope_snbt = scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, ("", "_1"))
	write_versioned_function("multiplayer/editor/scope/primary_1only",
f"""
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your optic attachment.",color:"gray"}}}}],\
actions:[{mosin_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_primary_scope — Store scope choice, compute full weapon ID, show secondary
	## ============================
	pick_scope_lines = ""
	for suffix in ALL_SCOPE_SUFFIXES:
		idx = ALL_SCOPE_SUFFIXES.index(suffix)
		trig = TRIG_PRIMARY_SCOPE_BASE + idx
		name = SCOPE_NAMES[suffix]
		pick_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.primary_scope set value "{suffix}"\n'
		)
		pick_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.primary_scope_name set value "{name}"\n'
		)

	write_versioned_function("multiplayer/editor/pick_primary_scope",
f"""
# Store scope choice
{pick_scope_lines}
# Compute full weapon ID: base + scope suffix (e.g. "ak47" + "_3" = "ak47_3")
function {ns}:v{version}/multiplayer/editor/set_primary_full with storage {ns}:temp editor

# Show secondary weapon dialog
function {ns}:v{version}/multiplayer/editor/show_secondary_dialog
""")

	## Macro: compute primary_full = primary + primary_scope
	write_versioned_function("multiplayer/editor/set_primary_full",
f"""$data modify storage {ns}:temp editor.primary_full set value "$(primary)$(primary_scope)"
""")

	## ============================
	## show_secondary_dialog — Build and show secondary weapon selection dialog
	## ============================
	secondary_actions: list[str] = []
	for idx, (gun_id, display, mag_id, _mc) in enumerate(SECONDARY_WEAPONS):
		trig = TRIG_SECONDARY_BASE + idx
		secondary_actions.append(
			f'{{label:{{text:"{display}",color:"green"}},'
			f'tooltip:{{text:"Pistol"}},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	# Add "None" option
	secondary_actions.append(
		f'{{label:{{text:"No Secondary",color:"red"}},'
		f'tooltip:{{text:"Skip secondary weapon"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SECONDARY_NONE}"}}}}'
	)
	secondary_actions_snbt = ",".join(secondary_actions)

	write_versioned_function("multiplayer/editor/show_secondary_dialog",
f"""
scoreboard players set @s {ns}.mp.edit_step 2

data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Secondary",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your secondary weapon (or skip).",color:"gray"}}}}],\
actions:[{secondary_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## Step 3: editor/pick_secondary — Store secondary choice, route to scope or equipment
	## ============================
	pick_secondary_lines = ""
	for idx, (gun_id, display, mag_id, mag_count) in enumerate(SECONDARY_WEAPONS):
		trig = TRIG_SECONDARY_BASE + idx
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary set value "{gun_id}"\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_name set value "{display}"\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_mag set value "{mag_id}"\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_mag_count set value {mag_count}\n'
		)
		# Set scope defaults
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope set value ""\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope_name set value "Iron Sights"\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_full set value "{gun_id}"\n'
		)
	# Handle "None" option
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary set value ""\n'
	)
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary_name set value "None"\n'
	)
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary_scope set value ""\n'
	)
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary_scope_name set value ""\n'
	)
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary_full set value ""\n'
	)

	# Route: deagle has scope variants → show scope dialog, others → equipment
	secondary_scope_route = (
		f'execute if data storage {ns}:temp editor{{secondary:"deagle"}} run '
		f'return run function {ns}:v{version}/multiplayer/editor/scope/secondary_4only\n'
	)

	write_versioned_function("multiplayer/editor/pick_secondary",
f"""
# Store secondary weapon choice based on trigger value
{pick_secondary_lines}
# Route: deagle → scope dialog, others → equipment dialog
{secondary_scope_route}
# No scope variants: go directly to equipment selection
function {ns}:v{version}/multiplayer/editor/show_equipment_dialog
""")

	## ============================
	## Secondary scope dialog: deagle (Iron Sights + 4x Scope)
	## ============================
	deagle_scope_snbt = scope_actions_snbt(TRIG_SECONDARY_SCOPE_BASE, ("", "_4"))
	write_versioned_function("multiplayer/editor/scope/secondary_4only",
f"""
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope (Secondary)",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your secondary optic.",color:"gray"}}}}],\
actions:[{deagle_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_secondary_scope — Store scope choice, compute full ID, show equipment
	## ============================
	pick_sec_scope_lines = ""
	for suffix in ALL_SCOPE_SUFFIXES:
		idx = ALL_SCOPE_SUFFIXES.index(suffix)
		trig = TRIG_SECONDARY_SCOPE_BASE + idx
		name = SCOPE_NAMES[suffix]
		pick_sec_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope set value "{suffix}"\n'
		)
		pick_sec_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope_name set value "{name}"\n'
		)

	write_versioned_function("multiplayer/editor/pick_secondary_scope",
f"""
# Store secondary scope choice
{pick_sec_scope_lines}
# Compute full secondary weapon ID
function {ns}:v{version}/multiplayer/editor/set_secondary_full with storage {ns}:temp editor

# Show equipment dialog
function {ns}:v{version}/multiplayer/editor/show_equipment_dialog
""")

	## Macro: compute secondary_full = secondary + secondary_scope
	write_versioned_function("multiplayer/editor/set_secondary_full",
f"""$data modify storage {ns}:temp editor.secondary_full set value "$(secondary)$(secondary_scope)"
""")

	## ============================
	## show_equipment_dialog — Build and show equipment preset selection dialog
	## ============================
	equipment_actions: list[str] = []
	for idx, (preset_id, display, items) in enumerate(EQUIPMENT_PRESETS):
		trig = TRIG_EQUIPMENT_BASE + idx
		equipment_actions.append(
			f'{{label:{{text:"{display}",color:"green"}},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	equipment_actions_snbt = ",".join(equipment_actions)

	write_versioned_function("multiplayer/editor/show_equipment_dialog",
f"""
scoreboard players set @s {ns}.mp.edit_step 3

data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Equipment",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your equipment loadout.",color:"gray"}}}}],\
actions:[{equipment_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## Step 4: editor/pick_equipment — Store equipment, show confirm dialog
	## ============================
	pick_equipment_lines = ""
	for idx, (preset_id, display, items) in enumerate(EQUIPMENT_PRESETS):
		trig = TRIG_EQUIPMENT_BASE + idx
		pick_equipment_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.equipment_idx set value {idx}\n'
		)
		pick_equipment_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.equipment_name set value "{display}"\n'
		)

	write_versioned_function("multiplayer/editor/pick_equipment",
f"""
# Store equipment preset choice
{pick_equipment_lines}
# Advance to step 4
scoreboard players set @s {ns}.mp.edit_step 4

# Build confirmation dialog with summary
# We use a notice-style dialog with two action buttons (public/private)
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Confirm",color:"gold",bold:true}},\
body:[\
{{type:"minecraft:plain_message",contents:{{text:"Review your loadout:",color:"white"}}}},\
{{type:"minecraft:item",item:{{id:"minecraft:poisonous_potato",components:{{"minecraft:item_model":"{ns}:placeholder"}}}},description:{{contents:[{{"text":"Loading...","color":"gray"}}]}}}}\
],\
actions:[\
{{label:{{text:"Save as Public",color:"green"}},tooltip:{{text:"Everyone can see and use this loadout"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PUBLIC}"}}}},\
{{label:{{text:"Save as Private",color:"yellow"}},tooltip:{{text:"Only you can see and use this loadout"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PRIVATE}"}}}}\
],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}

# Show dialog via macro-built summary
function {ns}:v{version}/multiplayer/editor/show_confirm with storage {ns}:temp editor
""")

	## ============================
	## editor/show_confirm — macro function to build the confirmation body text
	## ============================
	write_versioned_function("multiplayer/editor/show_confirm",
f"""
# Build summary body using macro substitution
$data modify storage {ns}:temp dialog.body set value [\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Primary: ","color":"white"}},{{"text":"$(primary_name)","color":"green","bold":true}},{{"text":" ($(primary_scope_name))","color":"dark_green"}}]}},\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Secondary: ","color":"white"}},{{"text":"$(secondary_name)","color":"yellow","bold":true}},{{"text":" ($(secondary_scope_name))","color":"gold"}}]}},\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Equipment: ","color":"white"}},{{"text":"$(equipment_name)","color":"aqua","bold":true}}]}},\
{{type:"minecraft:plain_message",contents:{{text:"\\nSave this loadout?","color":"gray"}}}}\
]

# Show the dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/save — Create the loadout entry and store it
	## Called with trigger 350 (public) or 351 (private)
	## ============================
	# Build the slot computation for every possible combination at runtime
	# Since we can't run Python at runtime, we pre-build slot data for each weapon combo.
	# Instead, we generate the slots dynamically using a macro function.
	# The save function reads from editor temp, computes slots, and appends to custom_loadouts.

	# First, generate a mapping from weapon IDs to their slot data
	# We need a macro that accepts primary/secondary/equipment_idx and builds slots
	# Since we can't do arbitrary computation in mcfunction, we pre-generate all possible
	# primary→slots and secondary→slots at build time as storage entries.

	# Pre-generate primary weapon slot data (hotbar.0 + magazines)
	primary_slot_entries: list[str] = []
	for gun_id, display, category, mag_id, mag_count in PRIMARY_WEAPONS:
		slots = [f'{{slot:"hotbar.0",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}']
		inv_slot = 0
		if mag_id in CONSUMABLE_MAGS:
			slots.append(f'{{slot:"inventory.{inv_slot}",loot:"{ns}:i/{mag_id}",count:1,consumable:1b,bullets:{mag_count}}}')
			inv_slot += 1
		else:
			for _ in range(mag_count):
				slots.append(f'{{slot:"inventory.{inv_slot}",loot:"{ns}:i/{mag_id}",count:1,consumable:0b,bullets:0}}')
				inv_slot += 1
		slots_snbt = ",".join(slots)
		primary_slot_entries.append(f'{{id:"{gun_id}",slots:[{slots_snbt}],next_inv_slot:{inv_slot}}}')

	primary_slot_table_snbt = ",".join(primary_slot_entries)

	# Pre-generate secondary weapon slot data (hotbar.1 + magazines, inv_slot is relative)
	secondary_slot_entries: list[str] = []
	for gun_id, display, mag_id, mag_count in SECONDARY_WEAPONS:
		slots = [f'{{slot:"hotbar.1",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}']
		# Secondary mag slots start at a variable inv_slot, so we use relative offsets
		# and fix them up at save time. Use placeholder "inv_offset_N" style.
		rel_slots: list[str] = []
		if mag_id in CONSUMABLE_MAGS:
			rel_slots.append(f'{{loot:"{ns}:i/{mag_id}",count:1,consumable:1b,bullets:{mag_count}}}')
		else:
			for _ in range(mag_count):
				rel_slots.append(f'{{loot:"{ns}:i/{mag_id}",count:1,consumable:0b,bullets:0}}')
		rel_snbt = ",".join(rel_slots)
		slots_snbt = ",".join(slots)
		secondary_slot_entries.append(f'{{id:"{gun_id}",fixed_slots:[{slots_snbt}],mag_slots:[{rel_snbt}]}}')

	secondary_slot_table_snbt = ",".join(secondary_slot_entries)

	# Pre-generate equipment slot data (hotbar.8, hotbar.7, ...)
	equipment_slot_entries: list[str] = []
	for preset_id, display, items in EQUIPMENT_PRESETS:
		equip_slots: list[str] = []
		equip_slot = 8
		for item_id, count in items.items():
			equip_slots.append(f'{{slot:"hotbar.{equip_slot}",loot:"{ns}:i/{item_id}",count:{count},consumable:0b,bullets:0}}')
			equip_slot -= 1
		equip_snbt = ",".join(equip_slots)
		equipment_slot_entries.append(f'{{id:"{preset_id}",slots:[{equip_snbt}]}}')

	equipment_slot_table_snbt = ",".join(equipment_slot_entries)

	# Write slot lookup tables to storage on load
	write_load_file(
f"""
# Slot lookup tables for custom loadout editor (pre-computed at build time)
data modify storage {ns}:multiplayer primary_slot_table set value [{primary_slot_table_snbt}]
data modify storage {ns}:multiplayer secondary_slot_table set value [{secondary_slot_table_snbt}]
data modify storage {ns}:multiplayer equipment_slot_table set value [{equipment_slot_table_snbt}]
""")

	## ============================
	## editor/save — Main save function
	## ============================
	# Generate dispatch lines to find the right slot data from the lookup tables
	save_primary_dispatch = ""
	for idx, (gun_id, *_) in enumerate(PRIMARY_WEAPONS):
		save_primary_dispatch += (
			f'execute if data storage {ns}:temp editor{{primary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.primary_data set from storage {ns}:multiplayer primary_slot_table[{idx}]\n'
		)

	save_secondary_dispatch = ""
	for idx, (gun_id, *_) in enumerate(SECONDARY_WEAPONS):
		save_secondary_dispatch += (
			f'execute if data storage {ns}:temp editor{{secondary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.secondary_data set from storage {ns}:multiplayer secondary_slot_table[{idx}]\n'
		)

	save_equipment_dispatch = ""
	for idx, (preset_id, *_) in enumerate(EQUIPMENT_PRESETS):
		save_equipment_dispatch += (
			f'execute if data storage {ns}:temp editor{{equipment_idx:{idx}}} run '
			f'data modify storage {ns}:temp _build.equipment_data set from storage {ns}:multiplayer equipment_slot_table[{idx}]\n'
		)

	write_versioned_function("multiplayer/editor/save",
f"""
# Determine visibility from trigger value
scoreboard players set #cl_public {ns}.data 0
execute if score @s {ns}.player.config matches {TRIG_SAVE_PUBLIC} run scoreboard players set #cl_public {ns}.data 1

# Initialize build workspace
data modify storage {ns}:temp _build set value {{}}

# Look up primary weapon slot data
{save_primary_dispatch}
# Look up secondary weapon slot data (skip if no secondary)
{save_secondary_dispatch}
# Look up equipment slot data
{save_equipment_dispatch}

# Build the final loadout entry
# Start with base structure
data modify storage {ns}:temp _new_loadout set value {{id:0,owner_pid:0,owner_name:"",name:"",public:0b,likes:0,main_gun:"",secondary_gun:"",slots:[]}}

# Set loadout ID from counter
execute store result storage {ns}:temp _new_loadout.id int 1 run data get storage {ns}:multiplayer next_loadout_id

# Increment the counter
execute store result score #temp {ns}.data run data get storage {ns}:multiplayer next_loadout_id
scoreboard players add #temp {ns}.data 1
execute store result storage {ns}:multiplayer next_loadout_id int 1 run scoreboard players get #temp {ns}.data

# Set owner info
execute store result storage {ns}:temp _new_loadout.owner_pid int 1 run scoreboard players get @s {ns}.mp.pid
# Owner name is set by a macro call (pass player display name via team prefix trick)

# Set weapon info (store the full scope-modified weapon IDs)
data modify storage {ns}:temp _new_loadout.main_gun set from storage {ns}:temp editor.primary_full
data modify storage {ns}:temp _new_loadout.secondary_gun set from storage {ns}:temp editor.secondary_full

# Set visibility
execute if score #cl_public {ns}.data matches 1 run data modify storage {ns}:temp _new_loadout.public set value 1b

# Override weapon loot entries with scope-modified weapon IDs (e.g. "ak47_3" instead of "ak47")
function {ns}:v{version}/multiplayer/editor/fix_primary_loot with storage {ns}:temp editor
execute if data storage {ns}:temp _build.secondary_data run function {ns}:v{version}/multiplayer/editor/fix_secondary_loot with storage {ns}:temp editor

# Build the combined slot list: primary slots + secondary slots + equipment slots
# 1. Copy primary weapon & magazine slots
data modify storage {ns}:temp _new_loadout.slots set from storage {ns}:temp _build.primary_data.slots

# 2. Append secondary gun slot (hotbar.1)
execute if data storage {ns}:temp _build.secondary_data run data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.secondary_data.fixed_slots[0]

# 3. Append secondary magazine slots (need to fix inventory slot numbers)
# Get next_inv_slot from primary data to know where secondary mags start
execute store result score #inv_slot {ns}.data run data get storage {ns}:temp _build.primary_data.next_inv_slot
# Use recursive function to append secondary mags with correct slot numbers
execute if data storage {ns}:temp _build.secondary_data.mag_slots[0] run function {ns}:v{version}/multiplayer/editor/append_sec_mags

# 4. Append equipment slots
execute if data storage {ns}:temp _build.equipment_data.slots[0] run function {ns}:v{version}/multiplayer/editor/append_equip_slots

# Auto-generate loadout name: "Primary + Secondary" or just "Primary"
function {ns}:v{version}/multiplayer/editor/set_name with storage {ns}:temp editor

# Append to the custom loadouts list
data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout

# Reset editor state
scoreboard players set @s {ns}.mp.edit_step 0

# Notify player
function {ns}:v{version}/multiplayer/editor/notify_saved with storage {ns}:temp editor
""")

	## ============================
	## editor/set_name — macro to auto-name the loadout
	## ============================
	write_versioned_function("multiplayer/editor/set_name",
f"""$data modify storage {ns}:temp _new_loadout.name set value "$(primary_name) + $(secondary_name)"
""")

	## ============================
	## editor/notify_saved — tellraw confirmation
	## ============================
	write_versioned_function("multiplayer/editor/notify_saved",
f"""$tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Loadout saved: ","color":"white"}},{{"text":"$(primary_name) + $(secondary_name)","color":"green","bold":true}}]
""")

	## ============================
	## editor/fix_primary_loot — macro: override primary weapon loot with scope-modified ID
	## ============================
	write_versioned_function("multiplayer/editor/fix_primary_loot",
f"""$data modify storage {ns}:temp _build.primary_data.slots[0].loot set value "{ns}:i/$(primary_full)"
""")

	## ============================
	## editor/fix_secondary_loot — macro: override secondary weapon loot with scope-modified ID
	## ============================
	write_versioned_function("multiplayer/editor/fix_secondary_loot",
f"""$data modify storage {ns}:temp _build.secondary_data.fixed_slots[0].loot set value "{ns}:i/$(secondary_full)"
""")

	## ============================
	## editor/append_sec_mags — recursive: fix inventory slot numbers for secondary magazines
	## ============================
	write_versioned_function("multiplayer/editor/append_sec_mags",
f"""
# Copy the first mag slot template
data modify storage {ns}:temp _sec_mag set from storage {ns}:temp _build.secondary_data.mag_slots[0]

# Set the correct inventory slot number using score
# Build the slot string: "inventory.N"
execute store result storage {ns}:temp _inv_n int 1 run scoreboard players get #inv_slot {ns}.data
function {ns}:v{version}/multiplayer/editor/set_sec_mag_slot with storage {ns}:temp

# Append to loadout slots
data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _sec_mag

# Increment inv_slot counter
scoreboard players add #inv_slot {ns}.data 1

# Remove processed and recurse
data remove storage {ns}:temp _build.secondary_data.mag_slots[0]
execute if data storage {ns}:temp _build.secondary_data.mag_slots[0] run function {ns}:v{version}/multiplayer/editor/append_sec_mags
""")

	## ============================
	## editor/set_sec_mag_slot — macro to set the slot field with correct inventory index
	## ============================
	write_versioned_function("multiplayer/editor/set_sec_mag_slot",
f"""$data modify storage {ns}:temp _sec_mag.slot set value "inventory.$(_inv_n)"
""")

	## ============================
	## editor/append_equip_slots — recursive: append equipment slots to the loadout
	## ============================
	write_versioned_function("multiplayer/editor/append_equip_slots",
f"""
# Append the first equipment slot
data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.equipment_data.slots[0]

# Remove and recurse
data remove storage {ns}:temp _build.equipment_data.slots[0]
execute if data storage {ns}:temp _build.equipment_data.slots[0] run function {ns}:v{version}/multiplayer/editor/append_equip_slots
""")
