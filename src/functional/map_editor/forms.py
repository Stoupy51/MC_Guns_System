""" Dialog forms configuring a spawn or a mystery box spot, and drawing a spawn's activation box with the Coord Stick. """
# Imports
import json
from collections.abc import Sequence

from stewbeet import JsonDict, Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.snbt import snbt
from ..helpers.text import Text
from ..map_editor_defs import FIELD_DOCS
from ..zombies.game.lifecycle.spawns import ARRIVALS, SPECIAL_SPAWNS, ZOMBIE_SPAWNS, SpawnKind
from ..zombies.machines.mystery_box.shared import ROLLS

# Constants
SPAWN_FORMS: dict[str, SpawnKind] = {"zombie_spawn": ZOMBIE_SPAWNS, "special_spawn": SPECIAL_SPAWNS}
FORM_ELEMENTS: tuple[str, ...] = (*SPAWN_FORMS, "mystery_box_pos")
""" Elements the Configure egg opens a form for, rather than listing their fields in chat. """


# Functions
def write_editor_forms() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	form: str = f"{ns}:v{version}/maps/editor/form"
	show_dialog: str = f"execute as @a[tag={ns}.ed_form_user] run function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp"
	target: str = f"@n[type=minecraft:marker,tag={ns}.ed_form_target]"
	gone: str = f'tellraw @s [{MGS_TAG},{{"text":"The element being edited is gone.","color":"red"}}]'

	## Run as the marker the form edits. It keeps ed_form_target until another form opens, so a save finds it wherever its editor went.
	write_versioned_function("maps/editor/form/target", f"""
tag @e[type=minecraft:marker,tag={ns}.ed_form_target] remove {ns}.ed_form_target
tag @s add {ns}.ed_form_target
""")

	for etype, kind in SPAWN_FORMS.items():
		write_spawn_form(ns, form, etype, kind, show_dialog)

	## Run as the editor. The fields go in storage first, so the rest of the save is no macro.
	## A dialog escapes its text fields for a quoted string, so they come quoted and turn back into SNBT here, in brackets so empty is [].
	write_versioned_function("maps/editor/form/spawn_apply", f"""
$data modify storage {ns}:temp _form set value {{data:{{group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:"$(arrival)",rise_ticks:$(rise_ticks),activation_box:[$(activation_box)],walk_to:[$(walk_to)]}},power:$(power)b,mob:[$(mob)],then:"$(then)"}}
execute unless entity {target} run return run {gone}
execute as {target} run function {form}/spawn_write
tellraw @s [{MGS_TAG},{{"text":"Spawn saved.","color":"green"}}]
execute if data storage {ns}:temp _form{{then:"box"}} run function {form}/box_start
""")
	default_mobs: str = "\n".join(
		f"execute unless data storage {ns}:temp _form.mob[0] if entity @s[tag={ns}.element.{etype}] run data modify entity @s data.mob set value {snbt(kind.defaults['mob'])}"
		for etype, kind in SPAWN_FORMS.items()
	)
	write_versioned_function("maps/editor/form/spawn_write", f"""
data modify entity @s data merge from storage {ns}:temp _form.data
execute if entity @s[tag={ns}.element.zombie_spawn] run data modify entity @s data.power set from storage {ns}:temp _form.power

# An empty mob field puts back the kind's own.
execute if data storage {ns}:temp _form.mob[0] run data modify entity @s data.mob set from storage {ns}:temp _form.mob[0]
{default_mobs}
""")

	write_mystery_box_form(ns, form, show_dialog, target, gone)
	write_box_drawing(ns, form, target)


def write_spawn_form(ns: str, form: str, etype: str, kind: SpawnKind, show_dialog: str) -> None:
	""" Write form/open/<etype>, the dialog of a zombie or special spawn filled from its marker's data. """
	has_power: bool = "power" in kind.defaults
	inputs: list[JsonDict] = [
		{"type": "minecraft:number_range", "key": "group_id", "label": "Group, opened by doors", "start": 0, "end": 64, "step": 1, "width": 300},
		{"type": "minecraft:number_range", "key": "min_round", "label": "From round (0: the first)", "start": 0, "end": 100, "step": 1, "width": 300},
		{"type": "minecraft:number_range", "key": "max_round", "label": "Until round (0: no end)", "start": 0, "end": 100, "step": 1, "width": 300},
		{"type": "minecraft:single_option", "key": "arrival", "label": "Arrival", "width": 300, "options": [{"id": arrival, "display": arrival.capitalize()} for arrival in ARRIVALS]},
		{"type": "minecraft:number_range", "key": "rise_ticks", "label": "Rise time, in ticks", "start": 1, "end": 100, "step": 1, "width": 300},
		*([{"type": "minecraft:boolean", "key": "power", "label": "Only once the power is on", "initial": False, "on_true": "1", "on_false": "0"}] if has_power else []),
		{"type": "minecraft:text", "key": "mob", "label": {"text": "Mob (SNBT, empty for the default)", "hover_event": doc_hover("mob")}, "initial": "", "max_length": 4096, "width": 400},
		{"type": "minecraft:text", "key": "activation_box", "label": {"text": "Activation box: x, y, z, dx, dy, dz", "hover_event": doc_hover("activation_box")}, "initial": "", "max_length": 128, "width": 300},
		{"type": "minecraft:text", "key": "walk_to", "label": {"text": "Walk to: x, y, z", "hover_event": doc_hover("walk_to")}, "initial": "", "max_length": 64, "width": 300},
	]
	index: dict[str, int] = {field["key"]: i for i, field in enumerate(inputs)}
	power: str = "$(power)" if has_power else "0"
	fields: str = (
		"group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:\"$(arrival)\",rise_ticks:$(rise_ticks),"
		f"power:{power},mob:\"$(mob)\",activation_box:\"$(activation_box)\",walk_to:\"$(walk_to)\""
	)
	legend: list[tuple[str, str]] = [
		("Group", "group_id"), ("From round", "min_round"), ("Until round", "max_round"), ("Arrival", "arrival"), ("Rise", "rise_ticks"),
		*([("Power", "power")] if has_power else []), ("Mob", "mob"), ("Activation box", "activation_box"), ("Walk to", "walk_to"),
	]
	dialog: JsonDict = {
		"type": "minecraft:multi_action",
		"title": {"text": kind.name, "color": "gold", "bold": True},
		"body": [
			help_legend(legend),
			{"type": "minecraft:plain_message", "width": 400, "contents": Text.help('Mob example: `{entity:"spider",riders:[{entity:"zombie"}]}`')},
		],
		"inputs": inputs,
		"actions": [
			{"label": {"text": "Save", "color": "green"}, "action": {"type": "dynamic/run_command", "template": f"/function {form}/spawn_apply {{{fields},then:\"\"}}"}},
			{"label": "📐 Save, then draw the box", "tooltip": "Then right-click two opposite\ncorners with the Coord Stick.",
				"action": {"type": "dynamic/run_command", "template": f"/function {form}/spawn_apply {{{fields},then:\"box\"}}"}},
		],
		"columns": 2,
		"exit_action": {"label": {"text": "Cancel", "color": "gray"}},
	}

	# Number fields are sliders, whose initial value must sit in their range or the dialog is refused.
	numbers: str = "\n".join(
		f"execute store result score #ed_v {ns}.data run data get entity @s data.{key}\n"
		f"execute if score #ed_v {ns}.data matches ..{inputs[index[key]]['start'] - 1} run scoreboard players set #ed_v {ns}.data {inputs[index[key]]['start']}\n"
		f"execute if score #ed_v {ns}.data matches {inputs[index[key]]['end'] + 1}.. run scoreboard players set #ed_v {ns}.data {inputs[index[key]]['end']}\n"
		f"execute store result storage {ns}:temp dialog.inputs[{index[key]}].initial float 1 run scoreboard players get #ed_v {ns}.data"
		for key in ("group_id", "min_round", "max_round", "rise_ticks")
	)
	arrivals: str = "\n".join(
		f'execute if data entity @s data{{arrival:"{arrival}"}} run data modify storage {ns}:temp dialog.inputs[{index["arrival"]}].options[{i}].initial set value 1b'
		for i, arrival in enumerate(ARRIVALS)
	)
	power_line: str = f"data modify storage {ns}:temp dialog.inputs[{index['power']}].initial set from entity @s data.power" if "power" in index else ""
	open_function: str = f"{form}/open/{etype}"
	write_versioned_function(f"maps/editor/form/open/{etype}", f"""
function {form}/target
data modify storage {ns}:temp dialog set value {json.dumps(dialog, ensure_ascii=False)}
{numbers}
{arrivals}
{power_line}

# The mob as SNBT, the lists without their brackets. A text holding a single quote breaks the macro, so the field stays empty and says so.
execute store result score #ed_texts {ns}.data run function {open_function}_texts with entity @s data
execute if score #ed_texts {ns}.data matches 0 run data modify storage {ns}:temp dialog.body append value {{type:"minecraft:plain_message",width:400,contents:{{text:"This mob holds a quote the form cannot show:\\nsaving would reset it.",color:"red"}}}}
{show_dialog}
""")
	write_versioned_function(f"maps/editor/form/open/{etype}_texts", f"""
$data modify storage {ns}:temp dialog.inputs[{index["mob"]}].initial set value '$(mob)'
$data modify storage {ns}:temp _form_text set value '$(activation_box)'
data modify storage {ns}:temp dialog.inputs[{index["activation_box"]}].initial set string storage {ns}:temp _form_text 1 -1
$data modify storage {ns}:temp _form_text set value '$(walk_to)'
data modify storage {ns}:temp dialog.inputs[{index["walk_to"]}].initial set string storage {ns}:temp _form_text 1 -1
return 1
""")


def write_mystery_box_form(ns: str, form: str, show_dialog: str, target: str, gone: str) -> None:
	""" Write the form of a mystery box spot: its yaw, pitch, roll, whether it can start, and its name. """
	rolls: list[int] = [roll * 90 for roll in range(ROLLS)]
	dialog: JsonDict = {
		"type": "minecraft:multi_action",
		"title": {"text": "Mystery Box", "color": "light_purple", "bold": True},
		"body": [
			{"type": "minecraft:plain_message", "width": 400, "contents": Text.help("The box turns about the centre of its block.\nUpside down, it hangs from the block above.")},
			help_legend([("Pitch", ("mystery_box_pos", "pitch")), ("Roll", ("mystery_box_pos", "roll")), ("First spot", "can_start_on"), ("Location name", ("mystery_box_pos", "location_name"))]),
		],
		"inputs": [
			{"type": "minecraft:number_range", "key": "yaw", "label": "Yaw", "start": 0, "end": 359, "step": 1, "width": 300},
			{"type": "minecraft:number_range", "key": "pitch", "label": "Pitch", "start": -90, "end": 90, "step": 1, "width": 300},
			{"type": "minecraft:single_option", "key": "roll", "label": "Roll", "width": 300,
				"options": [{"id": str(roll), "display": f"{roll} (upside down)" if roll == 180 else str(roll)} for roll in rolls]},
			{"type": "minecraft:boolean", "key": "can_start_on", "label": "Can be the first spot", "initial": True, "on_true": "1", "on_false": "0"},
			{"type": "minecraft:text", "key": "location_name", "label": {"text": "Location name", "hover_event": doc_hover(("mystery_box_pos", "location_name"))},
				"initial": "", "max_length": 64, "width": 300},
		],
		"actions": [{
			"label": {"text": "Save", "color": "green"},
			"action": {"type": "dynamic/run_command", "template": (
				f"/function {form}/mystery_box_apply {{yaw:$(yaw),pitch:$(pitch),roll:$(roll),can_start_on:$(can_start_on),location_name:\"$(location_name)\"}}"
			)},
		}],
		"exit_action": {"label": {"text": "Cancel", "color": "gray"}},
	}
	roll_options: str = "\n".join(
		f"execute if score #ed_v {ns}.data matches {roll} run data modify storage {ns}:temp dialog.inputs[2].options[{roll}].initial set value 1b"
		for roll in range(ROLLS)
	)
	write_versioned_function("maps/editor/form/open/mystery_box_pos", f"""
function {form}/target
data modify storage {ns}:temp dialog set value {json.dumps(dialog, ensure_ascii=False)}

execute store result score #ed_v {ns}.data run data get entity @s data.yaw
scoreboard players operation #ed_v {ns}.data %= #360 {ns}.data
execute store result storage {ns}:temp dialog.inputs[0].initial float 1 run scoreboard players get #ed_v {ns}.data
execute store result score #ed_v {ns}.data run data get entity @s data.pitch
execute if score #ed_v {ns}.data matches ..-91 run scoreboard players set #ed_v {ns}.data -90
execute if score #ed_v {ns}.data matches 91.. run scoreboard players set #ed_v {ns}.data 90
execute store result storage {ns}:temp dialog.inputs[1].initial float 1 run scoreboard players get #ed_v {ns}.data
execute store result score #ed_v {ns}.data run data get entity @s data.roll
scoreboard players operation #ed_v {ns}.data /= #90 {ns}.data
scoreboard players operation #ed_v {ns}.data %= #{ROLLS} {ns}.data
{roll_options}
data modify storage {ns}:temp dialog.inputs[3].initial set from entity @s data.can_start_on
data modify storage {ns}:temp dialog.inputs[4].initial set from entity @s data.location_name
{show_dialog}
""")

	## Run as the editor.
	write_versioned_function("maps/editor/form/mystery_box_apply", f"""
execute unless entity {target} run return run {gone}
$data modify storage {ns}:temp _form set value {{yaw:$(yaw)f,pitch:$(pitch)f,roll:$(roll),can_start_on:$(can_start_on)b,location_name:"$(location_name)"}}
execute as {target} run data modify entity @s data merge from storage {ns}:temp _form
tellraw @s [{MGS_TAG},{{"text":"Mystery box spot saved.","color":"green"}}]
""")


def write_box_drawing(ns: str, form: str, target: str) -> None:
	""" Write the Coord Stick mode that sets the activation box of the spawn in the form from two opposite corners. """
	version: str = Mem.ctx.project_version
	user: str = f"@a[tag={ns}.coord_stick_user]"

	## Run as the editor.
	write_versioned_function("maps/editor/form/box_start", f"""
tag @s add {ns}.cs_abox
data remove storage {ns}:temp coord_stick.abox
tellraw @s [{MGS_TAG},{{"text":"Right-click a corner of the box with the Coord Stick, then the opposite corner.","color":"yellow"}}]
""")
	write_versioned_function("maps/editor/cleanup", f"""
tag @s remove {ns}.cs_abox
""")

	## Run at the aimed block, from utils/coord_stick_relative.
	write_versioned_function("maps/editor/form/box_corner", f"""
execute align xyz run particle firework ~.5 ~.5 ~.5 0.4 0.4 0.4 0.01 100 force @a[distance=..20]
execute summon minecraft:marker run function {ns}:v{version}/utils/coord_stick_store_pos
execute unless data storage {ns}:temp coord_stick.abox run return run function {form}/box_first
function {form}/box_second
""")
	write_versioned_function("maps/editor/form/box_first", f"""
data modify storage {ns}:temp coord_stick.abox set value [0,0,0]
execute store result storage {ns}:temp coord_stick.abox[0] int 1 run scoreboard players get #cs_pos_x {ns}.data
execute store result storage {ns}:temp coord_stick.abox[1] int 1 run scoreboard players get #cs_pos_y {ns}.data
execute store result storage {ns}:temp coord_stick.abox[2] int 1 run scoreboard players get #cs_pos_z {ns}.data
tellraw {user} [{MGS_TAG},{{"text":"First corner saved: now the opposite one.","color":"yellow"}}]
""")

	# The lowest corner from the spawn, then the size: a selector box [x, y, z, dx, dy, dz] catches the blocks x to x+dx.
	corners: str = "\n".join(
		f"execute store result score #cs_{axis}1 {ns}.data run data get storage {ns}:temp coord_stick.abox[{i}]\n"
		f"scoreboard players operation #cs_{axis}2 {ns}.data = #cs_{axis}1 {ns}.data\n"
		f"scoreboard players operation #cs_{axis}1 {ns}.data < #cs_pos_{axis} {ns}.data\n"
		f"scoreboard players operation #cs_{axis}2 {ns}.data > #cs_pos_{axis} {ns}.data\n"
		f"scoreboard players operation #cs_{axis}2 {ns}.data -= #cs_{axis}1 {ns}.data\n"
		f"execute store result score #cs_t{axis} {ns}.data run data get entity {target} Pos[{i}]\n"
		f"scoreboard players operation #cs_{axis}1 {ns}.data -= #cs_t{axis} {ns}.data\n"
		f"execute store result storage {ns}:temp _form_box[{i}] int 1 run scoreboard players get #cs_{axis}1 {ns}.data\n"
		f"execute store result storage {ns}:temp _form_box[{i + 3}] int 1 run scoreboard players get #cs_{axis}2 {ns}.data"
		for i, axis in enumerate(("x", "y", "z"))
	)
	write_versioned_function("maps/editor/form/box_second", f"""
tag {user} remove {ns}.cs_abox
execute unless entity {target} run return run tellraw {user} [{MGS_TAG},{{"text":"The spawn being edited is gone.","color":"red"}}]

data modify storage {ns}:temp _form_box set value [0,0,0,0,0,0]
{corners}
data remove storage {ns}:temp coord_stick.abox
data modify entity {target} data.activation_box set from storage {ns}:temp _form_box
tellraw {user} [{MGS_TAG},{{"text":"Activation box set: ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_form_box","color":"white"}}]

# Back to the form, which now shows the box.
tag {user} add {ns}.ed_form_user
execute as {target} run function {form}/reopen
tag @a remove {ns}.ed_form_user
""")
	write_versioned_function("maps/editor/form/reopen", "\n".join(
		f"execute if entity @s[tag={ns}.element.{etype}] run function {form}/open/{etype}" for etype in SPAWN_FORMS
	))


def help_legend(fields: Sequence[tuple[str, tuple[str, str] | str]]) -> JsonDict:
	""" A dialog body of "ⓘ" chips, one per field label, five a line, each showing its FIELD_DOCS entry on hover.

	Only text inputs show a tooltip on their own label: sliders, option buttons and check boxes do not.
	"""
	contents: list[str | JsonDict] = ["", {"text": "Hover a name for its help:", "color": "gray"}]
	for i, (label, doc) in enumerate(fields):
		contents += ["\n" if i % 5 == 0 else "   ", {"text": f"ⓘ {label}", "color": "aqua", "hover_event": doc_hover(doc)}]
	return {"type": "minecraft:plain_message", "width": 400, "contents": contents}


def doc_hover(doc: tuple[str, str] | str) -> JsonDict:
	""" A hover event showing a FIELD_DOCS entry. """
	return {"action": "show_text", "value": Text.help(FIELD_DOCS[doc])}

