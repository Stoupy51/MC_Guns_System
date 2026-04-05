
# ruff: noqa: E501
# Shared helper for spawning item_display entities at machine positions.
# Used by perks, PAP, and any other zombies machine system.
from stewbeet import Mem, write_versioned_function


def generate_display_helpers() -> None:
	ns: str = Mem.ctx.project_id
	#version: str = Mem.ctx.project_version

	# Common macro: spawn a fixed item_display at the caller entity's position.
	# Must be called via `execute as <entity> at @s run function ...`.
	# Args: $(tag) - entity tag, $(item_id) - minecraft item id, $(item_model) - item_model component value.
	write_versioned_function("zombies/display/summon_machine_display", f"""
$summon minecraft:item_display ~ ~1.0 ~ {{Tags:["$(tag)","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"$(item_id)",count:1,components:{{"minecraft:item_model":"$(item_model)"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.85f,0.85f,0.85f]}}}}
""")

