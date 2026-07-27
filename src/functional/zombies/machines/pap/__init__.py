""" Pack-a-Punch machine system for zombies mode.

Resolves PAP upgrades at runtime from the selected gun's own stats.pap_stats. """
# Imports
from .anim import write_pap_animation
from .chat import write_pap_chat
from .collect import write_pap_collect
from .cosmetics import write_pap_cosmetics
from .free import write_free_pap
from .hooks import write_pap_hooks
from .lore import write_pap_lore
from .magazines import write_pap_magazines
from .purchase import write_pap_purchase
from .setup import write_pap_setup
from .stats import write_pap_stats


# Functions
def generate_pap() -> None:
	write_pap_setup()
	write_pap_stats()
	write_pap_cosmetics()
	write_pap_magazines()
	write_pap_lore()
	write_pap_purchase()
	write_pap_chat()
	write_pap_animation()
	write_pap_collect()
	write_pap_hooks()
	write_free_pap()

