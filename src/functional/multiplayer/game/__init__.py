""" Multiplayer game lifecycle: start, stop, join, respawn and scoring.  """
# Imports
from .death import write_death_and_kills
from .join import write_multiplayer_join
from .prep import write_multiplayer_prep
from .setup import write_multiplayer_setup
from .sidebar import write_multiplayer_sidebar
from .spawns import write_multiplayer_spawns
from .start import write_multiplayer_start
from .stop import write_multiplayer_stop
from .tick import write_multiplayer_tick


# Functions
def generate_game() -> None:
	write_multiplayer_setup()
	write_multiplayer_start()
	write_multiplayer_stop()
	write_multiplayer_join()
	write_death_and_kills()
	write_multiplayer_tick()
	write_multiplayer_spawns()
	write_multiplayer_sidebar()
	write_multiplayer_prep()

