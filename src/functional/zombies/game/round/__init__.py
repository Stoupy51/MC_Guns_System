""" Zombies round system.

Wave-based round progression with enemy spawning, scaling, and round completion.  """
# Imports
from ...enemies.mob import write_enemy_mobs
from ...enemies.types import write_enemy_types
from .arrival import write_arrivals
from .completion import write_round_completion
from .hooks import write_round_hooks
from .lifecycle import write_enemy_lifecycle
from .spawning import write_round_spawning
from .start import write_round_start
from .watchdog import write_watchdog


# Functions
def generate_zombies_rounds() -> None:
	write_round_start()
	write_round_spawning()
	write_arrivals()
	write_enemy_mobs()
	write_enemy_types()
	write_enemy_lifecycle()
	write_round_completion()
	write_watchdog()
	write_round_hooks()

