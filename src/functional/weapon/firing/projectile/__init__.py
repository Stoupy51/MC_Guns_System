""" Slow projectiles (RPG rockets and similar): summon, flight and impact.  """
# Imports
from .damage import write_projectile_damage
from .explode import write_projectile_explosion
from .flight import write_projectile_flight
from .summon import write_projectile_summon


# Functions
def main() -> None:
	write_projectile_summon()
	write_projectile_flight()
	write_projectile_explosion()
	write_projectile_damage()

