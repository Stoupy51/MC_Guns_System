""" Entering the editor for one map, and inviting everyone else into it. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..map_editor_defs import MODE_LIST


# Functions
def write_editor_enter() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	zombies_mode: int = MODE_LIST.index("zombies")

	# Macro with mode and idx.
	mode_score_lines = "\n".join(
		f'execute if data storage {ns}:temp map_edit{{mode:"{mk}"}} run scoreboard players set @s {ns}.mp.map_mode {i}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/enter", f"""
$scoreboard players set @s {ns}.mp.map_idx $(idx)
$data modify storage {ns}:temp map_edit.mode set value "$(mode)"

{mode_score_lines}

function {ns}:v{version}/maps/editor/next_session
scoreboard players set @s {ns}.mp.map_edit 1
tag @s add {ns}.map_editor

scoreboard players operation @s {ns}.mp.map_disp = @s {ns}.mp.map_mode

execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx

function {ns}:v{version}/maps/editor/load_map_data with storage {ns}:temp map_edit
data remove storage {ns}:temp map_edit.removed

# A zombies map is stored small: the markers are summoned from it whole (see map_editor/storage_format.py).
execute if score @s {ns}.mp.map_mode matches {zombies_mode} run data modify storage {ns}:temp _inf_map set from storage {ns}:temp map_edit.map
execute if score @s {ns}.mp.map_mode matches {zombies_mode} run function {ns}:v{version}/maps/inflate
execute if score @s {ns}.mp.map_mode matches {zombies_mode} run data modify storage {ns}:temp map_edit.map set from storage {ns}:temp _inf_map
data remove storage {ns}:temp _inf_map

gamemode creative @s
clear @s

# For the relative coordinates.
execute store result score #base_x {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #base_y {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #base_z {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]

execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #base_z {ns}.data
data modify storage {ns}:temp _tp.dimension set value "minecraft:overworld"
data modify storage {ns}:temp _tp.dimension set from storage {ns}:temp map_edit.map.dimension
function {ns}:v{version}/maps/editor/tp_to_map with storage {ns}:temp _tp

# Then their model displays, where the editor now stands.
execute at @s run function {ns}:v{version}/maps/editor/summon_existing
execute at @s run function {ns}:v{version}/maps/editor/refresh_displays

function {ns}:v{version}/maps/editor/give_tools

# Zombies mode only.
execute if score @s {ns}.mp.map_mode matches {zombies_mode} run function {ns}:v{version}/maps/editor/init_zb_defaults

tellraw @s [{MGS_TAG},{{"text":"Entered map editor for: ","color":"green"}},{{"text":"","color":"white"}},{{"storage":"{ns}:temp","nbt":"map_edit.map.name","interpret":true}}]
tellraw @s [{MGS_TAG},{{"text":"Place eggs to add elements. DESTROY egg (hotbar 9) removes nearest element.","color":"yellow"}}]
tellraw @s [{MGS_TAG},{{"text":"Need collaborators? ","color":"gray"}},{Dialogs.btn("Invite Players", f"/function {ns}:v{version}/players/list_editor", "aqua", "Choose who joins this editor session", action="run_command")}]
tellraw @s [{MGS_TAG},{{"text":"Use ","color":"gray"}},{Dialogs.btn("Save & Exit", f"/function {ns}:v{version}/maps/editor/save_exit", "green", "Save changes and exit editor")},{{"text":" or "}},{Dialogs.btn("Exit", f"/function {ns}:v{version}/maps/editor/exit", "red", "Discard changes and exit editor")}]
""")

	write_versioned_function("maps/editor/tp_to_map", "$execute in $(dimension) run tp @s $(x) $(y) $(z)")

	## Run as an editor: one row per online player, each with an Invite button (rows built in core/player_menus.py), and a button inviting everyone.
	write_versioned_function("players/list_editor", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"You must be in map editor to invite players.","color":"red"}}]

data modify storage {ns}:temp _plr_mode set value "editor"
data modify storage {ns}:temp _plr_iter set value []
execute as @a run function {ns}:v{version}/players/append_self

data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","👥 ",{{text:"Invite to the Editor",color:"aqua",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"Green players already edit this map. Click a name to refresh.",color:"gray"}}}}],actions:[],columns:2,pause:false,after_action:"none",exit_action:{{label:{{text:"Close",color:"gray"}}}}}}
function {ns}:v{version}/players/list_iter
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Everyone",color:"aqua"}},tooltip:{{text:"Invite every online player"}},action:{{type:"run_command",command:"/function {ns}:v{version}/maps/editor/invite_all"}}}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	write_versioned_function("maps/editor/invite_all", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"You must be in map editor to invite players.","color":"red"}}]
execute as @a unless score @s {ns}.mp.map_edit matches 1 run function {ns}:v{version}/players/editor_invite
""")

	## Run as the invited player: the session of the players already editing, their tools, and the map's base.
	write_versioned_function("players/editor_invite", f"""
execute if score @s {ns}.mp.map_edit matches 1 run return fail
execute unless entity @a[tag={ns}.map_editor] run return fail

scoreboard players operation @s {ns}.mp.map_idx = @a[tag={ns}.map_editor,limit=1] {ns}.mp.map_idx
scoreboard players operation @s {ns}.mp.map_mode = @a[tag={ns}.map_editor,limit=1] {ns}.mp.map_mode
scoreboard players operation @s {ns}.mp.map_disp = @a[tag={ns}.map_editor,limit=1] {ns}.mp.map_disp
scoreboard players set @s {ns}.mp.map_edit 1
tag @s add {ns}.map_editor

gamemode creative @s
clear @s
function {ns}:v{version}/maps/editor/give_tools

execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #base_z {ns}.data
data modify storage {ns}:temp _tp.dimension set value "minecraft:overworld"
data modify storage {ns}:temp _tp.dimension set from storage {ns}:temp map_edit.map.dimension
function {ns}:v{version}/maps/editor/tp_to_map with storage {ns}:temp _tp

tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"selector":"@s","color":"white"}},{{"text":" joined the editor session of ","color":"aqua"}},{{"storage":"{ns}:temp","nbt":"map_edit.map.name","interpret":true}}]
""")

	write_versioned_function("maps/editor/load_map_data", f"""
$data modify storage {ns}:temp map_edit.map set from storage {ns}:maps $(mode)[$(idx)]
""")

