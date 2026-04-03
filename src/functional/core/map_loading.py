
# Shared map loading functions (load by id, find, check)
from stewbeet import Mem, write_versioned_function


def write_shared_map_loading() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Map loading with optional overrides (macro function)
	## Usage: function shared/maps/load {id:"map_id",mode:"multiplayer",override:{}}
	write_versioned_function("shared/maps/load", f"""
$data modify storage {ns}:temp map_load.target set value {{id:"$(id)"}}
$data modify storage {ns}:temp map_load.override set value $(override)
$data modify storage {ns}:temp map_load.search set from storage {ns}:maps $(mode)

scoreboard players set #map_load_idx {ns}.data 0
scoreboard players set #map_load_found {ns}.data 0
function {ns}:v{version}/shared/maps/find_map
""")

	## Find map by ID (iterates list)
	write_versioned_function("shared/maps/find_map", f"""
execute unless data storage {ns}:temp map_load.search[0] run return fail

data modify storage {ns}:temp map_load.check set from storage {ns}:temp map_load.search[0]
function {ns}:v{version}/shared/maps/check_map_id with storage {ns}:temp map_load.target

execute if score #map_load_found {ns}.data matches 1 run return 1

data remove storage {ns}:temp map_load.search[0]
scoreboard players add #map_load_idx {ns}.data 1
function {ns}:v{version}/shared/maps/find_map
""")

	## Check if current element's ID matches (uses macro from target_id storage)
	write_versioned_function("shared/maps/check_map_id", f"""
$execute store success score #map_load_found {ns}.data if data storage {ns}:temp map_load.check{{id:"$(id)"}}
execute if score #map_load_found {ns}.data matches 1 run data modify storage {ns}:temp map_load.result set from storage {ns}:temp map_load.check

# Apply base_coordinates override if present
execute if score #map_load_found {ns}.data matches 1 if data storage {ns}:temp map_load.override.base_coordinates run data modify storage {ns}:temp map_load.result.base_coordinates set from storage {ns}:temp map_load.override.base_coordinates
""")  # noqa: E501

