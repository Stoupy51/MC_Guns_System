""" Trap system.

Area-of-effect devices that damage zombies in a radius for a duration, then enter cooldown.

Type 0 = fire: lethal to zombies (1000% of max health), 5 fire damage to players inside.
Type 1 = electric: lethal to zombies (1000% of max health), 5 electric damage to players inside.
Type 2 = turret: shoots the nearest zombie in range every 5 ticks for 45% of its max health;          the bullet stops at the first entity hit, so players between the turret and zombies take 2 damage instead. """
# ruff: noqa: E501
# Imports
from .active import write_trap_activity
from .hooks import write_trap_hooks
from .interact import write_trap_interaction
from .setup import write_trap_setup
from .turret import write_turret


# Functions
def generate_traps() -> None:
	write_trap_setup()
	write_trap_interaction()
	write_trap_activity()
	write_turret()
	write_trap_hooks()

