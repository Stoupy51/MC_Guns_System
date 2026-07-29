""" The camo submenus that finish a weapon or grenade pick and return to the hub. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..catalogs import (
	CAMO_VARIANTS,
	TRIG_EQUIP1_CAMO_BASE,
	TRIG_EQUIP2_CAMO_BASE,
	TRIG_KNIFE_CAMO_BASE,
	TRIG_PRIMARY_CAMO_BASE,
	TRIG_SECONDARY_CAMO_BASE,
)
from .shared import editor_fn, write_static_dialog


# Functions
def write_editor_camos() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## Camo dialogs (free) — finish the weapon submenu and return to the hub
	def camo_actions_snbt(trig_base: int) -> str:
		actions: list[str] = []
		for camo_idx, c in enumerate(CAMO_VARIANTS):
			suffix, camo_name = c.suffix, c.display_name
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
		("knife", "Knife Camo", TRIG_KNIFE_CAMO_BASE),
	]:
		write_static_dialog(ns, version, f"{prefix}_camo_dialog", title, "Choose your camo (free, cosmetic only)", camo_actions_snbt(trig_base))

	def gen_pick_camo_lines(field: str, trig_base: int) -> str:
		lines = ""
		for camo_idx, c in enumerate(CAMO_VARIANTS):
			suffix, camo_name = c.suffix, c.display_name
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
	# The knife needs no *_full field: it is always `combat_knife` + the camo suffix, never scoped.
	write_versioned_function("multiplayer/editor/pick_knife_camo", f"""
{gen_pick_camo_lines("knife", TRIG_KNIFE_CAMO_BASE)}
function {fn}/hub
""")

