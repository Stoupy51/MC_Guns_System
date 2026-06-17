
# Imports

from ..helpers import MGS_TAG
from ..generator import McfunctionGenerator


class MapsGenerator(McfunctionGenerator):
    """ Generates the maps datapack functions. """

    def generate(self) -> None:
    	ns: str = self.ns
    	version: str = self.version

    	## Initialize maps storage
    	self.load(f"""
# Initialize multiplayer maps storage (empty list, only if not set)
execute unless data storage {ns}:maps multiplayer run data modify storage {ns}:maps multiplayer set value []
""")

    	## Function tag for external datapacks to register maps
    	self.func("maps/multiplayer/default_maps", f"""
# Default Hijacked map (based of https://www.planetminecraft.com/project/cod-bo2-hijacked-recreation-amp-pvp-map-1-21-download/)
execute unless data storage {ns}:maps multiplayer[{{id:"hijacked"}}] run data modify storage {ns}:maps multiplayer append value {{base_coordinates: [31, 75, -18], search_and_destroy: [[-9, -3, -7], [-27, -5, 4]], domination: [[-35, -5, 0], [-4, -4, 0], [29, -4, 1]], name: "Hijacked", spawning_points: {{red: [[-47, -7, 9, -86.0f], [-48, -7, 7, -87.0f], [-48, -7, 5, -98.0f], [-51, -7, 5, -97.0f], [-50, -7, 7, -89.0f], [-53, -7, 5, -87.0f], [-55, -7, 5, -99.0f], [-43, -7, -2, -96.0f], [-43, -7, 3, -89.0f], [-46, -7, 3, -87.0f], [-46, -7, -2, -94.0f], [-48, -7, -5, -88.0f], [-46, -7, -8, -93.0f], [-48, -7, -7, -94.0f], [-50, -7, -6, -101.0f], [-50, -7, -4, -85.0f], [-52, -7, -6, -110.0f], [-52, -7, -4, -77.0f], [-54, -7, -5, -104.0f], [-53, -7, 7, -94.0f], [-45, -7, 8, -103.0f], [-43, -7, -9, -94.0f], [-43, -7, 10, -94.0f]], general: [[49, -3, -1, 135.0f], [49, -3, 2, 43.0f], [39, -3, 9, 71.0f], [39, -3, -8, 102.0f], [18, -3, -1, -16.0f], [21, 1, -5, -17.0f], [11, 1, 2, -132.0f], [18, 1, -3, 30.0f], [25, -3, -8, 108.0f], [17, -3, -4, -137.0f], [22, -3, 7, 105.0f], [-5, -4, 0, -148.0f], [3, -3, -13, 103.0f], [-17, -5, -13, -101.0f], [-24, -5, -6, 50.0f], [-18, -5, -8, 116.0f], [-31, -5, 4, -95.0f], [-19, -3, 5, 168.0f], [-20, 1, -2, -59.0f], [-25, -1, 3, 36.0f], [-30, -1, 7, 160.0f], [-30, -1, -6, 18.0f], [-60, -9, 3, -39.0f], [-60, -9, -2, -139.0f], [-49, -7, -3, -118.0f], [-49, -7, 4, -71.0f], [-38, -7, -8, 125.0f], [-38, -7, 9, 94.0f], [-28, -5, 9, -78.0f], [-19, -5, 9, 78.0f], [-10, -2, 8, -65.0f], [1, -2, 8, 71.0f], [9, -3, 9, -85.0f], [25, -3, 9, 82.0f], [27, -3, 7, -130.0f], [24, -3, -5, -93.0f], [21, 1, 4, -162.0f], [1, -3, -9, -38.0f], [7, -3, -13, -68.0f], [-54, -7, 8, -107.0f], [-53, -7, -7, -75.0f], [40, -3, 6, 153.0f], [40, -3, -5, 36.0f], [-20, 1, 7, 159.0f], [-24, -5, 0, 89.0f], [-24, -10, -5, -57.0f], [-21, -10, 4, -113.0f], [-12, -10, -4, -61.0f], [1, -10, 3, 168.0f], [6, -8, 3, 155.0f], [5, -8, -5, -69.0f], [16, -8, -4, 90.0f], [10, -3, -2, -39.0f]], blue: [[49, -3, 3, 76.0f], [49, -3, -2, 101.0f], [51, -3, 2, 79.0f], [51, -3, -1, 99.0f], [53, -3, 1, 82.0f], [53, -3, 0, 89.0f], [47, -3, 5, 96.0f], [44, -3, -6, 109.0f], [44, -3, -4, 75.0f], [41, -3, -3, 89.0f], [40, -3, 2, 92.0f], [40, -3, -1, 94.0f], [41, -3, 4, 89.0f], [44, -3, 7, 88.0f], [44, -3, 5, 89.0f], [47, -3, -4, 99.0f], [40, -3, -4, 72.0f], [40, -3, 5, 104.0f], [41, -3, 9, 65.0f], [40, -3, -8, 110.0f]]}}, out_of_bounds: [[-19, -12, -17], [-29, -12, -17], [-25, -11, -18], [-23, -12, -16]], description: "Black Ops 2 | BillyWAR", boundaries: [[-72, -13, -21], [59, 22, 15]], id: "hijacked", hardpoint: [[-4, -4, 0], [-5, -10, -1], [-27, -5, 3], [15, 1, -1]]}}
""", tags=[f"{ns}:maps/register"])  # noqa: E501

    	## Dynamic Map Registration (macro)
    	self.func("maps/multiplayer/register_map", f"""
# Append map from {ns}:input multiplayer.map to the maps list
# Expected format: {{id:"id", name:"Name", description:"Desc", base_coordinates:[x,y,z],
#   boundaries:[], spawning_points:{{red:[], blue:[], general:[]}},
#   out_of_bounds:[], search_and_destroy:[], domination:[], hardpoint:[]}}
data modify storage {ns}:maps multiplayer append from storage {ns}:input multiplayer.map
""")

    	## Store the index of loaded map for later use
    	self.func("maps/multiplayer/store_loaded_idx", f"""
execute store result storage {ns}:temp map_load.result_idx int 1 run scoreboard players get #map_load_idx {ns}.data
""")

    	# ── Hijacked map scripts ────────────────────────────────────────────────────
    	# Logic functions (actual work)
    	self.func("maps/multiplayer/hijacked/start", f"""
# Hijacked map start script
tellraw @a [{MGS_TAG},{{"text":"Welcome to Hijacked!","color":"yellow"}}]
""")
    	self.func("maps/multiplayer/hijacked/tick", "# Hijacked map tick (no-op placeholder)")
    	self.func("maps/multiplayer/hijacked/join", f"""
# Hijacked map join script
tellraw @a [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" joined Hijacked","color":"green"}}]
""")
    	self.func("maps/multiplayer/hijacked/leave", f"""
# Hijacked map leave script
tellraw @a [{MGS_TAG},{{"selector":"@s","color":"red"}},{{"text":" left Hijacked","color":"red"}}]
""")
    	self.func("maps/multiplayer/hijacked/respawn", """
# Hijacked map respawn script
# @s = respawning player
""")

    	# Calls functions — guard then delegate, registered to the shared function tags
    	guard_mp_hijacked: str = (
    		f'execute if data storage {ns}:multiplayer game{{state:"active"}}'
    		f' if data storage {ns}:multiplayer game{{map_id:"hijacked"}}'
    	)
    	for script in ["start", "tick", "join", "leave", "respawn"]:
    		self.func(f"maps/multiplayer/hijacked/calls/{script}",
    			f"{guard_mp_hijacked} run return run function {ns}:v{version}/maps/multiplayer/hijacked/{script}",
    			tags=[f"{ns}:maps/{script}_script"]
    		)


def generate_maps() -> None:
	""" Module-level entry (preserved signature); delegates to :class:`MapsGenerator`. """
	MapsGenerator()()


