
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function


# Default map scripts (version-dependent)
def default_scripts(ns: str, version: str) -> str:
	return (
		f'start_script:"{ns}:v{version}/maps/multiplayer/default/start",'
		f'tick_script:"{ns}:v{version}/maps/multiplayer/default/tick",'
		f'join_script:"{ns}:v{version}/maps/multiplayer/default/join",'
		f'leave_script:"{ns}:v{version}/maps/multiplayer/default/leave",'
		f'respawn_script:"{ns}:v{version}/maps/multiplayer/default/respawn"'
	)


def generate_maps() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Initialize maps storage
	write_load_file(f"""
# Initialize multiplayer maps storage (empty list, only if not set)
execute unless data storage {ns}:maps multiplayer run data modify storage {ns}:maps multiplayer set value []
""")

	## Function tag for external datapacks to register maps
	write_versioned_function("maps/multiplayer/default_maps", f"""
# Default Hijacked map (based of https://www.planetminecraft.com/project/cod-bo2-hijacked-recreation-amp-pvp-map-1-21-download/)
execute unless data storage {ns}:maps multiplayer[{{id:"hijacked"}}] run data modify storage {ns}:maps multiplayer append {{base_coordinates: [5, 118, -1], search_and_destroy: [[-9, -3, -7], [-27, -5, 4]], domination: [[-35, -5, 0], [-4, -4, 0], [29, -4, 1]], name: "Hijacked", spawning_points: {{red: [[-47, -7, 9, -86.0f], [-48, -7, 7, -87.0f], [-48, -7, 5, -98.0f], [-51, -7, 5, -97.0f], [-50, -7, 7, -89.0f], [-53, -7, 5, -87.0f], [-55, -7, 5, -99.0f], [-43, -7, -2, -96.0f], [-43, -7, 3, -89.0f], [-46, -7, 3, -87.0f], [-46, -7, -2, -94.0f], [-48, -7, -5, -88.0f], [-46, -7, -8, -93.0f], [-48, -7, -7, -94.0f], [-50, -7, -6, -101.0f], [-50, -7, -4, -85.0f], [-52, -7, -6, -110.0f], [-52, -7, -4, -77.0f], [-54, -7, -5, -104.0f], [-53, -7, 7, -94.0f], [-45, -7, 8, -103.0f], [-43, -7, -9, -94.0f], [-43, -7, 10, -94.0f]], general: [[49, -3, -1, 135.0f], [49, -3, 2, 43.0f], [39, -3, 9, 71.0f], [39, -3, -8, 102.0f], [18, -3, -1, -16.0f], [21, 1, -5, -17.0f], [11, 1, 2, -132.0f], [18, 1, -3, 30.0f], [25, -3, -8, 108.0f], [17, -3, -4, -137.0f], [22, -3, 7, 105.0f], [-5, -4, 0, -148.0f], [3, -3, -13, 103.0f], [-17, -5, -13, -101.0f], [-24, -5, -6, 50.0f], [-18, -5, -8, 116.0f], [-31, -5, 4, -95.0f], [-19, -3, 5, 168.0f], [-20, 1, -2, -59.0f], [-25, -1, 3, 36.0f], [-30, -1, 7, 160.0f], [-30, -1, -6, 18.0f], [-60, -9, 3, -39.0f], [-60, -9, -2, -139.0f], [-49, -7, -3, -118.0f], [-49, -7, 4, -71.0f], [-38, -7, -8, 125.0f], [-38, -7, 9, 94.0f], [-28, -5, 9, -78.0f], [-19, -5, 9, 78.0f], [-10, -2, 8, -65.0f], [1, -2, 8, 71.0f], [9, -3, 9, -85.0f], [25, -3, 9, 82.0f], [27, -3, 7, -130.0f], [24, -3, -5, -93.0f], [21, 1, 4, -162.0f], [1, -3, -9, -38.0f], [7, -3, -13, -68.0f], [-54, -7, 8, -107.0f], [-53, -7, -7, -75.0f], [40, -3, 6, 153.0f], [40, -3, -5, 36.0f], [-20, 1, 7, 159.0f], [-24, -5, 0, 89.0f], [-24, -10, -5, -57.0f], [-21, -10, 4, -113.0f], [-12, -10, -4, -61.0f], [1, -10, 3, 168.0f], [6, -8, 3, 155.0f], [5, -8, -5, -69.0f], [16, -8, -4, 90.0f], [10, -3, -2, -39.0f]], blue: [[49, -3, 3, 76.0f], [49, -3, -2, 101.0f], [51, -3, 2, 79.0f], [51, -3, -1, 99.0f], [53, -3, 1, 82.0f], [53, -3, 0, 89.0f], [47, -3, 5, 96.0f], [44, -3, -6, 109.0f], [44, -3, -4, 75.0f], [41, -3, -3, 89.0f], [40, -3, 2, 92.0f], [40, -3, -1, 94.0f], [41, -3, 4, 89.0f], [44, -3, 7, 88.0f], [44, -3, 5, 89.0f], [47, -3, -4, 99.0f], [40, -3, -4, 72.0f], [40, -3, 5, 104.0f], [41, -3, 9, 65.0f], [40, -3, -8, 110.0f]]}}, out_of_bounds: [[-19, -12, -17], [-29, -12, -17], [-25, -11, -18], [-23, -12, -16]], description: "Black Ops 2 | BillyWAR", boundaries: [[-72, -13, -21], [59, 22, 15]], id: "hijacked", hardpoint: []}}
""", tags=[f"{ns}:maps/register"])  # noqa: E501

	## Dynamic Map Registration (macro)
	write_versioned_function("maps/multiplayer/register_map",
f"""
# Append map from {ns}:input multiplayer.map to the maps list
# Expected format: {{id:"id", name:"Name", description:"Desc", base_coordinates:[x,y,z],
#   boundaries:[], spawning_points:{{red:[], blue:[], general:[]}},
#   out_of_bounds:[], search_and_destroy:[], domination:[], hardpoint:[],
#   start_script:"...", tick_script:"...", join_script:"...", leave_script:"...", respawn_script:"..."}}
data modify storage {ns}:maps multiplayer append from storage {ns}:input multiplayer.map
""")

	## Default map scripts (placeholders)
	write_versioned_function("maps/multiplayer/default/start", """
# Default map start script
tellraw @a [{"text":"","color":"gold"},"[",{"text":"MGS"},"] ",{"text":"Map started (default script)","color":"yellow"}]
""")
	write_versioned_function("maps/multiplayer/default/tick", "# Default map tick (no-op)")
	write_versioned_function("maps/multiplayer/default/join", """
# Default map join script
$tellraw @a [{"text":"","color":"gold"},"[",{"text":"MGS"},"] ",{"text":"$(player_name) joined the map","color":"green"}]
""")
	write_versioned_function("maps/multiplayer/default/leave", """
# Default map leave script
$tellraw @a [{"text":"","color":"gold"},"[",{"text":"MGS"},"] ",{"text":"$(player_name) left the map","color":"red"}]
""")
	write_versioned_function("maps/multiplayer/default/respawn", f"""
# Default map respawn script - teleport player to a random general spawn point
# @s = respawning player, spawn data in {ns}:temp
""")

	## Map loading with optional overrides (macro function)
	write_versioned_function("maps/multiplayer/load", f"""
# Load a map for gameplay or editing
# Usage: /function {ns}:v{version}/maps/multiplayer/load {{id:"map_id",override:{{}}}}
# Override can contain: dimension:"minecraft:overworld", base_coordinates:[x,y,z]

# Store the target ID for search
$data modify storage {ns}:temp map_load.target_id set value "$(id)"
$data modify storage {ns}:temp map_load.override set value $(override)

# Copy full map list to search through
data modify storage {ns}:temp map_load.search set from storage {ns}:maps multiplayer

# Initialize search
scoreboard players set #map_load_idx {ns}.data 0
scoreboard players set #map_load_found {ns}.data 0
function {ns}:v{version}/maps/multiplayer/find_map
""")

	## Find map by ID (iterates list)
	write_versioned_function("maps/multiplayer/find_map", f"""
# Check if the list still has elements
execute unless data storage {ns}:temp map_load.search[0] run return fail

# Copy first element to check
data modify storage {ns}:temp map_load.check set from storage {ns}:temp map_load.search[0]

# Use macro to compare IDs
function {ns}:v{version}/maps/multiplayer/check_map_id with storage {ns}:temp map_load.target_id

# If found, stop
execute if score #map_load_found {ns}.data matches 1 run return 1

# Not found, advance to next
data remove storage {ns}:temp map_load.search[0]
scoreboard players add #map_load_idx {ns}.data 1
function {ns}:v{version}/maps/multiplayer/find_map
""")

	## Check if current element's ID matches (uses macro from target_id storage)
	# target_id is stored as a raw string value, so we wrap in a compound for matching
	write_versioned_function("maps/multiplayer/check_map_id", f"""
$execute store success score #map_load_found {ns}.data if data storage {ns}:temp map_load{{check:{{id:"$(id)"}}}}
execute if score #map_load_found {ns}.data matches 1 run data modify storage {ns}:temp map_load.result set from storage {ns}:temp map_load.check

# Apply base_coordinates override if present
execute if score #map_load_found {ns}.data matches 1 if data storage {ns}:temp map_load.override.base_coordinates run data modify storage {ns}:temp map_load.result.base_coordinates set from storage {ns}:temp map_load.override.base_coordinates
""")  # noqa: E501

	## Store the index of loaded map for later use
	write_versioned_function("maps/multiplayer/store_loaded_idx", f"""
execute store result storage {ns}:temp map_load.result_idx int 1 run scoreboard players get #map_load_idx {ns}.data
""")

