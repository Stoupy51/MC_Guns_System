""" Multiplayer scoreboards, storage layout and the signal function tags. """
# Imports
from stewbeet import Mem, write_load_file, write_tag


# Functions
def write_multiplayer_setup() -> None:
	ns: str = Mem.ctx.project_id

	## Scoreboards & Storage Setup
	write_load_file(f"""
## Multiplayer scoreboards
# Team assignment (1 = red, 2 = blue, 0 = none/spectator)
scoreboard objectives add {ns}.mp.team dummy
# Personal stats
scoreboard objectives add {ns}.mp.kills dummy
scoreboard objectives add {ns}.mp.deaths dummy
# Round timer (ticks remaining)
scoreboard objectives add {ns}.mp.timer dummy
# In-game tag scoreboard (1 = in active game)
scoreboard objectives add {ns}.mp.in_game dummy

# Boundary checking coords
scoreboard objectives add {ns}.mp.bx dummy
scoreboard objectives add {ns}.mp.by dummy
scoreboard objectives add {ns}.mp.bz dummy

# Which of the 4 boundary-check phases a player belongs to (see multiplayer/enforce_bounds).
# #bphase_next is the round-robin cursor; seed it so the first assignment reads a real value.
scoreboard objectives add {ns}.mp.bphase dummy
scoreboard players set #bphase_next {ns}.data 0

# Class change detection (for prep phase)
scoreboard objectives add {ns}.mp.prev_class dummy

# Spectate timer (ticks remaining before respawn, 0 = not spectating)
scoreboard objectives add {ns}.mp.spectate_timer dummy

# FFA ranking (1 = most kills, 2 = second, ..., 0 = unranked)
scoreboard objectives add {ns}.mp.ffa_rank dummy

# Initialize team scores (only if not already set)
execute unless score #red {ns}.mp.team matches -2147483648.. run scoreboard players set #red {ns}.mp.team 0
execute unless score #blue {ns}.mp.team matches -2147483648.. run scoreboard players set #blue {ns}.mp.team 0

# Initialize game state (only if not yet set)
execute unless data storage {ns}:multiplayer game run data modify storage {ns}:multiplayer game set value {{state:"lobby",gamemode:"tdm",score_limit:30,time_limit:12000,map_id:"hijacked"}}
""")

	## Signal function tags
	for event in ["register_maps", "register_classes", "on_game_start", "on_game_end"]:
		write_tag(f"multiplayer/{event}", Mem.ctx.data[ns].function_tags, [])

