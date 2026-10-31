""" Mystery Box system.

Weighted weapon pool, visual animation with item cycling, random selection.

The pool is `[{weapon_id, weight}]` in `mgs:config zombies.mystery_box_pool`, or in a map's `mystery_box_pool`, which replaces it for that map.
`#mgs:zombies/register_mystery_box_item` runs after the game's pool is built and may append a catalog-shaped entry to `mgs:zombies mystery_box_pool` and its weight to `mystery_box_weights`.
Price: 950 points (`#zb_mystery_box_price` config). Uses Bookshelf interaction module for click/hover detection.
Positions use compound format: {pos:[x,y,z], rotation:[yaw,0.0f], group_id:N, can_start_on:1b} """
# Imports
from .collect import write_mystery_box_collect
from .fire_sale import write_fire_sale
from .hooks import write_mystery_box_hooks
from .hover import write_mystery_box_hover
from .interact import write_mystery_box_interaction
from .move import write_mystery_box_move
from .pool_menu import write_pool_menu
from .positions import write_mystery_box_positions
from .pull import write_mystery_box_pull
from .setup import write_mystery_box_setup
from .spin import write_mystery_box_spin


# Functions
def generate_mystery_box() -> None:
	write_mystery_box_setup()
	write_pool_menu()
	write_mystery_box_positions()
	write_mystery_box_interaction()
	write_fire_sale()
	write_mystery_box_pull()
	write_mystery_box_spin()
	write_mystery_box_move()
	write_mystery_box_collect()
	write_mystery_box_hover()
	write_mystery_box_hooks()

