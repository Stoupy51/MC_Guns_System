""" Entering the editor for one map, and inviting everyone else into it. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..map_editor_defs import MODE_LIST


# Functions
def write_editor_enter() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Enter Editor Mode (macro with mode+idx).
	mode_score_lines = "\n".join(
		f'execute if data storage {ns}:temp map_edit{{mode:"{mk}"}} run scoreboard players set @s {ns}.mp.map_mode {i}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/enter", f"""
# Store mode and index
$scoreboard players set @s {ns}.mp.map_idx $(idx)
$data modify storage {ns}:temp map_edit.mode set value "$(mode)"

# Set mode score from mode string
{mode_score_lines}

# Mark player as in editor mode
scoreboard players set @s {ns}.mp.map_edit 1
tag @s add {ns}.map_editor

# Set display mode to match save mode
scoreboard players operation @s {ns}.mp.map_disp = @s {ns}.mp.map_mode

# Store index for macro access
execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx

# Load map data
function {ns}:v{version}/maps/editor/load_map_data with storage {ns}:temp map_edit

# Switch to creative, clear inventory
gamemode creative @s
clear @s

# Load base_coordinates into scores for relative computation
execute store result score #base_x {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #base_y {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #base_z {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]

# Teleport to base coordinates
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #base_z {ns}.data
function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

# Summon markers for existing elements, then build their model displays
function {ns}:v{version}/maps/editor/summon_existing
function {ns}:v{version}/maps/editor/refresh_displays

# Give editor tools (dispatch by mode)
function {ns}:v{version}/maps/editor/give_tools

# Initialize zombies element defaults (only for zombies mode)
execute if score @s {ns}.mp.map_mode matches {MODE_LIST.index("zombies")} run function {ns}:v{version}/maps/editor/init_zb_defaults

# Announce
tellraw @s [{MGS_TAG},{{"text":"Entered map editor for: ","color":"green"}},{{"text":"","color":"white"}},{{"storage":"{ns}:temp","nbt":"map_edit.map.name","interpret":true}}]
tellraw @s [{MGS_TAG},{{"text":"Place eggs to add elements. DESTROY egg (hotbar 9) removes nearest element.","color":"yellow"}}]
tellraw @s [{MGS_TAG},{{"text":"Need collaborators? ","color":"gray"}},{Dialogs.btn("Invite All Players", f"/function {ns}:v{version}/maps/editor/invite_all", "aqua", "Put all online players into this editor session")}]
tellraw @s [{MGS_TAG},{{"text":"Use ","color":"gray"}},{Dialogs.btn("Save & Exit", f"/function {ns}:v{version}/maps/editor/save_exit", "green", "Save changes and exit editor")},{{"text":" or "}},{Dialogs.btn("Exit", f"/function {ns}:v{version}/maps/editor/exit", "red", "Discard changes and exit editor")}]
""")

	write_versioned_function("maps/editor/invite_all", f"""
# Must be called by a player already in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"You must be in map editor to invite players.","color":"red"}}]

# Share caller's editor session state with everyone not currently editing
scoreboard players set @a {ns}.mp.map_edit 1
scoreboard players operation @a[scores={{{ns}.mp.map_edit=1}}] {ns}.mp.map_idx = @s {ns}.mp.map_idx
scoreboard players operation @a[scores={{{ns}.mp.map_edit=1}}] {ns}.mp.map_mode = @s {ns}.mp.map_mode
scoreboard players operation @a[scores={{{ns}.mp.map_edit=1}}] {ns}.mp.map_disp = @s {ns}.mp.map_disp
tag @a[scores={{{ns}.mp.map_edit=1}}] add {ns}.map_editor

# Put invited players in creative and sync inventory/tools
gamemode creative @a[scores={{{ns}.mp.map_edit=1}}]
clear @a[scores={{{ns}.mp.map_edit=1}}]
execute as @a[scores={{{ns}.mp.map_edit=1}}] run function {ns}:v{version}/maps/editor/give_tools

# Teleport invited players to current base coordinates
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #base_z {ns}.data
execute as @a[scores={{{ns}.mp.map_edit=1}}] run function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

tellraw @a[scores={{{ns}.mp.map_edit=1}}] [{MGS_TAG},{{"text":"Editor session synced for all players.","color":"aqua"}}]
""")

	write_versioned_function("maps/editor/load_map_data", f"""
$data modify storage {ns}:temp map_edit.map set from storage {ns}:maps $(mode)[$(idx)]
""")

