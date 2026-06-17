
# Shared map loading functions (load by id, find, check, wrappers)
from ..generator import McfunctionGenerator


class SharedMapLoading(McfunctionGenerator):
	""" Writes the shared map-loading helpers (load by id with overrides, list search,
	id check) plus the per-mode load_map_from_storage wrappers. """

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## Map loading with optional overrides (macro function)
		## Usage: function shared/maps/load {id:"map_id",mode:"multiplayer",override:{}}
		self.func("shared/maps/load", f"""
$data modify storage {ns}:temp map_load.target set value {{id:"$(id)"}}
$data modify storage {ns}:temp map_load.override set value $(override)
$data modify storage {ns}:temp map_load.search set from storage {ns}:maps $(mode)

scoreboard players set #map_load_idx {ns}.data 0
scoreboard players set #map_load_found {ns}.data 0
function {ns}:v{version}/shared/maps/find_map
""")

		## Find map by ID (iterates list)
		self.func("shared/maps/find_map", f"""
execute unless data storage {ns}:temp map_load.search[0] run return fail

data modify storage {ns}:temp map_load.check set from storage {ns}:temp map_load.search[0]
function {ns}:v{version}/shared/maps/check_map_id with storage {ns}:temp map_load.target

execute if score #map_load_found {ns}.data matches 1 run return 1

data remove storage {ns}:temp map_load.search[0]
scoreboard players add #map_load_idx {ns}.data 1
function {ns}:v{version}/shared/maps/find_map
""")

		## Check if current element's ID matches (uses macro from target_id storage)
		self.func("shared/maps/check_map_id", f"""
$execute store success score #map_load_found {ns}.data if data storage {ns}:temp map_load.check{{id:"$(id)"}}
execute if score #map_load_found {ns}.data matches 1 run data modify storage {ns}:temp map_load.result set from storage {ns}:temp map_load.check

# Apply base_coordinates override if present
execute if score #map_load_found {ns}.data matches 1 if data storage {ns}:temp map_load.override.base_coordinates run data modify storage {ns}:temp map_load.result.base_coordinates set from storage {ns}:temp map_load.override.base_coordinates
""")  # noqa: E501

		# Mode-specific wrappers for loading map from storage
		for mode in ["multiplayer", "missions", "zombies"]:
			self.func(f"{mode}/load_map_from_storage", f"""
$function {ns}:v{version}/shared/maps/load {{id:"$(map_id)",mode:"{mode}",override:{{}}}}
""")


def write_shared_map_loading() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`SharedMapLoading`. """
	SharedMapLoading()()
