""" Throwable grenades: throw, flight, detonation and the per-type effects.  """
# Imports
from .detonate import write_grenade_detonation
from .effects import write_grenade_effects
from .flight import write_grenade_flight
from .setup import write_grenade_setup
from .throw import write_grenade_throw


# Functions
def main() -> None:
	write_grenade_setup()
	write_grenade_throw()
	write_grenade_flight()
	write_grenade_detonation()
	write_grenade_effects()

