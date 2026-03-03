
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ..classes import CLASS_IDS
from .catalogs import TRIG_EDITOR_START, TRIG_MARKETPLACE, TRIG_MY_LOADOUTS


def generate_class_selection() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Scoreboards for class selection
	## ============================
	write_load_file(
f"""
# Class selection scoreboard (1-10 = class id, 0 = none)
scoreboard objectives add {ns}.mp.class dummy

# Death detection for respawn
scoreboard objectives add {ns}.mp.death_count deathCount
""")

	## ============================
	## show_dialog macro: passes inline SNBT dialog to /dialog show
	## ============================
	write_versioned_function("multiplayer/show_dialog", "$dialog show @s $(dialog)")

	## ============================
	## build_class_btn: recursive — appends one action entry per class to the dialog
	## ============================
	write_versioned_function("multiplayer/build_class_btn",
f"""
# Build tooltip from current class
$data modify storage {ns}:temp _btn set value {{label:{{text:"$(name)",color:"green"}},tooltip:{{text:"$(lore)\\nMain: $(main_gun)\\nSecondary: $(secondary_gun)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(trigger_value)"}}}}

# Append to dialog actions
data modify storage {ns}:temp dialog.actions append from storage {ns}:temp _btn

# Remove processed class and recurse
data remove storage {ns}:temp class_iter[0]
execute if data storage {ns}:temp class_iter[0] run function {ns}:v{version}/multiplayer/build_class_btn with storage {ns}:temp class_iter[0]
""")

	## ============================
	## select_class: builds the class selection dialog dynamically and shows it
	## ============================
	write_versioned_function("multiplayer/select_class",
f"""
# Initialize dialog structure
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:{{text:"Select Your Class",color:"gold",bold:true}},body:[{{type:"minecraft:plain_message",contents:{{text:"Choose a class for multiplayer.",color:"gray"}}}}],actions:[],columns:2,after_action:"close",exit_action:{{label:"Cancel"}}}}

# Copy class list for iteration
data modify storage {ns}:temp class_iter set from storage {ns}:multiplayer classes_list

# Build dialog actions recursively (passes first class data as macro args)
execute if data storage {ns}:temp class_iter[0] run function {ns}:v{version}/multiplayer/build_class_btn with storage {ns}:temp class_iter[0]

# Append custom loadout buttons
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"✚ Create Loadout",color:"aqua",bold:true}},tooltip:{{text:"Build a custom loadout from scratch"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_EDITOR_START}"}}}}
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"📦 My Loadouts",color:"yellow",bold:true}},tooltip:{{text:"Manage your custom loadouts"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS}"}}}}
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"🌍 Marketplace",color:"light_purple",bold:true}},tooltip:{{text:"Browse public loadouts from other players"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE}"}}}}

# Show the completed dialog via macro
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## set_class macro: sets the class score and notifies player
	## Called from trigger dispatch (trigger values 11-20 → class 1-10)
	## ============================
	apply_now: str = f"""{{"text":" [✔]","color":"gold","hover_event":{{"action":"show_text","value":{{"text":"Click here to apply immediately (OP only)","color":"yellow"}}}},"click_event":{{"action":"run_command","command":"/function {ns}:v{version}/multiplayer/apply_class"}}}}"""
	write_versioned_function("multiplayer/set_class",
f"""
$scoreboard players set @s {ns}.mp.class $(class_num)

# If game active: queue for next respawn
$execute if data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Class set to ","color":"white"}},{{"text":"$(class_name)","color":"green","bold":true}},{{"text":" — will apply on respawn","color":"yellow"}},{apply_now}]

# If game not active: only save choice (no loadout outside multiplayer)
$execute unless data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Class set to ","color":"white"}},{{"text":"$(class_name)","color":"green","bold":true}},{apply_now}]
""")

	## ============================
	## apply_class: looks up class by score from storage, copies to temp, applies dynamically
	## ============================
	# We need to map class_num (score) to an entry in classes_list.
	# Since classes_list is ordered and 1-indexed via class_num, index = class_num - 1.
	# We use a helper that copies the correct class to temp using indexed access.
	apply_commands: str = f"""
# Check for custom loadout (negative mp.class = custom loadout ID)
execute if score @s {ns}.mp.class matches ..-1 run return run function {ns}:v{version}/multiplayer/apply_custom_class

# Standard class lookup by class_num score
"""
	for class_num in CLASS_IDS.values():
		apply_commands += f"execute if score @s {ns}.mp.class matches {class_num} run data modify storage {ns}:temp current_class set from storage {ns}:multiplayer classes_list[{class_num - 1}]\n"

	apply_commands += f"""
# Apply the loadout dynamically from the selected class
function {ns}:v{version}/multiplayer/apply_class_dynamic
"""

	write_versioned_function("multiplayer/apply_class", apply_commands)

	## ============================
	## apply_custom_class: find custom loadout by ID stored in mp.custom_class, then apply
	## ============================
	write_versioned_function("multiplayer/apply_custom_class",
f"""
# Store target loadout ID (negate to get positive ID)
scoreboard players operation #loadout_id {ns}.data = @s {ns}.mp.class
scoreboard players operation #loadout_id {ns}.data *= #minus_one {ns}.data

# Copy loadouts list for search
data modify storage {ns}:temp _find_iter set from storage {ns}:multiplayer custom_loadouts

# Recursive search by ID (score-based comparison)
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/apply_custom_found
""")

	## apply_custom_found — Recursive: find loadout by ID and apply it
	write_versioned_function("multiplayer/apply_custom_found",
f"""
# Check if this entry's ID matches the target
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _find_iter[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run return run function {ns}:v{version}/multiplayer/apply_custom_match

# Not found yet, continue search
data remove storage {ns}:temp _find_iter[0]
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/apply_custom_found
""")

	## apply_custom_match — Apply the found loadout
	write_versioned_function("multiplayer/apply_custom_match",
f"""
# Copy found loadout's slots to the format expected by apply_class_dynamic
data modify storage {ns}:temp current_class set value {{slots:[]}}
data modify storage {ns}:temp current_class.slots set from storage {ns}:temp _find_iter[0].slots

# Apply the loadout (clears inventory and gives items)
function {ns}:v{version}/multiplayer/apply_class_dynamic
""")

	## ============================
	## On respawn (called from player tick when death detected)
	## ============================
	write_versioned_function("multiplayer/on_respawn",
f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Increment death stats
scoreboard players add @s {ns}.mp.deaths 1

# Apply current class loadout (positive = standard, negative = custom)
execute unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class
""")

	## ============================
	## auto_apply_default: apply default custom loadout on game start
	## Sets mp.class = -(mp.default) then applies
	## ============================
	write_versioned_function("multiplayer/auto_apply_default",
f"""
# Set mp.class to negative default ID (custom loadout)
scoreboard players operation @s {ns}.mp.class = @s {ns}.mp.default
scoreboard players operation @s {ns}.mp.class *= #minus_one {ns}.data

# Apply the loadout
function {ns}:v{version}/multiplayer/apply_class
""")

	## ============================
	## Player tick hooks
	## ============================
	write_versioned_function("player/tick",
f"""
# Multiplayer: detect respawn (death_count incremented by deathCount criterion)
execute if data storage {ns}:multiplayer game{{state:"active"}} if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/multiplayer/on_respawn
""")

