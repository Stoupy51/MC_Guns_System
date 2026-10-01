""" Persistent loadout storage and per-player id assignment. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function


# Functions
def generate_storage() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
# mp.pid: unique player id (loadout ownership), #next_pid its counter; mp.default: default custom loadout (0 = standard class).
scoreboard objectives add {ns}.mp.pid dummy
execute unless score #next_pid {ns}.data matches 1.. run scoreboard players set #next_pid {ns}.data 1
scoreboard objectives add {ns}.mp.default dummy
# Pick-10 points left while editing.
scoreboard objectives add {ns}.mp.edit_points dummy
# 0 creates a new loadout; otherwise saving overwrites this id.
scoreboard objectives add {ns}.mp.edit_target dummy

# Custom loadouts are stored as a negative mp.class.
scoreboard players set #minus_one {ns}.data -1
""")

	write_load_file(f"""
# Survives reloads.
execute unless data storage {ns}:multiplayer custom_loadouts run data modify storage {ns}:multiplayer custom_loadouts set value []
execute unless data storage {ns}:multiplayer player_data run data modify storage {ns}:multiplayer player_data set value []
execute unless data storage {ns}:multiplayer next_loadout_id run data modify storage {ns}:multiplayer next_loadout_id set value 1
""")

	## Run from player tick while pid is 0.
	write_versioned_function("multiplayer/assign_pid", f"""
scoreboard players operation @s {ns}.mp.pid = #next_pid {ns}.data
scoreboard players add #next_pid {ns}.data 1

data modify storage {ns}:temp _new_player set value {{pid:0,favorites:[],liked:[],default_loadout:0}}
execute store result storage {ns}:temp _new_player.pid int 1 run scoreboard players get @s {ns}.mp.pid
data modify storage {ns}:multiplayer player_data append from storage {ns}:temp _new_player
""")

	write_versioned_function("player/tick", f"""
execute unless score @s {ns}.mp.pid matches 1.. run function {ns}:v{version}/multiplayer/assign_pid
""", prepend=True)
	## Tag the player {ns}.username_getter and summon an item_display at them; the username lands in {ns}:temp _new_loadout.owner_name.
	write_versioned_function("multiplayer/get_username", f"""
# Run as the item_display, at the player.
tag @s add {ns}.username_getter_entity

# As the player, so the loot table's `this` is them and the head carries their profile.
execute at @s as @n[tag={ns}.username_getter] run loot replace entity @n[tag={ns}.username_getter_entity] contents loot {ns}:get_username

data modify storage {ns}:temp _new_loadout.owner_name set from entity @s item.components."minecraft:profile".name

# No profile captured.
execute unless data storage {ns}:temp _new_loadout.owner_name run data modify storage {ns}:temp _new_loadout.owner_name set value ""

kill @s
""")

