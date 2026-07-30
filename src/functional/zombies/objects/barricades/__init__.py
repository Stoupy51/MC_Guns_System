""" Barricades: physical block-display obstacles that freeze zombies entering their radius.

Zombies can remove a barricade over 2 seconds, one remover at a time.
Players can repair a destroyed barricade by sneaking nearby for 1.5 seconds.
Block state is swapped in-place on destroy and repair, so each barricade stays a single block_display. """
# Imports
from .hooks import write_barricade_hooks
from .lighting import write_barricade_lighting
from .setup import write_barricade_setup
from .tick import write_barricade_tick


# Functions
def generate_barricades() -> None:
	write_barricade_setup()
	write_barricade_lighting()
	write_barricade_tick()
	write_barricade_hooks()

