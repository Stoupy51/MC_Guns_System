""" Entering the editor for one map, and inviting everyone else into it. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..map_editor_defs import MODE_LIST

# Constants
FORCE_RADIUS: int = 112
""" Blocks around a map's base kept loaded while it is edited: 15 by 15 chunks, under the 256 a forceload command takes. """


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
# One session at a time: a second editor joins it, on its own map only.
$execute if entity @a[tag={ns}.map_editor] if data storage {ns}:temp map_edit{{mode:"$(mode)",idx:$(idx)}} run return run function {ns}:v{version}/players/editor_invite
execute if entity @a[tag={ns}.map_editor] run return run tellraw @s [{MGS_TAG},{{"text":"Another map is being edited: ","color":"red"}},{{"storage":"{ns}:temp","nbt":"map_edit.map.name","interpret":true}},{{"text":". Join it or wait for its editors to leave.","color":"red"}}]

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

# The chunks within FORCE_RADIUS blocks of the base stay loaded while the map is edited: a marker in an unloaded chunk is neither summoned nor saved.
data modify storage {ns}:temp map_edit.force.dimension set from storage {ns}:temp _tp.dimension
execute store result storage {ns}:temp map_edit.force.x1 int 1 run scoreboard players remove #base_x {ns}.data {FORCE_RADIUS}
execute store result storage {ns}:temp map_edit.force.x2 int 1 run scoreboard players add #base_x {ns}.data {2 * FORCE_RADIUS}
scoreboard players remove #base_x {ns}.data {FORCE_RADIUS}
execute store result storage {ns}:temp map_edit.force.z1 int 1 run scoreboard players remove #base_z {ns}.data {FORCE_RADIUS}
execute store result storage {ns}:temp map_edit.force.z2 int 1 run scoreboard players add #base_z {ns}.data {2 * FORCE_RADIUS}
scoreboard players remove #base_z {ns}.data {FORCE_RADIUS}
function {ns}:v{version}/maps/editor/force_load with storage {ns}:temp map_edit.force

# The markers once those chunks have loaded; no save until then.
data modify storage {ns}:temp map_edit.loading set value 1b
schedule function {ns}:v{version}/maps/editor/summon_all 40t replace

function {ns}:v{version}/maps/editor/give_tools

# Zombies mode only.
execute if score @s {ns}.mp.map_mode matches {zombies_mode} run function {ns}:v{version}/maps/editor/init_zb_defaults

tellraw @s [{MGS_TAG},{{"text":"Entered map editor for: ","color":"green"}},{{"text":"","color":"white"}},{{"storage":"{ns}:temp","nbt":"map_edit.map.name","interpret":true}}]
tellraw @s [{MGS_TAG},{{"text":"Place eggs to add elements. DESTROY egg (hotbar 9) removes nearest element.","color":"yellow"}}]
tellraw @s [{MGS_TAG},{{"text":"Need collaborators? ","color":"gray"}},{Dialogs.btn("Invite Players", f"/function {ns}:v{version}/maps/editor/invite", "aqua", "Choose who joins this editor session", action="run_command")}]
tellraw @s [{MGS_TAG},{{"text":"Use ","color":"gray"}},{Dialogs.btn("Save & Exit", f"/function {ns}:v{version}/maps/editor/save_exit", "green", "Save changes and exit editor")},{{"text":" or "}},{Dialogs.btn("Exit", f"/function {ns}:v{version}/maps/editor/exit", "red", "Discard changes and exit editor")}]
""")

	write_versioned_function("maps/editor/tp_to_map", "$execute in $(dimension) run tp @s $(x) $(y) $(z)")
	write_versioned_function("maps/editor/force_load", "$execute in $(dimension) run forceload add $(x1) $(z1) $(x2) $(z2)")
	write_versioned_function("maps/editor/force_unload", "$execute in $(dimension) run forceload remove $(x1) $(z1) $(x2) $(z2)")

	## Scheduled after an editor entered, run as an editor for the mode summon_existing reads. An element out of the loaded chunks would be lost by a save, so saving is then off for the session.
	write_versioned_function("maps/editor/summon_all", f"""
execute unless entity @a[tag={ns}.map_editor] run return 0
scoreboard players set #ed_unloaded {ns}.data 0
scoreboard players set #ed_retry {ns}.data 0
data modify storage {ns}:temp map_edit.missed set value []
data modify storage {ns}:temp map_edit.kept set value []
execute as @a[tag={ns}.map_editor,limit=1] run function {ns}:v{version}/maps/editor/summon_in with storage {ns}:temp map_edit.force
data remove storage {ns}:temp map_edit.loading
function {ns}:v{version}/maps/editor/summon_report
""")

	## Run as an editor by the Retry button of the warning: summons only the elements the last pass could not load.
	write_versioned_function("maps/editor/summon_retry", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return fail
execute unless data storage {ns}:temp map_edit{{unsafe:1b}} run return fail
scoreboard players set #ed_unloaded {ns}.data 0
scoreboard players set #ed_retry {ns}.data 1
data modify storage {ns}:temp map_edit.missed_before set from storage {ns}:temp map_edit.missed
data modify storage {ns}:temp map_edit.missed set value []
function {ns}:v{version}/maps/editor/summon_in with storage {ns}:temp map_edit.force
scoreboard players set #ed_retry {ns}.data 0
data remove storage {ns}:temp map_edit.missed_before
function {ns}:v{version}/maps/editor/summon_report
execute if score #ed_unloaded {ns}.data matches 0 run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Every element is loaded. Saving is on.","color":"green"}}]
""")
	write_versioned_function("maps/editor/summon_report", f"""
execute if score #ed_unloaded {ns}.data matches 0 run data remove storage {ns}:temp map_edit.unsafe
execute if score #ed_unloaded {ns}.data matches 1.. run data modify storage {ns}:temp map_edit.unsafe set value 1b
execute if score #ed_unloaded {ns}.data matches 1.. run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"score":{{"name":"#ed_unloaded","objective":"{ns}.data"}},"color":"white"}},{{"text":" elements lie more than {FORCE_RADIUS} blocks from the base and could not be loaded. Saving is off for this session, so they are not lost. ","color":"red"}},{Dialogs.btn("Retry", f"/function {ns}:v{version}/maps/editor/summon_retry", "gold", "Load them again, once the chunks are loaded", action="run_command")}]
""")
	write_versioned_function("maps/editor/summon_in", f"""
$execute in $(dimension) run function {ns}:v{version}/maps/editor/summon_existing
function {ns}:v{version}/maps/editor/refresh_displays
""")

	## Run as an editor: a check box per online player not editing yet, and Invite sending the checked ones to invite_selected.
	invite_dialog: str = (
		f'{{type:"minecraft:multi_action",title:["","👥 ",{{text:"Invite to the Editor",color:"aqua",bold:true}}],'
		f'body:[{{type:"minecraft:plain_message",contents:{{text:"Check the players to invite.",color:"gray"}}}}],inputs:[],'
		f'actions:[{{label:{{text:"Invite",color:"green"}},action:{{type:"minecraft:dynamic/run_command",template:""}}}},'
		f'{{label:{{text:"Everyone",color:"aqua"}},tooltip:{{text:"Invite every online player"}},action:{{type:"run_command",command:"/function {ns}:v{version}/maps/editor/invite_all"}}}}],'
		f'columns:2,exit_action:{{label:{{text:"Close",color:"gray"}}}}}}'
	)
	write_versioned_function("maps/editor/invite", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"You must be in map editor to invite players.","color":"red"}}]

data modify storage {ns}:temp _plr_mode set value "editor"
data modify storage {ns}:temp _plr_iter set value []
execute as @a unless score @s {ns}.mp.map_edit matches 1 run function {ns}:v{version}/players/append_self

data modify storage {ns}:temp dialog set value {invite_dialog}
execute unless data storage {ns}:temp _plr_iter[0] run data modify storage {ns}:temp dialog.body[0].contents set value {{text:"Everyone online already edits this map.",color:"gray"}}

# A dialog refuses a template without variables, so Invite goes when there is no box.
execute unless data storage {ns}:temp _plr_iter[0] run data remove storage {ns}:temp dialog.actions[0]

# The Invite template lists every box, as `ids:[$(p12),$(p7),0]`: a box gives its player's bs.id when checked, else 0. `d` holds the "$" a macro cannot write itself.
data modify storage {ns}:temp _inv set value {{tpl:"",d:"$"}}
execute if data storage {ns}:temp _plr_iter[0] run function {ns}:v{version}/maps/editor/invite_box
execute unless data storage {ns}:temp _inv{{tpl:""}} run function {ns}:v{version}/maps/editor/invite_template with storage {ns}:temp _inv
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
	write_versioned_function("maps/editor/invite_box", f"""
data modify storage {ns}:temp _inv.id set from storage {ns}:temp _plr_iter[0].id
data modify storage {ns}:temp _inv.name set from storage {ns}:temp _plr_iter[0].name
function {ns}:v{version}/maps/editor/invite_box_add with storage {ns}:temp _inv
data remove storage {ns}:temp _plr_iter[0]
execute if data storage {ns}:temp _plr_iter[0] run function {ns}:v{version}/maps/editor/invite_box
""")
	write_versioned_function("maps/editor/invite_box_add", f"""
$data modify storage {ns}:temp dialog.inputs append value {{type:"minecraft:boolean",key:"p$(id)",label:"$(name)",initial:false,on_true:"$(id)",on_false:"0"}}
$data modify storage {ns}:temp _inv.tpl set value "$(tpl)$(d)(p$(id)),"
""")
	write_versioned_function("maps/editor/invite_template", f"""
$data modify storage {ns}:temp dialog.actions[0].action.template set value "/function {ns}:v{version}/maps/editor/invite_selected {{ids:[$(tpl)0]}}"
""")

	## Macro (ids), run as the editor who clicked Invite.
	write_versioned_function("maps/editor/invite_selected", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"You must be in map editor to invite players.","color":"red"}}]
$data modify storage {ns}:temp _inv_ids set value $(ids)
execute if data storage {ns}:temp _inv_ids[0] run function {ns}:v{version}/maps/editor/invite_next
""")
	write_versioned_function("maps/editor/invite_next", f"""
execute store result score #inv_id {ns}.data run data get storage {ns}:temp _inv_ids[0]
execute unless score #inv_id {ns}.data matches 0 as @a if score @s bs.id = #inv_id {ns}.data run function {ns}:v{version}/players/editor_invite
data remove storage {ns}:temp _inv_ids[0]
execute if data storage {ns}:temp _inv_ids[0] run function {ns}:v{version}/maps/editor/invite_next
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

