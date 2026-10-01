""" The primary, secondary and Overkill gun submenus, and removing a picked gun. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import (
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
	SecondaryWeapon,
	Weapon,
)
from .shared import editor_fn, write_static_dialog


# Functions
def write_editor_weapons() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## Weapon submenus: gun (or remove), then scope, then camo.

	primaries: list[Weapon] = [w for w in PRIMARY_WEAPONS if w.in_loadout]
	secondaries: list[SecondaryWeapon] = [w for w in SECONDARY_WEAPONS if w.in_loadout]
	primary_actions: list[str] = [
		gun_button(ns, wp.display_name, wp.category, COST_PRIMARY_WEAPON, TRIG_PRIMARY_BASE + idx) for idx, wp in enumerate(primaries)
	]
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

	# Pistols, the default secondary list.
	secondary_actions: list[str] = [
		*(gun_button(ns, wp.display_name, "Pistol", COST_SECONDARY_WEAPON, TRIG_SECONDARY_BASE + idx) for idx, wp in enumerate(secondaries)),
		remove_secondary_btn,
	]
	write_static_dialog(ns, version, "secondary_pistol_dialog", "Secondary Weapon", f"Choose your secondary weapon ({COST_SECONDARY_WEAPON} pt + {COST_SECONDARY_MAG} pt per magazine)", ",".join(secondary_actions))

	# Overkill: primaries as secondary (iron sights, camo selectable).
	overkill_actions: list[str] = [
		*(gun_button(ns, wp.display_name, wp.category, COST_SECONDARY_WEAPON, TRIG_OVERKILL_SEC_BASE + idx) for idx, wp in enumerate(primaries)),
		remove_secondary_btn,
	]
	write_static_dialog(ns, version, "secondary_overkill_dialog", "Overkill Secondary", f"Choose a second primary ({COST_SECONDARY_WEAPON} pt + {COST_SECONDARY_MAG} pt per magazine)", ",".join(overkill_actions))

	# Overkill holders pick a primary, everyone else a pistol.
	write_versioned_function("multiplayer/editor/show_secondary_dialog", f"""
execute if data storage {ns}:temp editor{{perks:["overkill"]}} run return run function {fn}/show_secondary_overkill_dialog
function {fn}/show_secondary_pistol_dialog
""")

	# Gun pick: snapshot, merge the gun (scope and camo reset), commit, then scope or camo, or back to the hub on failure.
	scope_set_func: dict[tuple[str, ...], str] = {
		("", "_1", "_2", "_3", "_4"): "show_scope_primary_full",
		("", "_1", "_2", "_3"):       "show_scope_primary_no4",
		("", "_1"):                   "show_scope_primary_1only",
	}
	scope_route_lines: str = "".join(
		f'execute if data storage {ns}:temp editor{{primary:"{wp.item_id}"}} run '
		f'return run function {fn}/{scope_set_func[SCOPE_VARIANTS[wp.item_id]]}\n'
		for wp in PRIMARY_WEAPONS if wp.item_id in SCOPE_VARIANTS
	)
	pick_primary_lines: str = "".join(pick_gun_line(ns, "primary", TRIG_PRIMARY_BASE + idx, wp, mag_count=1) for idx, wp in enumerate(primaries))

	write_versioned_function("multiplayer/editor/pick_primary", f"""
# Scope and camo reset, 1 magazine.
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{pick_primary_lines}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
execute if score #ed_ok {ns}.data matches 0 run return run function {fn}/hub

# Scope dialog for guns with variants, camo otherwise.
{scope_route_lines}
function {fn}/show_primary_camo_dialog
""")

	pick_secondary_lines: str = "".join(pick_gun_line(ns, "secondary", TRIG_SECONDARY_BASE + idx, wp, mag_count=0) for idx, wp in enumerate(secondaries))
	secondary_scope_route = (
		f'execute if data storage {ns}:temp editor{{secondary:"deagle"}} run '
		f'return run function {fn}/show_scope_secondary_4only\n'
	)

	write_versioned_function("multiplayer/editor/pick_secondary", f"""
# Scope and camo reset, no magazine.
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{pick_secondary_lines}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
execute if score #ed_ok {ns}.data matches 0 run return run function {fn}/hub

# Scope dialog for guns with variants, camo otherwise.
{secondary_scope_route}
function {fn}/show_secondary_camo_dialog
""")

	# Overkill: a primary as the secondary (iron sights, camo selectable).
	pick_overkill_lines: str = "".join(pick_gun_line(ns, "secondary", TRIG_OVERKILL_SEC_BASE + idx, wp, mag_count=0) for idx, wp in enumerate(primaries))

	write_versioned_function("multiplayer/editor/pick_overkill_secondary", f"""
# Overkill is checked here, not only in the dialog router: a trigger can reach this function without it
# (a trigger-range overlap once did, see TRIG_KNIFE_CAMO_BASE).
execute unless data storage {ns}:temp editor{{perks:["overkill"]}} run return run function {fn}/hub

# The chosen primary becomes the secondary, with no magazine.
data modify storage {ns}:temp _ed_bak set from storage {ns}:temp editor
{pick_overkill_lines}
execute store success score #ed_ok {ns}.data run function {fn}/commit_check
execute if score #ed_ok {ns}.data matches 0 run return run function {fn}/hub

# Iron sights only, so straight to camo.
function {fn}/show_secondary_camo_dialog
""")

	# No navigation; shared by remove and the Overkill toggle.
	write_versioned_function("multiplayer/editor/clear_secondary", f"""
data modify storage {ns}:temp editor merge value {{secondary:"",secondary_name:"None",secondary_mag:"",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:""}}
""")

	# The recompute refunds automatically.
	write_versioned_function("multiplayer/editor/remove_primary", f"""
data modify storage {ns}:temp editor merge value {{primary:"",primary_name:"None",primary_mag:"",primary_mag_count:1,primary_scope:"",primary_scope_name:"Iron Sights",primary_camo:"",primary_camo_name:"Default",primary_full:""}}
function {fn}/hub
""")
	write_versioned_function("multiplayer/editor/remove_secondary", f"""
function {fn}/clear_secondary
function {fn}/hub
""")


def gun_button(ns: str, label: str, subtitle: str, cost: int, trigger: int) -> str:
	""" Dialog action picking one gun, with its subtitle and point cost in the tooltip. """
	return (
		f'{{label:{{text:"{label}",color:"yellow"}},'
		f'tooltip:["",{{"text":"{subtitle}","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{cost}","color":"gold"}}]," pt"],'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trigger}"}}}}'
	)


def pick_gun_line(ns: str, field: str, trigger: int, weapon: Weapon | SecondaryWeapon, mag_count: int) -> str:
	""" Line merging a picked gun into the editor's `field` slot when the trigger matches, resetting its scope and camo.

	Args:
		field: `primary` or `secondary`, the prefix of every editor field written.
	"""
	return (
		f'execute if score @s {ns}.player.config matches {trigger} run '
		f'data modify storage {ns}:temp editor merge value '
		f'{{{field}:"{weapon.item_id}",{field}_name:"{weapon.display_name}",{field}_mag:"{weapon.magazine_id}",{field}_mag_count:{mag_count},'
		f'{field}_scope:"",{field}_scope_name:"Iron Sights",{field}_camo:"",{field}_camo_name:"Default",{field}_full:"{weapon.item_id}"}}\n'
	)

