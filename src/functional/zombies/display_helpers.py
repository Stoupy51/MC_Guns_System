
# ruff: noqa: E501
# Shared helper for spawning item_display entities at machine positions.
# Used by perks, PAP, and any other zombies machine system.
from stewbeet import Mem, write_versioned_function
from ..generator import McfunctionGenerator


class DisplayHelpersGenerator(McfunctionGenerator):
    """ Generates the displayhelpers datapack functions. """

    def generate(self) -> None:
    	ns: str = self.ns
    	#version: str = self.version

    	# Common macro: spawn a fixed item_display at the caller entity's position.
    	# Must be called via `execute as <entity> at @s run function ...`.
    	# Args: $(tag) - entity tag, $(item_id) - minecraft item id, $(item_model) - item_model component value, $(yaw) - facing rotation.
    	self.func("zombies/display/summon_machine_display", f"""
$summon minecraft:item_display ~ ~1.0 ~ {{Rotation:[$(yaw)f,0f],Tags:["$(tag)","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"$(item_id)",count:1,components:{{"minecraft:item_model":"$(item_model)"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.25f,1.25f,1.25f]}}}}
""")


def generate_display_helpers() -> None:
	""" Module-level entry (preserved signature); delegates to :class:`DisplayHelpersGenerator`. """
	DisplayHelpersGenerator()()


