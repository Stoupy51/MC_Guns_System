
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function


def generate_storage() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Scoreboards & Storage for custom loadouts
	## ============================
	write_load_file(
f"""
## Custom loadout system
# Unique player IDs (auto-increment, used to identify loadout ownership)
# Global next-pid counter
# Player's default custom loadout ID (0 = none → use standard class)
# Editor state tracker (0 = not editing)
scoreboard objectives add {ns}.mp.pid dummy
execute unless score #next_pid {ns}.data matches 1.. run scoreboard players set #next_pid {ns}.data 1
scoreboard objectives add {ns}.mp.default dummy
scoreboard objectives add {ns}.mp.edit_step dummy
# Pick-10 points remaining during loadout editing
scoreboard objectives add {ns}.mp.edit_points dummy

# Constant for negation (used to store custom loadout ID as negative mp.class)
scoreboard players set #minus_one {ns}.data -1
""")

	## Initialize custom loadout storage (only if not already set)
	write_load_file(
f"""
# Custom loadouts list (persists across reloads)
execute unless data storage {ns}:multiplayer custom_loadouts run data modify storage {ns}:multiplayer custom_loadouts set value []
# Per-player preference data (persists across reloads)
execute unless data storage {ns}:multiplayer player_data run data modify storage {ns}:multiplayer player_data set value []
# Auto-increment counter for loadout IDs
execute unless data storage {ns}:multiplayer next_loadout_id run data modify storage {ns}:multiplayer next_loadout_id set value 1
""")

	## ============================
	## Assign player ID on first interaction (called from player tick if pid == 0)
	## ============================
	write_versioned_function("multiplayer/assign_pid",
f"""
# Assign a unique player ID
scoreboard players operation @s {ns}.mp.pid = #next_pid {ns}.data
scoreboard players add #next_pid {ns}.data 1

# Initialize player data entry in storage
data modify storage {ns}:temp _new_player set value {{pid:0,favorites:[],liked:[],default_loadout:0}}
execute store result storage {ns}:temp _new_player.pid int 1 run scoreboard players get @s {ns}.mp.pid
data modify storage {ns}:multiplayer player_data append from storage {ns}:temp _new_player
""")

	## ============================
	## Player tick hook: assign pid if needed
	## ============================
	write_versioned_function("player/tick",
f"""
# Custom loadouts: assign player ID if not yet assigned
execute unless score @s {ns}.mp.pid matches 1.. run function {ns}:v{version}/multiplayer/assign_pid
""", prepend=True)
