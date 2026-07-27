""" Wandering-trader pathfinding taxi for stuck zombies.

Zombie A* fails over long or complex routes (PathNavigation.java) and the zombie strolls randomly.
A trader's `wander_target` NBT drives WanderToPositionGoal, which re-paths in 10-block segments, so
it crosses any map. An escort is an invisible trader summoned at the zombie, with the zombie frozen
(NoAI) and glued to it until a player is close and visible.

Trader gotchas (verified in minecraft_source_code):
- AvoidEntityGoal(Zombie, 8) outranks WanderToPositionGoal and zombies target AbstractVillager;
  both fail for ALLIED entities, hence the shared horde team.
- WanderToPositionGoal.stop() nulls wander_target, so it is re-applied every second.
- The goal walks at 0.35 * movement_speed; trader base speed is zombie_speed / 0.35.
- DespawnDelay:0 never despawns, Offers:{Recipes:[]} makes right-click a no-op, and traders tp
  1000 blocks down before the kill so the death poof is invisible. """
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

