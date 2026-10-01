""" Favouriting a loadout and keeping its favourites counter in sync. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import TRIG_FAVORITE_BASE
from ....helpers import MGS_TAG


# Functions
def write_loadout_favorites() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Add or remove the loadout id from the player's favorites.
	write_versioned_function("multiplayer/custom/toggle_favorite", f"""
# The trigger value carries the loadout id.
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_FAVORITE_BASE}

# player_data is rebuilt, toggling the favorite in this player's entry.
data modify storage {ns}:temp _pd_src set from storage {ns}:multiplayer player_data
data modify storage {ns}:multiplayer player_data set value []
scoreboard players set #fav_found {ns}.data 0
execute if data storage {ns}:temp _pd_src[0] run function {ns}:v{version}/multiplayer/custom/fav_pd_rebuild

function {ns}:v{version}/multiplayer/custom/fav_count_update

execute if score #fav_found {ns}.data matches 1 run tellraw @s ["",{MGS_TAG},{{"text":"Removed from favorites","color":"yellow"}}]
execute if score #fav_found {ns}.data matches 0 run tellraw @s ["",{MGS_TAG},{{"text":"Added to favorites!","color":"green"}}]

# Reopen the Marketplace with the update.
function {ns}:v{version}/multiplayer/marketplace/browse
""")

	write_versioned_function("multiplayer/custom/fav_pd_rebuild", f"""
execute store result score #pd_pid {ns}.data run data get storage {ns}:temp _pd_src[0].pid
execute if score #pd_pid {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/custom/fav_modify_entry

data modify storage {ns}:multiplayer player_data append from storage {ns}:temp _pd_src[0]

data remove storage {ns}:temp _pd_src[0]
execute if data storage {ns}:temp _pd_src[0] run function {ns}:v{version}/multiplayer/custom/fav_pd_rebuild
""")

	write_versioned_function("multiplayer/custom/fav_modify_entry", f"""
data modify storage {ns}:temp _fav_iter set from storage {ns}:temp _pd_src[0].favorites
data modify storage {ns}:temp _pd_src[0].favorites set value []

# Remove it if present.
execute if data storage {ns}:temp _fav_iter[0] run function {ns}:v{version}/multiplayer/custom/fav_check_each

# Not present: add it.
execute if score #fav_found {ns}.data matches 0 run function {ns}:v{version}/multiplayer/custom/fav_append_new
""")

	write_versioned_function("multiplayer/custom/fav_append_new", f"""
data modify storage {ns}:temp _new_fav set value {{id:0}}
execute store result storage {ns}:temp _new_fav.id int 1 run scoreboard players get #loadout_id {ns}.data
data modify storage {ns}:temp _pd_src[0].favorites append from storage {ns}:temp _new_fav
""")

	write_versioned_function("multiplayer/custom/fav_check_each", f"""
execute store result score #fav_id {ns}.data run data get storage {ns}:temp _fav_iter[0].id
execute if score #fav_id {ns}.data = #loadout_id {ns}.data run scoreboard players set #fav_found {ns}.data 1

execute unless score #fav_id {ns}.data = #loadout_id {ns}.data run data modify storage {ns}:temp _pd_src[0].favorites append from storage {ns}:temp _fav_iter[0]

data remove storage {ns}:temp _fav_iter[0]
execute if data storage {ns}:temp _fav_iter[0] run function {ns}:v{version}/multiplayer/custom/fav_check_each
""")

	## #fav_found 0: just added (+1), 1: just removed (-1).
	write_versioned_function("multiplayer/custom/fav_count_update", f"""
data modify storage {ns}:temp _fav_count_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
execute if data storage {ns}:temp _fav_count_src[0] run function {ns}:v{version}/multiplayer/custom/fav_count_rebuild
""")

	write_versioned_function("multiplayer/custom/fav_count_rebuild", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _fav_count_src[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run function {ns}:v{version}/multiplayer/custom/fav_count_entry

data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _fav_count_src[0]

data remove storage {ns}:temp _fav_count_src[0]
execute if data storage {ns}:temp _fav_count_src[0] run function {ns}:v{version}/multiplayer/custom/fav_count_rebuild
""")

	write_versioned_function("multiplayer/custom/fav_count_entry", f"""
execute unless data storage {ns}:temp _fav_count_src[0].favorites_count run data modify storage {ns}:temp _fav_count_src[0].favorites_count set value 0

execute store result score #fav_cnt {ns}.data run data get storage {ns}:temp _fav_count_src[0].favorites_count

execute if score #fav_found {ns}.data matches 0 run scoreboard players add #fav_cnt {ns}.data 1
execute if score #fav_found {ns}.data matches 1 run scoreboard players remove #fav_cnt {ns}.data 1

# Never below 0.
execute if score #fav_cnt {ns}.data matches ..-1 run scoreboard players set #fav_cnt {ns}.data 0

execute store result storage {ns}:temp _fav_count_src[0].favorites_count int 1 run scoreboard players get #fav_cnt {ns}.data
""")

