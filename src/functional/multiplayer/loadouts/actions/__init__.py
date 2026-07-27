""" Loadout actions: select, favorite, like, delete and visibility toggles.  """
# Imports
from .favorites import write_loadout_favorites
from .likes import write_loadout_likes
from .manage import write_loadout_management
from .selection import write_loadout_selection


# Functions
def generate_actions() -> None:
	write_loadout_selection()
	write_loadout_favorites()
	write_loadout_likes()
	write_loadout_management()

