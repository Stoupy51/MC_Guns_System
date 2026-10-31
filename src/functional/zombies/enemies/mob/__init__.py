""" Every enemy, whatever its entity, is built from a spawn's `mob` compound and scaled to the round the same way. """
# Imports
from .build import write_mob_build
from .health import write_health_curve
from .presets import write_presets


# Functions
def write_enemy_mobs() -> None:
	write_health_curve()
	write_presets()
	write_mob_build()

