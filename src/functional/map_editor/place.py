""" Catching an egg placement and routing it to the handler for that element. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS


# Functions
def write_editor_place() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# On Place (Advancement Reward).
	write_versioned_function("maps/editor/on_place", f"""
# Revoke advancement immediately so it can trigger again
advancement revoke @s only {ns}:v{version}/maps/editor/on_place

# Only process if player is in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Find the newly spawned bat entity (tagged by entity_data)
execute as @n[tag={ns}.new_element] at @s run function {ns}:v{version}/maps/editor/process_element
""")

	# Process Placed Element (universal - handles all types).
	process_lines: list[str] = []
	# Destroy handler first
	process_lines.append('# DESTROY handler')
	process_lines.append(f'execute if entity @s[tag={ns}.element.destroy] run function {ns}:v{version}/maps/editor/handle_destroy')
	process_lines.append(f'execute if entity @s[tag={ns}.element.destroy] run return run kill @s')
	process_lines.append("")

	for etype, einfo in ALL_ELEMENTS.items():
		save_type = einfo.save_type
		if save_type == "base":
			handler = "handle_base"
		elif save_type == "spawn":
			handler = "handle_spawn"
		elif save_type == "point":
			handler = "handle_point"
		elif save_type == "config":
			handler = "handle_config"
		elif save_type == "enemy":
			handler = "handle_enemy"
		elif save_type == "start_command":
			handler = "handle_start_command"
		elif save_type == "respawn_command":
			handler = "handle_respawn_command"
		elif save_type == "zb_object":
			handler = "handle_zb_object"
		else:
			continue
		process_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run function {ns}:v{version}/maps/editor/{handler}')
		process_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run return run kill @s')
		process_lines.append("")

	# Zombies utility tool handlers
	process_lines.append("# Zombies utility tool handlers")
	process_lines.append(f'execute if entity @s[tag={ns}.element.zb_defaults] run function {ns}:v{version}/maps/editor/handle_zb_defaults')
	process_lines.append(f'execute if entity @s[tag={ns}.element.zb_defaults] run return run kill @s')
	process_lines.append(f'execute if entity @s[tag={ns}.element.zb_configure] run function {ns}:v{version}/maps/editor/handle_zb_configure')
	process_lines.append(f'execute if entity @s[tag={ns}.element.zb_configure] run return run kill @s')
	process_lines.append("")

	# Editor utility handlers (save, exit, save & exit)
	process_lines.append("# Editor utility handlers")
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_save_exit] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/save_exit')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_save_exit] run return run kill @s')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_exit] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/exit')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_exit] run return run kill @s')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_save] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/save_only')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_save] run return run kill @s')
	process_lines.append("")

	process_lines.append("# Fallback: unknown type")
	process_lines.append("kill @s")

	write_versioned_function("maps/editor/process_element", "\n".join(process_lines))

