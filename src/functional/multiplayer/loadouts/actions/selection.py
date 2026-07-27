""" Selecting a custom loadout and deleting one you own. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ..catalogs import TRIG_DELETE_BASE, TRIG_SELECT_BASE


# Functions
def write_loadout_selection() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## CUSTOM LOADOUT ACTIONS - Select, Delete, Toggle Visibility, Set Default

	## custom/select - Store custom loadout choice (items applied on respawn/apply_class)
	write_versioned_function("multiplayer/custom/select", f"""
# Extract loadout ID from trigger value: id = trigger - {TRIG_SELECT_BASE}
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_SELECT_BASE}

# Store as active custom class (negative mp.class = custom loadout ID)
scoreboard players operation @s {ns}.mp.class = #loadout_id {ns}.data
scoreboard players operation @s {ns}.mp.class *= #minus_one {ns}.data

# Find the loadout name for notification
data modify storage {ns}:temp _find_iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/custom/find_and_notify
""")

	## custom/find_and_notify - Recursive: find loadout by ID and notify player
	write_versioned_function("multiplayer/custom/find_and_notify", f"""
# Check if this entry's ID matches the target
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _find_iter[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run return run function {ns}:v{version}/multiplayer/custom/notify_selected with storage {ns}:temp _find_iter[0]

# Not found yet, continue search
data remove storage {ns}:temp _find_iter[0]
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/custom/find_and_notify
""")

	## custom/notify_selected - Macro tellraw (same message pattern as set_class with OP apply button)
	apply_now: str = f"""{{"text":" [✔]","color":"gold","hover_event":{{"action":"show_text","value":{{"text":"Click here to apply immediately (OP only)","color":"yellow"}}}},"click_event":{{"action":"suggest_command","command":"/function {ns}:v{version}/multiplayer/apply_class"}}}}"""
	write_versioned_function("multiplayer/custom/notify_selected", f"""$tellraw @s ["",{MGS_TAG},["",{{"text":"Class set to"}}," "],{{"text":"$(name)","color":"green","bold":true}},[{{"text":"","color":"aqua"}}," (",{{"text":"custom"}},")"],{{"text":" - will apply on respawn","color":"yellow"}},{apply_now}]
""")

	## custom/delete - Verify ownership and remove loadout from list
	write_versioned_function("multiplayer/custom/delete", f"""
# Extract loadout ID from trigger value: id = trigger - {TRIG_DELETE_BASE}
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_DELETE_BASE}

# Copy the list, rebuild without the deleted entry
data modify storage {ns}:temp _del_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []

# Rebuild list, skipping the entry that matches both ID and owner (score-based)
scoreboard players set #del_removed {ns}.data 0
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/delete_filter

# Clear dangling references: if the deleted loadout was the default or active class, reset them
scoreboard players operation #del_neg_id {ns}.data = #loadout_id {ns}.data
scoreboard players operation #del_neg_id {ns}.data *= #minus_one {ns}.data
execute if score #del_removed {ns}.data matches 1 if score @s {ns}.mp.default = #loadout_id {ns}.data run scoreboard players set @s {ns}.mp.default 0
execute if score #del_removed {ns}.data matches 1 if score @s {ns}.mp.class = #del_neg_id {ns}.data run scoreboard players set @s {ns}.mp.class 0

# Notify
tellraw @s ["",{MGS_TAG},{{"text":"Loadout deleted","color":"red"}}]

# Reopen My Loadouts dialog with updated data
function {ns}:v{version}/multiplayer/my_loadouts/browse
""")

	## custom/delete_filter - Recursive: rebuild list without the target entry (score-based)
	write_versioned_function("multiplayer/custom/delete_filter", f"""
# Check if this entry matches BOTH the target ID and our PID
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _del_src[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _del_src[0].owner_pid
scoreboard players set #del_match {ns}.data 0
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run scoreboard players set #del_match {ns}.data 1
execute if score #del_match {ns}.data matches 1 run scoreboard players set #del_removed {ns}.data 1

# If NOT a delete match, keep the entry
execute unless score #del_match {ns}.data matches 1 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _del_src[0]

# Next
data remove storage {ns}:temp _del_src[0]
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/delete_filter
""")

