""" Zombies inventory management.

Handles strict zombies slot layout, slot-tagged items, and recovery from moved/dropped items.  """
# Imports
from .grenades import write_grenade_slots
from .hooks import write_inventory_hooks
from .info import write_info_item
from .loadout import write_zombies_loadout
from .slots import write_slot_enforcement


# Functions
def generate_zombies_inventory() -> None:
	write_slot_enforcement()
	write_zombies_loadout()
	write_info_item()
	write_grenade_slots()
	write_inventory_hooks()

