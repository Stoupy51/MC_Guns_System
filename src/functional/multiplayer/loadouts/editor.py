
# ruff: noqa: E501
# Custom Loadout Editor — CoD-style hub.
#
# The editor opens on a HUB page listing every category (guns, magazines, grenades, perks)
# with the current selection on each button and the Pick-10 points at the top.
# Clicking a row opens a short submenu (e.g. Primary: gun → scope → camo) that returns
# to the hub when done. Rows whose prerequisite is missing (magazines without the gun,
# saving without a primary) are grayed out as "Unavailable".
#
# Points are never deducted/refunded incrementally: editor/recompute_points derives the
# cost from the current state, and every mutation goes through a snapshot+commit check
# that reverts and denies when the budget would be exceeded.
from stewbeet import Mem, write_load_file, write_versioned_function

from ...helpers import MGS_TAG
from ..classes import CONSUMABLE_MAGS
from .catalogs import (
	ALL_SCOPE_SUFFIXES,
	CAMO_VARIANTS,
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
	TRIG_EQUIP1_CAMO_BASE,
	TRIG_EQUIP2_CAMO_BASE,
	TRIG_EQUIP_SLOT1_BASE,
	TRIG_EQUIP_SLOT2_BASE,
	TRIG_HUB,
	TRIG_HUB_EQUIP1,
	TRIG_HUB_EQUIP2,
	TRIG_HUB_PERKS,
	TRIG_HUB_PRIMARY,
	TRIG_HUB_PRIMARY_MAGS,
	TRIG_HUB_SECONDARY,
	TRIG_HUB_SECONDARY_MAGS,
	TRIG_OVERKILL_SEC_BASE,
	TRIG_PERK_BASE,
	TRIG_PRIMARY_BASE,
	TRIG_PRIMARY_CAMO_BASE,
	TRIG_PRIMARY_MAGS_BASE,
	TRIG_PRIMARY_SCOPE_BASE,
	TRIG_REMOVE_PRIMARY,
	TRIG_REMOVE_SECONDARY,
	TRIG_SAVE_PRIVATE,
	TRIG_SAVE_PUBLIC,
	TRIG_SECONDARY_BASE,
	TRIG_SECONDARY_CAMO_BASE,
	TRIG_SECONDARY_MAGS_BASE,
	TRIG_SECONDARY_SCOPE_BASE,
)


# Empty editor state (display fields default to readable values so hub rows always render)
def _empty_state() -> str:
	return (
		'{primary:"",primary_name:"None",primary_mag:"",primary_mag_count:1,'
		'primary_scope:"",primary_scope_name:"Iron Sights",primary_camo:"",primary_camo_name:"Default",primary_full:"",'
		'secondary:"",secondary_name:"None",secondary_mag:"",secondary_mag_count:0,'
		'secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"",'
		'equip_slot1:"",equip_slot1_name:"None",equip_slot1_camo:"",'
		'equip_slot2:"",equip_slot2_name:"None",equip_slot2_camo:"",'
		'perks:[]}'
	)


def generate_editor() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	fn = f"{ns}:v{version}/multiplayer/editor"

	## ====================================================================
	## Per-player editor state isolation
	## Editor state is stored in {ns}:editor.{pid} (one per player).
	## At dispatch start, we load to {ns}:temp editor; at end, save back.
	## ====================================================================
	write_versioned_function("multiplayer/editor/load_state", f"""
# Initialize this player's slot first: if the copy failed (first interaction), {ns}:temp editor
# would otherwise keep another player's in-progress state
$execute unless data storage {ns}:editor "$(_pid)" run data modify storage {ns}:editor "$(_pid)" set value {{}}
$data modify storage {ns}:temp editor set from storage {ns}:editor "$(_pid)"
""")
	write_versioned_function("multiplayer/editor/save_state", f"""
$data modify storage {ns}:editor "$(_pid)" set from storage {ns}:temp editor
""")

	## ====================================================================
	## State init, budget recompute, and the snapshot/commit pattern
	## ====================================================================
	write_versioned_function("multiplayer/editor/init_state", f"""
data modify storage {ns}:temp editor set value {_empty_state()}
""")

	## Derive the Pick-10 cost from the current state (mags only count when their gun is picked)
	recompute_lines: list[str] = [f"scoreboard players set #lc_cost {ns}.data 0"]
	for prefix, w_cost, s_cost, m_cost in [
		("primary", COST_PRIMARY_WEAPON, COST_PRIMARY_SCOPE, COST_PRIMARY_MAG),
		("secondary", COST_SECONDARY_WEAPON, COST_SECONDARY_SCOPE, COST_SECONDARY_MAG),
	]:
		recompute_lines += [
			f'execute unless data storage {ns}:temp editor{{{prefix}:""}} run scoreboard players add #lc_cost {ns}.data {w_cost}',
			f'execute unless data storage {ns}:temp editor{{{prefix}:""}} unless data storage {ns}:temp editor{{{prefix}_scope:""}} run scoreboard players add #lc_cost {ns}.data {s_cost}',
			f'execute unless data storage {ns}:temp editor{{{prefix}:""}} store result score #lc_t {ns}.data run data get storage {ns}:temp editor.{prefix}_mag_count {m_cost}',
			f'execute unless data storage {ns}:temp editor{{{prefix}:""}} run scoreboard players operation #lc_cost {ns}.data += #lc_t {ns}.data',
		]
	for field in ("equip_slot1", "equip_slot2"):
		recompute_lines.append(
			f'execute unless data storage {ns}:temp editor{{{field}:""}} run scoreboard players add #lc_cost {ns}.data {COST_GRENADE}'
		)
	recompute_lines += [
		f"execute store result score #lc_t {ns}.data run data get storage {ns}:temp editor.perks {COST_PERK}",
		f"scoreboard players operation #lc_cost {ns}.data += #lc_t {ns}.data",
		f"scoreboard players set @s {ns}.mp.edit_points {PICK10_TOTAL}",
		f"scoreboard players operation @s {ns}.mp.edit_points -= #lc_cost {ns}.data",
	]
	write_versioned_function("multiplayer/editor/recompute_points", "\n".join(recompute_lines))

	## Commit check: callers snapshot {ns}:temp editor into {ns}:temp _ed_bak before mutating,
	## then `execute store success score #ed_ok ... run function .../commit_check`.
	## On overflow the mutation is reverted and the player is notified.
	write_versioned_function("multiplayer/editor/commit_check", f"""
function {fn}/recompute_points
execute if score @s {ns}.mp.edit_points matches 0.. run return 1

# Over budget: revert and deny
data modify storage {ns}:temp editor set from storage {ns}:temp _ed_bak
function {fn}/recompute_points
tellraw @s [{MGS_TAG},{{"text":"Not enough points for that!","color":"red"}}]
return fail
""")

	## ====================================================================
	## HUB — the main loadout page (CoD-style)
	## ====================================================================

	## editor/start - Create a new loadout: fresh state, then open the hub
	write_versioned_function("multiplayer/editor/start", f"""
scoreboard players set @s {ns}.mp.edit_step 1
# Default to creating a new loadout (custom/edit overrides this after calling start)
scoreboard players set @s {ns}.mp.edit_target 0
function {fn}/init_state
function {fn}/hub
""")

	# Base hub dialog (empty actions, points in body) — actions are appended afterwards
	write_versioned_function("multiplayer/editor/hub_base", f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Loadout",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",["",{{"text":"Points used"}},": "],{{"text":"$(used)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}},{{"text":"  ($(pts) left)","color":"gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Click a category to change it",color:"gray"}}\
}}],\
actions:[],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel",action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}\
}}
""")

	# Hub rows whose label depends on the current state (macro append with editor fields)
	def _row(trig: int, label_snbt: str, tooltip_snbt: str) -> str:
		return (
			f'$data modify storage {ns}:temp dialog.actions append value '
			f'{{label:{label_snbt},tooltip:{tooltip_snbt},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)

	write_versioned_function("multiplayer/editor/hub_row_primary", _row(
		TRIG_HUB_PRIMARY,
		'[{text:"\\ud83d\\udd2b ",color:"gold"},{text:"Primary: ",color:"white"},{text:"$(primary_name)",color:"green"}]',
		'{text:"$(primary_scope_name), $(primary_camo_name)\\nClick to change",color:"gray"}',
	))
	write_versioned_function("multiplayer/editor/hub_row_primary_mags", _row(
		TRIG_HUB_PRIMARY_MAGS,
		'[{text:"\\ud83d\\udce6 ",color:"gold"},{text:"Primary Mags: ",color:"white"},{text:"$(primary_mag_count)x",color:"green"}]',
		f'{{text:"{COST_PRIMARY_MAG} pt per magazine",color:"gray"}}',
	))
	write_versioned_function("multiplayer/editor/hub_row_secondary", _row(
		TRIG_HUB_SECONDARY,
		'[{text:"\\ud83d\\udd2b ",color:"yellow"},{text:"Secondary: ",color:"white"},{text:"$(secondary_name)",color:"green"}]',
		'{text:"$(secondary_scope_name), $(secondary_camo_name)\\nClick to change",color:"gray"}',
	))
	write_versioned_function("multiplayer/editor/hub_row_secondary_mags", _row(
		TRIG_HUB_SECONDARY_MAGS,
		'[{text:"\\ud83d\\udce6 ",color:"yellow"},{text:"Secondary Mags: ",color:"white"},{text:"$(secondary_mag_count)x",color:"green"}]',
		f'{{text:"{COST_SECONDARY_MAG} pt per magazine",color:"gray"}}',
	))
	write_versioned_function("multiplayer/editor/hub_row_equip1", _row(
		TRIG_HUB_EQUIP1,
		'[{text:"\\ud83d\\udca3 ",color:"red"},{text:"Grenade 1: ",color:"white"},{text:"$(equip_slot1_name)",color:"green"}]',
		f'{{text:"{COST_GRENADE} pt\\nClick to change",color:"gray"}}',
	))
	write_versioned_function("multiplayer/editor/hub_row_equip2", _row(
		TRIG_HUB_EQUIP2,
		'[{text:"\\ud83d\\udca3 ",color:"red"},{text:"Grenade 2: ",color:"white"},{text:"$(equip_slot2_name)",color:"green"}]',
		f'{{text:"{COST_GRENADE} pt\\nClick to change",color:"gray"}}',
	))
	write_versioned_function("multiplayer/editor/hub_row_perks", _row(
		TRIG_HUB_PERKS,
		f'[{{text:"\\u2b50 ",color:"aqua"}},{{text:"Perks: ",color:"white"}},{{text:"$(perks)/{MAX_PERKS}",color:"green"}}]',
		f'{{text:"{COST_PERK} pt per perk",color:"gray"}}',
	))

	# Static hub buttons
	_unavailable_mags_primary = (
		f'{{label:{{text:"\\ud83d\\udce6 Primary Mags \\u2014 Unavailable",color:"dark_gray"}},'
		f'tooltip:{{text:"Pick a primary weapon first",color:"red"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}'
	)
	_unavailable_mags_secondary = (
		f'{{label:{{text:"\\ud83d\\udce6 Secondary Mags \\u2014 Unavailable",color:"dark_gray"}},'
		f'tooltip:{{text:"Pick a secondary weapon first",color:"red"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}'
	)
	_save_public_btn = (
		f'{{label:{{text:"\\ud83d\\udcbe Save as Public",color:"green",bold:true}},'
		f'tooltip:{{text:"Everyone can see and use this loadout"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PUBLIC}"}}}}'
	)
	_save_private_btn = (
		f'{{label:{{text:"\\ud83d\\udcbe Save as Private",color:"yellow",bold:true}},'
		f'tooltip:{{text:"Only you can see and use this loadout"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PRIVATE}"}}}}'
	)
	_unavailable_save = (
		f'{{label:{{text:"\\ud83d\\udcbe Save \\u2014 Unavailable",color:"dark_gray"}},'
		f'tooltip:{{text:"A primary weapon is required",color:"red"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}'
	)

	write_versioned_function("multiplayer/editor/hub", f"""
# Points summary
function {fn}/recompute_points
scoreboard players set #pts_used {ns}.data {PICK10_TOTAL}
scoreboard players operation #pts_used {ns}.data -= @s {ns}.mp.edit_points
execute store result storage {ns}:temp _hub.pts int 1 run scoreboard players get @s {ns}.mp.edit_points
execute store result storage {ns}:temp _hub.used int 1 run scoreboard players get #pts_used {ns}.data
execute store result storage {ns}:temp _hub.perks int 1 run data get storage {ns}:temp editor.perks

# Base dialog, then one row per category (labels show the current selection)
function {fn}/hub_base with storage {ns}:temp _hub
function {fn}/hub_row_primary with storage {ns}:temp editor
execute if data storage {ns}:temp editor{{primary:""}} run data modify storage {ns}:temp dialog.actions append value {_unavailable_mags_primary}
execute unless data storage {ns}:temp editor{{primary:""}} run function {fn}/hub_row_primary_mags with storage {ns}:temp editor
function {fn}/hub_row_secondary with storage {ns}:temp editor
execute if data storage {ns}:temp editor{{secondary:""}} run data modify storage {ns}:temp dialog.actions append value {_unavailable_mags_secondary}
execute unless data storage {ns}:temp editor{{secondary:""}} run function {fn}/hub_row_secondary_mags with storage {ns}:temp editor
function {fn}/hub_row_equip1 with storage {ns}:temp editor
function {fn}/hub_row_equip2 with storage {ns}:temp editor
function {fn}/hub_row_perks with storage {ns}:temp _hub

# Save buttons (grayed out until a primary weapon is selected)
execute if data storage {ns}:temp editor{{primary:""}} run data modify storage {ns}:temp dialog.actions append value {_unavailable_save}
execute unless data storage {ns}:temp editor{{primary:""}} run data modify storage {ns}:temp dialog.actions append value {_save_public_btn}
execute unless data storage {ns}:temp editor{{primary:""}} run data modify storage {ns}:temp dialog.actions append value {_save_private_btn}

# Show
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ====================================================================
	## Shared dialog builder (static action lists, points in body, Back → hub)
	## ====================================================================
	def write_static_dialog(name: str, title: str, hint: str, actions_snbt: str, columns: int = 2, guard: str = "") -> None:
		""" Write show_<name> (+_macro): a static-actions dialog with the points line. """
		write_versioned_function(f"multiplayer/editor/show_{name}", f"""
{guard}function {fn}/recompute_points
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
function {fn}/show_{name}_macro with storage {ns}:temp
""")
		write_versioned_function(f"multiplayer/editor/show_{name}_macro", f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Loadout - {title}",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",["",{{"text":"Points remaining"}},": "],{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"{hint}",color:"gray"}}\
}}],\
actions:[{actions_snbt}],\
columns:{columns},\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ====================================================================
	## PRIMARY / SECONDARY weapon submenus: gun (or remove) → scope → camo
	## ====================================================================

	# Gun action lists (+ Remove button)
	primary_actions: list[str] = []
	for idx, (_gun_id, display, category, _mag, _mc, _il) in enumerate(w for w in PRIMARY_WEAPONS if w[5]):
		trig = TRIG_PRIMARY_BASE + idx
		primary_actions.append(
			f'{{label:{{text:"{display}",color:"yellow"}},'
			f'tooltip:["",{{"text":"{category}","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{COST_PRIMARY_WEAPON}","color":"gold"}}]," pt"],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	primary_actions.append(
		f'{{label:{{text:"\\ud83d\\uddd1 Remove Primary",color:"red"}},'
		f'tooltip:{{text:"Clear the primary weapon (refunds its points)"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_REMOVE_PRIMARY}"}}}}'
	)
	write_static_dialog("primary_dialog", "Primary Weapon", f"Choose your primary weapon ({COST_PRIMARY_WEAPON} pt + {COST_PRIMARY_MAG} pt per magazine)", ",".join(primary_actions))

	_remove_secondary_btn = (
		f'{{label:{{text:"\\ud83d\\uddd1 Remove Secondary",color:"red"}},'
		f'tooltip:{{text:"Clear the secondary weapon (refunds its points)"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_REMOVE_SECONDARY}"}}}}'
	)

	# Pistol secondary list (default)
	secondary_actions: list[str] = []
	for idx, (_gun_id, display, _mag_id, _mc, _il) in enumerate(w for w in SECONDARY_WEAPONS if w[4]):
		trig = TRIG_SECONDARY_BASE + idx
		secondary_actions.append(
			f'{{label:{{text:"{display}",color:"yellow"}},'
			f'tooltip:["",{{"text":"Pistol","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{COST_SECONDARY_WEAPON}","color":"gold"}}]," pt"],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	secondary_actions.append(_remove_secondary_btn)
	write_static_dialog("secondary_pistol_dialog", "Secondary Weapon", f"Choose your secondary weapon ({COST_SECONDARY_WEAPON} pt + {COST_SECONDARY_MAG} pt per magazine)", ",".join(secondary_actions))

	# Overkill secondary list: primaries (iron sights only, camo selectable)
	overkill_actions: list[str] = []
	for idx, (_gun_id, display, category, _mag, _mc, _il) in enumerate(w for w in PRIMARY_WEAPONS if w[5]):
		trig = TRIG_OVERKILL_SEC_BASE + idx
		overkill_actions.append(
			f'{{label:{{text:"{display}",color:"yellow"}},'
			f'tooltip:["",{{"text":"{category}","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{COST_SECONDARY_WEAPON}","color":"gold"}}]," pt"],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	overkill_actions.append(_remove_secondary_btn)
	write_static_dialog("secondary_overkill_dialog", "Overkill Secondary", f"Choose a second primary ({COST_SECONDARY_WEAPON} pt + {COST_SECONDARY_MAG} pt per magazine)", ",".join(overkill_actions))

	# Router: Overkill holders pick a primary as their secondary, everyone else picks a pistol
	write_versioned_function("multiplayer/editor/show_secondary_dialog", f"""
execute if data storage {ns}:temp editor{{perks:["overkill"]}} run return run function {fn}/show_secondary_overkill_dialog
function {fn}/show_secondary_pistol_dialog
""")

	# Gun pick handlers: snapshot → merge gun fields (resets scope/camo, mags to 1) → commit →
	# on success continue to scope (if the gun has variants) or camo; on failure back to hub.
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
				f'return run function {fn}/{func_name}\n'
			)

	pick_primary_lines = ""
	for idx, (gun_id, display, _category, mag_id, _mag_count, _il) in enumerate(w for w in PRIMARY_WEAPONS if w[5]):
		trig = TRIG_PRIMARY_BASE + idx
		pick_primary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor merge value '
			f'{{primary:"{gun_id}",primary_name:"{display}",primary_mag:"{mag_id}",primary_mag_count:1,'
			f'primary_scope:"",primary_scope_name:"Iron Sights",primary_camo:"",primary_camo_name:"Default",primary_full:"{gun_id}"}}\n'
		)

	write_versioned_function("multiplayer/editor/pick_primary", f"""
# Snapshot, apply the gun (scope/camo reset, 1 magazine), then commit against the budget
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{pick_primary_lines}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
execute if score #ed_ok {ns}.data matches 0 run return run function {fn}/hub

# Continue: scope dialog for guns with variants, camo otherwise
{scope_route_lines}
function {fn}/show_primary_camo_dialog
""")

	pick_secondary_lines = ""
	for idx, (gun_id, display, mag_id, _mag_count, _il) in enumerate(w for w in SECONDARY_WEAPONS if w[4]):
		trig = TRIG_SECONDARY_BASE + idx
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor merge value '
			f'{{secondary:"{gun_id}",secondary_name:"{display}",secondary_mag:"{mag_id}",secondary_mag_count:0,'
			f'secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"{gun_id}"}}\n'
		)
	secondary_scope_route = (
		f'execute if data storage {ns}:temp editor{{secondary:"deagle"}} run '
		f'return run function {fn}/scope/secondary_4only\n'
	)

	write_versioned_function("multiplayer/editor/pick_secondary", f"""
# Snapshot, apply the gun (scope/camo reset, 0 magazines), then commit against the budget
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{pick_secondary_lines}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
execute if score #ed_ok {ns}.data matches 0 run return run function {fn}/hub

# Continue: scope dialog for guns with variants, camo otherwise
{secondary_scope_route}
function {fn}/show_secondary_camo_dialog
""")

	# Overkill: pick a primary weapon as the secondary (iron sights, camo selectable)
	pick_overkill_lines = ""
	for idx, (gun_id, display, _category, mag_id, _mag_count, _il) in enumerate(w for w in PRIMARY_WEAPONS if w[5]):
		trig = TRIG_OVERKILL_SEC_BASE + idx
		pick_overkill_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor merge value '
			f'{{secondary:"{gun_id}",secondary_name:"{display}",secondary_mag:"{mag_id}",secondary_mag_count:0,'
			f'secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"{gun_id}"}}\n'
		)

	write_versioned_function("multiplayer/editor/pick_overkill_secondary", f"""
# Snapshot, store the chosen primary as the secondary (0 magazines), commit against the budget
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{pick_overkill_lines}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
execute if score #ed_ok {ns}.data matches 0 run return run function {fn}/hub

# Overkill secondaries keep iron sights; go straight to camo
function {fn}/show_secondary_camo_dialog
""")

	# Clear-secondary state (no navigation) — reused by remove + the Overkill toggle
	write_versioned_function("multiplayer/editor/clear_secondary", f"""
data modify storage {ns}:temp editor merge value {{secondary:"",secondary_name:"None",secondary_mag:"",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:""}}
""")

	# Remove handlers (recompute makes the refund automatic)
	write_versioned_function("multiplayer/editor/remove_primary", f"""
data modify storage {ns}:temp editor merge value {{primary:"",primary_name:"None",primary_mag:"",primary_mag_count:1,primary_scope:"",primary_scope_name:"Iron Sights",primary_camo:"",primary_camo_name:"Default",primary_full:""}}
function {fn}/hub
""")
	write_versioned_function("multiplayer/editor/remove_secondary", f"""
function {fn}/clear_secondary
function {fn}/hub
""")

	## Scope dialogs (variant subsets per gun)
	def scope_actions_snbt(trig_base: int, variants: tuple[str, ...], cost: int) -> str:
		actions: list[str] = []
		for suffix in variants:
			i = ALL_SCOPE_SUFFIXES.index(suffix)
			trig = trig_base + i
			name = SCOPE_NAMES[suffix]
			scope_cost = cost if suffix != "" else 0
			tooltip: str = '{text:"Free"}' if scope_cost == 0 else f'[{{text:"-{scope_cost}","color":"gold"}}, " pt"]'
			label_color = "green" if scope_cost == 0 else "yellow"
			actions.append(
				f'{{label:{{text:"{name}",color:"{label_color}"}},'
				f'tooltip:{tooltip},'
				f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
			)
		return ",".join(actions)

	suffix_variants: dict[str, tuple[str, ...]] = {
		"full": ("", "_1", "_2", "_3", "_4"),
		"no4": ("", "_1", "_2", "_3"),
		"1only": ("", "_1"),
	}
	for func_suffix, variants in suffix_variants.items():
		write_static_dialog(
			f"scope_primary_{func_suffix}", "Primary Scope",
			f"Choose your optic (-{COST_PRIMARY_SCOPE} pt for any scope, iron sights free)",
			scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, variants, COST_PRIMARY_SCOPE),
		)
		# Alias kept at the historical path used by the per-gun scope routing
		write_versioned_function(f"multiplayer/editor/scope/primary_{func_suffix}", f"""
function {fn}/show_scope_primary_{func_suffix}
""")
	write_static_dialog(
		"scope_secondary_4only", "Secondary Scope",
		f"Choose your secondary optic (-{COST_SECONDARY_SCOPE} pt for scope, iron sights free)",
		scope_actions_snbt(TRIG_SECONDARY_SCOPE_BASE, ("", "_4"), COST_SECONDARY_SCOPE),
	)
	write_versioned_function("multiplayer/editor/scope/secondary_4only", f"""
function {fn}/show_scope_secondary_4only
""")

	## Scope pick handlers: snapshot → set → commit (overflow keeps iron sights) → camo dialog
	def gen_pick_scope_lines(prefix: str, trig_base: int) -> str:
		lines = ""
		for i, suffix in enumerate(ALL_SCOPE_SUFFIXES):
			trig = trig_base + i
			name = SCOPE_NAMES[suffix]
			lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'data modify storage {ns}:temp editor merge value {{{prefix}_scope:"{suffix}",{prefix}_scope_name:"{name}"}}\n'
			)
		return lines

	write_versioned_function("multiplayer/editor/pick_primary_scope", f"""
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{gen_pick_scope_lines("primary", TRIG_PRIMARY_SCOPE_BASE)}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check

# Continue to camo either way (a denied scope simply stays on iron sights)
function {fn}/show_primary_camo_dialog
""")
	write_versioned_function("multiplayer/editor/pick_secondary_scope", f"""
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{gen_pick_scope_lines("secondary", TRIG_SECONDARY_SCOPE_BASE)}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check

# Continue to camo either way (a denied scope simply stays on iron sights)
function {fn}/show_secondary_camo_dialog
""")

	## Camo dialogs (free) — finish the weapon submenu and return to the hub
	def camo_actions_snbt(trig_base: int) -> str:
		actions: list[str] = []
		for camo_idx, (suffix, camo_name) in enumerate(CAMO_VARIANTS):
			label_color = "green" if suffix == "" else "yellow"
			actions.append(
				f'{{label:{{text:"{camo_name}",color:"{label_color}"}},'
				f'tooltip:{{text:"Free"}},'
				f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig_base + camo_idx}"}}}}'
			)
		return ",".join(actions)

	for prefix, title, trig_base in [
		("primary", "Primary Camo", TRIG_PRIMARY_CAMO_BASE),
		("secondary", "Secondary Camo", TRIG_SECONDARY_CAMO_BASE),
		("equip1", "Grenade 1 Camo", TRIG_EQUIP1_CAMO_BASE),
		("equip2", "Grenade 2 Camo", TRIG_EQUIP2_CAMO_BASE),
	]:
		write_static_dialog(f"{prefix}_camo_dialog", title, "Choose your camo (free, cosmetic only)", camo_actions_snbt(trig_base))

	def gen_pick_camo_lines(field: str, trig_base: int) -> str:
		lines = ""
		for camo_idx, (suffix, camo_name) in enumerate(CAMO_VARIANTS):
			trig = trig_base + camo_idx
			lines += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'data modify storage {ns}:temp editor.{field}_camo set value "{suffix}"\n'
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'data modify storage {ns}:temp editor.{field}_camo_name set value "{camo_name}"\n'
			)
		return lines

	write_versioned_function("multiplayer/editor/set_primary_full", f"""$data modify storage {ns}:temp editor.primary_full set value "$(primary)$(primary_scope)$(primary_camo)"
""")
	write_versioned_function("multiplayer/editor/set_secondary_full", f"""$data modify storage {ns}:temp editor.secondary_full set value "$(secondary)$(secondary_scope)$(secondary_camo)"
""")

	write_versioned_function("multiplayer/editor/pick_primary_camo", f"""
{gen_pick_camo_lines("primary", TRIG_PRIMARY_CAMO_BASE)}
function {fn}/set_primary_full with storage {ns}:temp editor
function {fn}/hub
""")
	write_versioned_function("multiplayer/editor/pick_secondary_camo", f"""
{gen_pick_camo_lines("secondary", TRIG_SECONDARY_CAMO_BASE)}
function {fn}/set_secondary_full with storage {ns}:temp editor
function {fn}/hub
""")
	write_versioned_function("multiplayer/editor/pick_equip1_camo", f"""
{gen_pick_camo_lines("equip_slot1", TRIG_EQUIP1_CAMO_BASE)}
function {fn}/hub
""")
	write_versioned_function("multiplayer/editor/pick_equip2_camo", f"""
{gen_pick_camo_lines("equip_slot2", TRIG_EQUIP2_CAMO_BASE)}
function {fn}/hub
""")

	## ====================================================================
	## MAGAZINE submenus (guarded: their gun must be selected)
	## ====================================================================
	mag_actions_primary: list[str] = []
	for count in range(1, 6):
		trig = TRIG_PRIMARY_MAGS_BASE + count
		mag_actions_primary.append(
			f'{{label:{{text:"{count}x Magazine",color:"yellow"}},'
			f'tooltip:["",{{"text":"-{count * COST_PRIMARY_MAG}","color":"gold"}}," ",{{"text":"pt","color":"gold"}},{{"text":"\\n{count} magazine(s) in inventory","color":"gray"}}],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	guard_primary = f'execute if data storage {ns}:temp editor{{primary:""}} run return run function {fn}/hub\n'
	write_static_dialog("primary_mags_dialog", "Primary Magazines", f"Select the number of magazines ({COST_PRIMARY_MAG} pt each)", ",".join(mag_actions_primary), columns=1, guard=guard_primary)

	mag_actions_secondary: list[str] = []
	for count in range(0, 6):
		trig = TRIG_SECONDARY_MAGS_BASE + count
		label = f"{count}x Magazine" if count > 0 else "No Mags (0)"
		label_color = "yellow" if count > 0 else "green"
		tooltip: str = '{text:"Free","color":"gold"}' if count == 0 else f'[{{text:"-{count * COST_SECONDARY_MAG}","color":"gold"}}, " pt"]'
		mag_actions_secondary.append(
			f'{{label:{{text:"{label}",color:"{label_color}"}},'
			f'tooltip:["",{tooltip},{{"text":"\\n{count} magazine(s) in inventory","color":"gray"}}],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	guard_secondary = f'execute if data storage {ns}:temp editor{{secondary:""}} run return run function {fn}/hub\n'
	write_static_dialog("secondary_mags_dialog", "Secondary Magazines", f"Select the number of magazines ({COST_SECONDARY_MAG} pt each)", ",".join(mag_actions_secondary), columns=1, guard=guard_secondary)

	def gen_pick_mags(prefix: str, trig_base: int, counts: range, guard: str) -> str:
		lines = ""
		for count in counts:
			lines += (
				f'execute if score @s {ns}.player.config matches {trig_base + count} run '
				f'data modify storage {ns}:temp editor.{prefix}_mag_count set value {count}\n'
			)
		return f"""
# Guard: the gun must be selected (hub grays this out, but triggers can be sent manually)
{guard}
# Snapshot, apply, commit (reverts on overflow), back to hub
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{lines}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
function {fn}/hub
"""

	write_versioned_function("multiplayer/editor/pick_primary_mags", gen_pick_mags("primary", TRIG_PRIMARY_MAGS_BASE, range(1, 6), guard_primary.strip()))
	write_versioned_function("multiplayer/editor/pick_secondary_mags", gen_pick_mags("secondary", TRIG_SECONDARY_MAGS_BASE, range(0, 6), guard_secondary.strip()))

	## ====================================================================
	## GRENADE submenus: grenade (None = remove) → camo
	## ====================================================================
	equip_dialog_actions: dict[int, str] = {}
	equip_pick_lines: dict[int, str] = {}
	for slot_num, field, trig_base in [(1, "equip_slot1", TRIG_EQUIP_SLOT1_BASE), (2, "equip_slot2", TRIG_EQUIP_SLOT2_BASE)]:
		actions: list[str] = []
		pick = ""
		for grenade_idx, (item_id, display) in enumerate(GRENADE_TYPES):
			trig = trig_base + grenade_idx
			tooltip = '{text:"Free"}' if not item_id else f'[{{text:"-{COST_GRENADE}"}}, " pt"]'
			label_color = "yellow" if item_id else "green"
			actions.append(
				f'{{label:{{text:"{display}",color:"{label_color}"}},'
				f'tooltip:{tooltip},'
				f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
			)
			pick += (
				f'execute if score @s {ns}.player.config matches {trig} run '
				f'data modify storage {ns}:temp editor merge value {{{field}:"{item_id}",{field}_name:"{display}",{field}_camo:""}}\n'
			)
		equip_dialog_actions[slot_num] = ",".join(actions)
		equip_pick_lines[slot_num] = pick

	write_static_dialog("equip_slot1_dialog", "Grenade 1", f"Choose a grenade for slot 1 ({COST_GRENADE} pt, None is free)", equip_dialog_actions[1], columns=3)
	write_static_dialog("equip_slot2_dialog", "Grenade 2", f"Choose a grenade for slot 2 ({COST_GRENADE} pt, None is free)", equip_dialog_actions[2], columns=3)

	for slot_num in (1, 2):
		write_versioned_function(f"multiplayer/editor/pick_equip_slot{slot_num}", f"""
# Snapshot, apply (None clears the slot), commit
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{equip_pick_lines[slot_num]}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
execute if score #ed_ok {ns}.data matches 0 run return run function {fn}/hub

# None → hub, otherwise pick a camo for the grenade (free)
execute if data storage {ns}:temp editor{{equip_slot{slot_num}:""}} run return run function {fn}/hub
function {fn}/show_equip{slot_num}_camo_dialog
""")

	## ====================================================================
	## PERKS submenu (toggle, recompute-based budget)
	## Selected perks are shown green with a ✔; unselected are aqua.
	## ====================================================================
	# Per-perk append lines: a selected variant and an unselected variant
	_perk_tooltip = '["",{{"text":"{desc}","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{cost}","color":"gold"}}]," pt",{{"text":"\\nClick to toggle on/off","color":"dark_gray"}}]'
	perk_button_lines = ""
	for perk_idx, (perk_id, perk_name, perk_desc, _score) in enumerate(PERKS):
		trig = TRIG_PERK_BASE + perk_idx
		tip = _perk_tooltip.format(desc=perk_desc, cost=COST_PERK)
		sel = (
			f'{{label:{{text:"\\u2714 {perk_name}",color:"green",bold:true}},'
			f'tooltip:{tip},action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
		unsel = (
			f'{{label:{{text:"{perk_name}",color:"aqua"}},'
			f'tooltip:{tip},action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
		perk_button_lines += (
			f'execute if data storage {ns}:temp editor{{perks:["{perk_id}"]}} run data modify storage {ns}:temp dialog.actions append value {sel}\n'
			f'execute unless data storage {ns}:temp editor{{perks:["{perk_id}"]}} run data modify storage {ns}:temp dialog.actions append value {unsel}\n'
		)

	write_versioned_function("multiplayer/editor/show_perks_dialog", f"""
function {fn}/recompute_points
execute store result storage {ns}:temp _pts int 1 run scoreboard players get @s {ns}.mp.edit_points
execute store result storage {ns}:temp _perk_count int 1 run data get storage {ns}:temp editor.perks

# Base dialog (no actions yet), then one button per perk (green+✔ if selected, aqua if not)
function {fn}/show_perks_dialog_base with storage {ns}:temp
{perk_button_lines}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	write_versioned_function("multiplayer/editor/show_perks_dialog_base", f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Loadout - Perks",color:"gold",bold:true}},\
body:[{{\
type:"minecraft:plain_message",\
contents:["",["",{{"text":"Points remaining"}},": "],{{"text":"$(_pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:{{text:"Toggle perks below (max {MAX_PERKS}, {COST_PERK} pt each). Selected: $(_perk_count)/{MAX_PERKS}",color:"gray"}}\
}}],\
actions:[],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}\
}}
""")

	## pick_perk - Toggle a perk on/off; re-show perks dialog
	pick_perk_dispatch = ""
	for perk_idx, (perk_id, *_) in enumerate(PERKS):
		trig = TRIG_PERK_BASE + perk_idx
		pick_perk_dispatch += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp _toggle_perk set value "{perk_id}"\n'
		)

	write_versioned_function("multiplayer/editor/pick_perk", f"""
# Store which perk was toggled
{pick_perk_dispatch}
# Toggle the selected perk (generic macro function)
function {fn}/toggle_perk with storage {ns}:temp

# Overkill changes what the secondary slot means (pistol vs primary), so toggling it
# always clears the current secondary to avoid an invalid combination
execute if data storage {ns}:temp {{_toggle_perk:"overkill"}} run function {fn}/clear_secondary

# Re-open the perks dialog to reflect updated state
function {fn}/show_perks_dialog
""")

	# Generic toggle perk (macro function using _toggle_perk)
	write_versioned_function("multiplayer/editor/toggle_perk", f"""
# Already selected → remove it (recompute refunds automatically)
$execute if data storage {ns}:temp editor{{perks:["$(_toggle_perk)"]}} run return run function {fn}/remove_perk

# Check max perks limit
execute store result score #perk_count {ns}.data run data get storage {ns}:temp editor.perks
execute if score #perk_count {ns}.data matches {MAX_PERKS}.. run return run tellraw @s [{MGS_TAG},{{"text":"Max {MAX_PERKS} perks allowed!","color":"red"}}]

# Snapshot, add, commit (reverts on overflow)
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
$data modify storage {ns}:temp editor.perks append value "$(_toggle_perk)"
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
""")

	# Generic remove perk (rebuild the list without the toggled perk)
	write_versioned_function("multiplayer/editor/remove_perk", f"""
data modify storage {ns}:temp _remove_iter set from storage {ns}:temp editor.perks
data modify storage {ns}:temp editor.perks set value []
function {fn}/rebuild_perks with storage {ns}:temp
""")
	write_versioned_function("multiplayer/editor/rebuild_perks", f"""
execute unless data storage {ns}:temp _remove_iter[0] run return 0
data modify storage {ns}:temp _perk_val set from storage {ns}:temp _remove_iter[0]
data remove storage {ns}:temp _remove_iter[0]
$execute unless data storage {ns}:temp {{_perk_val:"$(_toggle_perk)"}} run data modify storage {ns}:temp editor.perks append from storage {ns}:temp _perk_val
function {fn}/rebuild_perks with storage {ns}:temp
""")

	## ====================================================================
	## SAVE — build the loadout entry from the editor state
	## ====================================================================
	# Pre-generate weapon slot lookup tables
	primary_slot_entries: list[str] = []
	for gun_id, _display, _category, mag_id, mag_count, *_ in PRIMARY_WEAPONS:
		gun_slot = f'{{slot:"hotbar.0",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}'
		is_consumable = "1b" if mag_id in CONSUMABLE_MAGS else "0b"
		bullets = mag_count if mag_id in CONSUMABLE_MAGS else 0
		primary_slot_entries.append(
			f'{{id:"{gun_id}",gun_slot:{gun_slot},mag_id:"{mag_id}",mag_consumable:{is_consumable},mag_bullets:{bullets}}}'
		)
	secondary_slot_entries: list[str] = []
	for gun_id, _display, mag_id, mag_count, _il in (w for w in SECONDARY_WEAPONS if w[4]):
		gun_slot = f'{{slot:"hotbar.1",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}'
		is_consumable = "1b" if mag_id in CONSUMABLE_MAGS else "0b"
		bullets = mag_count if mag_id in CONSUMABLE_MAGS else 0
		secondary_slot_entries.append(
			f'{{id:"{gun_id}",gun_slot:{gun_slot},mag_id:"{mag_id}",mag_consumable:{is_consumable},mag_bullets:{bullets}}}'
		)

	write_load_file(f"""
# Slot lookup tables for custom loadout editor (pre-computed at build time)
data modify storage {ns}:multiplayer primary_slot_table set value [{",".join(primary_slot_entries)}]
data modify storage {ns}:multiplayer secondary_slot_table set value [{",".join(secondary_slot_entries)}]
""")

	save_primary_dispatch = ""
	for idx, (gun_id, *_) in enumerate(PRIMARY_WEAPONS):
		save_primary_dispatch += (
			f'execute if data storage {ns}:temp editor{{primary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.primary_data set from storage {ns}:multiplayer primary_slot_table[{idx}]\n'
		)
	save_secondary_dispatch = ""
	for idx, (gun_id, *_) in enumerate(w for w in SECONDARY_WEAPONS if w[4]):
		save_secondary_dispatch += (
			f'execute if data storage {ns}:temp editor{{secondary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.secondary_data set from storage {ns}:multiplayer secondary_slot_table[{idx}]\n'
		)
	# Overkill: the secondary may be a primary weapon — look it up in the primary table instead
	for idx, (gun_id, *_) in enumerate(PRIMARY_WEAPONS):
		save_secondary_dispatch += (
			f'execute if data storage {ns}:temp editor{{secondary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.secondary_data set from storage {ns}:multiplayer primary_slot_table[{idx}]\n'
		)

	equip_name_dispatch: dict[int, str] = {}
	for slot_num, field in [(1, "equip_slot1"), (2, "equip_slot2")]:
		equip_name_dispatch[slot_num] = "\n".join(
			f'execute if data storage {ns}:temp editor{{{field}:"{item_id}"}} run data modify storage {ns}:temp _new_loadout.{field}_name set value "{display}"'
			for item_id, display in GRENADE_TYPES if item_id
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
# Overkill: a primary used as secondary comes from the primary table (slot hotbar.0) — force hotbar.1
execute if data storage {ns}:temp _build.secondary_data run data modify storage {ns}:temp _build.secondary_data.gun_slot.slot set value "hotbar.1"

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
# 1. Primary weapon (hotbar.0)
data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.primary_data.gun_slot

# 2. Secondary weapon (hotbar.1) - if selected
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

	## save_replace - Editing flow: rebuild the list, swapping the original entry (by id + owner)
	## for the freshly built _new_loadout while preserving its social stats.
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
