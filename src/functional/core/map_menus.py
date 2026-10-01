""" Shared map selection menu entry (recursive dialog builder). """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_shared_map_menus() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		## Adds the mode to each entry and calls select_entry, which appends one button per map; the caller sets _map_iter and _map_select_mode, builds the base dialog with no actions, and shows it after.
		write_versioned_function("shared/maps/select_iter", f"""
execute unless data storage {ns}:temp _map_iter[0] run return fail

data modify storage {ns}:temp _map_entry set from storage {ns}:temp _map_iter[0]
data modify storage {ns}:temp _map_entry.mode set from storage {ns}:temp _map_select_mode

function {ns}:v{version}/shared/maps/select_entry with storage {ns}:temp _map_entry

data remove storage {ns}:temp _map_iter[0]
scoreboard players add #map_idx {ns}.data 1
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter
""")

		## Macro (mode, id, name, description): a button selecting this map, run as the clicking player.
		write_versioned_function("shared/maps/select_entry", f"""
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:{{text:"$(description)"}},action:{{type:"run_command",command:"/data modify storage {ns}:$(mode) game.map_id set value \\"$(id)\\""}}}}
""")

