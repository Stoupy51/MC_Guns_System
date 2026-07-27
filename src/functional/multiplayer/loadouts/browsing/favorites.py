""" Loading a player's favourites and testing one loadout against them. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_favorites_lookup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## SHARED HELPERS - player favorites loading & is-fav check

	## shared/load_player_favorites - Copy current player's favorites list into _cur_favorites
	write_versioned_function("multiplayer/shared/load_player_favorites", f"""
# Default to empty favorites
data modify storage {ns}:temp _cur_favorites set value []
# Scan player_data for our PID entry and copy its favorites list
data modify storage {ns}:temp _pd_iter set from storage {ns}:multiplayer player_data
execute if data storage {ns}:temp _pd_iter[0] run function {ns}:v{version}/multiplayer/shared/load_fav_iter
""")

	## shared/load_fav_iter - Recursive: find our entry by PID and copy favorites
	write_versioned_function("multiplayer/shared/load_fav_iter", f"""
execute store result score #pd_pid {ns}.data run data get storage {ns}:temp _pd_iter[0].pid
execute if score #pd_pid {ns}.data = @s {ns}.mp.pid run data modify storage {ns}:temp _cur_favorites set from storage {ns}:temp _pd_iter[0].favorites
data remove storage {ns}:temp _pd_iter[0]
# Stop early once our entry is found
execute unless score #pd_pid {ns}.data = @s {ns}.mp.pid if data storage {ns}:temp _pd_iter[0] run function {ns}:v{version}/multiplayer/shared/load_fav_iter
""")

	## shared/check_is_fav - Sets #is_fav = 1 if _iter[0].id is in _cur_favorites, else 0
	write_versioned_function("multiplayer/shared/check_is_fav", f"""
execute store result score #check_id {ns}.data run data get storage {ns}:temp _iter[0].id
data modify storage {ns}:temp _fav_check set from storage {ns}:temp _cur_favorites
scoreboard players set #is_fav {ns}.data 0
execute if data storage {ns}:temp _fav_check[0] run function {ns}:v{version}/multiplayer/shared/check_fav_iter
""")

	## shared/check_fav_iter - Recursive: compare each _fav_check entry against #check_id
	write_versioned_function("multiplayer/shared/check_fav_iter", f"""
execute store result score #fav_entry_id {ns}.data run data get storage {ns}:temp _fav_check[0].id
execute if score #fav_entry_id {ns}.data = #check_id {ns}.data run scoreboard players set #is_fav {ns}.data 1
data remove storage {ns}:temp _fav_check[0]
execute unless score #is_fav {ns}.data matches 1 if data storage {ns}:temp _fav_check[0] run function {ns}:v{version}/multiplayer/shared/check_fav_iter
""")

