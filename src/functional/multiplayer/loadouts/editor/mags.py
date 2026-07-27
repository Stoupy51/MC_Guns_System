""" The magazine-count submenus, guarded on their gun being selected. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..catalogs import COST_PRIMARY_MAG, COST_SECONDARY_MAG, TRIG_PRIMARY_MAGS_BASE, TRIG_SECONDARY_MAGS_BASE
from .shared import editor_fn, write_static_dialog


# Functions
def write_editor_mags() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## MAGAZINE submenus (guarded: their gun must be selected)
	mag_actions_primary: list[str] = []
	for count in range(1, 6):
		trig = TRIG_PRIMARY_MAGS_BASE + count
		mag_actions_primary.append(
			f'{{label:{{text:"{count}x Magazine",color:"yellow"}},'
			f'tooltip:["",{{"text":"-{count * COST_PRIMARY_MAG}","color":"gold"}}," ",{{"text":"pt","color":"gold"}},{{"text":"\\n{count} magazine(s) in inventory","color":"gray"}}],'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	guard_primary = f'execute if data storage {ns}:temp editor{{primary:""}} run return run function {fn}/hub\n'
	write_static_dialog(ns, version, "primary_mags_dialog", "Primary Magazines", f"Select the number of magazines ({COST_PRIMARY_MAG} pt each)", ",".join(mag_actions_primary), columns=1, guard=guard_primary)

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
	write_static_dialog(ns, version, "secondary_mags_dialog", "Secondary Magazines", f"Select the number of magazines ({COST_SECONDARY_MAG} pt each)", ",".join(mag_actions_secondary), columns=1, guard=guard_secondary)

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

