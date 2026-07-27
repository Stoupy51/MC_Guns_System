""" Favouriting a loadout and keeping its favourites counter in sync. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ..catalogs import TRIG_FAVORITE_BASE


# Functions
def write_loadout_favorites() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

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

	## Rebuild custom_loadouts, updating favorites_count on the target loadout.
	## #fav_found 0 means just added (increment), 1 means just removed (decrement).
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

