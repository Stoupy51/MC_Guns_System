""" Multiplayer mode entry point. """
# Imports
from .game import generate_game
from .gamemodes import generate_gamemodes
from .loadout import generate_loadouts
from .loadouts import generate_class_selection, generate_custom_loadouts
from .maps import generate_maps
from .menus import generate_menus
from .teams import generate_teams
from .xp import generate_multiplayer_xp


# Functions
def main() -> None:
	generate_game()
	generate_gamemodes()
	generate_multiplayer_xp()
	generate_teams()
	generate_loadouts()
	generate_class_selection()
	generate_custom_loadouts()
	generate_maps()
	generate_menus()

