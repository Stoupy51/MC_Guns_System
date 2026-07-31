""" Gamemode-specific logic for multiplayer: FFA, TDM, Domination, Hardpoint, Search & Destroy, Demolition. """
# Imports
from stewbeet import Mem, write_load_file

from .bomb import generate_demolition, generate_search_and_destroy
from .domination import generate_domination
from .free_for_all import generate_free_for_all
from .hardpoint import generate_hardpoint
from .team_deathmatch import generate_team_deathmatch


# Functions
def generate_gamemodes() -> None:
	ns: str = Mem.ctx.project_id

	## Scoreboards for gamemodes.
	## The four demo_* objectives are per-ENTITY: Demolition keeps each bomb site's state on its own marker
	## because two sites can be planted, contested and defused at the same time.
	write_load_file(f"""
# Gamemode scoreboards
scoreboard objectives add {ns}.mp.dom_progress dummy
scoreboard objectives add {ns}.mp.dom_owner dummy
scoreboard objectives add {ns}.mp.gm_timer dummy
scoreboard objectives add {ns}.demo_state dummy
scoreboard objectives add {ns}.demo_prog dummy
scoreboard objectives add {ns}.demo_fuse dummy
scoreboard objectives add {ns}.demo_owner dummy
""")

	generate_free_for_all()
	generate_team_deathmatch()
	generate_domination()
	generate_hardpoint()
	generate_search_and_destroy()
	generate_demolition()

