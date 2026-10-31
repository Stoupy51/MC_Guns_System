""" Per-map zombies defaults and the field-by-field panel for one placed element. """
# Imports
import json

from stewbeet import McFunction, Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..helpers.snbt import snbt
from ..helpers.text import Text
from ..map_editor_defs import ALL_ELEMENTS, FIELD_DOCS, OPTIONAL_LIST_FIELDS, ElementDef
from .forms import FORM_ELEMENTS
from .shared import SEP, ZB_ELEMENTS

# Constants
GROUP_ID_ELEMENTS: tuple[str, ...] = ("zombie_spawn", "player_spawn_zb", "special_spawn")
""" Spawn-type elements showing a group_id row.
Doors carry none: a door's link_id is its front-room group, and back_group_id is the back room. """


# Functions
def write_editor_zb_config() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_zb_defaults(ns)

	write_versioned_function("maps/editor/handle_zb_configure", f"""
# Within 10 blocks. A form opens for the editor who placed the egg.
tag @p[tag={ns}.map_editor,distance=..6,sort=nearest] add {ns}.ed_form_user
execute at @s as @n[tag={ns}.map_element,distance=..10] run function {ns}:v{version}/maps/editor/show_element_config
execute at @s unless entity @n[tag={ns}.map_element,distance=..10] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 10 blocks!","color":"red"}}]
tag @a remove {ns}.ed_form_user
""")

	# Run as the nearest marker: a form for the elements that have one, else its type-specific fields in chat.
	write_versioned_function("maps/editor/show_element_config", "\n".join([
		*(
			f"execute if entity @s[tag={ns}.element.{etype}] run return run function {ns}:v{version}/maps/editor/form/open/{etype}"
			for etype in FORM_ELEMENTS
		),
		f"tellraw @a[tag={ns}.map_editor] {SEP}",
		*zb_object_config_lines(ns, version),
		*marker_config_lines(ns),
		*base_coordinates_config_lines(ns),
		f"tellraw @a[tag={ns}.map_editor] {SEP}",
	]))

	# Markers from an already-saved map get fields added to `defaults` since then (partial_price on doors and perk machines),
	# so the config UI shows the default instead of a blank row; a set value is never touched.
	light_dispatch: str = write_light_fields()
	missing_defaults: str = "\n".join(
		f"execute if entity @s[tag={ns}.element.{etype}] unless data entity @s data.{field} "
		f"run data modify entity @s data.{field} set value {snbt(default_val)}"
		for etype, einfo in ZB_ELEMENTS.items()
		for field, default_val in einfo.defaults.items()
	)
	write_versioned_function("maps/editor/backfill_zb_defaults", f"""
{light_dispatch}
{missing_defaults}
""")


def write_zb_defaults(ns: str) -> None:
	""" Write the panel editing the defaults new zombies elements are placed with, and its init on editor enter. """
	group_id_btn = Dialogs.btn(
		"\u270e",
		f"/data modify storage {ns}:temp map_edit.zb_defaults.group_id set value 0",
		"aqua", "Click to edit group_id", action="suggest_command"
	)
	handle_zb_defaults: McFunction = f"""
tellraw @a[tag={ns}.map_editor] {SEP}
tellraw @a[tag={ns}.map_editor] [{{"text":"","color":"white","bold":true}},"  ⚙ ",{{"text":"Zombies Element Defaults"}}]
tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"New elements use these values on placement","color":"gray","italic":true}}]
tellraw @a[tag={ns}.map_editor] {SEP}

# Shared group_id default.
tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"group_id: ","color":"gray"}},{{"storage":"{ns}:temp","nbt":"map_edit.zb_defaults.group_id","color":"white"}}," ",{group_id_btn}]
tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"Applies to Zombie Spawn & Player Spawn.","color":"dark_gray","italic":true}}]
"""

	# No type-specific defaults, no section.
	for etype, einfo in ZB_ELEMENTS.items():
		if not einfo.defaults:
			continue
		handle_zb_defaults += f"""
tellraw @a[tag={ns}.map_editor] ["  ","{einfo.emoji} ",{{"text":"{einfo.name}","color":"{einfo.color}","bold":true}}]
"""
		for field, default_val in einfo.defaults.items():
			edit_btn = Dialogs.btn(
				"✎",
				f"/data modify storage {ns}:temp map_edit.zb_defaults.{etype}.{field} set value {snbt(default_val)}",
				"aqua", f"Click to edit {field}", action="suggest_command"
			)
			handle_zb_defaults += (
				f'tellraw @a[tag={ns}.map_editor] '
				f'["    ",{{"text":"{field}: ","color":"gray"}},'
				f'{{"storage":"{ns}:temp","nbt":"map_edit.zb_defaults.{etype}.{field}","color":"white"}}," ",{edit_btn}]\n'
			)

	handle_zb_defaults += f"""
tellraw @a[tag={ns}.map_editor] {SEP}
"""
	write_versioned_function("maps/editor/handle_zb_defaults", handle_zb_defaults)

	# On editor entry, zombies mode only.
	element_defaults: str = "\n".join(
		f"data modify storage {ns}:temp map_edit.zb_defaults.{etype} set value {snbt(einfo.defaults)}" for etype, einfo in ZB_ELEMENTS.items()
	)
	write_versioned_function("maps/editor/init_zb_defaults", f"""
data modify storage {ns}:temp map_edit.zb_defaults.group_id set value 0
{element_defaults}
""")


def zb_object_config_lines(ns: str, version: str) -> list[str]:
	""" Config panel lines of every zombies element: a title, group_id for spawns, then one row per default field. """
	lines: list[str] = []
	for etype, einfo in ZB_ELEMENTS.items():
		shown: str = f"execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] "
		lines.append(shown + f'["  ","{einfo.emoji} ",{{"text":"{einfo.name} Configuration","color":"{einfo.color}","bold":true}}]')
		if etype in GROUP_ID_ELEMENTS:
			group_id_edit_btn = Dialogs.btn(
				"✎",
				f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.group_id set value 0",
				"yellow", "Click to edit group_id", action="suggest_command"
			)
			lines.append(shown + f'["    ",{{"text":"group_id: ","color":"gray"}},{{"entity":"@s","nbt":"data.group_id","color":"white"}}," ",{group_id_edit_btn}]')
		lines += [shown + field_config_row(ns, version, etype, field, default_val) for field, default_val in einfo.defaults.items()]
	return lines


def field_config_row(ns: str, version: str, etype: str, field: str, default_val: object) -> str:
	""" Tellraw component of one field row: its value, an edit button, a clear button for optional lists and an info tooltip when documented. """
	snbt_val: str = snbt(default_val)

	# Door fields except link_id apply to every door with the same link_id; two entry points, since a macro cannot re-quote its argument.
	if etype == "door" and field != "link_id":
		kind: str = "text" if isinstance(default_val, str) else "number"
		edit_cmd: str = f'/function {ns}:v{version}/maps/editor/set_door_link_{kind} {{field:"{field}",value:{snbt_val}}}'
		hover_text: str = f"Sets {field} on ALL doors with same link_id"
	else:
		# Optional list fields suggest a usable template instead of empty brackets.
		edit_cmd = f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.{field} set value {OPTIONAL_LIST_FIELDS.get(field, snbt_val)}"
		hover_text = f"Click to edit {field}"
	edit_btn = Dialogs.btn("✎", edit_cmd, "yellow", hover_text, action="suggest_command")

	# Optional list fields get a "✗" button that sets them back to [].
	clear_component: str = ""
	if field in OPTIONAL_LIST_FIELDS:
		clear_btn = Dialogs.btn(
			"✗",
			f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.{field} set value []",
			"red", f"Clear (disable) {field}", action="run_command"
		)
		clear_component = f'," ",{clear_btn}'

	# Info tooltip for constant and enum fields (trap type, door animation).
	doc: str | None = FIELD_DOCS.get((etype, field)) or FIELD_DOCS.get(field)
	info_component: str = ""
	if doc:
		info_component = f',"  ",{{"text":"ⓘ","color":"aqua","hover_event":{{"action":"show_text","value":{json.dumps(Text.help(doc), ensure_ascii=False)}}}}}'

	return (
		f'["    ",{{"text":"{field}: ","color":"gray"}},'
		f'{{"entity":"@s","nbt":"data.{field}","color":"white"}}," ",{edit_btn}{clear_component}{info_component}]'
	)


def marker_config_lines(ns: str) -> list[str]:
	""" Config panel lines shared by marker kinds: yaw for spawns and zombies elements, the enemy function, and a note on points. """
	lines: list[str] = []

	# Spawn types: yaw.
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo.save_type != "spawn":
			continue
		shown: str = f"execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] "
		lines += [
			shown + f'["  ","{einfo.emoji} ",{{"text":"{einfo.name}","color":"{einfo.color}","bold":true}}]',
			shown + yaw_row(ns, etype),
		]

	# Zombies objects: yaw.
	lines += [f"execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] " + yaw_row(ns, etype) for etype in ZB_ELEMENTS]

	# Enemy types: the function. The suggestion stays unversioned like the map default, or a saved map would call a path a later version removes.
	edit_cmd_btn = Dialogs.btn(
		"✎",
		f"/data modify entity @n[tag={ns}.element.enemy,distance=..10] data.function set value '{ns}:mob/default/level_1'",
		"yellow", "Click to edit function", action="suggest_command"
	)
	lines += [
		f'execute if entity @s[tag={ns}.element.enemy] run tellraw @a[tag={ns}.map_editor] '
		f'["  ","👤 ",{{"text":"Enemy Configuration","color":"red","bold":true}}]',
		f'execute if entity @s[tag={ns}.element.enemy] run tellraw @a[tag={ns}.map_editor] '
		f'["    ",{{"text":"function: ","color":"gray"}},'
		f'{{"entity":"@s","nbt":"data.function","color":"white"}}," ",{edit_cmd_btn}]',
	]

	# Point types have nothing to configure.
	lines += [
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
		f'["  ","{einfo.emoji} ",{{"text":"{einfo.name}: no configurable fields","color":"gray","italic":true}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "point"
	]
	return lines


def yaw_row(ns: str, etype: str) -> str:
	""" Tellraw component of a marker's yaw row, with its edit button. """
	edit_yaw_btn = Dialogs.btn(
		"✎",
		f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.yaw set value 0.0f",
		"yellow", "Click to edit yaw", action="suggest_command"
	)
	return f'["    ",{{"text":"yaw: ","color":"gray"}},{{"entity":"@s","nbt":"data.yaw","color":"white"}}," ",{edit_yaw_btn}]'


def base_coordinates_config_lines(ns: str) -> list[str]:
	""" Config panel lines of the base coordinates marker: its start_command and tick_command. """
	edit_start_cmd_btn = Dialogs.btn(
		"✎",
		f"/data modify entity @n[tag={ns}.element.base_coordinates,distance=..10] data.start_command set value 'say Game started'",
		"yellow", "Click to edit start_command (run once when the game starts)", action="suggest_command"
	)
	clear_start_cmd_btn = Dialogs.btn(
		"✗",
		f'/data remove entity @n[tag={ns}.element.base_coordinates,distance=..10] data.start_command',
		"red", "Clear start_command (won't be run)", action="run_command"
	)
	edit_tick_cmd_btn = Dialogs.btn(
		"✎",
		f"/data modify entity @n[tag={ns}.element.base_coordinates,distance=..10] data.tick_command set value 'function namespace:path/to/function'",
		"yellow", "Click to edit tick_command (run every game tick)", action="suggest_command"
	)
	clear_tick_cmd_btn = Dialogs.btn(
		"✗",
		f'/data remove entity @n[tag={ns}.element.base_coordinates,distance=..10] data.tick_command',
		"red", "Clear tick_command (won't be run)", action="run_command"
	)
	shown: str = f"execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] "
	return [
		shown + '["  ","⬟ ",{"text":"Base Coordinates Configuration","color":"light_purple","bold":true}]',
		shown + f'["    ",{{"text":"start_command: ","color":"gray"}},{{"entity":"@s","nbt":"data.start_command","color":"white"}}," ",{edit_start_cmd_btn}," ",{clear_start_cmd_btn}]',
		shown + f'["    ",{{"text":"tick_command: ","color":"gray"}},{{"entity":"@s","nbt":"data.tick_command","color":"white"}}," ",{edit_tick_cmd_btn}," ",{clear_tick_cmd_btn}]',
		shown + '["    ","💎 ",{"text":"Commands run at the base: start_command once when the game starts, tick_command every game tick.","color":"dark_gray","italic":true}]',
	]


def write_light_fields() -> str:
	""" Write maps/light_fields/<etype>, restoring the fields a saved map leaves out and upgrading pre-26.3 block states.

	Returns:
		The lines an editor marker runs to dispatch to them.
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	light_elements: dict[str, ElementDef] = {etype: einfo for etype, einfo in ZB_ELEMENTS.items() if einfo.light_fields}
	for etype, einfo in light_elements.items():
		light_fields: McFunction = f"""
# @s = an entity holding one saved {etype} compound in data (editor marker or in-game display)
"""
		for field in einfo.light_fields:
			path: str = f"entity @s data.{field}"
			light_fields += f"""
execute if data {path}.Name run data modify {path}.id set from {path}.Name
execute if data {path}.Properties run data modify {path}.properties set from {path}.Properties
data remove {path}.Name
data remove {path}.Properties
execute unless data {path} run data modify {path} set value {snbt(einfo.defaults[field])}
"""
		write_versioned_function(f"maps/light_fields/{etype}", light_fields)
	return "\n".join(
		f"execute if entity @s[tag={ns}.element.{etype}] run function {ns}:v{version}/maps/light_fields/{etype}"
		for etype in light_elements
	)

