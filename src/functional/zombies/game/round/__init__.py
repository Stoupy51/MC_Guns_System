""" Zombies round system.

Wave-based round progression with zombie spawning, scaling, and round completion.  """
# Imports
from .completion import write_round_completion
from .enemies import write_enemy_types
from .hooks import write_round_hooks
from .lifecycle import write_enemy_lifecycle
from .spawning import write_round_spawning
from .start import write_round_start
from .watchdog import write_watchdog


# Functions
def generate_zombies_rounds() -> None:
	write_round_start()
	write_round_spawning()
	write_enemy_types()
	write_enemy_lifecycle()
	write_round_completion()
	write_watchdog()
	write_round_hooks()

