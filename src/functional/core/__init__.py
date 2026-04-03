
# Core shared functions (shared mcfunctions used by multiplayer, missions, and zombies)
from .bounds import write_shared_bounds_functions
from .commands import write_shared_command_functions
from .map_loading import write_shared_map_loading
from .map_menus import write_shared_map_menus
from .spawning import write_shared_spawning_functions
from .teleport import write_shared_teleport_functions


def main() -> None:
	write_shared_bounds_functions()
	write_shared_teleport_functions()
	write_shared_map_loading()
	write_shared_map_menus()
	write_shared_command_functions()
	write_shared_spawning_functions()

