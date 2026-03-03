
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .catalogs import TRIG_DELETE_BASE, TRIG_SELECT_BASE


def generate_browsing() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ====================================================================
	## MY LOADOUTS — Browse and manage player's own custom loadouts
	## ====================================================================

	## my_loadouts/browse — Build dialog listing player's own loadouts
	write_versioned_function("multiplayer/my_loadouts/browse",
f"""
# Initialize dialog with 2 columns: [Use][Delete] per loadout
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"My Loadouts",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Select a loadout to use, or delete it.",color:"gray"}}}}],\
actions:[],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Back"}}\
}}

# Copy all loadouts for iteration
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts

# Build list recursively (filtered by owner_pid via score comparison)
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## my_loadouts/build_list — Recursive: filter by owner_pid using score comparison
	write_versioned_function("multiplayer/my_loadouts/build_list",
f"""
# Check if this loadout belongs to the player (score-based PID comparison)
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn

# Next entry
data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list
""")

	## my_loadouts/prep_btn — Compute trigger values from loadout ID
	write_versioned_function("multiplayer/my_loadouts/prep_btn",
f"""
# Copy entry data for macro use
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute select trigger: {TRIG_SELECT_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_SELECT_BASE}
execute store result storage {ns}:temp _btn_data.select_trig int 1 run scoreboard players get #trig {ns}.data

# Compute delete trigger: {TRIG_DELETE_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_DELETE_BASE}
execute store result storage {ns}:temp _btn_data.delete_trig int 1 run scoreboard players get #trig {ns}.data

# Add buttons to dialog
function {ns}:v{version}/multiplayer/my_loadouts/add_btn with storage {ns}:temp _btn_data
""")

	## my_loadouts/add_btn — Macro: append 2 action buttons (Use + Delete)
	write_versioned_function("multiplayer/my_loadouts/add_btn",
f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:{{text:"Main: $(main_gun) | Secondary: $(secondary_gun)\\nClick to use this loadout"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Delete",color:"red"}},tooltip:{{text:"Delete: $(name)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(delete_trig)"}}}}
""")

	## ====================================================================
	## MARKETPLACE — Browse all public custom loadouts
	## ====================================================================

	## marketplace/browse — Build dialog listing all public loadouts
	write_versioned_function("multiplayer/marketplace/browse",
f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Marketplace",color:"light_purple",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Browse public loadouts from all players.",color:"gray"}}}}],\
actions:[],\
columns:1,\
after_action:"close",\
exit_action:{{label:"Back"}}\
}}

# Copy all loadouts for iteration
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts

# Build list recursively (filtered by public:1b)
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## marketplace/build_list — Recursive: filter by public flag, add buttons
	write_versioned_function("multiplayer/marketplace/build_list",
f"""
# If this loadout is public, add a button for it (score-based check)
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

# Next entry
data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list
""")

	## marketplace/prep_btn — Compute select trigger
	write_versioned_function("multiplayer/marketplace/prep_btn",
f"""
# Copy entry data for macro use
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute select trigger: {TRIG_SELECT_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_SELECT_BASE}
execute store result storage {ns}:temp _btn_data.select_trig int 1 run scoreboard players get #trig {ns}.data

# Add button to dialog
function {ns}:v{version}/multiplayer/marketplace/add_btn with storage {ns}:temp _btn_data
""")

	## marketplace/add_btn — Macro: append select button for marketplace entry
	write_versioned_function("multiplayer/marketplace/add_btn",
f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:{{text:"Main: $(main_gun) | Secondary: $(secondary_gun)\\nLikes: $(likes)\\nClick to use this loadout"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
""")
