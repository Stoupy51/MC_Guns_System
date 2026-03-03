
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ..classes import CONSUMABLE_MAGS
from .catalogs import (
	ALL_SCOPE_SUFFIXES,
	COST_GRENADE,
	COST_PERK,
	COST_PRIMARY_MAG,
	COST_PRIMARY_SCOPE,
	COST_PRIMARY_WEAPON,
	COST_SECONDARY_MAG,
	COST_SECONDARY_SCOPE,
	COST_SECONDARY_WEAPON,
	GRENADE_TYPES,
	MAX_PERKS,
	PERKS,
	PICK10_TOTAL,
	PRIMARY_WEAPONS,
	SCOPE_NAMES,
	SCOPE_VARIANTS,
	SECONDARY_WEAPONS,
	TRIG_BACK_EQUIPMENT,
	TRIG_BACK_PERKS,
	TRIG_BACK_SECONDARY,
	TRIG_EDITOR_START,
	TRIG_EQUIP_SLOT1_BASE,
	TRIG_EQUIP_SLOT2_BASE,
	TRIG_PERK_BASE,
	TRIG_PERKS_DONE,
	TRIG_PRIMARY_BASE,
	TRIG_PRIMARY_MAGS_BASE,
	TRIG_PRIMARY_SCOPE_BASE,
	TRIG_SAVE_PRIVATE,
	TRIG_SAVE_PUBLIC,
	TRIG_SECONDARY_BASE,
	TRIG_SECONDARY_MAGS_BASE,
	TRIG_SECONDARY_NONE,
	TRIG_SECONDARY_SCOPE_BASE,
)


def generate_editor() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ====================================================================
	## LOADOUT EDITOR — Pick-10 dialog flow
	## Steps: Primary → Scope → Mags → Secondary → Scope → Mags → Equip1 → Equip2 → Perks → Confirm
	## ====================================================================

	## ============================
	## Step 1: editor/start — Initialize Pick-10 budget, show primary weapon selection
	## ============================
	primary_actions: list[str] = []
	for idx, (_gun_id, display, category, _mag, _mc) in enumerate(PRIMARY_WEAPONS):
		trig = TRIG_PRIMARY_BASE + idx
		primary_actions.append(
			f'{{label:{{text:"{display}",color:"yellow"}},'
			f'tooltip:["",{{"text":"{category}","color":"gray"}},{{"text":"\\nCost: ","color":"white"}},{{"text":"{COST_PRIMARY_WEAPON} pt","color":"gold"}}],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	primary_actions_snbt = ",".join(primary_actions)

	write_versioned_function("multiplayer/editor/start",
f"""
# Initialize Pick-10 budget
scoreboard players set @s {ns}.mp.edit_points {PICK10_TOTAL}
# Mark editor as active (step 1 = picking primary)
scoreboard players set @s {ns}.mp.edit_step 1

# Show primary weapon selection dialog
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {ns}:v{version}/multiplayer/editor/show_primary_dialog_macro with storage {ns}:temp
""")

	write_versioned_function("multiplayer/editor/show_primary_dialog_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Primary",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Choose your primary weapon (-{COST_PRIMARY_WEAPON} pt).",color:"gray"}}\
}}],\
actions:[{primary_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_primary — Store primary, deduct cost, route to scope
	## ============================
	pick_primary_lines = ""
	for idx, (gun_id, display, _category, mag_id, mag_count) in enumerate(PRIMARY_WEAPONS):
		trig = TRIG_PRIMARY_BASE + idx
		pick_primary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor set value '
			f'{{primary:"{gun_id}",primary_name:"{display}",primary_mag:"{mag_id}",primary_mag_count:{mag_count},'
			f'primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"{gun_id}",'
			f'secondary:"",secondary_name:"None",secondary_mag:"",secondary_mag_count:0,'
			f'secondary_scope:"",secondary_scope_name:"",secondary_full:"",'
			f'equip_slot1:"",equip_slot2:"",perks:[]}}\n'
		)

	# Build scope routing
	scope_set_func: dict[tuple[str, ...], str] = {
		("", "_1", "_2", "_3", "_4"): "scope/primary_full",
		("", "_1", "_2", "_3"):       "scope/primary_no4",
		("", "_1"):                   "scope/primary_1only",
	}
	scope_route_lines = ""
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
# Deduct primary weapon cost
scoreboard players remove @s {ns}.mp.edit_points {COST_PRIMARY_WEAPON}

# Store primary weapon choice based on trigger value
{pick_primary_lines}
# Route: weapons with scope variants go to scope dialog, others skip to mag count
{scope_route_lines}
# No scope variants: go directly to primary mag count selection
function {ns}:v{version}/multiplayer/editor/show_primary_mags_dialog
""")

	## ============================
	## Primary scope dialogs
	## ============================
	def scope_actions_snbt(trig_base: int, variants: tuple[str, ...], cost: int) -> str:
		actions: list[str] = []
		for suffix in variants:
			i = ALL_SCOPE_SUFFIXES.index(suffix)
			trig = trig_base + i
			name = SCOPE_NAMES[suffix]
			scope_cost = cost if suffix != "" else 0
			cost_text = f"-{scope_cost} pt" if scope_cost > 0 else "Free"
			label_color = "green" if scope_cost == 0 else "yellow"
			actions.append(
				f'{{label:{{text:"{name}",color:"{label_color}"}},'
				f'tooltip:{{text:"{cost_text}"}},'
				f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
			)
		return ",".join(actions)

	def write_primary_scope_dialog(func_suffix: str, variants: tuple[str, ...]) -> None:
		snbt = scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, variants, COST_PRIMARY_SCOPE)
		write_versioned_function(f"multiplayer/editor/scope/primary_{func_suffix}",
f"""
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {ns}:v{version}/multiplayer/editor/scope/primary_{func_suffix}_macro with storage {ns}:temp
""")
		write_versioned_function(f"multiplayer/editor/scope/primary_{func_suffix}_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Choose your optic (-{COST_PRIMARY_SCOPE} pt for any scope, iron sights free).",color:"gray"}}\
}}],\
actions:[{snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_EDITOR_START}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	write_primary_scope_dialog("full", ("", "_1", "_2", "_3", "_4"))
	write_primary_scope_dialog("no4", ("", "_1", "_2", "_3"))
	write_primary_scope_dialog("1only", ("", "_1"))

	## ============================
	## editor/pick_primary_scope — Store scope, deduct cost if non-iron, show mag dialog
	## ============================
	pick_scope_lines = ""
	for suffix in ALL_SCOPE_SUFFIXES:
		i = ALL_SCOPE_SUFFIXES.index(suffix)
		trig = TRIG_PRIMARY_SCOPE_BASE + i
		name = SCOPE_NAMES[suffix]
		scope_cost = COST_PRIMARY_SCOPE if suffix != "" else 0
		if scope_cost > 0:
			pick_scope_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'execute if score @s {ns}.mp.edit_points matches ..{scope_cost - 1} run '
				f'return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Not enough points for a scope!","color":"red"}}]\n'
			)
		pick_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.primary_scope set value "{suffix}"\n'
		)
		pick_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.primary_scope_name set value "{name}"\n'
		)
		if scope_cost > 0:
			pick_scope_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'scoreboard players remove @s {ns}.mp.edit_points {scope_cost}\n'
			)

	write_versioned_function("multiplayer/editor/pick_primary_scope",
f"""
# Store scope choice and deduct cost if non-iron
{pick_scope_lines}
# Compute full weapon ID
function {ns}:v{version}/multiplayer/editor/set_primary_full with storage {ns}:temp editor

# Show primary mag count dialog
function {ns}:v{version}/multiplayer/editor/show_primary_mags_dialog
""")

	write_versioned_function("multiplayer/editor/set_primary_full",
f"""$data modify storage {ns}:temp editor.primary_full set value "$(primary)$(primary_scope)"
""")

	## ============================
	## show_primary_mags_dialog — Pick how many primary magazines (1-5)
	## ============================
	mag_actions_primary: list[str] = []
	for count in range(1, 6):
		trig = TRIG_PRIMARY_MAGS_BASE + count
		extra_cost = count * COST_PRIMARY_MAG
		mag_actions_primary.append(
			f'{{label:{{text:"{count}x Magazine",color:"yellow"}},'
			f'tooltip:["",{{"text":"-{extra_cost} pt","color":"gold"}},{{"text":"\\n{count} magazine(s) in inventory","color":"gray"}}],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	mag_actions_primary_snbt = ",".join(mag_actions_primary)

	write_versioned_function("multiplayer/editor/show_primary_mags_dialog",
f"""
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {ns}:v{version}/multiplayer/editor/show_primary_mags_dialog_macro with storage {ns}:temp
""")
	write_versioned_function("multiplayer/editor/show_primary_mags_dialog_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Primary Magazines",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Select number of primary magazines ({COST_PRIMARY_MAG} pt each).",color:"gray"}}\
}}],\
actions:[{mag_actions_primary_snbt}],\
columns:1,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_EDITOR_START}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_primary_mags — Store mag count, deduct cost, show secondary dialog
	## ============================
	pick_primary_mags_lines = ""
	for count in range(1, 6):
		trig = TRIG_PRIMARY_MAGS_BASE + count
		extra_cost = count * COST_PRIMARY_MAG
		min_needed = extra_cost
		pick_primary_mags_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'execute if score @s {ns}.mp.edit_points matches ..{min_needed - 1} run '
			f'return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Not enough points for {count} magazine(s)!","color":"red"}}]\n'
		)
		pick_primary_mags_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.primary_mag_count set value {count}\n'
		)
		pick_primary_mags_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'scoreboard players remove @s {ns}.mp.edit_points {extra_cost}\n'
		)

	write_versioned_function("multiplayer/editor/pick_primary_mags",
f"""
# Validate and store primary mag count and deduct cost
{pick_primary_mags_lines}
# Show secondary weapon dialog
function {ns}:v{version}/multiplayer/editor/show_secondary_dialog
""")

	## ============================
	## editor/back_to_secondary — Refund secondary weapon and scope costs, go back to secondary
	## ============================
	# Build scope refund: check if a scope was selected and refund accordingly
	scope_refund_lines = "\n".join(
		f'execute if data storage {ns}:temp editor{{secondary_scope:"{suffix}"}} run scoreboard players add @s {ns}.mp.edit_points {COST_SECONDARY_SCOPE}'
		for suffix in ALL_SCOPE_SUFFIXES if suffix != ""
	)
	write_versioned_function("multiplayer/editor/back_to_secondary",
f"""
# Refund secondary mags cost (secondary_mag_count * COST_SECONDARY_MAG)
execute store result score #refund_mags {ns}.data run data get storage {ns}:temp editor.secondary_mag_count
scoreboard players operation @s {ns}.mp.edit_points += #refund_mags {ns}.data
# Refund scope cost if a scope was selected
{scope_refund_lines}
# Refund secondary weapon cost if one was selected
execute unless data storage {ns}:temp editor{{secondary:""}} run scoreboard players add @s {ns}.mp.edit_points {COST_SECONDARY_WEAPON}
# Clear secondary state
data modify storage {ns}:temp editor.secondary set value ""
data modify storage {ns}:temp editor.secondary_scope set value ""
data modify storage {ns}:temp editor.secondary_mag_count set value 0
# Show secondary dialog
function {ns}:v{version}/multiplayer/editor/show_secondary_dialog
""")

	## ============================
	## show_secondary_dialog — Pick secondary weapon or skip
	## ============================
	secondary_actions: list[str] = []
	for idx, (_gun_id, display, _mag_id, _mc) in enumerate(SECONDARY_WEAPONS):
		trig = TRIG_SECONDARY_BASE + idx
		secondary_actions.append(
			f'{{label:{{text:"{display}",color:"yellow"}},'
			f'tooltip:["",{{"text":"Pistol","color":"gray"}},{{"text":"\\nCost: ","color":"white"}},{{"text":"{COST_SECONDARY_WEAPON} pt","color":"gold"}}],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	secondary_actions.append(
		f'{{label:{{text:"No Secondary",color:"green"}},'
		f'tooltip:{{text:"Skip secondary weapon (0 pts)"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SECONDARY_NONE}"}}}}'
	)
	secondary_actions_snbt = ",".join(secondary_actions)

	write_versioned_function("multiplayer/editor/show_secondary_dialog",
f"""
scoreboard players set @s {ns}.mp.edit_step 2
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {ns}:v{version}/multiplayer/editor/show_secondary_dialog_macro with storage {ns}:temp
""")
	write_versioned_function("multiplayer/editor/show_secondary_dialog_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Secondary",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Choose your secondary weapon (-{COST_SECONDARY_WEAPON} pt) or skip.",color:"gray"}}\
}}],\
actions:[{secondary_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_EDITOR_START}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_secondary — Store secondary choice, route to scope or mags
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
	# Handle "None"
	pick_secondary_lines += f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run data modify storage {ns}:temp editor.secondary set value ""\n'
	pick_secondary_lines += f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run data modify storage {ns}:temp editor.secondary_name set value "None"\n'
	pick_secondary_lines += f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run data modify storage {ns}:temp editor.secondary_scope set value ""\n'
	pick_secondary_lines += f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run data modify storage {ns}:temp editor.secondary_scope_name set value ""\n'
	pick_secondary_lines += f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run data modify storage {ns}:temp editor.secondary_full set value ""\n'
	pick_secondary_lines += f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run data modify storage {ns}:temp editor.secondary_mag set value ""\n'
	pick_secondary_lines += f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run data modify storage {ns}:temp editor.secondary_mag_count set value 0\n'

	secondary_scope_route = (
		f'execute if data storage {ns}:temp editor{{secondary:"deagle"}} run '
		f'return run function {ns}:v{version}/multiplayer/editor/scope/secondary_4only\n'
	)

	write_versioned_function("multiplayer/editor/pick_secondary",
f"""
# Store secondary weapon choice
{pick_secondary_lines}
# Check budget before deducting (secondary weapon costs {COST_SECONDARY_WEAPON} pt; None is free)
execute unless data storage {ns}:temp editor{{secondary:""}} run execute if score @s {ns}.mp.edit_points matches ..{COST_SECONDARY_WEAPON - 1} run return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Not enough points for a secondary weapon!","color":"red"}}]

# Deduct cost if a secondary was chosen
execute unless data storage {ns}:temp editor{{secondary:""}} run scoreboard players remove @s {ns}.mp.edit_points {COST_SECONDARY_WEAPON}

# Route: none → skip to equip slot 1, deagle → scope, others → secondary mag count
execute if data storage {ns}:temp editor{{secondary:""}} run return run function {ns}:v{version}/multiplayer/editor/show_equip_slot1_dialog
{secondary_scope_route}
# No scope variants: go directly to secondary mag count
function {ns}:v{version}/multiplayer/editor/show_secondary_mags_dialog
""")

	## ============================
	## Secondary scope dialog: deagle (Iron Sights + 4x Scope)
	## ============================
	deagle_scope_snbt = scope_actions_snbt(TRIG_SECONDARY_SCOPE_BASE, ("", "_4"), COST_SECONDARY_SCOPE)
	write_versioned_function("multiplayer/editor/scope/secondary_4only",
f"""
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {ns}:v{version}/multiplayer/editor/scope/secondary_4only_macro with storage {ns}:temp
""")
	write_versioned_function("multiplayer/editor/scope/secondary_4only_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Scope (Secondary)",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Choose your secondary optic (-{COST_SECONDARY_SCOPE} pt for scope, iron sights free).",color:"gray"}}\
}}],\
actions:[{deagle_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_BACK_SECONDARY}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_secondary_scope — Store scope, deduct cost, show secondary mags
	## ============================
	pick_sec_scope_lines = ""
	for suffix in ALL_SCOPE_SUFFIXES:
		i = ALL_SCOPE_SUFFIXES.index(suffix)
		trig = TRIG_SECONDARY_SCOPE_BASE + i
		name = SCOPE_NAMES[suffix]
		scope_cost = COST_SECONDARY_SCOPE if suffix != "" else 0
		pick_sec_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope set value "{suffix}"\n'
		)
		pick_sec_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope_name set value "{name}"\n'
		)
		if scope_cost > 0:
			pick_sec_scope_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'execute if score @s {ns}.mp.edit_points matches ..{scope_cost - 1} run '
				f'return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Not enough points for a scope!","color":"red"}}]\n'
			)
		pick_sec_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope set value "{suffix}"\n'
		)
		pick_sec_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope_name set value "{name}"\n'
		)
		if scope_cost > 0:
			pick_sec_scope_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'scoreboard players remove @s {ns}.mp.edit_points {scope_cost}\n'
			)

	write_versioned_function("multiplayer/editor/pick_secondary_scope",
f"""
# Store secondary scope and deduct cost
{pick_sec_scope_lines}
# Compute full secondary ID
function {ns}:v{version}/multiplayer/editor/set_secondary_full with storage {ns}:temp editor

# Show secondary mag count dialog
function {ns}:v{version}/multiplayer/editor/show_secondary_mags_dialog
""")

	write_versioned_function("multiplayer/editor/set_secondary_full",
f"""$data modify storage {ns}:temp editor.secondary_full set value "$(secondary)$(secondary_scope)"
""")

	## ============================
	## show_secondary_mags_dialog — Pick how many secondary magazines (0-5)
	## ============================
	mag_actions_secondary: list[str] = []
	for count in range(0, 6):
		trig = TRIG_SECONDARY_MAGS_BASE + count
		extra_cost = count * COST_SECONDARY_MAG
		label = f"{count}x Magazine" if count > 0 else "No Mags (0)"
		label_color = "yellow" if count > 0 else "green"
		cost_text = f"-{extra_cost} pt" if extra_cost > 0 else "Free"
		desc = f"{count} magazine(s) in inventory" if count > 0 else "No secondary magazines"
		mag_actions_secondary.append(
			f'{{label:{{text:"{label}",color:"{label_color}"}},'
			f'tooltip:["",{{"text":"{cost_text}","color":"gold"}},{{"text":"\\n{desc}","color":"gray"}}],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	mag_actions_secondary_snbt = ",".join(mag_actions_secondary)

	write_versioned_function("multiplayer/editor/show_secondary_mags_dialog",
f"""
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {ns}:v{version}/multiplayer/editor/show_secondary_mags_dialog_macro with storage {ns}:temp
""")
	write_versioned_function("multiplayer/editor/show_secondary_mags_dialog_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Secondary Magazines",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Select number of secondary magazines ({COST_SECONDARY_MAG} pt each).",color:"gray"}}\
}}],\
actions:[{mag_actions_secondary_snbt}],\
columns:1,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_BACK_SECONDARY}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_secondary_mags — Store mag count, deduct cost, show equip slot 1
	## ============================
	pick_secondary_mags_lines = ""
	for count in range(0, 6):
		trig = TRIG_SECONDARY_MAGS_BASE + count
		extra_cost = count * COST_SECONDARY_MAG
		if extra_cost > 0:
			pick_secondary_mags_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'execute if score @s {ns}.mp.edit_points matches ..{extra_cost - 1} run '
				f'return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Not enough points for {count} secondary magazine(s)!","color":"red"}}]\n'
			)
		pick_secondary_mags_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_mag_count set value {count}\n'
		)
		if extra_cost > 0:
			pick_secondary_mags_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'scoreboard players remove @s {ns}.mp.edit_points {extra_cost}\n'
			)

	write_versioned_function("multiplayer/editor/pick_secondary_mags",
f"""
# Store secondary mag count and deduct cost
{pick_secondary_mags_lines}
# Show equipment slot 1 dialog
function {ns}:v{version}/multiplayer/editor/show_equip_slot1_dialog
""")

	## ============================
	## show_equip_slot1_dialog — Pick grenade for slot 1 (hotbar.8)
	## ============================
	equip1_actions: list[str] = []
	for grenade_idx, (item_id, display) in enumerate(GRENADE_TYPES):
		trig = TRIG_EQUIP_SLOT1_BASE + grenade_idx
		cost_text = f"-{COST_GRENADE} pt" if item_id else "Free"
		label_color = "yellow" if item_id else "green"
		equip1_actions.append(
			f'{{label:{{text:"{display}",color:"{label_color}"}},'
			f'tooltip:{{text:"{cost_text}"}},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	equip1_actions_snbt = ",".join(equip1_actions)

	write_versioned_function("multiplayer/editor/show_equip_slot1_dialog",
f"""
scoreboard players set @s {ns}.mp.edit_step 3
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {ns}:v{version}/multiplayer/editor/show_equip_slot1_dialog_macro with storage {ns}:temp
""")
	write_versioned_function("multiplayer/editor/show_equip_slot1_dialog_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Equipment Slot 1",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Choose grenade for slot 1 (hotbar.8) — {COST_GRENADE} pt if not None.",color:"gray"}}\
}}],\
actions:[{equip1_actions_snbt}],\
columns:3,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_BACK_SECONDARY}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_equip_slot1 — Store slot 1 grenade, deduct cost, show slot 2
	## ============================
	pick_equip1_lines = ""
	for grenade_idx, (item_id, _display) in enumerate(GRENADE_TYPES):
		trig = TRIG_EQUIP_SLOT1_BASE + grenade_idx
		if item_id:  # not "None" — check budget first
			pick_equip1_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'execute if score @s {ns}.mp.edit_points matches ..{COST_GRENADE - 1} run '
				f'return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Not enough points for a grenade!","color":"red"}}]\n'
			)
		pick_equip1_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.equip_slot1 set value "{item_id}"\n'
		)
		if item_id:  # not "None"
			pick_equip1_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'scoreboard players remove @s {ns}.mp.edit_points {COST_GRENADE}\n'
			)

	write_versioned_function("multiplayer/editor/pick_equip_slot1",
f"""
# Store slot 1 grenade and deduct cost
{pick_equip1_lines}
# Show equipment slot 2 dialog
function {ns}:v{version}/multiplayer/editor/show_equip_slot2_dialog
""")

	## ============================
	## editor/back_to_equip1 — Refund equip_slot1 cost, go back to slot 1 dialog
	##   (called when pressing Back from equip slot 2 dialog, edit_step=4)
	## ============================
	write_versioned_function("multiplayer/editor/back_to_equip1",
f"""
# Refund equip_slot1 grenade cost if one was selected
execute unless data storage {ns}:temp editor{{equip_slot1:""}} run scoreboard players add @s {ns}.mp.edit_points {COST_GRENADE}
# Clear equip_slot1 state
data modify storage {ns}:temp editor.equip_slot1 set value ""
# Show equip slot 1 dialog
function {ns}:v{version}/multiplayer/editor/show_equip_slot1_dialog
""")

	## ============================
	## editor/back_from_perks — Refund equip_slot2 cost, go back to slot 2 dialog
	##   (called when pressing Back from perks dialog, edit_step=9)
	## ============================
	write_versioned_function("multiplayer/editor/back_from_perks",
f"""
# Refund equip_slot2 grenade cost if one was selected
execute unless data storage {ns}:temp editor{{equip_slot2:""}} run scoreboard players add @s {ns}.mp.edit_points {COST_GRENADE}
# Clear equip_slot2 state and perks list
data modify storage {ns}:temp editor.equip_slot2 set value ""
data modify storage {ns}:temp editor.perks set value []
# Show equip slot 2 dialog
function {ns}:v{version}/multiplayer/editor/show_equip_slot2_dialog
""")

	## ============================
	## show_equip_slot2_dialog — Pick grenade for slot 2 (hotbar.7)
	## ============================
	equip2_actions: list[str] = []
	for grenade_idx, (item_id, display) in enumerate(GRENADE_TYPES):
		trig = TRIG_EQUIP_SLOT2_BASE + grenade_idx
		cost_text = f"-{COST_GRENADE} pt" if item_id else "Free"
		label_color = "yellow" if item_id else "green"
		equip2_actions.append(
			f'{{label:{{text:"{display}",color:"{label_color}"}},'
			f'tooltip:{{text:"{cost_text}"}},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	equip2_actions_snbt = ",".join(equip2_actions)

	write_versioned_function("multiplayer/editor/show_equip_slot2_dialog",
f"""
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {ns}:v{version}/multiplayer/editor/show_equip_slot2_dialog_macro with storage {ns}:temp
""")
	write_versioned_function("multiplayer/editor/show_equip_slot2_dialog_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Equipment Slot 2",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Choose grenade for slot 2 (hotbar.7) — {COST_GRENADE} pt if not None.",color:"gray"}}\
}}],\
actions:[{equip2_actions_snbt}],\
columns:3,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_BACK_EQUIPMENT}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_equip_slot2 — Store slot 2, deduct cost, show perks dialog
	## ============================
	pick_equip2_lines = ""
	for grenade_idx, (item_id, _display) in enumerate(GRENADE_TYPES):
		trig = TRIG_EQUIP_SLOT2_BASE + grenade_idx
		if item_id:  # not "None" — check budget first
			pick_equip2_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'execute if score @s {ns}.mp.edit_points matches ..{COST_GRENADE - 1} run '
				f'return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Not enough points for a grenade!","color":"red"}}]\n'
			)
		pick_equip2_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.equip_slot2 set value "{item_id}"\n'
		)
		if item_id:
			pick_equip2_lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'scoreboard players remove @s {ns}.mp.edit_points {COST_GRENADE}\n'
			)

	write_versioned_function("multiplayer/editor/pick_equip_slot2",
f"""
# Store slot 2 grenade and deduct cost
{pick_equip2_lines}
# Clear perks list (fresh start)
data modify storage {ns}:temp editor.perks set value []
# Show perks dialog
function {ns}:v{version}/multiplayer/editor/show_perks_dialog
""")

	## ============================
	## show_perks_dialog — Toggle perks (up to MAX_PERKS)
	## ============================
	perks_actions: list[str] = []
	for perk_idx, (_perk_id, perk_name, perk_desc, _score) in enumerate(PERKS):
		trig = TRIG_PERK_BASE + perk_idx
		perks_actions.append(
			f'{{label:{{text:"{perk_name}",color:"aqua"}},'
			f'tooltip:["",{{"text":"{perk_desc}","color":"gray"}},{{"text":"\\nCost: ","color":"white"}},{{"text":"{COST_PERK} pt","color":"gold"}}],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	# Done button
	perks_actions.append(
		f'{{label:{{text:"Done (Confirm)",color:"green","bold":true}},'
		f'tooltip:{{text:"Finish perks and review loadout — free action"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_PERKS_DONE}"}}}}'
	)
	perks_actions_snbt = ",".join(perks_actions)

	# Build perk status check lines for the macro
	perk_status_checks = ""
	for perk_idx, (perk_id, *_) in enumerate(PERKS):
		perk_status_checks += (
			f'execute if data storage {ns}:temp editor{{perks:["{perk_id}"]}} '
			f'run data modify storage {ns}:temp _perk_{perk_idx} set value 1\n'
		)
		perk_status_checks += (
			f'execute unless data storage {ns}:temp editor{{perks:["{perk_id}"]}} '
			f'run data modify storage {ns}:temp _perk_{perk_idx} set value 0\n'
		)

	perk_count_checks = "".join(
		f'execute if data storage {ns}:temp editor{{perks:["{perk_id}"]}} run scoreboard players add #perk_count {ns}.data 1\n'
		for perk_id, *_ in PERKS
	)

	write_versioned_function("multiplayer/editor/show_perks_dialog",
f"""
scoreboard players set @s {ns}.mp.edit_step 9
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points

# Determine which perks are selected
{perk_status_checks}

# Count selected perks
scoreboard players set #perk_count {ns}.data 0
{perk_count_checks}
execute store result storage {ns}:temp _perk_count int 1 run scoreboard players get #perk_count {ns}.data

function {ns}:v{version}/multiplayer/editor/show_perks_dialog_macro with storage {ns}:temp
""")

	# Perks body includes per-perk lines showing if each is selected
	perks_body_lines = ""
	for perk_idx, (_perk_id, perk_name, _perk_desc, _) in enumerate(PERKS):
		# We'll add a static indicator based on the macro variable _perk_N
		perks_body_lines += (
			f'{{{{"type":"minecraft:plain_message",'
			f'"contents":["",{{"text":"$(_perk_{perk_idx})","obfuscated":false,"color":"green"}},'
			f'{{"text":" {perk_name}","color":{{}}}}]}}}}'
		)

	# Build perk status lines for the macro — each shows ✔ or ✘ based on _perk_N value
	# Since we can't do conditional text in one SNBT, we'll show the check mark count and list names
	write_versioned_function("multiplayer/editor/show_perks_dialog_macro",
f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Perks",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",{{"text":"Points remaining: ","color":"white"}},{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Toggle perks below (max {MAX_PERKS}, {COST_PERK} pt each). Selected: $(_perk_count)/{MAX_PERKS}",color:"gray"}}\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"(Click a perk to toggle. Currently selected perks are removed for refund.)",color:"dark_gray"}}\
}}],\
actions:[{perks_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_BACK_EQUIPMENT}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_perk — Toggle a perk on/off; re-show perks dialog
	## ============================
	pick_perk_dispatch = ""
	for perk_idx, (_perk_id, _perk_name, _perk_desc, _) in enumerate(PERKS):
		trig = TRIG_PERK_BASE + perk_idx
		pick_perk_dispatch += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'function {ns}:v{version}/multiplayer/editor/toggle_perk_{perk_idx}\n'
		)

	write_versioned_function("multiplayer/editor/pick_perk",
f"""
# Toggle the selected perk
{pick_perk_dispatch}
# Re-open the perks dialog to reflect updated state
function {ns}:v{version}/multiplayer/editor/show_perks_dialog
""")

	# Generate toggle functions per perk
	for perk_idx, (perk_id, _perk_name, _perk_desc, _) in enumerate(PERKS):
		perk_count_check = "".join(
			f'execute if data storage {ns}:temp editor{{perks:["{pid}"]}} run scoreboard players add #perk_count {ns}.data 1\n'
			for pid, *_ in PERKS
		)
		write_versioned_function(f"multiplayer/editor/toggle_perk_{perk_idx}",
f"""
# Check if already selected → remove (refund) and early-exit
execute if data storage {ns}:temp editor{{perks:["{perk_id}"]}} run scoreboard players add @s {ns}.mp.edit_points {COST_PERK}
execute if data storage {ns}:temp editor{{perks:["{perk_id}"]}} run return run function {ns}:v{version}/multiplayer/editor/remove_perk_{perk_idx}

# Check max perks limit
scoreboard players set #perk_count {ns}.data 0
{perk_count_check}
execute if score #perk_count {ns}.data matches {MAX_PERKS}.. run return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Max {MAX_PERKS} perks allowed!","color":"red"}}]

# Check points budget
execute if score @s {ns}.mp.edit_points matches ..0 run return run tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Not enough points!","color":"red"}}]

# Add perk and deduct points
data modify storage {ns}:temp editor.perks append value "{perk_id}"
scoreboard players remove @s {ns}.mp.edit_points {COST_PERK}
""")

		write_versioned_function(f"multiplayer/editor/remove_perk_{perk_idx}",
f"""
# Rebuild perks list without "{perk_id}"
data modify storage {ns}:temp _remove_iter set from storage {ns}:temp editor.perks
data modify storage {ns}:temp editor.perks set value []
function {ns}:v{version}/multiplayer/editor/rebuild_perks_{perk_idx}
""")

		write_versioned_function(f"multiplayer/editor/rebuild_perks_{perk_idx}",
f"""
execute unless data storage {ns}:temp _remove_iter[0] run return 0
data modify storage {ns}:temp _perk_val set from storage {ns}:temp _remove_iter[0]
data remove storage {ns}:temp _remove_iter[0]
# Re-add if not the removed perk, then continue loop
execute unless data storage {ns}:temp {{_perk_val:"{perk_id}"}} run data modify storage {ns}:temp editor.perks append from storage {ns}:temp _perk_val
function {ns}:v{version}/multiplayer/editor/rebuild_perks_{perk_idx}
""")

	## ============================
	## editor/perks_done — Advance to confirm step
	## ============================
	write_versioned_function("multiplayer/editor/perks_done",
f"""
scoreboard players set @s {ns}.mp.edit_step 10
# Show confirmation dialog
function {ns}:v{version}/multiplayer/editor/show_confirm with storage {ns}:temp editor
""")

	## ============================
	## editor/show_confirm — Macro function to build the review dialog
	## ============================
	write_versioned_function("multiplayer/editor/show_confirm",
f"""
# Compute points used = PICK10_TOTAL - remaining
scoreboard players set #pts_used {ns}.data {PICK10_TOTAL}
scoreboard players operation #pts_used {ns}.data -= @s {ns}.mp.edit_points
execute store result storage {ns}:temp _pts_used int 1 run scoreboard players get #pts_used {ns}.data

$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Review",color:"gold",bold:true}},\
body:[\
{{type:"minecraft:plain_message",contents:["",{{"text":"Points used: ","color":"white"}},{{"text":"PLACEHOLDER","color":"gold"}}]}},\
{{type:"minecraft:plain_message",contents:{{text:"Review your loadout before saving:",color:"white"}}}},\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Primary: ","color":"white"}},{{"text":"$(primary_name)","color":"green","bold":true}},{{"text":" ($(primary_scope_name)) x$(primary_mag_count) mags","color":"dark_green"}}]}},\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Secondary: ","color":"white"}},{{"text":"$(secondary_name)","color":"yellow","bold":true}},{{"text":" x$(secondary_mag_count) mags","color":"gold"}}]}},\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Equip 1: ","color":"white"}},{{"text":"$(equip_slot1)","color":"aqua","bold":true}}]}},\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Equip 2: ","color":"white"}},{{"text":"$(equip_slot2)","color":"aqua","bold":true}}]}}\
],\
actions:[\
{{label:{{text:"Save as Public",color:"green"}},tooltip:{{text:"Everyone can see and use this loadout"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PUBLIC}"}}}},\
{{label:{{text:"Save as Private",color:"yellow"}},tooltip:{{text:"Only you can see and use this loadout"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PRIVATE}"}}}}\
],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_BACK_PERKS}"}}}}\
}}

# Fix the pts used line (body[0])
function {ns}:v{version}/multiplayer/editor/patch_pts_used with storage {ns}:temp

# Append perk lines to body
execute if data storage {ns}:temp editor.perks[0] run function {ns}:v{version}/multiplayer/editor/append_perks_to_confirm

# Show
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	write_versioned_function("multiplayer/editor/patch_pts_used",
f"""$data modify storage {ns}:temp dialog.body[0].contents set value ["",{{"text":"Points used: ","color":"white"}},{{"text":"$(_pts_used)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]
""")

	write_versioned_function("multiplayer/editor/append_perks_to_confirm",
f"""
data modify storage {ns}:temp _perk_iter set from storage {ns}:temp editor.perks
function {ns}:v{version}/multiplayer/editor/append_perk_line
""")

	write_versioned_function("multiplayer/editor/append_perk_line",
f"""
execute unless data storage {ns}:temp _perk_iter[0] run return 0
data modify storage {ns}:temp _perk_val set from storage {ns}:temp _perk_iter[0]
data remove storage {ns}:temp _perk_iter[0]
function {ns}:v{version}/multiplayer/editor/append_perk_line_macro with storage {ns}:temp
""")

	write_versioned_function("multiplayer/editor/append_perk_line_macro",
f"""$data modify storage {ns}:temp dialog.body append value {{type:"minecraft:plain_message",contents:["",{{"text":"  ✔ Perk: ","color":"white"}},{{"text":"$(_perk_val)","color":"aqua"}}]}}
function {ns}:v{version}/multiplayer/editor/append_perk_line
""")

	## ============================
	## editor/save — Create the loadout entry with Pick-10 data
	## ============================
	# Pre-generate primary weapon slot lookup table
	primary_slot_entries: list[str] = []
	for gun_id, _display, _category, mag_id, mag_count in PRIMARY_WEAPONS:
		gun_slot = f'{{slot:"hotbar.0",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}'
		is_consumable = "1b" if mag_id in CONSUMABLE_MAGS else "0b"
		bullets = mag_count if mag_id in CONSUMABLE_MAGS else 0
		primary_slot_entries.append(
			f'{{id:"{gun_id}",gun_slot:{gun_slot},mag_id:"{mag_id}",mag_consumable:{is_consumable},mag_bullets:{bullets}}}'
		)
	primary_slot_table_snbt = ",".join(primary_slot_entries)

	# Pre-generate secondary weapon slot lookup table
	secondary_slot_entries: list[str] = []
	for gun_id, _display, mag_id, mag_count in SECONDARY_WEAPONS:
		gun_slot = f'{{slot:"hotbar.1",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}'
		is_consumable = "1b" if mag_id in CONSUMABLE_MAGS else "0b"
		bullets = mag_count if mag_id in CONSUMABLE_MAGS else 0
		secondary_slot_entries.append(
			f'{{id:"{gun_id}",gun_slot:{gun_slot},mag_id:"{mag_id}",mag_consumable:{is_consumable},mag_bullets:{bullets}}}'
		)
	secondary_slot_table_snbt = ",".join(secondary_slot_entries)

	write_load_file(
f"""
# Slot lookup tables for custom loadout editor (pre-computed at build time)
data modify storage {ns}:multiplayer primary_slot_table set value [{primary_slot_table_snbt}]
data modify storage {ns}:multiplayer secondary_slot_table set value [{secondary_slot_table_snbt}]
""")

	# Primary dispatch (match base weapon ID stored in editor.primary)
	save_primary_dispatch = ""
	for idx, (gun_id, *_) in enumerate(PRIMARY_WEAPONS):
		save_primary_dispatch += (
			f'execute if data storage {ns}:temp editor{{primary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.primary_data set from storage {ns}:multiplayer primary_slot_table[{idx}]\n'
		)

	# Secondary dispatch
	save_secondary_dispatch = ""
	for idx, (gun_id, *_) in enumerate(SECONDARY_WEAPONS):
		save_secondary_dispatch += (
			f'execute if data storage {ns}:temp editor{{secondary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.secondary_data set from storage {ns}:multiplayer secondary_slot_table[{idx}]\n'
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
# Look up secondary weapon slot data
{save_secondary_dispatch}

# Build the new loadout entry (include new Pick-10 fields)
data modify storage {ns}:temp _new_loadout set value {{id:0,owner_pid:0,owner_name:"",name:"",public:0b,likes:0,main_gun:"",secondary_gun:"",primary_mag_count:1,secondary_mag_count:0,equip_slot1:"",equip_slot2:"",perks:[],slots:[]}}

# Set loadout ID from counter
execute store result storage {ns}:temp _new_loadout.id int 1 run data get storage {ns}:multiplayer next_loadout_id

# Increment the counter
execute store result score #temp {ns}.data run data get storage {ns}:multiplayer next_loadout_id
scoreboard players add #temp {ns}.data 1
execute store result storage {ns}:multiplayer next_loadout_id int 1 run scoreboard players get #temp {ns}.data

# Set owner info
execute store result storage {ns}:temp _new_loadout.owner_pid int 1 run scoreboard players get @s {ns}.mp.pid

# Set weapon IDs (scope-modified)
data modify storage {ns}:temp _new_loadout.main_gun set from storage {ns}:temp editor.primary_full
data modify storage {ns}:temp _new_loadout.secondary_gun set from storage {ns}:temp editor.secondary_full

# Copy Pick-10 fields from editor
data modify storage {ns}:temp _new_loadout.primary_mag_count set from storage {ns}:temp editor.primary_mag_count
data modify storage {ns}:temp _new_loadout.secondary_mag_count set from storage {ns}:temp editor.secondary_mag_count
data modify storage {ns}:temp _new_loadout.equip_slot1 set from storage {ns}:temp editor.equip_slot1
data modify storage {ns}:temp _new_loadout.equip_slot2 set from storage {ns}:temp editor.equip_slot2
data modify storage {ns}:temp _new_loadout.perks set from storage {ns}:temp editor.perks

# Set visibility
execute if score #cl_public {ns}.data matches 1 run data modify storage {ns}:temp _new_loadout.public set value 1b

# Override weapon loot entries with scope-modified IDs
function {ns}:v{version}/multiplayer/editor/fix_primary_loot with storage {ns}:temp editor
execute if data storage {ns}:temp _build.secondary_data run function {ns}:v{version}/multiplayer/editor/fix_secondary_loot with storage {ns}:temp editor

# Build slot list
# 1. Primary weapon (hotbar.0)
data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.primary_data.gun_slot

# 2. Secondary weapon (hotbar.1) — if selected
execute if data storage {ns}:temp _build.secondary_data run data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.secondary_data.gun_slot

# 3. Equipment slots (hotbar.8 and hotbar.7)
execute unless data storage {ns}:temp editor{{equip_slot1:""}} run function {ns}:v{version}/multiplayer/editor/append_equip1 with storage {ns}:temp editor
execute unless data storage {ns}:temp editor{{equip_slot2:""}} run function {ns}:v{version}/multiplayer/editor/append_equip2 with storage {ns}:temp editor

# 4. Primary magazine slots (inventory slots starting at 0)
scoreboard players set #inv_slot {ns}.data 0
data modify storage {ns}:temp _mag_data set from storage {ns}:temp _build.primary_data
execute store result score #pmag_count {ns}.data run data get storage {ns}:temp editor.primary_mag_count
execute if score #pmag_count {ns}.data matches 1.. run function {ns}:v{version}/multiplayer/editor/append_mag_slots

# 5. Secondary magazine slots (continuing from #inv_slot)
execute if data storage {ns}:temp _build.secondary_data run function {ns}:v{version}/multiplayer/editor/start_secondary_mags

# Auto-name the loadout
function {ns}:v{version}/multiplayer/editor/set_name with storage {ns}:temp editor

# Append to custom loadouts list
data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout

# Reset editor state
scoreboard players set @s {ns}.mp.edit_step 0

# Notify player
function {ns}:v{version}/multiplayer/editor/notify_saved with storage {ns}:temp editor
""")

	## Equip slot append macros
	write_versioned_function("multiplayer/editor/append_equip1",
f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"hotbar.8",loot:"{ns}:i/$(equip_slot1)",count:1,consumable:0b,bullets:0}}
""")

	write_versioned_function("multiplayer/editor/append_equip2",
f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"hotbar.7",loot:"{ns}:i/$(equip_slot2)",count:1,consumable:0b,bullets:0}}
""")

	## append_mag_slots — Add magazine slots based on type and count
	write_versioned_function("multiplayer/editor/append_mag_slots",
f"""
# Flatten mag_id for macro use (macro vars can't use dot-paths)
data modify storage {ns}:temp _mag_id set from storage {ns}:temp _mag_data.mag_id
data modify storage {ns}:temp _mag_bullets set from storage {ns}:temp _mag_data.mag_bullets

# Consumable mag: one slot only (with count and bullets)
execute if data storage {ns}:temp _mag_data{{mag_consumable:1b}} run function {ns}:v{version}/multiplayer/editor/append_mag_consumable
execute if data storage {ns}:temp _mag_data{{mag_consumable:1b}} run return 0

# Non-consumable: add one slot per count
execute if score #pmag_count {ns}.data matches 1.. run function {ns}:v{version}/multiplayer/editor/append_mag_loop
""")

	write_versioned_function("multiplayer/editor/append_mag_consumable",
f"""
execute store result storage {ns}:temp _inv_n int 1 run scoreboard players get #inv_slot {ns}.data
function {ns}:v{version}/multiplayer/editor/append_mag_consumable_macro with storage {ns}:temp
scoreboard players add #inv_slot {ns}.data 1
""")

	write_versioned_function("multiplayer/editor/append_mag_consumable_macro",
f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"inventory.$(_inv_n)",loot:"{ns}:i/$(_mag_id)",count:1,consumable:1b,bullets:$(_mag_bullets)}}
""")

	write_versioned_function("multiplayer/editor/append_mag_loop",
f"""
execute if score #pmag_count {ns}.data matches ..0 run return 0
execute store result storage {ns}:temp _inv_n int 1 run scoreboard players get #inv_slot {ns}.data
function {ns}:v{version}/multiplayer/editor/append_mag_regular with storage {ns}:temp
scoreboard players add #inv_slot {ns}.data 1
scoreboard players remove #pmag_count {ns}.data 1
return run function {ns}:v{version}/multiplayer/editor/append_mag_loop
""")

	write_versioned_function("multiplayer/editor/append_mag_regular",
f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"inventory.$(_inv_n)",loot:"{ns}:i/$(_mag_id)",count:1,consumable:0b,bullets:0}}
""")

	## start_secondary_mags — setup secondary mag data and loop
	write_versioned_function("multiplayer/editor/start_secondary_mags",
f"""
data modify storage {ns}:temp _mag_data set from storage {ns}:temp _build.secondary_data
execute store result score #pmag_count {ns}.data run data get storage {ns}:temp editor.secondary_mag_count
execute if score #pmag_count {ns}.data matches 1.. run function {ns}:v{version}/multiplayer/editor/append_mag_slots
""")

	## ============================
	## Fix loot macros
	## ============================
	write_versioned_function("multiplayer/editor/fix_primary_loot",
f"""$data modify storage {ns}:temp _build.primary_data.gun_slot.loot set value "{ns}:i/$(primary_full)"
""")

	write_versioned_function("multiplayer/editor/fix_secondary_loot",
f"""$data modify storage {ns}:temp _build.secondary_data.gun_slot.loot set value "{ns}:i/$(secondary_full)"
""")

	## ============================
	## Name and notification macros
	## ============================
	write_versioned_function("multiplayer/editor/set_name", f"""$data modify storage {ns}:temp _new_loadout.name set value "$(primary_name) + $(secondary_name)"\n""")

	write_versioned_function("multiplayer/editor/notify_saved", """$tellraw @s ["",{"text":"[MGS] ","color":"gold"},{"text":"Loadout saved: ","color":"white"},{"text":"$(primary_name) + $(secondary_name)","color":"green","bold":true}]""")

