""" Loading a player's favourites and testing one loadout against them. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_favorites_lookup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Loading the player's favorites, and the is-favorite check.

	## Copies the player's favorites into _cur_favorites.
	write_versioned_function("multiplayer/shared/load_player_favorites", f"""
data modify storage {ns}:temp _cur_favorites set value []
data modify storage {ns}:temp _pd_iter set from storage {ns}:multiplayer player_data
execute if data storage {ns}:temp _pd_iter[0] run function {ns}:v{version}/multiplayer/shared/load_fav_iter
""")

	## Find this player's entry by pid.
	write_versioned_function("multiplayer/shared/load_fav_iter", f"""
execute store result score #pd_pid {ns}.data run data get storage {ns}:temp _pd_iter[0].pid
execute if score #pd_pid {ns}.data = @s {ns}.mp.pid run data modify storage {ns}:temp _cur_favorites set from storage {ns}:temp _pd_iter[0].favorites
data remove storage {ns}:temp _pd_iter[0]
# Stops once found.
execute unless score #pd_pid {ns}.data = @s {ns}.mp.pid if data storage {ns}:temp _pd_iter[0] run function {ns}:v{version}/multiplayer/shared/load_fav_iter
""")

	## #is_fav = 1 when _iter[0].id is in _cur_favorites.
	write_versioned_function("multiplayer/shared/check_is_fav", f"""
execute store result score #check_id {ns}.data run data get storage {ns}:temp _iter[0].id
data modify storage {ns}:temp _fav_check set from storage {ns}:temp _cur_favorites
scoreboard players set #is_fav {ns}.data 0
execute if data storage {ns}:temp _fav_check[0] run function {ns}:v{version}/multiplayer/shared/check_fav_iter
""")

	write_versioned_function("multiplayer/shared/check_fav_iter", f"""
execute store result score #fav_entry_id {ns}.data run data get storage {ns}:temp _fav_check[0].id
execute if score #fav_entry_id {ns}.data = #check_id {ns}.data run scoreboard players set #is_fav {ns}.data 1
data remove storage {ns}:temp _fav_check[0]
execute unless score #is_fav {ns}.data matches 1 if data storage {ns}:temp _fav_check[0] run function {ns}:v{version}/multiplayer/shared/check_fav_iter
""")

