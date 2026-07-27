""" Zombies game system.

Wave-based survival mode with zombie spawning, points, perks, mystery box, wallbuys, doors, and traps.

Map definitions are dynamic (stored in storage, registered via function tags). """
# Imports
from .join import write_zombies_join
from .over import write_zombies_over
from .setup import write_zombies_setup
from .sidebar import write_zombies_sidebar
from .spawns import write_zombies_spawns
from .start import write_zombies_start
from .stuck import write_stuck_and_bounds
from .tick import write_zombies_tick


# Functions
def generate_zombies_game() -> None:
	write_zombies_setup()
	write_zombies_start()
	write_zombies_tick()
	write_zombies_over()
	write_zombies_join()
	write_stuck_and_bounds()
	write_zombies_spawns()
	write_zombies_sidebar()

