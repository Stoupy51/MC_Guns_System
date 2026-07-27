""" Mystery Box system.

Dynamic weapon pool, visual animation with item cycling, random selection.

Price: 950 points (configurable via #zb_mystery_box_price config) Pool can be extended via function tag #mgs:zombies/register_mystery_box_item Uses Bookshelf interaction module for click/hover detection.
Positions use compound format: {pos:[x,y,z], rotation:[yaw,0.0f], group_id:N, can_start_on:1b} """
# ruff: noqa: E501
# Imports
from .collect import write_mystery_box_collect
from .fire_sale import write_fire_sale
from .hooks import write_mystery_box_hooks
from .hover import write_mystery_box_hover
from .interact import write_mystery_box_interaction
from .move import write_mystery_box_move
from .positions import write_mystery_box_positions
from .pull import write_mystery_box_pull
from .setup import write_mystery_box_setup
from .spin import write_mystery_box_spin


# Functions
def generate_mystery_box() -> None:
	write_mystery_box_setup()
	write_mystery_box_positions()
	write_mystery_box_interaction()
	write_fire_sale()
	write_mystery_box_pull()
	write_mystery_box_spin()
	write_mystery_box_move()
	write_mystery_box_collect()
	write_mystery_box_hover()
	write_mystery_box_hooks()

