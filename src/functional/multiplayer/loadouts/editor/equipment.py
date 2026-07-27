""" The two grenade submenus, where None clears the slot. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..catalogs import COST_GRENADE, GRENADE_TYPES, TRIG_EQUIP_SLOT1_BASE, TRIG_EQUIP_SLOT2_BASE
from .shared import editor_fn, write_static_dialog


# Functions
def write_editor_equipment() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## ==================================================================== GRENADE submenus: grenade (None = remove) → camo.
	equip_dialog_actions: dict[int, str] = {}
	equip_pick_lines: dict[int, str] = {}
	for slot_num, field, trig_base in [(1, "equip_slot1", TRIG_EQUIP_SLOT1_BASE), (2, "equip_slot2", TRIG_EQUIP_SLOT2_BASE)]:
		actions: list[str] = []
		pick = ""
		for grenade_idx, g in enumerate(GRENADE_TYPES):
			item_id, display = g.item_id, g.display_name
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

	write_static_dialog(ns, version, "equip_slot1_dialog", "Grenade 1", f"Choose a grenade for slot 1 ({COST_GRENADE} pt, None is free)", equip_dialog_actions[1], columns=3)
	write_static_dialog(ns, version, "equip_slot2_dialog", "Grenade 2", f"Choose a grenade for slot 2 ({COST_GRENADE} pt, None is free)", equip_dialog_actions[2], columns=3)

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

