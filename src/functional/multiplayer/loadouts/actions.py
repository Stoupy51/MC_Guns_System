
# Imports
from stewbeet import Mem, write_versioned_function

from .catalogs import (
	TRIG_DELETE_BASE,
	TRIG_FAVORITE_BASE,
	TRIG_LIKE_BASE,
	TRIG_SELECT_BASE,
	TRIG_SET_DEFAULT_BASE,
	TRIG_TOGGLE_VIS_BASE,
)


def generate_actions() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ====================================================================
	## CUSTOM LOADOUT ACTIONS — Select, Delete, Toggle Visibility, Set Default
	## ====================================================================

	## custom/select — Find loadout by ID and apply it
	write_versioned_function("multiplayer/custom/select",
f"""
# Extract loadout ID from trigger value: id = trigger - {TRIG_SELECT_BASE}
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_SELECT_BASE}

# Copy loadouts list for search
data modify storage {ns}:temp _find_iter set from storage {ns}:multiplayer custom_loadouts

# Recursive search by ID (score-based comparison)
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/custom/find_and_apply
""")

	## custom/find_and_apply — Recursive: find loadout by ID and apply it (score-based)
	write_versioned_function("multiplayer/custom/find_and_apply",
f"""
# Check if this entry's ID matches the target
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _find_iter[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run return run function {ns}:v{version}/multiplayer/custom/apply_found

# Not found yet, continue search
data remove storage {ns}:temp _find_iter[0]
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/custom/find_and_apply
""")

	## custom/apply_found — Apply the found loadout
	write_versioned_function("multiplayer/custom/apply_found",
f"""
# Copy found loadout's slots to the format expected by apply_class_dynamic
data modify storage {ns}:temp current_class set value {{slots:[]}}
data modify storage {ns}:temp current_class.slots set from storage {ns}:temp _find_iter[0].slots

# Apply the loadout (clears inventory and gives items)
function {ns}:v{version}/multiplayer/apply_class_dynamic

# Notify player
function {ns}:v{version}/multiplayer/custom/notify_selected with storage {ns}:temp _find_iter[0]
""")

	## custom/notify_selected — Macro tellraw
	write_versioned_function("multiplayer/custom/notify_selected",
"""$tellraw @s ["",{"text":"[MGS] ","color":"gold"},{"text":"Custom loadout applied: ","color":"white"},{"text":"$(name)","color":"green","bold":true}]
""")

	## custom/delete — Verify ownership and remove loadout from list
	write_versioned_function("multiplayer/custom/delete",
f"""
# Extract loadout ID from trigger value: id = trigger - {TRIG_DELETE_BASE}
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_DELETE_BASE}

# Copy the list, rebuild without the deleted entry
data modify storage {ns}:temp _del_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []

# Rebuild list, skipping the entry that matches both ID and owner (score-based)
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/delete_filter

# Notify
tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Loadout deleted.","color":"green"}}]
""")

	## custom/delete_filter — Recursive: rebuild list without the target entry (score-based)
	write_versioned_function("multiplayer/custom/delete_filter",
f"""
# Check if this entry matches BOTH the target ID and our PID
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _del_src[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _del_src[0].owner_pid
scoreboard players set #del_match {ns}.data 0
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run scoreboard players set #del_match {ns}.data 1

# If NOT a delete match, keep the entry
execute unless score #del_match {ns}.data matches 1 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _del_src[0]

# Next
data remove storage {ns}:temp _del_src[0]
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/delete_filter
""")

	## custom/toggle_favorite — Add/remove loadout ID from player's favorites list
	write_versioned_function("multiplayer/custom/toggle_favorite",
f"""
# Extract loadout ID from trigger value
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_FAVORITE_BASE}

# TODO: Find player data entry by PID and toggle the loadout ID in favorites[]
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Favorites coming soon!","color":"yellow"}}]
""")

	## custom/like — Increment loadout's like counter
	write_versioned_function("multiplayer/custom/like",
f"""
# Extract loadout ID from trigger value
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_LIKE_BASE}

# TODO: Find loadout by ID, increment likes counter, add to player's liked[] list
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Likes coming soon!","color":"yellow"}}]
""")

	## custom/toggle_visibility — Toggle public/private on own loadout
	write_versioned_function("multiplayer/custom/toggle_visibility",
f"""
# Extract loadout ID from trigger value
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_TOGGLE_VIS_BASE}

# Rebuild list with toggled visibility on the matching entry
data modify storage {ns}:temp _del_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/toggle_vis_rebuild

tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Loadout visibility toggled.","color":"green"}}]
""")

	## custom/toggle_vis_rebuild — Recursive: rebuild list, toggling public on the matching entry
	write_versioned_function("multiplayer/custom/toggle_vis_rebuild",
f"""
# Check if this entry matches our target (ID + ownership)
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _del_src[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _del_src[0].owner_pid
scoreboard players set #vis_match {ns}.data 0
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run scoreboard players set #vis_match {ns}.data 1

# If this is the target, toggle its public flag
execute if score #vis_match {ns}.data matches 1 run function {ns}:v{version}/multiplayer/custom/toggle_entry_vis

# Append entry (possibly toggled)
data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _del_src[0]

data remove storage {ns}:temp _del_src[0]
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/toggle_vis_rebuild
""")

	## custom/toggle_entry_vis — Toggle the public flag on _del_src[0]
	write_versioned_function("multiplayer/custom/toggle_entry_vis",
f"""
# Read current value and flip
execute store result score #pub {ns}.data run data get storage {ns}:temp _del_src[0].public
execute if score #pub {ns}.data matches 1 run data modify storage {ns}:temp _del_src[0].public set value 0b
execute if score #pub {ns}.data matches 0 run data modify storage {ns}:temp _del_src[0].public set value 1b
""")

	## custom/set_default — Set the default loadout for auto-selection
	write_versioned_function("multiplayer/custom/set_default",
f"""
# Extract loadout ID from trigger value
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_SET_DEFAULT_BASE}

# Store as player's default (scoreboard)
scoreboard players operation @s {ns}.mp.default = #loadout_id {ns}.data

# Notify
tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Default loadout set! It will auto-apply when a game starts.","color":"green"}}]
""")

	# Unset default loadout
	write_versioned_function("multiplayer/custom/unset_default",
f"""
# Unset default custom loadout - use standard class instead
scoreboard players set @s {ns}.mp.default 0
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Default loadout cleared. Standard class will be used.","color":"green"}}]
""")
