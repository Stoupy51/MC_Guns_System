""" Ammo system: firing cost, reloading, magazines and infinite-ammo refills.  """
# Imports
from .consume import write_magazine_consumption
from .core import write_ammo_core
from .reload import write_reload
from .shells import write_shell_reload


# Functions
def main() -> None:
	write_ammo_core()
	write_reload()
	write_magazine_consumption()
	write_shell_reload()

