""" The missions config panel and its edit-nearest suggestions. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS
from .shared import SEP


# Functions
def write_editor_config() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Handle Config (missions utility).
	config_target = f"@p[tag={ns}.map_editor,distance=..6,sort=nearest]"
	config_lines: list[str] = []
	config_lines.append("# Initialize default enemy function if missing")
	config_lines.append(f'execute unless data storage {ns}:temp map_edit.map.default_enemy_function run data modify storage {ns}:temp map_edit.map.default_enemy_function set value "{ns}:mob/default/level_1 {{\\"entity\\":\\"pillager\\"}}"')
	config_lines.append("")
	config_lines.append(f"tellraw {config_target} {SEP}")
	config_lines.append(f'tellraw {config_target} [{{"text":"","color":"white","bold":true}},"  ⚙ ",{{"text":"Enemy Configuration"}}]')
	config_lines.append(f"tellraw {config_target} {SEP}")
	config_lines.append(
		f'tellraw {config_target} '
		f'["  ",{{"text":"Default Function: ","color":"gray"}},'
		f'{{"storage":"{ns}:temp","nbt":"map_edit.map.default_enemy_function","color":"white"}}]'
	)
	config_lines.append(f'data modify storage {ns}:temp _cfg.default_fn set from storage {ns}:temp map_edit.map.default_enemy_function')
	config_lines.append(f'function {ns}:v{version}/maps/editor/handle_config_default_btn with storage {ns}:temp _cfg')
	config_lines.append(f'tellraw {config_target} ["  ",{{"text":"ℹ Edit the function path above, then run the command.","color":"dark_gray","italic":true}}]')  # noqa: RUF001
	config_lines.append("")

	# Show nearest configurable elements that can use the default function.
	for etype, einfo in ALL_ELEMENTS.items():
		if not einfo.config_uses_default_function:
			continue
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run data modify storage {ns}:temp _cfg.default_fn set from storage {ns}:temp map_edit.map.default_enemy_function')
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run data modify storage {ns}:temp _cfg.nearest_fn set from entity @n[tag={ns}.element.{etype},distance=..10] data.function')
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run function {ns}:v{version}/maps/editor/handle_config_nearest_{etype}_btn with storage {ns}:temp _cfg')

	# Show nearest command-based mission objects.
	for etype in ("start_command", "respawn_command"):
		einfo = ALL_ELEMENTS[etype]
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run data modify storage {ns}:temp _cfg.nearest_cmd set from entity @n[tag={ns}.element.{etype},distance=..10] data.command')
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run function {ns}:v{version}/maps/editor/handle_config_nearest_{etype}_btn with storage {ns}:temp _cfg')

	config_lines.append(f"tellraw {config_target} {SEP}")

	write_versioned_function("maps/editor/handle_config", "\n".join(config_lines))

	write_versioned_function("maps/editor/handle_config_default_btn", f"""
$tellraw {config_target} ["    ",{{"text":"[Edit Function]","color":"aqua","click_event":{{"action":"suggest_command","command":"/data modify storage {ns}:temp map_edit.map.default_enemy_function set value \\"$(default_fn)\\""}},"hover_event":{{"action":"show_text","value":"Click to edit the default spawn function for new enemies"}}}}]
""")

	for etype, einfo in ALL_ELEMENTS.items():
		if not einfo.config_uses_default_function:
			continue
		write_versioned_function(f"maps/editor/handle_config_nearest_{etype}_btn", f"""
tellraw {config_target} {SEP}
tellraw {config_target} ["  ",{{"text":"Nearest {einfo.name}: ","color":"yellow","bold":true}},{{"entity":"@n[tag={ns}.element.{etype},distance=..10]","nbt":"data.function","color":"white"}}]
$tellraw {config_target} ["    ",{{"text":"[Edit Nearest {einfo.name}]","color":"yellow","click_event":{{"action":"suggest_command","command":"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.function set value \\"$(nearest_fn)\\""}},"hover_event":{{"action":"show_text","value":"Edit nearest {einfo.name.lower()} using its current function"}}}}]
""")

	for etype in ("start_command", "respawn_command"):
		einfo = ALL_ELEMENTS[etype]
		write_versioned_function(f"maps/editor/handle_config_nearest_{etype}_btn", f"""
tellraw {config_target} {SEP}
tellraw {config_target} ["  ",{{"text":"Nearest {einfo.name}: ","color":"yellow","bold":true}},{{"entity":"@n[tag={ns}.element.{etype},distance=..10]","nbt":"data.command","color":"white"}}]
$tellraw {config_target} ["    ",{{"text":"[Edit Nearest {einfo.name}]","color":"yellow","click_event":{{"action":"suggest_command","command":"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.command set value \\"$(nearest_cmd)\\""}},"hover_event":{{"action":"show_text","value":"Edit nearest {einfo.name.lower()} command using its current value"}}}}]
""")

