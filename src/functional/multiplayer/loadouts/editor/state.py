""" Per-player editor state, the Pick-10 budget recompute and the snapshot/commit pattern. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ..catalogs import COST_GRENADE, COST_PERK, COST_PRIMARY_MAG, COST_PRIMARY_SCOPE, COST_PRIMARY_WEAPON, COST_SECONDARY_MAG, COST_SECONDARY_SCOPE, COST_SECONDARY_WEAPON, PICK10_TOTAL
from .shared import editor_fn, empty_state


# Functions
def write_editor_state() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## ==================================================================== Per-player editor state isolation Editor state is stored in {ns}:editor.{pid} (one per player).
	## At dispatch start, we load to {ns}:temp editor; at end, save back.
	write_versioned_function("multiplayer/editor/load_state", f"""
# Initialize this player's slot first: if the copy failed (first interaction), {ns}:temp editor
# would otherwise keep another player's in-progress state
$execute unless data storage {ns}:editor "$(_pid)" run data modify storage {ns}:editor "$(_pid)" set value {{}}
$data modify storage {ns}:temp editor set from storage {ns}:editor "$(_pid)"
""")
	write_versioned_function("multiplayer/editor/save_state", f"""
$data modify storage {ns}:editor "$(_pid)" set from storage {ns}:temp editor
""")

	## State init, budget recompute, and the snapshot/commit pattern
	write_versioned_function("multiplayer/editor/init_state", f"""
data modify storage {ns}:temp editor set value {empty_state()}
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
	# Perks: data get on a LIST cannot take a scale (throws "not a number", silently costing 0 points and letting players overspend the budget) — get the count, then multiply by the cost constant.
	recompute_lines += [
		f"execute store result score #lc_t {ns}.data run data get storage {ns}:temp editor.perks",
		f"scoreboard players operation #lc_t {ns}.data *= #{COST_PERK} {ns}.data",
		f"scoreboard players operation #lc_cost {ns}.data += #lc_t {ns}.data",
		f"scoreboard players set @s {ns}.mp.edit_points {PICK10_TOTAL}",
		f"scoreboard players operation @s {ns}.mp.edit_points -= #lc_cost {ns}.data",
		# Mirrored into storage here so every submenu can hand it straight to show_static_dialog
		f"execute store result storage {ns}:temp _dlg.pts int 1 run scoreboard players get @s {ns}.mp.edit_points",
	]
	write_versioned_function("multiplayer/editor/recompute_points", "\n".join(recompute_lines))

	## Commit check: callers snapshot {ns}:temp editor into {ns}:temp _ed_bak before mutating, then `execute store success score #ed_ok ... run function .../commit_check`.
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

