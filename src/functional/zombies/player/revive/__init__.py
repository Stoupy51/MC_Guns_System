""" Revive system, Black Ops Zombies-style and mannequin-based.

When a player takes lethal damage, they enter a "downed" state.

A mannequin is spawned at their death location wearing their armor/skin.
The player spectates the mannequin and can crawl (slow movement via WASD input predicates).
Teammates revive by standing near the mannequin.
After 60s without revive, player bleed out.
Solo + Quick Revive: auto-revive after 10s, up to 3 times. """
# Imports
from .complete import write_revive_completion
from .down import write_going_down
from .hooks import write_revive_hooks
from .round_end import write_round_end_revives
from .setup import write_revive_setup
from .tick import write_downed_tick
from .void import write_void_deaths


# Functions
def generate_revive() -> None:
	write_revive_setup()
	write_going_down()
	write_downed_tick()
	write_revive_completion()
	write_round_end_revives()
	write_void_deaths()
	write_revive_hooks()

