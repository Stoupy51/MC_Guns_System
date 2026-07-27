""" Power-up system.

On each zombie death there is a min(2%, 1/total_round_zombies) chance to drop a power-up, until one full shuffle-bag cycle has dropped this round.

Rares only appear after round 5.
Visual: item entity + text_display.
Pickup by proximity (1.5 blocks). 26.5s lifetime. """
# Imports
from .bossbars import write_powerup_bossbars
from .drops import write_powerup_drops
from .effects import write_powerup_effects
from .pickup import write_powerup_pickup
from .spawn import write_powerup_spawn


# Functions
def generate_powerups() -> None:
	write_powerup_drops()
	write_powerup_spawn()
	write_powerup_pickup()
	write_powerup_effects()
	write_powerup_bossbars()

