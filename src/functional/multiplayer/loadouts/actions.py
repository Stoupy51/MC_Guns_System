
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG
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
	## CUSTOM LOADOUT ACTIONS - Select, Delete, Toggle Visibility, Set Default
	## ====================================================================

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
	apply_now: str = f"""{{"text":" [✔]","color":"gold","hover_event":{{"action":"show_text","value":{{"text":"Click here to apply immediately (OP only)","color":"yellow"}}}},"click_event":{{"action":"run_command","command":"/function {ns}:v{version}/multiplayer/apply_class"}}}}"""
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
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/delete_filter

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

# If NOT a delete match, keep the entry
execute unless score #del_match {ns}.data matches 1 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _del_src[0]

# Next
data remove storage {ns}:temp _del_src[0]
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/delete_filter
""")

	## custom/toggle_favorite - Add/remove loadout ID from player's favorites list
	write_versioned_function("multiplayer/custom/toggle_favorite", f"""
# Extract loadout ID from trigger value
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_FAVORITE_BASE}

# Rebuild player_data, toggling favorite in our entry
data modify storage {ns}:temp _pd_src set from storage {ns}:multiplayer player_data
data modify storage {ns}:multiplayer player_data set value []
scoreboard players set #fav_found {ns}.data 0
execute if data storage {ns}:temp _pd_src[0] run function {ns}:v{version}/multiplayer/custom/fav_pd_rebuild

# Update favorites_count on the affected loadout in custom_loadouts
function {ns}:v{version}/multiplayer/custom/fav_count_update

# Notify based on whether it was added or removed
execute if score #fav_found {ns}.data matches 1 run tellraw @s ["",{MGS_TAG},{{"text":"Removed from favorites","color":"yellow"}}]
execute if score #fav_found {ns}.data matches 0 run tellraw @s ["",{MGS_TAG},{{"text":"Added to favorites!","color":"green"}}]

# Reopen Marketplace dialog with updated data
function {ns}:v{version}/multiplayer/marketplace/browse
""")

	## fav_pd_rebuild - Iterate player_data, modify our entry's favorites
	write_versioned_function("multiplayer/custom/fav_pd_rebuild", f"""
# Check if this entry's PID matches ours
execute store result score #pd_pid {ns}.data run data get storage {ns}:temp _pd_src[0].pid
execute if score #pd_pid {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/custom/fav_modify_entry

# Append entry (possibly modified) to player_data
data modify storage {ns}:multiplayer player_data append from storage {ns}:temp _pd_src[0]

# Next
data remove storage {ns}:temp _pd_src[0]
execute if data storage {ns}:temp _pd_src[0] run function {ns}:v{version}/multiplayer/custom/fav_pd_rebuild
""")

	## fav_modify_entry - Toggle loadout ID in our favorites list
	write_versioned_function("multiplayer/custom/fav_modify_entry", f"""
# Copy favorites for iteration, clear them for rebuild
data modify storage {ns}:temp _fav_iter set from storage {ns}:temp _pd_src[0].favorites
data modify storage {ns}:temp _pd_src[0].favorites set value []

# Iterate favorites to remove if found
execute if data storage {ns}:temp _fav_iter[0] run function {ns}:v{version}/multiplayer/custom/fav_check_each

# If not found (wasn't in favorites), add it
execute if score #fav_found {ns}.data matches 0 run function {ns}:v{version}/multiplayer/custom/fav_append_new
""")

	## fav_append_new - Append loadout ID to favorites
	write_versioned_function("multiplayer/custom/fav_append_new", f"""
# Create a new favorite entry with the loadout ID
data modify storage {ns}:temp _new_fav set value {{id:0}}
execute store result storage {ns}:temp _new_fav.id int 1 run scoreboard players get #loadout_id {ns}.data
data modify storage {ns}:temp _pd_src[0].favorites append from storage {ns}:temp _new_fav
""")

	## fav_check_each - Check each favorite entry, remove matching ID
	write_versioned_function("multiplayer/custom/fav_check_each", f"""
# Check if this favorite's ID matches the target
execute store result score #fav_id {ns}.data run data get storage {ns}:temp _fav_iter[0].id
execute if score #fav_id {ns}.data = #loadout_id {ns}.data run scoreboard players set #fav_found {ns}.data 1

# If not matching, keep it
execute unless score #fav_id {ns}.data = #loadout_id {ns}.data run data modify storage {ns}:temp _pd_src[0].favorites append from storage {ns}:temp _fav_iter[0]

# Next
data remove storage {ns}:temp _fav_iter[0]
execute if data storage {ns}:temp _fav_iter[0] run function {ns}:v{version}/multiplayer/custom/fav_check_each
""")

	## fav_count_update - Rebuild custom_loadouts, updating favorites_count on target loadout
	## #fav_found = 0 means just added (increment), 1 means just removed (decrement)
	write_versioned_function("multiplayer/custom/fav_count_update", f"""
data modify storage {ns}:temp _fav_count_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
execute if data storage {ns}:temp _fav_count_src[0] run function {ns}:v{version}/multiplayer/custom/fav_count_rebuild
""")

	## fav_count_rebuild - Iterate loadouts, update favorites_count on matching ID
	write_versioned_function("multiplayer/custom/fav_count_rebuild", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _fav_count_src[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run function {ns}:v{version}/multiplayer/custom/fav_count_entry

data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _fav_count_src[0]

data remove storage {ns}:temp _fav_count_src[0]
execute if data storage {ns}:temp _fav_count_src[0] run function {ns}:v{version}/multiplayer/custom/fav_count_rebuild
""")

	## fav_count_entry - Increment or decrement favorites_count based on #fav_found
	write_versioned_function("multiplayer/custom/fav_count_entry", f"""
# Ensure favorites_count field exists
execute unless data storage {ns}:temp _fav_count_src[0].favorites_count run data modify storage {ns}:temp _fav_count_src[0].favorites_count set value 0

# Load current count into score
execute store result score #fav_cnt {ns}.data run data get storage {ns}:temp _fav_count_src[0].favorites_count

# fav_found=0 means just added → increment; fav_found=1 means just removed → decrement
execute if score #fav_found {ns}.data matches 0 run scoreboard players add #fav_cnt {ns}.data 1
execute if score #fav_found {ns}.data matches 1 run scoreboard players remove #fav_cnt {ns}.data 1

# Clamp to 0 minimum
execute if score #fav_cnt {ns}.data matches ..-1 run scoreboard players set #fav_cnt {ns}.data 0

# Store back
execute store result storage {ns}:temp _fav_count_src[0].favorites_count int 1 run scoreboard players get #fav_cnt {ns}.data
""")

	## custom/like - Increment loadout's like counter (one per player)
	write_versioned_function("multiplayer/custom/like", f"""
# Extract loadout ID from trigger value
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_LIKE_BASE}

# Step 1: Check if already liked in our player_data, and add to liked[] if not
data modify storage {ns}:temp _pd_src set from storage {ns}:multiplayer player_data
data modify storage {ns}:multiplayer player_data set value []
scoreboard players set #already_liked {ns}.data 0
execute if data storage {ns}:temp _pd_src[0] run function {ns}:v{version}/multiplayer/custom/like_pd_rebuild

# Step 2: If not already liked, increment like counter on the loadout
execute if score #already_liked {ns}.data matches 0 run function {ns}:v{version}/multiplayer/custom/like_increment_setup

# Notify
execute if score #already_liked {ns}.data matches 0 run tellraw @s ["",{MGS_TAG},{{"text":"Loadout liked!","color":"green"}}]
execute if score #already_liked {ns}.data matches 1 run tellraw @s ["",{MGS_TAG},{{"text":"You already liked this loadout","color":"yellow"}}]

# Reopen Marketplace dialog with updated data
function {ns}:v{version}/multiplayer/marketplace/browse
""")

	## like_pd_rebuild - Iterate player_data to check/update liked[] in our entry
	write_versioned_function("multiplayer/custom/like_pd_rebuild", f"""
# Check if this entry's PID matches ours
execute store result score #pd_pid {ns}.data run data get storage {ns}:temp _pd_src[0].pid
execute if score #pd_pid {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/custom/like_modify_entry

# Append entry to player_data
data modify storage {ns}:multiplayer player_data append from storage {ns}:temp _pd_src[0]

# Next
data remove storage {ns}:temp _pd_src[0]
execute if data storage {ns}:temp _pd_src[0] run function {ns}:v{version}/multiplayer/custom/like_pd_rebuild
""")

	## like_modify_entry - Check if loadout already liked, add if not
	write_versioned_function("multiplayer/custom/like_modify_entry", f"""
# Iterate liked[] to check if already liked
data modify storage {ns}:temp _liked_iter set from storage {ns}:temp _pd_src[0].liked
execute if data storage {ns}:temp _liked_iter[0] run function {ns}:v{version}/multiplayer/custom/like_check_each

# If not already liked, add to liked[] list
execute if score #already_liked {ns}.data matches 0 run function {ns}:v{version}/multiplayer/custom/like_append_new
""")

	## like_append_new - Append loadout ID to liked list
	write_versioned_function("multiplayer/custom/like_append_new", f"""
data modify storage {ns}:temp _new_liked set value {{id:0}}
execute store result storage {ns}:temp _new_liked.id int 1 run scoreboard players get #loadout_id {ns}.data
data modify storage {ns}:temp _pd_src[0].liked append from storage {ns}:temp _new_liked
""")

	## like_check_each - Check each liked entry
	write_versioned_function("multiplayer/custom/like_check_each", f"""
execute store result score #liked_id {ns}.data run data get storage {ns}:temp _liked_iter[0].id
execute if score #liked_id {ns}.data = #loadout_id {ns}.data run scoreboard players set #already_liked {ns}.data 1

data remove storage {ns}:temp _liked_iter[0]
execute if data storage {ns}:temp _liked_iter[0] unless score #already_liked {ns}.data matches 1 run function {ns}:v{version}/multiplayer/custom/like_check_each
""")

	## like_increment_setup - Rebuild custom_loadouts, incrementing likes on target
	write_versioned_function("multiplayer/custom/like_increment_setup", f"""
data modify storage {ns}:temp _like_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
execute if data storage {ns}:temp _like_src[0] run function {ns}:v{version}/multiplayer/custom/like_increment_rebuild
""")

	## like_increment_rebuild - Iterate loadouts, increment likes on matching ID
	write_versioned_function("multiplayer/custom/like_increment_rebuild", f"""
# Check if this loadout's ID matches the target
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _like_src[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run function {ns}:v{version}/multiplayer/custom/like_increment_entry

# Append to custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _like_src[0]

data remove storage {ns}:temp _like_src[0]
execute if data storage {ns}:temp _like_src[0] run function {ns}:v{version}/multiplayer/custom/like_increment_rebuild
""")

	## like_increment_entry - Increment the likes counter
	write_versioned_function("multiplayer/custom/like_increment_entry", f"""
# Ensure likes field exists, then increment
execute unless data storage {ns}:temp _like_src[0].likes run data modify storage {ns}:temp _like_src[0].likes set value 0
execute store result score #likes {ns}.data run data get storage {ns}:temp _like_src[0].likes
scoreboard players add #likes {ns}.data 1
execute store result storage {ns}:temp _like_src[0].likes int 1 run scoreboard players get #likes {ns}.data
""")

	## custom/toggle_visibility - Toggle public/private on own loadout
	write_versioned_function("multiplayer/custom/toggle_visibility", f"""
# Extract loadout ID from trigger value
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_TOGGLE_VIS_BASE}

# Rebuild list with toggled visibility on the matching entry
data modify storage {ns}:temp _del_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
execute if data storage {ns}:temp _del_src[0] run function {ns}:v{version}/multiplayer/custom/toggle_vis_rebuild

tellraw @s ["",{MGS_TAG},{{"text":"Loadout visibility toggled","color":"green"}}]

# Reopen My Loadouts dialog with updated data
function {ns}:v{version}/multiplayer/my_loadouts/browse
""")

	## custom/toggle_vis_rebuild - Recursive: rebuild list, toggling public on the matching entry
	write_versioned_function("multiplayer/custom/toggle_vis_rebuild", f"""
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

	## custom/toggle_entry_vis - Toggle the public flag on _del_src[0]
	write_versioned_function("multiplayer/custom/toggle_entry_vis", f"""
# Read current value and flip
execute store result score #pub {ns}.data run data get storage {ns}:temp _del_src[0].public
execute if score #pub {ns}.data matches 1 run data modify storage {ns}:temp _del_src[0].public set value 0b
execute if score #pub {ns}.data matches 0 run data modify storage {ns}:temp _del_src[0].public set value 1b
""")

	## custom/set_default - Set the default loadout for auto-selection
	write_versioned_function("multiplayer/custom/set_default", f"""
# Extract loadout ID from trigger value
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_SET_DEFAULT_BASE}

# Store as player's default (scoreboard)
scoreboard players operation @s {ns}.mp.default = #loadout_id {ns}.data

# Notify
tellraw @s ["",{MGS_TAG},{{"text":"Default loadout set! It will auto-apply when a game starts","color":"green"}}]
""")

	# Unset default loadout
	write_versioned_function("multiplayer/custom/unset_default", f"""
# Unset default custom loadout - use standard class instead
scoreboard players set @s {ns}.mp.default 0
tellraw @s [{MGS_TAG},{{"text":"Default loadout cleared. Standard class will be used","color":"green"}}]
""")
