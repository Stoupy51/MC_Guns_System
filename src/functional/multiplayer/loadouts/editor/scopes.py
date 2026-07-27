""" The scope submenu, whose variant list depends on the gun it was opened from. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..catalogs import ALL_SCOPE_SUFFIXES, COST_PRIMARY_SCOPE, COST_SECONDARY_SCOPE, SCOPE_NAMES, TRIG_PRIMARY_SCOPE_BASE, TRIG_SECONDARY_SCOPE_BASE
from .shared import editor_fn, write_static_dialog


# Functions
def write_editor_scopes() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

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
		write_static_dialog(ns, version,
			f"scope_primary_{func_suffix}", "Primary Scope",
			f"Choose your optic (-{COST_PRIMARY_SCOPE} pt for any scope, iron sights free)",
			scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, variants, COST_PRIMARY_SCOPE),
		)
	write_static_dialog(ns, version,
		"scope_secondary_4only", "Secondary Scope",
		f"Choose your secondary optic (-{COST_SECONDARY_SCOPE} pt for scope, iron sights free)",
		scope_actions_snbt(TRIG_SECONDARY_SCOPE_BASE, ("", "_4"), COST_SECONDARY_SCOPE),
	)

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

