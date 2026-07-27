""" Roam animation timings, the perk roll table and the orb's bottle model command. """
# Imports

from ..perks.definitions import PERK_DEFINITIONS

# Constants
# Roam move animation length (ticks).
# The bear rises, the machine relocates (model swap) at the midpoint, then settles.
# In-engine timing polish is a HUMAN eyeball pass.
WF_MOVE_TICKS: int = 100
WF_MOVE_RELOCATE: int = 55
""" Tick the active spot actually changes (model swap + visibility). """
WF_MOVE_BEAR_POOF: int = 48
""" Tick the bear despawns. """
# Uses on the active machine before it may roll to roam (mirrors the Mystery Box's 4-pull threshold)
WF_MOVE_THRESHOLD: int = 4

PERK_IDS: list[str] = list(PERK_DEFINITIONS)
""" Every perk the machine can roll, in registry order; the index is the orb's roll value. """
NUM_PERKS: int = len(PERK_IDS)
""" Roll range for a spin: random value 0..NUM_PERKS-1. """


# Functions
def orb_model_cmd(ns: str, pid: str) -> str:
	""" The command setting the spinning orb's item to a perk's bottle model. """
	return f'data modify entity @s item set value {{id:"minecraft:potion",count:1,components:{{"minecraft:item_model":"{ns}:perk_machine_{pid}"}}}}'

