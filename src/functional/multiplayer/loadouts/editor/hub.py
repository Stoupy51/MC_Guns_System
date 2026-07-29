""" The main loadout page: one row per category plus the save buttons. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..catalogs import (
	COST_GRENADE,
	COST_PERK,
	COST_PRIMARY_MAG,
	COST_SECONDARY_MAG,
	MAX_PERKS,
	PICK10_TOTAL,
	TRIG_HUB,
	TRIG_HUB_EQUIP1,
	TRIG_HUB_EQUIP2,
	TRIG_HUB_KNIFE,
	TRIG_HUB_PERKS,
	TRIG_HUB_PRIMARY,
	TRIG_HUB_PRIMARY_MAGS,
	TRIG_HUB_SECONDARY,
	TRIG_HUB_SECONDARY_MAGS,
	TRIG_SAVE_PRIVATE,
	TRIG_SAVE_PUBLIC,
)
from .shared import editor_fn


# Functions
def write_editor_hub() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## ==================================================================== HUB — the main loadout page (CoD-style).

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
contents:["",["",{{"text":"Points used"}},": "],{{"text":"$(used)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}},{{"text":" ($(pts) left)","color":"gray"}}]\
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
	def row(trig: int, label_snbt: str, tooltip_snbt: str) -> str:
		return (
			f'$data modify storage {ns}:temp dialog.actions append value '
			f'{{label:{label_snbt},tooltip:{tooltip_snbt},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)

	write_versioned_function("multiplayer/editor/hub_row_primary", row(
		TRIG_HUB_PRIMARY,
		'["",{text:"\\ud83d\\udd2b "},{text:"Primary: ",color:"white"},{text:"$(primary_name)",color:"green"}]',
		'{text:"$(primary_scope_name), $(primary_camo_name)\\nClick to change",color:"gray"}',
	))
	write_versioned_function("multiplayer/editor/hub_row_primary_mags", row(
		TRIG_HUB_PRIMARY_MAGS,
		'["",{text:"\\ud83d\\udce6 "},{text:"Primary Mags: ",color:"white"},{text:"$(primary_mag_count)x",color:"green"}]',
		f'{{text:"{COST_PRIMARY_MAG} pt per magazine",color:"gray"}}',
	))
	write_versioned_function("multiplayer/editor/hub_row_secondary", row(
		TRIG_HUB_SECONDARY,
		'["",{text:"\\ud83d\\udd2b "},{text:"Secondary: ",color:"white"},{text:"$(secondary_name)",color:"green"}]',
		'{text:"$(secondary_scope_name), $(secondary_camo_name)\\nClick to change",color:"gray"}',
	))
	write_versioned_function("multiplayer/editor/hub_row_secondary_mags", row(
		TRIG_HUB_SECONDARY_MAGS,
		'["",{text:"\\ud83d\\udce6 "},{text:"Secondary Mags: ",color:"white"},{text:"$(secondary_mag_count)x",color:"green"}]',
		f'{{text:"{COST_SECONDARY_MAG} pt per magazine",color:"gray"}}',
	))
	# Knife: camo only, and free — every loadout carries it, so there is nothing else to choose.
	write_versioned_function("multiplayer/editor/hub_row_knife", row(
		TRIG_HUB_KNIFE,
		'["",{text:"\\ud83d\\udd2a "},{text:"Knife: ",color:"white"},{text:"$(knife_camo_name)",color:"green"}]',
		'{text:"Free, cosmetic only\\nClick to change",color:"gray"}',
	))
	write_versioned_function("multiplayer/editor/hub_row_equip1", row(
		TRIG_HUB_EQUIP1,
		'["",{text:"\\ud83d\\udca3 "},{text:"Grenade 1: ",color:"white"},{text:"$(equip_slot1_name)",color:"green"}]',
		f'{{text:"{COST_GRENADE} pt\\nClick to change",color:"gray"}}',
	))
	write_versioned_function("multiplayer/editor/hub_row_equip2", row(
		TRIG_HUB_EQUIP2,
		'["",{text:"\\ud83d\\udca3 "},{text:"Grenade 2: ",color:"white"},{text:"$(equip_slot2_name)",color:"green"}]',
		f'{{text:"{COST_GRENADE} pt\\nClick to change",color:"gray"}}',
	))
	write_versioned_function("multiplayer/editor/hub_row_perks", row(
		TRIG_HUB_PERKS,
		f'["",{{text:"\\u2b50 "}},{{text:"Perks: ",color:"white"}},{{text:"$(perks)/{MAX_PERKS}",color:"green"}}]',
		f'{{text:"{COST_PERK} pt per perk",color:"gray"}}',
	))

	# Static hub buttons
	unavailable_mags_primary = (
		f'{{label:["","\\ud83d\\udce6 ",{{text:"Primary Mags \\u2014 Unavailable",color:"dark_gray"}}],'
		f'tooltip:{{text:"Pick a primary weapon first",color:"red"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}'
	)
	unavailable_mags_secondary = (
		f'{{label:["","\\ud83d\\udce6 ",{{text:"Secondary Mags \\u2014 Unavailable",color:"dark_gray"}}],'
		f'tooltip:{{text:"Pick a secondary weapon first",color:"red"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}'
	)
	save_public_btn = (
		f'{{label:["","\\ud83d\\udcbe ",{{text:"Save as Public",color:"green",bold:true}}],'
		f'tooltip:{{text:"Everyone can see and use this loadout"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PUBLIC}"}}}}'
	)
	save_private_btn = (
		f'{{label:["","\\ud83d\\udcbe ",{{text:"Save as Private",color:"yellow",bold:true}}],'
		f'tooltip:{{text:"Only you can see and use this loadout"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PRIVATE}"}}}}'
	)
	unavailable_save = (
		f'{{label:["","\\ud83d\\udcbe ",{{text:"Save \\u2014 Unavailable",color:"dark_gray"}}],'
		f'tooltip:{{text:"A primary weapon is required",color:"red"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}'
	)

	write_versioned_function("multiplayer/editor/hub", f"""
# Backfill fields added after a state was stored: in-progress states in {ns}:editor and the
# editor_state embedded in older saved loadouts predate the knife row, and hub_row_knife is a
# macro — a missing $(knife_camo_name) would fail the whole row.
execute unless data storage {ns}:temp editor.knife_camo run data modify storage {ns}:temp editor.knife_camo set value ""
execute unless data storage {ns}:temp editor.knife_camo_name run data modify storage {ns}:temp editor.knife_camo_name set value "Default"

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
execute if data storage {ns}:temp editor{{primary:""}} run data modify storage {ns}:temp dialog.actions append value {unavailable_mags_primary}
execute unless data storage {ns}:temp editor{{primary:""}} run function {fn}/hub_row_primary_mags with storage {ns}:temp editor
function {fn}/hub_row_secondary with storage {ns}:temp editor
execute if data storage {ns}:temp editor{{secondary:""}} run data modify storage {ns}:temp dialog.actions append value {unavailable_mags_secondary}
execute unless data storage {ns}:temp editor{{secondary:""}} run function {fn}/hub_row_secondary_mags with storage {ns}:temp editor
function {fn}/hub_row_knife with storage {ns}:temp editor
function {fn}/hub_row_equip1 with storage {ns}:temp editor
function {fn}/hub_row_equip2 with storage {ns}:temp editor
function {fn}/hub_row_perks with storage {ns}:temp _hub

# Save buttons (grayed out until a primary weapon is selected)
execute if data storage {ns}:temp editor{{primary:""}} run data modify storage {ns}:temp dialog.actions append value {unavailable_save}
execute unless data storage {ns}:temp editor{{primary:""}} run data modify storage {ns}:temp dialog.actions append value {save_public_btn}
execute unless data storage {ns}:temp editor{{primary:""}} run data modify storage {ns}:temp dialog.actions append value {save_private_btn}

# Show
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

