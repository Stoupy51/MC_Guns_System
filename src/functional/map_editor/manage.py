""" The map list actions that need no editing session: settings, duplicate, export and delete. """
# Imports
import json

from stewbeet import JsonDict, Mem, write_versioned_function

from ..helpers import MGS_TAG


# Functions
def write_editor_manage() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	editor: str = f"{ns}:v{version}/maps/editor"
	show_dialog: str = f"function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp"

	# Each dialog is set as a whole, then the macros below fill in the map's own values with `set from`, so no map text ever goes through a macro.
	settings_dialog: JsonDict = {
		"type": "minecraft:confirmation",
		"title": {"text": "Map Settings", "color": "gold", "bold": True},
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Dimension: minecraft:overworld, mgs:zombies, minecraft:the_nether, minecraft:the_end or any other.", "color": "gray"}}],
		"inputs": [
			{"type": "minecraft:text", "key": "name", "label": "Name", "initial": "", "max_length": 64, "width": 300},
			{"type": "minecraft:text", "key": "description", "label": "Description", "initial": "", "max_length": 256, "width": 300},
			{"type": "minecraft:text", "key": "dimension", "label": "Dimension", "initial": "minecraft:overworld", "max_length": 128, "width": 300},
		],
		"yes": {"label": {"text": "Save", "color": "green"}, "action": {
			"type": "dynamic/run_command",
			"template": f'/function {editor}/settings_apply {{name:"$(name)",description:"$(description)",dimension:"$(dimension)"}}',
		}},
		"no": {"label": {"text": "Cancel", "color": "red"}, "action": {"type": "run_command", "command": ""}},
	}
	delete_dialog: JsonDict = {
		"type": "minecraft:confirmation",
		"title": {"text": "Delete Map", "color": "red", "bold": True},
		"body": [{"type": "minecraft:plain_message", "contents": [{"text": "Delete "}, {"text": "", "color": "gold"}, {"text": "? This cannot be undone."}]}],
		"yes": {"label": {"text": "Delete", "color": "red"}, "action": {"type": "run_command", "command": ""}},
		"no": {"label": {"text": "Cancel", "color": "gray"}, "action": {"type": "run_command", "command": ""}},
	}
	export_dialog: JsonDict = {
		"type": "minecraft:notice",
		"title": {"text": "Export Map", "color": "aqua", "bold": True},
		"body": [{"type": "minecraft:plain_message", "width": 400, "contents": {"text": f"Click the box, then Ctrl+A and Ctrl+C. To import it, paste it after \"data modify storage {ns}:maps <mode> append value\" in a command block or a function, since chat cuts commands at 256 characters.", "color": "gray"}}],
		"inputs": [{"type": "minecraft:text", "key": "map", "label": "Map data", "initial": "", "max_length": 2000000, "width": 400, "multiline": {"max_lines": 512, "height": 200}}],
		"action": {"label": {"text": "Back", "color": "gray"}, "action": {"type": "run_command", "command": ""}},
	}

	## Macro (mode, idx). The target is kept in storage for settings_apply, which only receives the inputs.
	write_versioned_function("maps/editor/settings", f"""
$data modify storage {ns}:temp map_settings.target set value {{mode:"$(mode)",idx:$(idx)}}
data modify storage {ns}:temp dialog set value {json.dumps(settings_dialog)}
$data modify storage {ns}:temp dialog.inputs[0].initial set from storage {ns}:maps $(mode)[$(idx)].name
$data modify storage {ns}:temp dialog.inputs[1].initial set from storage {ns}:maps $(mode)[$(idx)].description
$data modify storage {ns}:temp dialog.inputs[2].initial set from storage {ns}:maps $(mode)[$(idx)].dimension
$data modify storage {ns}:temp dialog.no.action.command set value "/function {editor}/list/$(mode)"
{show_dialog}
""")

	write_versioned_function("maps/editor/settings_apply", f"""
$data modify storage {ns}:temp map_settings.fields set value {{name:"$(name)",description:"$(description)",dimension:"$(dimension)"}}
function {editor}/settings_write with storage {ns}:temp map_settings.target
tellraw @s [{MGS_TAG},{{"text":"Map settings saved.","color":"green"}}]
""")

	write_versioned_function("maps/editor/settings_write", f"""
$data modify storage {ns}:maps $(mode)[$(idx)] merge from storage {ns}:temp map_settings.fields
$function {editor}/list/$(mode)
""")

	## Macro (mode, idx): the copy goes at the end, so no index of the list moves under an open editing session.
	write_versioned_function("maps/editor/duplicate", f"""
$data modify storage {ns}:temp _dup.map set from storage {ns}:maps $(mode)[$(idx)]
$data modify storage {ns}:temp _dup.mode set value "$(mode)"
data modify storage {ns}:temp _dup.id set from storage {ns}:temp _dup.map.id
function {editor}/duplicate_id with storage {ns}:temp _dup
$data modify storage {ns}:maps $(mode) append from storage {ns}:temp _dup.map
tellraw @s [{MGS_TAG},{{"text":"Map duplicated as ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_dup.map.id","color":"white"}}]
$function {editor}/list/$(mode)
""")

	## Macro (mode, id): adds "_copy" until no map of the mode has that id, since games pick maps by id.
	write_versioned_function("maps/editor/duplicate_id", f"""
$data modify storage {ns}:temp _dup.map.id set value "$(id)_copy"
data modify storage {ns}:temp _dup.id set from storage {ns}:temp _dup.map.id
$execute if data storage {ns}:maps $(mode)[{{id:"$(id)_copy"}}] run function {editor}/duplicate_id with storage {ns}:temp _dup
""")

	## Macro (mode, idx). `set string` rejects compounds, so the SNBT text comes from a macro, which prints a compound as compact SNBT.
	write_versioned_function("maps/editor/export", f"""
data modify storage {ns}:temp dialog set value {json.dumps(export_dialog)}
$data modify storage {ns}:temp dialog.action.action.command set value "/function {editor}/list/$(mode)"
$data modify storage {ns}:temp _export.map set from storage {ns}:maps $(mode)[$(idx)]
scoreboard players set #export_ok {ns}.data 0
execute store result score #export_ok {ns}.data run function {editor}/export_text with storage {ns}:temp _export
execute if score #export_ok {ns}.data matches 1 run return run {show_dialog}

# A text holding a double quote is printed in single quotes, which ends the one wrapping the macro value: chat and logs/latest.log get the map instead.
tellraw @s [{MGS_TAG},{{"text":"This map has a text with a double quote, so it is printed below and in logs/latest.log instead.","color":"yellow"}}]
tellraw @s {{"storage":"{ns}:temp","nbt":"_export.map","color":"white"}}
""")

	write_versioned_function("maps/editor/export_text", f"""
$data modify storage {ns}:temp dialog.inputs[0].initial set value '$(map)'
return 1
""")

	write_versioned_function("maps/editor/delete_confirm", f"""
data modify storage {ns}:temp dialog set value {json.dumps(delete_dialog)}
$data modify storage {ns}:temp dialog.body[0].contents[1].text set from storage {ns}:maps $(mode)[$(idx)].name
$data modify storage {ns}:temp dialog.yes.action.command set value "/function {editor}/delete {{idx:$(idx),mode:$(mode)}}"
$data modify storage {ns}:temp dialog.no.action.command set value "/function {editor}/list/$(mode)"
{show_dialog}
""")

	write_versioned_function("maps/editor/delete", f"""
$data remove storage {ns}:maps $(mode)[$(idx)]
tellraw @s [{MGS_TAG},{{"text":"Map deleted.","color":"red"}}]

$function {editor}/list/$(mode)
""")

