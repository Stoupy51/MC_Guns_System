
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .classes import CLASS_IDS


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

# Show the completed dialog via macro
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## set_class macro: sets the class score and notifies player
	## Called from trigger dispatch (trigger values 11-20 → class 1-10)
	## ============================
	write_versioned_function("multiplayer/set_class",
f"""
$scoreboard players set @s {ns}.mp.class $(class_num)

# If game active: queue for next respawn
$execute if data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Class set to ","color":"white"}},{{"text":"$(class_name)","color":"green","bold":true}},{{"text":" — will apply on respawn","color":"yellow"}}]

# If game not active: only save choice (no loadout outside multiplayer)
$execute unless data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Class set to ","color":"white"}},{{"text":"$(class_name)","color":"green","bold":true}}]
""")

	## ============================
	## apply_class: looks up class by score from storage, copies to temp, applies dynamically
	## ============================
	# We need to map class_num (score) to an entry in classes_list.
	# Since classes_list is ordered and 1-indexed via class_num, index = class_num - 1.
	# We use a helper that copies the correct class to temp using indexed access.
	apply_commands: str = ""
	for class_num in CLASS_IDS.values():
		apply_commands += f"execute if score @s {ns}.mp.class matches {class_num} run data modify storage {ns}:temp current_class set from storage {ns}:multiplayer classes_list[{class_num - 1}]\n"

	apply_commands += f"""
# Apply the loadout dynamically from the selected class
function {ns}:v{version}/multiplayer/apply_class_dynamic
"""

	write_versioned_function("multiplayer/apply_class", apply_commands)

	## ============================
	## On respawn (called from player tick when death detected)
	## ============================
	write_versioned_function("multiplayer/on_respawn",
f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Increment death stats
scoreboard players add @s {ns}.mp.deaths 1

# Apply current class loadout
execute if score @s {ns}.mp.class matches 1.. run function {ns}:v{version}/multiplayer/apply_class
""")

	## ============================
	## Player tick hooks
	## ============================
	write_versioned_function("player/tick",
f"""
# Multiplayer: detect respawn (death_count incremented by deathCount criterion)
execute if data storage {ns}:multiplayer game{{state:"active"}} if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/multiplayer/on_respawn
""")

