""" The perk submenu: toggling one on or off against the remaining budget. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ..catalogs import COST_PERK, MAX_PERKS, PERKS, PICK10_TOTAL, TRIG_HUB, TRIG_PERK_BASE
from .shared import editor_fn


# Functions
def write_editor_perks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## PERKS submenu (toggle, recompute-based budget) Selected perks are shown green with a ✔; unselected are aqua.
	## Per-perk append lines: a selected variant and an unselected variant
	perk_tooltip = '["",{{"text":"{desc}","color":"gray"}},["","\\n",{{"text":"Cost"}},": "],[{{"text":"{cost}","color":"gold"}}]," pt",{{"text":"\\nClick to toggle on/off","color":"dark_gray"}}]'
	perk_button_lines = ""
	for perk_idx, p in enumerate(PERKS):
		perk_id, perk_name, perk_desc = p.perk_id, p.display_name, p.description
		trig = TRIG_PERK_BASE + perk_idx
		tip = perk_tooltip.format(desc=perk_desc, cost=COST_PERK)
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
	for perk_idx, p in enumerate(PERKS):
		perk_id = p.perk_id
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

