""" Perk machines: stationary buyables granting gameplay-enhancing perks.

Every perk and its behaviour is declared in PERK_DEFINITIONS. """
# Imports
from .apply import write_perk_apply
from .cherry import write_electric_cherry
from .dying_wish import write_dying_wish
from .hooks import write_perk_hooks
from .pool import write_perk_pool
from .purchase import write_perk_purchase
from .setup import write_perk_setup
from .state import write_perk_effect_state
from .tombstone import write_tombstone
from .widow import write_widows_wine


# Functions
def generate_perks() -> None:
	write_perk_setup()
	write_perk_pool()
	write_perk_purchase()
	write_perk_apply()
	write_perk_effect_state()
	write_electric_cherry()
	write_widows_wine()
	write_dying_wish()
	write_tombstone()
	write_perk_hooks()

