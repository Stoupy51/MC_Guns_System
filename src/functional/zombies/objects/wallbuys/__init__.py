""" Wallbuy System Wall-mounted stations.

Players interact to buy items.
Each wallbuy displays its item on the wall and shows info on hover.
The item KIND is probed from the item's custom_data at setup and routes the purchase flow:
  0 = gun (+magazine, hotbar.1-3)        1 = knife (hotbar.0, no refill)
  2 = lethal grenade (hotbar.7, max 4)   3 = tactical e.g. monkey bomb (hotbar.6, max 3) """
# Imports
from .give import write_wallbuy_give
from .hover import write_wallbuy_hover
from .purchase import write_wallbuy_purchase
from .setup import write_wallbuy_setup


# Functions
def generate_wallbuys() -> None:
	write_wallbuy_setup()
	write_wallbuy_purchase()
	write_wallbuy_give()
	write_wallbuy_hover()

