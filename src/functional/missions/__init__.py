""" Missions mode entry point. """
# Imports
from .game import generate_missions_game
from .maps import generate_missions_maps
from .menus import generate_missions_menus


# Functions
def main() -> None:
	generate_missions_game()
	generate_missions_maps()
	generate_missions_menus()

