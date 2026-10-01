""" Removing the nearest marker and reporting what was destroyed. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..map_editor_defs import ALL_ELEMENTS


# Functions
def write_editor_destroy() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("maps/editor/handle_destroy", f"""
# Within 3 blocks.
execute at @s unless entity @n[tag={ns}.map_element,distance=..3] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 3 blocks!","color":"red"}}]
execute at @s as @n[tag={ns}.map_element,distance=..3] run function {ns}:v{version}/maps/editor/destroy_element

# So a destroyed machine's model disappears at once.
function {ns}:v{version}/maps/editor/refresh_displays
""")

	destroy_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo.name} removed!","color":"{einfo.color}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type != "config"
	)

	write_versioned_function("maps/editor/destroy_element", f"""
# Run as the marker to destroy.
{destroy_msg_lines}

# Elements with compound data (zb_object, enemy, spawn).
execute if data entity @s data run tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"Data: ","color":"gray"}},{{"entity":"@s","nbt":"data","color":"white"}}]

kill @s
""")

