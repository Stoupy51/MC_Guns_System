""" Loadout browsing: the marketplace and My Loadouts list builders.  """
# Imports
from .favorites import write_favorites_lookup
from .marketplace import write_marketplace
from .my_loadouts import write_my_loadouts


# Functions
def generate_browsing() -> None:
	write_favorites_lookup()
	write_my_loadouts()
	write_marketplace()

