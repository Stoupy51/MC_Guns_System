
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .catalogs import TRIG_DELETE_BASE, TRIG_FAVORITE_BASE, TRIG_LIKE_BASE, TRIG_SELECT_BASE, TRIG_TOGGLE_VIS_BASE


def generate_browsing() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ====================================================================
	## MY LOADOUTS — Browse and manage player's own custom loadouts
	## ====================================================================

	## my_loadouts/browse — Build dialog listing player's own loadouts
	write_versioned_function("multiplayer/my_loadouts/browse",
f"""
# Initialize dialog with 3 columns: [Name/Select][👁 Toggle Vis][🗑 Delete]
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"My Loadouts",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Manage your custom loadouts.",color:"gray"}}}}],\
actions:[],\
columns:3,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}\
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

	## my_loadouts/prep_btn — Compute trigger values and route by public/private color
	write_versioned_function("multiplayer/my_loadouts/prep_btn",
f"""
# Copy entry data for macro use
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute select trigger: {TRIG_SELECT_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_SELECT_BASE}
execute store result storage {ns}:temp _btn_data.select_trig int 1 run scoreboard players get #trig {ns}.data

# Compute toggle visibility trigger: {TRIG_TOGGLE_VIS_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_TOGGLE_VIS_BASE}
execute store result storage {ns}:temp _btn_data.vis_trig int 1 run scoreboard players get #trig {ns}.data

# Compute delete trigger: {TRIG_DELETE_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_DELETE_BASE}
execute store result storage {ns}:temp _btn_data.delete_trig int 1 run scoreboard players get #trig {ns}.data

# Route to correct color variant based on public flag (green=public, red=private)
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/add_btn_public with storage {ns}:temp _btn_data
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/add_btn_private with storage {ns}:temp _btn_data
""")

	## my_loadouts/add_btn_public — Macro: green name (public loadout)
	write_versioned_function("multiplayer/my_loadouts/add_btn_public",
f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:["",{{text:"$(main_gun)",color:"green"}},{{text:" + ",color:"gray"}},{{text:"$(secondary_gun)",color:"yellow"}},"\\n",{{text:"Public",color:"green",italic:true}},"\\n\\n",{{text:"\u25b6 Click to select",color:"dark_gray",italic:true}}],action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"\U0001f441",color:"aqua"}},width:20,tooltip:["",{{text:"Toggle to ",color:"white"}},{{text:"Private",color:"red"}}],action:{{type:"run_command",command:"/trigger {ns}.player.config set $(vis_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"\U0001f5d1",color:"red"}},width:20,tooltip:{{text:"Delete this loadout",color:"red"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(delete_trig)"}}}}
""")

	## my_loadouts/add_btn_private — Macro: red name (private loadout)
	write_versioned_function("multiplayer/my_loadouts/add_btn_private",
f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"red"}},tooltip:["",{{text:"$(main_gun)",color:"green"}},{{text:" + ",color:"gray"}},{{text:"$(secondary_gun)",color:"yellow"}},"\\n",{{text:"Private",color:"red",italic:true}},"\\n\\n",{{text:"\u25b6 Click to select",color:"dark_gray",italic:true}}],action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"\U0001f441",color:"gray"}},width:20,tooltip:["",{{text:"Toggle to ",color:"white"}},{{text:"Public",color:"green"}}],action:{{type:"run_command",command:"/trigger {ns}.player.config set $(vis_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"\U0001f5d1",color:"red"}},width:20,tooltip:{{text:"Delete this loadout",color:"red"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(delete_trig)"}}}}
""")

	## ====================================================================
	## MARKETPLACE — Browse all public custom loadouts
	## ====================================================================

	## marketplace/browse — Build dialog listing all public loadouts
	write_versioned_function("multiplayer/marketplace/browse",
f"""
# Initialize dialog with 3 columns: [Name/Select][👍 Like][⭐ Favorite]
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Marketplace",color:"light_purple",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Browse public loadouts from all players.",color:"gray"}}}}],\
actions:[],\
columns:3,\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}\
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

	## marketplace/prep_btn — Compute select, like, and favorite triggers
	write_versioned_function("multiplayer/marketplace/prep_btn",
f"""
# Copy entry data for macro use
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute select trigger: {TRIG_SELECT_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_SELECT_BASE}
execute store result storage {ns}:temp _btn_data.select_trig int 1 run scoreboard players get #trig {ns}.data

# Compute like trigger: {TRIG_LIKE_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_LIKE_BASE}
execute store result storage {ns}:temp _btn_data.like_trig int 1 run scoreboard players get #trig {ns}.data

# Compute favorite trigger: {TRIG_FAVORITE_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_FAVORITE_BASE}
execute store result storage {ns}:temp _btn_data.fav_trig int 1 run scoreboard players get #trig {ns}.data

# Add buttons to dialog
function {ns}:v{version}/multiplayer/marketplace/add_btn with storage {ns}:temp _btn_data
""")

	## marketplace/add_btn — Macro: append 3 buttons (Use + Like + Favorite)
	write_versioned_function("multiplayer/marketplace/add_btn",
f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:["",{{text:"$(main_gun)",color:"green"}},{{text:" + ",color:"gray"}},{{text:"$(secondary_gun)",color:"yellow"}},"\\n",{{text:"by $(owner_name)",color:"aqua",italic:true}},"\\n",{{text:"\u2665 $(likes) likes",color:"red"}},"\\n\\n",{{text:"\u25b6 Click to select",color:"dark_gray",italic:true}}],action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"\U0001f44d",color:"yellow"}},width:20,tooltip:{{text:"Like this loadout",color:"yellow"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(like_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"\u2b50",color:"gold"}},width:20,tooltip:{{text:"Add to favorites",color:"gold"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(fav_trig)"}}}}
""")

