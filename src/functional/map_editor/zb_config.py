""" Per-map zombies defaults and the field-by-field panel for one placed element. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..map_editor_defs import ALL_ELEMENTS, FIELD_DOCS, OPTIONAL_LIST_FIELDS
from .shared import SEP, ZB_ELEMENTS, snbt_compound, snbt_suggest


# Functions
def write_editor_zb_config() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Handle ZB Defaults (configure defaults for new zombies elements)
	zb_defaults_lines: list[str] = []
	zb_defaults_lines.append(f"tellraw @a[tag={ns}.map_editor] {SEP}")
	zb_defaults_lines.append(f'tellraw @a[tag={ns}.map_editor] [{{"text":"","color":"white","bold":true}},"  ⚙ ",{{"text":"Zombies Element Defaults"}}]')
	zb_defaults_lines.append(f'tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"New elements use these values on placement","color":"gray","italic":true}}]')
	zb_defaults_lines.append(f"tellraw @a[tag={ns}.map_editor] {SEP}")
	zb_defaults_lines.append("")

	# Shared group_id default
	group_id_btn = Dialogs.btn(
		"\u270e",
		f"/data modify storage {ns}:temp map_edit.zb_defaults.group_id set value 0",
		"aqua", "Click to edit group_id", action="suggest_command"
	)
	zb_defaults_lines.append(
		f'tellraw @a[tag={ns}.map_editor] '
		f'["  ",{{"text":"group_id: ","color":"gray"}},'
		f'{{"storage":"{ns}:temp","nbt":"map_edit.zb_defaults.group_id","color":"white"}}," ",{group_id_btn}]'
	)
	zb_defaults_lines.append(f'tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"Applies to Zombie Spawn & Player Spawn.","color":"dark_gray","italic":true}}]')
	zb_defaults_lines.append("")

	for etype, einfo in ZB_ELEMENTS.items():
		if not einfo.defaults:
			continue  # Skip elements with no type-specific defaults
		zb_defaults_lines.append(
			f'tellraw @a[tag={ns}.map_editor] ["  ","{einfo.emoji} ",{{"text":"{einfo.name}","color":"{einfo.color}","bold":true}}]'
		)
		for field, default_val in einfo.defaults.items():
			snbt_val = snbt_suggest(default_val)
			edit_btn = Dialogs.btn(
				"✎",
				f"/data modify storage {ns}:temp map_edit.zb_defaults.{etype}.{field} set value {snbt_val}",
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

	# Init ZB Defaults (called on editor enter for zombies mode) ─
	init_defaults_lines: list[str] = []
	init_defaults_lines.append(f'data modify storage {ns}:temp map_edit.zb_defaults.group_id set value 0')
	for etype, einfo in ZB_ELEMENTS.items():
		compound = snbt_compound(einfo.defaults)
		init_defaults_lines.append(f'data modify storage {ns}:temp map_edit.zb_defaults.{etype} set value {compound}')

	write_versioned_function("maps/editor/init_zb_defaults", "\n".join(init_defaults_lines))

	# Handle ZB Configure (configure nearest element).
	write_versioned_function("maps/editor/handle_zb_configure", f"""
# Find the nearest map element marker (within 10 blocks)
execute at @s as @n[tag={ns}.map_element,distance=..10] run function {ns}:v{version}/maps/editor/show_element_config
execute at @s unless entity @n[tag={ns}.map_element,distance=..10] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 10 blocks!","color":"red"}}]
""")

	# show_element_config: runs as the nearest marker, shows type-specific fields
	zb_config_lines: list[str] = []
	zb_config_lines.append(f"tellraw @a[tag={ns}.map_editor] {SEP}")

	# For each zb_object type, show its fields
	for etype, einfo in ZB_ELEMENTS.items():
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["  ","{einfo.emoji} ",{{"text":"{einfo.name} Configuration","color":"{einfo.color}","bold":true}}]'
		)
		# group_id only shown for spawn-type zombies elements.
		# Doors don't carry a separate group_id: a door's link_id is its front-room group, and back_group_id is the back room.
		if etype in ("zombie_spawn", "player_spawn_zb", "special_spawn"):
			group_id_edit_btn = Dialogs.btn(
				"✎",
				f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.group_id set value 0",
				"yellow", "Click to edit group_id", action="suggest_command"
			)
			zb_config_lines.append(
				f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
				f'["    ",{{"text":"group_id: ","color":"gray"}},'
				f'{{"entity":"@s","nbt":"data.group_id","color":"white"}}," ",{group_id_edit_btn}]'
			)
		for field, default_val in einfo.defaults.items():
			snbt_val = snbt_suggest(default_val)
			# Edit button suggests the current default value; optional list fields suggest a usable template instead of empty brackets so they're easy to fill in.
			edit_value = OPTIONAL_LIST_FIELDS.get(field, snbt_val)
			# Door fields (except link_id) use propagation to all doors with same link_id.
			if etype == "door" and field != "link_id":
				# Two entry points, not eight: a macro cannot re-quote its argument, so the string fields and the numeric fields need one variant each.
				kind: str = "text" if isinstance(default_val, str) else "number"
				edit_cmd = f'/function {ns}:v{version}/maps/editor/set_door_link_{kind} {{field:"{field}",value:{snbt_val}}}'
				hover_text = f"Sets {field} on ALL doors with same link_id"
			else:
				edit_cmd = f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.{field} set value {edit_value}"
				hover_text = f"Click to edit {field}"
			edit_btn = Dialogs.btn(
				"✎",
				edit_cmd,
				"yellow", hover_text, action="suggest_command"
			)
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
			zb_config_lines.append(
				f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
				f'["    ",{{"text":"{field}: ","color":"gray"}},'
				f'{{"entity":"@s","nbt":"data.{field}","color":"white"}}," ",{edit_btn}{clear_component}{info_component}]'
			)

	# Backfill missing config fields on markers summoned from an already-saved map, so a field added to `defaults` after the map was written shows its default in the config UI instead of a blank row (e.g. partial_price on doors/perk machines).
	# Absent-only: never touches a set value.
	backfill_lines: list[str] = []
	for etype, einfo in ZB_ELEMENTS.items():
		for field, default_val in einfo.defaults.items():
			backfill_lines.append(
				f"execute if entity @s[tag={ns}.element.{etype}] unless data entity @s data.{field} "
				f"run data modify entity @s data.{field} set value {snbt_suggest(default_val)}"
			)
	write_versioned_function("maps/editor/backfill_zb_defaults", "\n".join(backfill_lines))

	# For spawn types: show yaw
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo.save_type != "spawn":
			continue
		edit_yaw_btn = Dialogs.btn(
			"✎",
			f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.yaw set value 0.0f",
			"yellow", "Click to edit yaw", action="suggest_command"
		)
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["  ","{einfo.emoji} ",{{"text":"{einfo.name}","color":"{einfo.color}","bold":true}}]'
		)
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["    ",{{"text":"yaw: ","color":"gray"}},'
			f'{{"entity":"@s","nbt":"data.yaw","color":"white"}}," ",{edit_yaw_btn}]'
		)

	# For zb_object types: show yaw (rotation)
	for etype, _ in ZB_ELEMENTS.items():
		edit_yaw_btn = Dialogs.btn(
			"✎",
			f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.yaw set value 0.0f",
			"yellow", "Click to edit yaw", action="suggest_command"
		)
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["    ",{{"text":"yaw: ","color":"gray"}},'
			f'{{"entity":"@s","nbt":"data.yaw","color":"white"}}," ",{edit_yaw_btn}]'
		)

	# For enemy types: show function.
	# The suggestion must stay version-independent like the map default above, or a map saved today calls a path that a later pack version no longer ships.
	edit_fn_btn = Dialogs.btn(
		"✎",
		f"/data modify entity @n[tag={ns}.element.enemy,distance=..10] data.function set value '{ns}:mob/default/level_1'",
		"yellow", "Click to edit function", action="suggest_command"
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.enemy] run tellraw @a[tag={ns}.map_editor] '
		f'["  ","👤 ",{{"text":"Enemy Configuration","color":"red","bold":true}}]'
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.enemy] run tellraw @a[tag={ns}.map_editor] '
		f'["    ",{{"text":"function: ","color":"gray"}},'
		f'{{"entity":"@s","nbt":"data.function","color":"white"}}," ",{edit_fn_btn}]'
	)

	# For point types: no configurable fields
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo.save_type != "point":
			continue
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["  ","{einfo.emoji} ",{{"text":"{einfo.name} — no configurable fields","color":"gray","italic":true}}]'
		)

	# For base_coordinates: show start_function and tick_function
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
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] '
		f'["  ","⬟ ",{{"text":"Base Coordinates Configuration","color":"light_purple","bold":true}}]'
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] '
		f'["    ",{{"text":"start_function: ","color":"gray"}},{{"entity":"@s","nbt":"data.start_function","color":"white"}}," ",{edit_start_fn_btn}," ",{clear_start_fn_btn}]'
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] '
		f'["    ",{{"text":"tick_function: ","color":"gray"}},{{"entity":"@s","nbt":"data.tick_function","color":"white"}}," ",{edit_tick_fn_btn}," ",{clear_tick_fn_btn}]'
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] '
		f'["    ","💎 ",{{"text":"start_function is called once when the game starts, tick_function every game tick.","color":"dark_gray","italic":true}}]'
	)

	zb_config_lines.append(f"tellraw @a[tag={ns}.map_editor] {SEP}")

	write_versioned_function("maps/editor/show_element_config", "\n".join(zb_config_lines))

