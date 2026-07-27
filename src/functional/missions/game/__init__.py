""" Missions game system.

Cooperative PvE game mode: all enemies spawn at game start, players kill them all.

Enemy positions and spawn functions are stored per-map via the editor.
When all enemies are killed, the game ends with a performance score. """
# Imports
from .death import write_missions_death
from .enemies import write_enemy_drops
from .setup import write_missions_setup
from .spawns import write_missions_spawns
from .start import write_missions_start
from .stop import write_missions_stop
from .tick import write_missions_tick


# Functions
def generate_missions_game() -> None:
	write_missions_setup()
	write_missions_start()
	write_enemy_drops()
	write_missions_death()
	write_missions_tick()
	write_missions_stop()
	write_missions_spawns()

