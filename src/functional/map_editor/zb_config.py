""" Per-map zombies defaults and the field-by-field panel for one placed element. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..map_editor_defs import ALL_ELEMENTS, FIELD_DOCS, OPTIONAL_LIST_FIELDS, ElementDef
from .shared import SEP, ZB_ELEMENTS, snbt_compound, snbt_suggest

# Constants
GROUP_ID_ELEMENTS: tuple[str, ...] = ("zombie_spawn", "player_spawn_zb", "special_spawn")
""" Spawn-type elements showing a group_id row.
Doors carry none: a door's link_id is its front-room group, and back_group_id is the back room. """


# Functions
def write_editor_zb_config() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_zb_defaults(ns)

	# Handle ZB Configure (configure nearest element).
	write_versioned_function("maps/editor/handle_zb_configure", f"""
# Find the nearest map element marker (within 10 blocks)
execute at @s as @n[tag={ns}.map_element,distance=..10] run function {ns}:v{version}/maps/editor/show_element_config
execute at @s unless entity @n[tag={ns}.map_element,distance=..10] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 10 blocks!","color":"red"}}]
""")

	# show_element_config: runs as the nearest marker, shows type-specific fields
	write_versioned_function("maps/editor/show_element_config", "\n".join([
		f"tellraw @a[tag={ns}.map_editor] {SEP}",
		*zb_object_config_lines(ns, version),
		*marker_config_lines(ns),
		*base_coordinates_config_lines(ns),
		f"tellraw @a[tag={ns}.map_editor] {SEP}",
	]))

	# Backfill missing config fields on markers summoned from an already-saved map, so a field added to `defaults` after the map was written shows its default in the config UI instead of a blank row (e.g. partial_price on doors/perk machines).
	# Absent-only: never touches a set value.
	backfill_lines: list[str] = [
		*write_light_fields(),
		*(
			f"execute if entity @s[tag={ns}.element.{etype}] unless data entity @s data.{field} "
			f"run data modify entity @s data.{field} set value {snbt_suggest(default_val)}"
			for etype, einfo in ZB_ELEMENTS.items()
			for field, default_val in einfo.defaults.items()
		),
	]
	write_versioned_function("maps/editor/backfill_zb_defaults", "\n".join(backfill_lines))


def write_zb_defaults(ns: str) -> None:
	""" Write the panel editing the defaults new zombies elements are placed with, and its init on editor enter. """
	group_id_btn = Dialogs.btn(
		"\u270e",
		f"/data modify storage {ns}:temp map_edit.zb_defaults.group_id set value 0",
		"aqua", "Click to edit group_id", action="suggest_command"
	)
	zb_defaults_lines: list[str] = [
		f"tellraw @a[tag={ns}.map_editor] {SEP}",
		f'tellraw @a[tag={ns}.map_editor] [{{"text":"","color":"white","bold":true}},"  ⚙ ",{{"text":"Zombies Element Defaults"}}]',
		f'tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"New elements use these values on placement","color":"gray","italic":true}}]',
		f"tellraw @a[tag={ns}.map_editor] {SEP}",
		"",

		# Shared group_id default
		f'tellraw @a[tag={ns}.map_editor] '
		f'["  ",{{"text":"group_id: ","color":"gray"}},'
		f'{{"storage":"{ns}:temp","nbt":"map_edit.zb_defaults.group_id","color":"white"}}," ",{group_id_btn}]',
		f'tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"Applies to Zombie Spawn & Player Spawn.","color":"dark_gray","italic":true}}]',
		"",
	]

	# Elements with no type-specific defaults get no section
	for etype, einfo in ZB_ELEMENTS.items():
		if not einfo.defaults:
			continue
		zb_defaults_lines.append(
			f'tellraw @a[tag={ns}.map_editor] ["  ","{einfo.emoji} ",{{"text":"{einfo.name}","color":"{einfo.color}","bold":true}}]'
		)
		for field, default_val in einfo.defaults.items():
			edit_btn = Dialogs.btn(
				"✎",
				f"/data modify storage {ns}:temp map_edit.zb_defaults.{etype}.{field} set value {snbt_suggest(default_val)}",
				"aqua", f"Click to edit {field}", action="suggest_command"
			)
			zb_defaults_lines.append(
				f'tellraw @a[tag={ns}.map_editor] '
				f'["    ",{{"text":"{field}: ","color":"gray"}},'
				f'{{"storage":"{ns}:temp","nbt":"map_edit.zb_defaults.{etype}.{field}","color":"white"}}," ",{edit_btn}]'
			)
		zb_defaults_lines.append("")

	zb_defaults_lines.append(f"tellraw @a[tag={ns}.map_editor] {SEP}")
	write_versioned_function("maps/editor/handle_zb_defaults", "\n".join(zb_defaults_lines))

	# Init ZB Defaults (called on editor enter for zombies mode)
	write_versioned_function("maps/editor/init_zb_defaults", "\n".join([
		f"data modify storage {ns}:temp map_edit.zb_defaults.group_id set value 0",
		*(f"data modify storage {ns}:temp map_edit.zb_defaults.{etype} set value {snbt_compound(einfo.defaults)}" for etype, einfo in ZB_ELEMENTS.items()),
	]))


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
	snbt_val: str = snbt_suggest(default_val)

	# Door fields (except link_id) propagate to every door sharing the link_id.
	# Two entry points, not eight: a macro cannot re-quote its argument, so the string fields and the numeric fields need one variant each.
	if etype == "door" and field != "link_id":
		kind: str = "text" if isinstance(default_val, str) else "number"
		edit_cmd: str = f'/function {ns}:v{version}/maps/editor/set_door_link_{kind} {{field:"{field}",value:{snbt_val}}}'
		hover_text: str = f"Sets {field} on ALL doors with same link_id"
	else:
		# Optional list fields suggest a usable template instead of empty brackets, so they are easy to fill in
		edit_cmd = f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.{field} set value {OPTIONAL_LIST_FIELDS.get(field, snbt_val)}"
		hover_text = f"Click to edit {field}"
	edit_btn = Dialogs.btn("✎", edit_cmd, "yellow", hover_text, action="suggest_command")

	# Optional list fields get a "✗" button to clear/disable them (set back to []).
	clear_component: str = ""
	if field in OPTIONAL_LIST_FIELDS:
		clear_btn = Dialogs.btn(
			"✗",
			f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.{field} set value []",
			"red", f"Clear (disable) {field}", action="run_command"
		)
		clear_component = f'," ",{clear_btn}'

	# Optional info tooltip for constant/enum fields (e.g. trap type, door animation).
	doc: str | None = FIELD_DOCS.get((etype, field)) or FIELD_DOCS.get(field)
	info_component: str = ""
	if doc:
		doc_escaped = doc.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
		info_component = f',"  ",{{"text":"ⓘ","color":"aqua","hover_event":{{"action":"show_text","value":"{doc_escaped}"}}}}'

	return (
		f'["    ",{{"text":"{field}: ","color":"gray"}},'
		f'{{"entity":"@s","nbt":"data.{field}","color":"white"}}," ",{edit_btn}{clear_component}{info_component}]'
	)


def marker_config_lines(ns: str) -> list[str]:
	""" Config panel lines shared by marker kinds: yaw for spawns and zombies elements, the enemy function, and a note on points. """
	lines: list[str] = []

	# For spawn types: show yaw
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo.save_type != "spawn":
			continue
		shown: str = f"execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] "
		lines += [
			shown + f'["  ","{einfo.emoji} ",{{"text":"{einfo.name}","color":"{einfo.color}","bold":true}}]',
			shown + yaw_row(ns, etype),
		]

	# For zb_object types: show yaw (rotation)
	lines += [f"execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] " + yaw_row(ns, etype) for etype in ZB_ELEMENTS]

	# For enemy types: show function.
	# The suggestion must stay version-independent like the map default above, or a map saved today calls a path that a later pack version no longer ships.
	edit_fn_btn = Dialogs.btn(
		"✎",
		f"/data modify entity @n[tag={ns}.element.enemy,distance=..10] data.function set value '{ns}:mob/default/level_1'",
		"yellow", "Click to edit function", action="suggest_command"
	)
	lines += [
		f'execute if entity @s[tag={ns}.element.enemy] run tellraw @a[tag={ns}.map_editor] '
		f'["  ","👤 ",{{"text":"Enemy Configuration","color":"red","bold":true}}]',
		f'execute if entity @s[tag={ns}.element.enemy] run tellraw @a[tag={ns}.map_editor] '
		f'["    ",{{"text":"function: ","color":"gray"}},'
		f'{{"entity":"@s","nbt":"data.function","color":"white"}}," ",{edit_fn_btn}]',
	]

	# For point types: no configurable fields
	lines += [
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
		f'["  ","{einfo.emoji} ",{{"text":"{einfo.name} — no configurable fields","color":"gray","italic":true}}]'
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
	""" Config panel lines of the base coordinates marker: its start_function and tick_function. """
	edit_start_fn_btn = Dialogs.btn(
		"✎",
		f'/data modify entity @n[tag={ns}.element.base_coordinates,distance=..10] data.start_function set value "namespace:path/to/function"',
		"yellow", "Click to edit start_function (called once when game starts)", action="suggest_command"
	)
	clear_start_fn_btn = Dialogs.btn(
		"✗",
		f'/data remove entity @n[tag={ns}.element.base_coordinates,distance=..10] data.start_function',
		"red", "Clear start_function (won't be called)", action="run_command"
	)
	edit_tick_fn_btn = Dialogs.btn(
		"✎",
		f'/data modify entity @n[tag={ns}.element.base_coordinates,distance=..10] data.tick_function set value "namespace:path/to/function"',
		"yellow", "Click to edit tick_function (called every game tick)", action="suggest_command"
	)
	clear_tick_fn_btn = Dialogs.btn(
		"✗",
		f'/data remove entity @n[tag={ns}.element.base_coordinates,distance=..10] data.tick_function',
		"red", "Clear tick_function (won't be called)", action="run_command"
	)
	shown: str = f"execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] "
	return [
		shown + '["  ","⬟ ",{"text":"Base Coordinates Configuration","color":"light_purple","bold":true}]',
		shown + f'["    ",{{"text":"start_function: ","color":"gray"}},{{"entity":"@s","nbt":"data.start_function","color":"white"}}," ",{edit_start_fn_btn}," ",{clear_start_fn_btn}]',
		shown + f'["    ",{{"text":"tick_function: ","color":"gray"}},{{"entity":"@s","nbt":"data.tick_function","color":"white"}}," ",{edit_tick_fn_btn}," ",{clear_tick_fn_btn}]',
		shown + '["    ","💎 ",{"text":"start_function is called once when the game starts, tick_function every game tick.","color":"dark_gray","italic":true}]',
	]


def write_light_fields() -> list[str]:
	""" Write maps/light_fields/<etype>, restoring the fields a saved map leaves out and upgrading pre-26.3 block states.

	Returns:
		The lines an editor marker runs to dispatch to them.
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	light_elements: dict[str, ElementDef] = {etype: einfo for etype, einfo in ZB_ELEMENTS.items() if einfo.light_fields}
	for etype, einfo in light_elements.items():
		light_lines: list[str] = [f"# @s = an entity holding one saved {etype} compound in data (editor marker or in-game display)"]
		for field in einfo.light_fields:
			path: str = f"entity @s data.{field}"
			light_lines += [
				f"execute if data {path}.Name run data modify {path}.id set from {path}.Name",
				f"execute if data {path}.Properties run data modify {path}.properties set from {path}.Properties",
				f"data remove {path}.Name",
				f"data remove {path}.Properties",
				f"execute unless data {path} run data modify {path} set value {snbt_suggest(einfo.defaults[field])}",
			]
		write_versioned_function(f"maps/light_fields/{etype}", "\n".join(light_lines))
	return [
		f"execute if entity @s[tag={ns}.element.{etype}] run function {ns}:v{version}/maps/light_fields/{etype}"
		for etype in light_elements
	]

