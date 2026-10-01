""" Wandering-trader pathfinding taxi: stuck zombies, monkey bombs, the PaP lure and walk-to spawns.

Zombie A* fails over long or complex routes (PathNavigation.java), and the zombie then strolls randomly.
A trader's `wander_target` drives WanderToPositionGoal, which re-paths in 10-block segments and so crosses any map.
An escort is an invisible trader summoned at the zombie, with the zombie frozen (NoAI) and glued to it until a player is close and visible.

Trader details (checked in the Minecraft source):
- AvoidEntityGoal(Zombie, 8) outranks WanderToPositionGoal, and zombies target AbstractVillager; both fail between allies, hence the shared horde team.
- WanderToPositionGoal.stop() nulls wander_target, so it is re-applied every second.
- The goal walks at 0.35 x movement_speed, so the trader's base speed is zombie speed / 0.35.
- DespawnDelay:0 never despawns, Offers:{Recipes:[]} makes right-click do nothing, and traders are moved 1000 blocks down before the kill so the death poof is invisible.
"""
# Imports
from .end import write_escort_end
from .hooks import write_escort_hooks
from .lure import write_escort_lure
from .start import write_escort_start
from .targeting import write_escort_targeting
from .tick import write_escort_tick


# Functions
def generate_zombies_escort() -> None:
	write_escort_start()
	write_escort_targeting()
	write_escort_tick()
	write_escort_end()
	write_escort_lure()
	write_escort_hooks()

