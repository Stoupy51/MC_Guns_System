""" Leaving the editor without saving, and the cleanup that follows. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


# Functions
def write_editor_exit() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("maps/editor/exit", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return fail
function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Exited map editor (changes discarded).","color":"red"}}]
""")

	# Shared by save_exit and exit.
	write_versioned_function("maps/editor/cleanup", f"""
scoreboard players set @s {ns}.mp.map_edit 0
tag @s remove {ns}.map_editor

# The other editors keep the session, its markers and its loaded chunks.
execute unless entity @a[tag={ns}.map_editor] run kill @e[tag={ns}.map_element]
execute unless entity @a[tag={ns}.map_editor] run kill @e[tag={ns}.editor_display]
execute unless entity @a[tag={ns}.map_editor] run function {ns}:v{version}/maps/editor/force_unload with storage {ns}:temp map_edit.force
function {ns}:v{version}/maps/editor/next_session
execute unless entity @a[scores={{{ns}.mp.map_edit=1}}] run data remove storage {ns}:temp map_edit

clear @s
""")

