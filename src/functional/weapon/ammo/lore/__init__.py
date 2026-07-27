""" Rebuilds item lore from a weapon's stats, including Pack-a-Punch values.  """
# Imports
from .build import write_lore_build
from .extract import write_lore_extraction
from .templates import write_lore_templates


# Functions
def main() -> None:
	write_lore_templates()
	write_lore_extraction()
	write_lore_build()

