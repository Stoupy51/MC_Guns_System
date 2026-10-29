""" Catching an egg placement and routing it to the handler for that element. """

# Imports
from stewbeet import McFunction, Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS


# Functions
def write_editor_place() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("maps/editor/on_place", f"""
advancement revoke @s only {ns}:v{version}/maps/editor/on_place

execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# The bat the egg spawned (tagged through entity_data).
execute as @n[tag={ns}.new_element] at @s run function {ns}:v{version}/maps/editor/process_element
""")

	process_element: McFunction = f"""
# DESTROY handler
execute if entity @s[tag={ns}.element.destroy] run function {ns}:v{version}/maps/editor/handle_destroy
execute if entity @s[tag={ns}.element.destroy] run return run kill @s
"""
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
		process_element += f"""
execute if entity @s[tag={ns}.element.{etype}] run function {ns}:v{version}/maps/editor/{handler}
execute if entity @s[tag={ns}.element.{etype}] run return run kill @s
"""
	# Finally, add the handlers for the utility elements (zombies and editor)
	write_versioned_function("maps/editor/process_element", process_element + f"""
# Zombies utility tool handlers
execute if entity @s[tag={ns}.element.zb_defaults] run function {ns}:v{version}/maps/editor/handle_zb_defaults
execute if entity @s[tag={ns}.element.zb_defaults] run return run kill @s
execute if entity @s[tag={ns}.element.zb_configure] run function {ns}:v{version}/maps/editor/handle_zb_configure
execute if entity @s[tag={ns}.element.zb_configure] run return run kill @s

# Editor utility handlers
execute if entity @s[tag={ns}.element.editor_save_exit] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/save_exit
execute if entity @s[tag={ns}.element.editor_save_exit] run return run kill @s
execute if entity @s[tag={ns}.element.editor_exit] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/exit
execute if entity @s[tag={ns}.element.editor_exit] run return run kill @s
execute if entity @s[tag={ns}.element.editor_save] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/save_only
execute if entity @s[tag={ns}.element.editor_save] run return run kill @s

# Fallback: unknown type
kill @s
""")

