""" Built-in multiplayer maps and map registration. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function


# Functions
def generate_maps() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Initialize maps storage
	write_load_file(f"""
# Initialize multiplayer maps storage (empty list, only if not set)
execute unless data storage {ns}:maps multiplayer run data modify storage {ns}:maps multiplayer set value []
""")

	## Function tag for external datapacks to register maps
	hijacked_map: str = r"""{base_coordinates: [31, 75, -18], search_and_destroy: [[-9, -3, -7], [-27, -5, 4]], domination: [[-35, -5, 0], [-4, -4, 0], [29, -4, 1]], name: "Hijacked", spawning_points: {red: [[-47, -7, 9, -86.0f], [-48, -7, 7, -87.0f], [-48, -7, 5, -98.0f], [-51, -7, 5, -97.0f], [-50, -7, 7, -89.0f], [-53, -7, 5, -87.0f], [-55, -7, 5, -99.0f], [-43, -7, -2, -96.0f], [-43, -7, 3, -89.0f], [-46, -7, 3, -87.0f], [-46, -7, -2, -94.0f], [-48, -7, -5, -88.0f], [-46, -7, -8, -93.0f], [-48, -7, -7, -94.0f], [-50, -7, -6, -101.0f], [-50, -7, -4, -85.0f], [-52, -7, -6, -110.0f], [-52, -7, -4, -77.0f], [-54, -7, -5, -104.0f], [-53, -7, 7, -94.0f], [-45, -7, 8, -103.0f], [-43, -7, -9, -94.0f], [-43, -7, 10, -94.0f]], general: [[49, -3, -1, 135.0f], [49, -3, 2, 43.0f], [39, -3, 9, 71.0f], [39, -3, -8, 102.0f], [18, -3, -1, -16.0f], [21, 1, -5, -17.0f], [11, 1, 2, -132.0f], [18, 1, -3, 30.0f], [25, -3, -8, 108.0f], [17, -3, -4, -137.0f], [22, -3, 7, 105.0f], [-5, -4, 0, -148.0f], [3, -3, -13, 103.0f], [-17, -5, -13, -101.0f], [-24, -5, -6, 50.0f], [-18, -5, -8, 116.0f], [-31, -5, 4, -95.0f], [-19, -3, 5, 168.0f], [-20, 1, -2, -59.0f], [-25, -1, 3, 36.0f], [-30, -1, 7, 160.0f], [-30, -1, -6, 18.0f], [-60, -9, 3, -39.0f], [-60, -9, -2, -139.0f], [-49, -7, -3, -118.0f], [-49, -7, 4, -71.0f], [-38, -7, -8, 125.0f], [-38, -7, 9, 94.0f], [-28, -5, 9, -78.0f], [-19, -5, 9, 78.0f], [-10, -2, 8, -65.0f], [1, -2, 8, 71.0f], [9, -3, 9, -85.0f], [25, -3, 9, 82.0f], [27, -3, 7, -130.0f], [24, -3, -5, -93.0f], [21, 1, 4, -162.0f], [1, -3, -9, -38.0f], [7, -3, -13, -68.0f], [-54, -7, 8, -107.0f], [-53, -7, -7, -75.0f], [40, -3, 6, 153.0f], [40, -3, -5, 36.0f], [-20, 1, 7, 159.0f], [-24, -5, 0, 89.0f], [-24, -10, -5, -57.0f], [-21, -10, 4, -113.0f], [-12, -10, -4, -61.0f], [1, -10, 3, 168.0f], [6, -8, 3, 155.0f], [5, -8, -5, -69.0f], [16, -8, -4, 90.0f], [10, -3, -2, -39.0f]], blue: [[49, -3, 3, 76.0f], [49, -3, -2, 101.0f], [51, -3, 2, 79.0f], [51, -3, -1, 99.0f], [53, -3, 1, 82.0f], [53, -3, 0, 89.0f], [47, -3, 5, 96.0f], [44, -3, -6, 109.0f], [44, -3, -4, 75.0f], [41, -3, -3, 89.0f], [40, -3, 2, 92.0f], [40, -3, -1, 94.0f], [41, -3, 4, 89.0f], [44, -3, 7, 88.0f], [44, -3, 5, 89.0f], [47, -3, -4, 99.0f], [40, -3, -4, 72.0f], [40, -3, 5, 104.0f], [41, -3, 9, 65.0f], [40, -3, -8, 110.0f]]}, out_of_bounds: [[-19, -12, -17], [-29, -12, -17], [-25, -11, -18], [-23, -12, -16]], description: "Black Ops 2 | BillyWAR", boundaries: [[-72, -13, -21], [59, 22, 15]], id: "hijacked", hardpoint: [[-4, -4, 0], [-5, -10, -1], [-27, -5, 3], [15, 1, -1]]}"""  # noqa: E501
	highrise_map: str = r"""{base_coordinates: [336, 123, 332], search_and_destroy: [[4, -7, -17], [20, -7, 6]], domination: [[72, -6, -23], [5, -7, -17], [-56, -6, 19]], name: "Highrise", spawning_points: {red: [[78, -6, -36, 90.0f], [78, -6, -34, 90.0f], [78, -6, -32, 90.0f], [76, -6, -31, 90.0f], [76, -6, -33, 90.0f], [76, -6, -35, 90.0f], [74, -6, -36, 90.0f], [74, -6, -34, 90.0f], [74, -6, -32, 90.0f], [74, -6, -30, 90.0f], [72, -6, -30, 90.0f], [72, -6, -32, 90.0f], [72, -6, -34, 90.0f], [72, -6, -36, 90.0f], [70, -6, -36, 90.0f], [70, -6, -34, 90.0f], [70, -6, -32, 90.0f], [71, -6, -28, 0.0f], [74, -6, -26, 0.0f], [70, -6, -26, 0.0f], [70, -6, -24, 0.0f], [74, -6, -24, 0.0f], [74, -6, -22, 0.0f], [74, -6, -16, 90.0f], [70, -6, -17, 0.0f]], general: [[-65, -6, 27, 180.0f], [-51, -6, 15, 90.0f], [-67, -6, 8, 180.0f], [-67, -6, -26, 0.0f], [-55, -11, -22, 180.0f], [-56, -11, -28, 270.0f], [-45, -11, -27, 180.0f], [-46, -11, -18, 270.0f], [-30, -11, -17, 180.0f], [-43, -6, -19, 270.0f], [-61, -6, -17, 0.0f], [-50, -6, 0, 90.0f], [-39, -6, -17, 180.0f], [-37, -6, 9, 180.0f], [-43, -6, 28, 180.0f], [-49, -6, 22, 270.0f], [-41, -6, 20, 90.0f], [-41, -6, 11, 180.0f], [-6, -11, 31, 90.0f], [31, -11, 26, 90.0f], [-23, -7, 3, 180.0f], [-17, -7, 14, 90.0f], [-27, -7, 6, 270.0f], [-22, -7, 18, 270.0f], [-16, -7, -8, 180.0f], [-26, -7, -11, 180.0f], [-26, -7, -23, 90.0f], [-16, -7, -25, 270.0f], [-9, -7, -34, 180.0f], [-4, -7, -36, 270.0f], [6, -7, -36, 90.0f], [-3, -7, -32, 180.0f], [3, -7, -32, 0.0f], [-14, -7, 6, 180.0f], [-5, -7, 20, 90.0f], [3, -7, 15, 180.0f], [3, -7, 18, 0.0f], [3, -11, -4, 90.0f], [21, -11, -8, 90.0f], [3, -11, -21, 270.0f], [36, -11, -18, 0.0f], [45, -11, -11, 180.0f], [52, -11, -20, 270.0f], [57, -6, -18, 270.0f], [75, -6, -18, 90.0f], [79, -6, -30, 90.0f], [69, -6, -29, 270.0f], [41, -6, -35, 0.0f], [58, -6, -26, 90.0f], [66, -6, -30, 90.0f], [0, -2, 25, 180.0f], [27, -7, 14, 0.0f], [12, -7, 15, 90.0f], [9, -7, -13, 90.0f], [0, -7, -21, 270.0f], [38, 1, -35, 180.0f], [37, 1, -16, 0.0f], [37, 1, 8, 180.0f], [41, -6, 28, 270.0f], [54, -6, 8, 90.0f], [36, -6, -17, 0.0f], [57, -6, -16, 180.0f], [55, -6, -17, 180.0f], [32, -7, 18, 180.0f], [45, -6, -9, 180.0f], [5, -7, -1, 270.0f], [2, -7, 29, 90.0f], [-38, 2, -27, 180.0f], [0, -3, -33, 180.0f]], blue: [[-65, -6, 28, 180.0f], [-67, -6, 28, 180.0f], [-65, -6, 26, 180.0f], [-67, -6, 26, 180.0f], [-67, -6, 23, 270.0f], [-65, -6, 24, 270.0f], [-65, -6, 22, 270.0f], [-63, -6, 23, 270.0f], [-63, -6, 21, 270.0f], [-61, -6, 23, 270.0f], [-61, -6, 21, 270.0f], [-59, -6, 23, 270.0f], [-59, -6, 21, 270.0f], [-59, -6, 19, 270.0f], [-57, -6, 22, 225.0f], [-58, -6, 19, 225.0f], [-58, -6, 16, 225.0f], [-55, -6, 18, 270.0f], [-55, -6, 20, 270.0f], [-55, -6, 22, 270.0f]]}, out_of_bounds: [], description: "Modern Warfare 2 | N11cK", boundaries: [[97, 16, 35], [-99, -17, -78]], id: "highrise", respawn_commands: [], hardpoint: [[5, -7, -17], [-54, -6, -3], [47, -6, -4], [0, -1, 12], [0, -11, -1]], start_commands: []}"""  # noqa: E501
	write_versioned_function("maps/multiplayer/default_maps", f"""
# Default Hijacked map (based of https://www.planetminecraft.com/project/cod-bo2-hijacked-recreation-amp-pvp-map-1-21-download/)
execute unless data storage {ns}:maps multiplayer[{{id:"hijacked"}}] run data modify storage {ns}:maps multiplayer append value {hijacked_map}

# Default highrise map (based of https://www.planetminecraft.com/member/niicknumber1/submissions/)
execute unless data storage {ns}:maps multiplayer[{{id:"highrise"}}] run data modify storage {ns}:maps multiplayer append value {highrise_map}
""", tags=[f"{ns}:maps/register"])

	## Dynamic Map Registration (macro)
	write_versioned_function("maps/multiplayer/register_map", f"""
# Append map from {ns}:input multiplayer.map to the maps list
# Expected format: {{id:"id", name:"Name", description:"Desc", base_coordinates:[x,y,z],
#   boundaries:[], spawning_points:{{red:[], blue:[], general:[]}},
#   out_of_bounds:[], search_and_destroy:[], domination:[], hardpoint:[]}}
data modify storage {ns}:maps multiplayer append from storage {ns}:input multiplayer.map
""")

	## Store the index of loaded map for later use
	write_versioned_function("maps/multiplayer/store_loaded_idx", f"""
execute store result storage {ns}:temp map_load.result_idx int 1 run scoreboard players get #map_load_idx {ns}.data
""")

	# ── Hijacked map scripts.
	# Logic functions (actual work)
	write_versioned_function("maps/multiplayer/hijacked/start", "# Hijacked map start script")
	write_versioned_function("maps/multiplayer/hijacked/tick", "# Hijacked map tick")
	write_versioned_function("maps/multiplayer/hijacked/join", "# Hijacked map join")
	write_versioned_function("maps/multiplayer/hijacked/leave", "# Hijacked map leave")
	write_versioned_function("maps/multiplayer/hijacked/respawn", "# Hijacked map respawn")

	# Calls functions — guard then delegate, registered to the shared function tags
	guard_mp_hijacked: str = (
		f'execute if data storage {ns}:multiplayer game{{state:"active"}}'
		f' if data storage {ns}:multiplayer game{{map_id:"hijacked"}}'
	)
	for script in ["start", "tick", "join", "leave", "respawn"]:
		write_versioned_function(f"maps/multiplayer/hijacked/calls/{script}",
			f"{guard_mp_hijacked} run return run function {ns}:v{version}/maps/multiplayer/hijacked/{script}",
			tags=[f"{ns}:maps/{script}_script"]
		)

