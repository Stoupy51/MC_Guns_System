""" Spawn markers and picking one to respawn at. """
# Imports
from stewbeet import write_versioned_function

from ...core.spawning import CoreSpawning


# Functions
def write_missions_spawns() -> None:
	# Spawn Point Markers.
	write_versioned_function("missions/summon_spawns", f"""
# Mission spawns
{CoreSpawning.spawn_category_lines("missions", "mission", "spawn_mission")}
""")

	CoreSpawning.write_array_spawn_iter("missions")
	CoreSpawning.write_summon_spawn_at("missions")

	# Smart Spawn Teleportation.
	CoreSpawning.write_random_spawn_selection("missions", "spawn_mission", "mi.in_game")
