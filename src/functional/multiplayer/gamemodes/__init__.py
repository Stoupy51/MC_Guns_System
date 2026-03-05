
# Gamemode-specific logic for multiplayer: FFA, TDM, Domination, Hardpoint, Search & Destroy
from stewbeet import Mem, write_load_file

from .domination import generate_domination
from .free_for_all import generate_free_for_all
from .hardpoint import generate_hardpoint
from .search_and_destroy import generate_search_and_destroy
from .team_deathmatch import generate_team_deathmatch


def generate_gamemodes() -> None:
	ns: str = Mem.ctx.project_id

	## Scoreboards for gamemodes
	write_load_file(f"""
# Gamemode scoreboards
scoreboard objectives add {ns}.mp.dom_progress dummy
scoreboard objectives add {ns}.mp.dom_owner dummy
scoreboard objectives add {ns}.mp.gm_timer dummy
""")

	generate_free_for_all()
	generate_team_deathmatch()
	generate_domination()
	generate_hardpoint()
	generate_search_and_destroy()

