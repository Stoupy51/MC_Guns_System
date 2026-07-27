""" Core shared functions (shared mcfunctions used by multiplayer, missions, and zombies). """
# Imports
from .bounds import write_shared_bounds_functions
from .commands import write_shared_command_functions
from .map_loading import write_shared_map_loading
from .map_menus import write_shared_map_menus
from .player_menus import write_player_menus
from .spawning import CoreSpawning
from .teleport import write_shared_teleport_functions
from .weapon_drop import WeaponDrop


# Functions
def main() -> None:
	write_shared_bounds_functions()
	write_shared_teleport_functions()
	write_shared_map_loading()
	write_shared_map_menus()
	write_player_menus()
	write_shared_command_functions()
	CoreSpawning.write_shared_spawning_functions()
	WeaponDrop.write_shared_weapon_drop_functions()

