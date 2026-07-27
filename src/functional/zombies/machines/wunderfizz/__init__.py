""" Der Wunderfizz — a Mystery-Box-style machine that grants a RANDOM perk.

Like the Mystery Box, a map can hold SEVERAL Wunderfizz spots but only ONE is active at a time; the rest show a grayed-out "disabled" cabinet (der_wunderfizz_disabled) marking where it might roam to.
After a few uses the active machine can roam to another spot (teddy-bear move easter egg, shared with the Mystery Box via zombies/roaming.py).
The roam is a model-swap (old spot → disabled, new spot → live) rather than physically flying the big cabinet, with the bear as the visual cue.
On use it cycles perk bottles, lands on a random perk the buyer doesn't own, and leaves it collectable by the buyer only for 10s.
The pool is the shared "available perk pool" helper (zombies/perks/pool/*): perks with a machine on this map, widened to every perk when the editor `all_perks` flag is set (BO2 Origins behaviour). """
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

