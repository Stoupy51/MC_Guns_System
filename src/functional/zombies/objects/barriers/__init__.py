""" Barriers: physical block-display obstacles that freeze zombies entering their radius.

Zombies can remove a barrier over 2 seconds, one remover at a time.
Players can repair a destroyed barrier by sneaking nearby for 1.5 seconds.
Block state is swapped in-place on destroy and repair, so each barrier stays a single block_display. """
# Imports
from .hooks import write_barrier_hooks
from .lighting import write_barrier_lighting
from .setup import write_barrier_setup
from .tick import write_barrier_tick


# Functions
def generate_barriers() -> None:
	write_barrier_setup()
	write_barrier_lighting()
	write_barrier_tick()
	write_barrier_hooks()

