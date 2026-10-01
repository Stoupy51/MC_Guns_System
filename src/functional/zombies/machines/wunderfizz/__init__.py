""" Der Wunderfizz: a Mystery-Box-style machine that grants a random perk.

A map can hold several Wunderfizz spots, but only one is active; the others show a grayed cabinet (der_wunderfizz_disabled).
After a few uses the active machine can roam to another spot (teddy bear, shared with the Mystery Box through enemies/roaming).
The roam swaps models (old spot disabled, new spot live) instead of moving the cabinet, with the bear as the visual cue.
On use it cycles perk bottles, lands on a random perk the buyer does not own, and keeps it for the buyer for 10 s.
The pool is the shared perk pool (perks/pool/*): perks with a machine on the map, or every perk with the editor's `all_perks` flag (BO2 Origins).
"""
# Imports
from .collect import write_wunderfizz_collect
from .roam import write_wunderfizz_roam
from .setup import write_wunderfizz_setup
from .spin import write_wunderfizz_spin


# Functions
def generate_wunderfizz() -> None:
	write_wunderfizz_setup()
	write_wunderfizz_spin()
	write_wunderfizz_roam()
	write_wunderfizz_collect()

