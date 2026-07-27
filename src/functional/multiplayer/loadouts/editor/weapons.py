""" The primary, secondary and Overkill gun submenus, and removing a picked gun. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..catalogs import (
	COST_PRIMARY_MAG,
	COST_PRIMARY_WEAPON,
	COST_SECONDARY_MAG,
	COST_SECONDARY_WEAPON,
	PRIMARY_WEAPONS,
	SCOPE_VARIANTS,
	SECONDARY_WEAPONS,
	TRIG_OVERKILL_SEC_BASE,
	TRIG_PRIMARY_BASE,
	TRIG_REMOVE_PRIMARY,
	TRIG_REMOVE_SECONDARY,
	TRIG_SECONDARY_BASE,
)
from .shared import editor_fn, write_static_dialog


# Functions
def write_editor_weapons() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## PRIMARY / SECONDARY weapon submenus: gun (or remove) → scope → camo

	# Gun action lists (+ Remove button)
	primary_actions: list[str] = []
	for idx, wp in enumerate(w for w in PRIMARY_WEAPONS if w.in_loadout):
		display, category = wp.display_name, wp.category
		trig = TRIG_PRIMARY_BASE + idx
		primary_actions.append(
			f'{{label:{{text:"{display}",color:"yellow"}},'
			f'tooltip:["",{{"text":"{category}","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{COST_PRIMARY_WEAPON}","color":"gold"}}]," pt"],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	primary_actions.append(
		f'{{label:["","\\ud83d\\uddd1 ",{{text:"Remove Primary",color:"red"}}],'
		f'tooltip:{{text:"Clear the primary weapon (refunds its points)"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_REMOVE_PRIMARY}"}}}}'
	)
	write_static_dialog(ns, version, "primary_dialog", "Primary Weapon", f"Choose your primary weapon ({COST_PRIMARY_WEAPON} pt + {COST_PRIMARY_MAG} pt per magazine)", ",".join(primary_actions))

	remove_secondary_btn = (
		f'{{label:["","\\ud83d\\uddd1 ",{{text:"Remove Secondary",color:"red"}}],'
		f'tooltip:{{text:"Clear the secondary weapon (refunds its points)"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_REMOVE_SECONDARY}"}}}}'
	)

	# Pistol secondary list (default)
	secondary_actions: list[str] = []
	for idx, wp in enumerate(w for w in SECONDARY_WEAPONS if w.in_loadout):
		display = wp.display_name
		trig = TRIG_SECONDARY_BASE + idx
		secondary_actions.append(
			f'{{label:{{text:"{display}",color:"yellow"}},'
			f'tooltip:["",{{"text":"Pistol","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{COST_SECONDARY_WEAPON}","color":"gold"}}]," pt"],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	secondary_actions.append(remove_secondary_btn)
	write_static_dialog(ns, version, "secondary_pistol_dialog", "Secondary Weapon", f"Choose your secondary weapon ({COST_SECONDARY_WEAPON} pt + {COST_SECONDARY_MAG} pt per magazine)", ",".join(secondary_actions))

	# Overkill secondary list: primaries (iron sights only, camo selectable)
	overkill_actions: list[str] = []
	for idx, wp in enumerate(w for w in PRIMARY_WEAPONS if w.in_loadout):
		display, category = wp.display_name, wp.category
		trig = TRIG_OVERKILL_SEC_BASE + idx
		overkill_actions.append(
			f'{{label:{{text:"{display}",color:"yellow"}},'
			f'tooltip:["",{{"text":"{category}","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{COST_SECONDARY_WEAPON}","color":"gold"}}]," pt"],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	overkill_actions.append(remove_secondary_btn)
	write_static_dialog(ns, version, "secondary_overkill_dialog", "Overkill Secondary", f"Choose a second primary ({COST_SECONDARY_WEAPON} pt + {COST_SECONDARY_MAG} pt per magazine)", ",".join(overkill_actions))

	# Router: Overkill holders pick a primary as their secondary, everyone else picks a pistol
	write_versioned_function("multiplayer/editor/show_secondary_dialog", f"""
execute if data storage {ns}:temp editor{{perks:["overkill"]}} run return run function {fn}/show_secondary_overkill_dialog
function {fn}/show_secondary_pistol_dialog
""")

	# Gun pick handlers: snapshot → merge gun fields (resets scope/camo, mags to 1) → commit → on success continue to scope (if the gun has variants) or camo; on failure back to hub.
	scope_set_func: dict[tuple[str, ...], str] = {
		("", "_1", "_2", "_3", "_4"): "show_scope_primary_full",
		("", "_1", "_2", "_3"):       "show_scope_primary_no4",
		("", "_1"):                   "show_scope_primary_1only",
	}
	scope_route_lines = ""
	for wp in PRIMARY_WEAPONS:
		gun_id = wp.item_id
		if gun_id in SCOPE_VARIANTS:
			variants = SCOPE_VARIANTS[gun_id]
			func_name = scope_set_func[variants]
			scope_route_lines += (
				f'execute if data storage {ns}:temp editor{{primary:"{gun_id}"}} run '
				f'return run function {fn}/{func_name}\n'
			)

	pick_primary_lines = ""
	for idx, wp in enumerate(w for w in PRIMARY_WEAPONS if w.in_loadout):
		gun_id, display, mag_id = wp.item_id, wp.display_name, wp.magazine_id
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
	for idx, wp in enumerate(w for w in SECONDARY_WEAPONS if w.in_loadout):
		gun_id, display, mag_id = wp.item_id, wp.display_name, wp.magazine_id
		trig = TRIG_SECONDARY_BASE + idx
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor merge value '
			f'{{secondary:"{gun_id}",secondary_name:"{display}",secondary_mag:"{mag_id}",secondary_mag_count:0,'
			f'secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"{gun_id}"}}\n'
		)
	secondary_scope_route = (
		f'execute if data storage {ns}:temp editor{{secondary:"deagle"}} run '
		f'return run function {fn}/show_scope_secondary_4only\n'
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
	for idx, wp in enumerate(w for w in PRIMARY_WEAPONS if w.in_loadout):
		gun_id, display, mag_id = wp.item_id, wp.display_name, wp.magazine_id
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

