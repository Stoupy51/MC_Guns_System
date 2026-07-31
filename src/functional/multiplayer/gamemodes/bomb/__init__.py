""" The two bomb gamemodes, and the machinery they share.

Search & Destroy and Demolition mark the same objectives on the same maps and ask the same opening
question (which side already stands on the objective), so `sites.py` and `visuals.py` are written once and
emitted into each mode's own function path. What is NOT shared is the bomb itself: S&D has one carried
bomb and global channel scores, Demolition arms everyone and keeps per-site state on the site markers.
Forcing those two into one abstraction would hide the only interesting difference between the modes.
"""
# Imports
from .demo import Demolition, generate_demolition
from .snd import SearchAndDestroy, generate_search_and_destroy

# Constants
__all__ = ["Demolition", "SearchAndDestroy", "generate_demolition", "generate_search_and_destroy"]
""" What the gamemode package imports from here. """
