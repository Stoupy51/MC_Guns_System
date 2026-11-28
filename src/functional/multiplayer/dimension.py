""" The mgs:multiplayer dimension: an empty overworld-like world with a clock of its own.

The public lobby is built in it; nothing assumes that a multiplayer map lives here.
"""
# Imports
from beet.contrib.worldgen import Dimension, DimensionType
from beet.library.data_pack import WorldClock
from stewbeet import Mem


# Functions
def generate_multiplayer_dimension() -> None:
	ns: str = Mem.ctx.project_id
	Mem.ctx.require("beet.contrib.worldgen")

	# Its own clock, so /time in a multiplayer match never reaches the overworld.
	Mem.ctx.data[f"{ns}:multiplayer"] = WorldClock({})
	Mem.ctx.data[f"{ns}:multiplayer"] = DimensionType({
		"ambient_light": 0.0,
		"attributes": {
			"minecraft:gameplay/monsters_burn": False,
			"minecraft:visual/ambient_light_color": "#0a0a0a",
			"minecraft:visual/cloud_color": "#ccffffff",
			"minecraft:visual/cloud_height": 192.33,
			"minecraft:visual/fog_color": "#c0d8ff",
			"minecraft:visual/sky_color": "#78a7ff"
		},
		"coordinate_scale": 1.0,
		"default_clock": f"{ns}:multiplayer",
		"has_ceiling": False,
		"has_ender_dragon_fight": False,
		"has_skylight": True,
		"height": 384,
		"infiniburn": "#minecraft:infiniburn_overworld",
		"logical_height": 384,
		"min_y": -64,
		"monster_spawn_block_light_limit": 0,
		"monster_spawn_light_level": 0,
	})
	Mem.ctx.data[f"{ns}:multiplayer"] = Dimension({
		"type": f"{ns}:multiplayer",
		"generator": {
			"type": "minecraft:flat",
			"settings": {"biome": "minecraft:plains", "layers": [], "lakes": False, "features": False, "structure_overrides": []},
		},
	})

