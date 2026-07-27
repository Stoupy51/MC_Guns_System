""" Mission scoreboards, storage layout and the signal function tags. """
# Imports
from stewbeet import Mem, write_load_file, write_tag


# Functions
def write_missions_setup() -> None:
	ns: str = Mem.ctx.project_id

	## Scoreboards & Storage Setup
	write_load_file(f"""
## Missions scoreboards
scoreboard objectives add {ns}.mi.in_game dummy
scoreboard objectives add {ns}.mi.timer dummy
scoreboard objectives add {ns}.mi.total_enemies dummy
scoreboard objectives add {ns}.mi.kills dummy
scoreboard objectives add {ns}.mi.deaths dummy
scoreboard objectives add {ns}.mi.kill_total totalKillCount
scoreboard objectives add {ns}.mi.kill_base dummy

# Was the death simulated? Then the body never moved and spectator mode already looks at the spot
scoreboard objectives add {ns}.mi.died_here dummy

# Boundary checking coords (reuse mp prefix scores)
scoreboard objectives add {ns}.mp.bx dummy
scoreboard objectives add {ns}.mp.by dummy
scoreboard objectives add {ns}.mp.bz dummy

# Initialize missions game state
execute unless data storage {ns}:missions game run data modify storage {ns}:missions game set value {{state:"lobby",map_id:""}}
""")

	## Signal function tags
	for event in ["on_mission_start", "on_mission_end"]:
		write_tag(f"missions/{event}", Mem.ctx.data[ns].function_tags, [])

