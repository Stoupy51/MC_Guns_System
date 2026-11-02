""" Loading a map by id into {ns}:temp map_load.result. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_shared_map_loading() -> None:
		ns: str = Mem.ctx.project_id

		# Copies only the map asked for: a mode's whole list would be copied into temp storage and left there.
		for mode in ["multiplayer", "missions", "zombies"]:
			write_versioned_function(f"{mode}/load_map_from_storage", f"""
data remove storage {ns}:temp map_load
$execute store success score #map_load_found {ns}.data run data modify storage {ns}:temp map_load.result set from storage {ns}:maps {mode}[{{id:"$(map_id)"}}]
""")

