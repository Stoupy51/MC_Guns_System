""" The mgs:zombies dimension: an empty world frozen at midnight, with a clock of its own.

A map is placed in it by recording its dimension in the editor; nothing assumes that a zombies map lives here.
"""
# Imports
from beet.contrib.worldgen import Dimension, DimensionType
from beet.library.data_pack import WorldClock
from stewbeet import Mem

# Constants
MIDNIGHT_ATTRIBUTES: dict[str, object] = {
	"minecraft:gameplay/monsters_burn": False,
	"minecraft:gameplay/sky_light_level": 4.0,
	"minecraft:visual/sky_color": "#000000",
	"minecraft:visual/fog_color": "#0b0d16",
	"minecraft:visual/cloud_color": "#cc191926",
	"minecraft:visual/sky_light_color": "#7a7aff",
	"minecraft:visual/sky_light_factor": 0.24,
	"minecraft:visual/star_brightness": 0.5,
	"minecraft:visual/sun_angle": 180.0,
	"minecraft:visual/moon_angle": 360.0,
	"minecraft:visual/star_angle": 180.0,
}
""" The overworld's `minecraft:day` timeline read at tick 18000, applied to its base attributes. """


# Functions
def generate_zombies_dimension() -> None:
	ns: str = Mem.ctx.project_id
	Mem.ctx.require("beet.contrib.worldgen")

	# Its own clock, so /time and its pause in a zombies run never reach the overworld.
	Mem.ctx.data[f"{ns}:zombies"] = WorldClock({})
	Mem.ctx.data[f"{ns}:zombies"] = DimensionType({
		"ambient_light": 0.0,
		"attributes": MIDNIGHT_ATTRIBUTES,
		"coordinate_scale": 1.0,
		"default_clock": f"{ns}:zombies",
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
	Mem.ctx.data[f"{ns}:zombies"] = Dimension({
		"type": f"{ns}:zombies",
		"generator": {
			"type": "minecraft:flat",
			"settings": {"biome": "minecraft:the_void", "layers": [], "lakes": False, "features": False, "structure_overrides": []},
		},
	})

