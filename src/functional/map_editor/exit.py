""" Leaving the editor without saving, and the cleanup that follows. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


# Functions
def write_editor_exit() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Exit Without Saving.
	write_versioned_function("maps/editor/exit", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return fail
function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Exited map editor (changes discarded).","color":"red"}}]
""")

	# Cleanup (shared by save_exit and exit).
	write_versioned_function("maps/editor/cleanup", f"""
# Kill all editor markers and model displays
kill @e[tag={ns}.map_element]
kill @e[tag={ns}.editor_display]

# Reset editor state
scoreboard players set @s {ns}.mp.map_edit 0
tag @s remove {ns}.map_editor

# Clear editor tools
clear @s
""")

