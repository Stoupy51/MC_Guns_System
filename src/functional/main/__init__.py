""" Core datapack setup: player tick, regen, damage types, fonts and shared utilities.  """
# Imports
from .assets import write_assets
from .config_menu import write_config_menu
from .damage import write_damage_and_signals
from .objectives import write_objectives


# Functions
def main() -> None:
	write_objectives()
	write_damage_and_signals()
	write_assets()
	write_config_menu()

