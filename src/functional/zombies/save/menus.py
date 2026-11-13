""" The dialogs of the save slots: Save & Quit from the admin menu, Load Save from the setup menu. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG


# Functions
def write_save_menus(slot_count: int) -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	slots: str = f"storage {ns}:zombies_saves slots"
	show: str = f"function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp"
	save_command: str = f'/function {ns}:v{version}/zombies/save/save {{slot:$(slot),name:\\"$(name)\\"}}'
	cancel: str = '{label:{text:"Cancel",color:"gray"}}'

	## A slot button carries a dynamic template: the client replaces `$(name)` with the text input.
	slot_buttons: str = ""
	for slot in range(slot_count):
		slot_buttons += f"""
data modify storage {ns}:temp dialog.actions append value {{label:["","Slot {slot + 1}: ",{{text:"Empty",color:"gray"}}],tooltip:{{text:"Save the running game in this slot"}},action:{{type:"minecraft:dynamic/run_command",template:"/function {ns}:v{version}/zombies/save/request {{slot:{slot},name:\\"$(name)\\"}}"}}}}
execute if data {slots}[{slot}].name run data modify storage {ns}:temp dialog.actions[{slot}].label[2] set from {slots}[{slot}].name
"""

	## #zb_next_round only counts down in the gap after a round, the one moment a game can be saved.
	write_versioned_function("zombies/save/save_menu", f"""
execute unless score #zb_next_round {ns}.data matches 1.. run return run tellraw @s [{MGS_TAG},{{"text":"A game can only be saved between two rounds.","color":"red"}}]

data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","💾 ",{{text:"Save & Quit",color:"gold",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"Name the save and pick a slot. The game stops once saved.",color:"gray"}}}}],inputs:[{{type:"minecraft:text",key:"name",label:"Save name",initial:"",max_length:32}}],actions:[],columns:1,pause:false,after_action:"close",exit_action:{cancel}}}
{slot_buttons}
data modify storage {ns}:temp _sv_name set value {{}}
data modify storage {ns}:temp _sv_name.map_id set from storage {ns}:zombies game.map_id
execute store result storage {ns}:temp _sv_name.round int 1 run data get storage {ns}:zombies game.round
function {ns}:v{version}/zombies/save/menu_name with storage {ns}:temp _sv_name

{show}
""")

	write_versioned_function("zombies/save/menu_name", f"""
$data modify storage {ns}:temp dialog.inputs[0].initial set value "$(map_id) r$(round)"
""")

	## Macro {slot, name}: saves at once in an empty slot, otherwise asks first.
	write_versioned_function("zombies/save/request", f"""
$execute unless data {slots}[$(slot)].format run return run function {ns}:v{version}/zombies/save/save {{slot:$(slot),name:"$(name)"}}

$data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","Overwrite ","","?"],body:[{{type:"minecraft:plain_message",contents:{{text:"The running game replaces this save.",color:"gray"}}}}],actions:[{{label:{{text:"Overwrite",color:"gold"}},tooltip:{{text:"Replace the save"}},action:{{type:"run_command",command:"{save_command}"}}}}],columns:1,pause:false,after_action:"close",exit_action:{cancel}}}
$data modify storage {ns}:temp dialog.title[2] set from {slots}[$(slot)].name
{show}
""")

	slot_rows: str = ""
	for slot in range(slot_count):
		slot_rows += f"""
data modify storage {ns}:temp _sv_row set value {{slot:{slot},n:{slot + 1}}}
execute if data {slots}[{slot}].format run function {ns}:v{version}/zombies/save/load_row with storage {ns}:temp _sv_row
execute unless data {slots}[{slot}].format run data modify storage {ns}:temp dialog.body append value {{type:"minecraft:plain_message",contents:{{text:"{slot + 1}. Empty",color:"gray"}}}}
"""

	## A dialog needs one button, so a link back to setup stands in when every slot is empty.
	write_versioned_function("zombies/save/load_menu", f"""
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","📂 ",{{text:"Load Save",color:"gold",bold:true}}],body:[],actions:[],columns:2,pause:false,after_action:"none",exit_action:{{label:["","◀ ",{{text:"Back",color:"gray"}}],tooltip:{{text:"Return to setup"}},action:{{type:"show_dialog",dialog:"{ns}:v{version}/zombies/setup"}}}}}}
{slot_rows}
execute unless data storage {ns}:temp dialog.actions[0] run data modify storage {ns}:temp dialog.actions append value {{label:{{text:"No saves yet",color:"red"}},tooltip:{{text:"Save a running game between two rounds from the admin menu"}},action:{{type:"show_dialog",dialog:"{ns}:v{version}/zombies/setup"}}}}

{show}
""")

	## Macro {slot, n}: reads the slot's summary into _sv_row, then appends its line and its two buttons.
	write_versioned_function("zombies/save/load_row", f"""
$data modify storage {ns}:temp _sv_row.name set from {slots}[$(slot)].name
$data modify storage {ns}:temp _sv_row.map_id set from {slots}[$(slot)].map_id
$data modify storage {ns}:temp _sv_row.round set from {slots}[$(slot)].round
function {ns}:v{version}/zombies/save/load_row_add with storage {ns}:temp _sv_row
""")

	write_versioned_function("zombies/save/load_row_add", f"""
$data modify storage {ns}:temp dialog.body append value {{type:"minecraft:plain_message",contents:["",{{text:"$(n). ",color:"gray"}},{{text:"$(name)",color:"gold"}},{{text:"  $(map_id)  Round $(round)",color:"gray"}}]}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"📂 Load $(n)",color:"green"}},tooltip:{{text:"Load this save"}},action:{{type:"run_command",command:"/function {ns}:v{version}/dialog/close_then {{run:\\"zombies/save/load {{slot:$(slot)}}\\"}}"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"🗑 Delete $(n)",color:"red"}},tooltip:{{text:"Ask before emptying this slot"}},action:{{type:"run_command",command:"/function {ns}:v{version}/zombies/save/delete_ask {{slot:$(slot)}}"}}}}
""")

	## Macro {slot}: Delete empties the slot then reopens the list, Cancel only reopens it.
	write_versioned_function("zombies/save/delete_ask", f"""
$data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","Delete ","","?"],body:[{{type:"minecraft:plain_message",contents:{{text:"The slot is emptied for good.",color:"gray"}}}}],actions:[{{label:{{text:"Delete",color:"red"}},tooltip:{{text:"Empty the slot"}},action:{{type:"run_command",command:"/function {ns}:v{version}/zombies/save/delete {{slot:$(slot)}}"}}}}],columns:1,pause:false,after_action:"close",exit_action:{{label:{{text:"Cancel",color:"gray"}},action:{{type:"run_command",command:"/function {ns}:v{version}/zombies/save/load_menu"}}}}}}
$data modify storage {ns}:temp dialog.title[2] set from {slots}[$(slot)].name
{show}
""")

