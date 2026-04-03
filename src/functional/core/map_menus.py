
# Shared map selection menu entry (recursive tellraw)
from stewbeet import Mem, write_versioned_function


def write_shared_map_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Map select iterator: injects mode into each entry, then calls select_entry
	## Caller must set: _map_iter (list), _map_select_mode (string)
	write_versioned_function("shared/maps/select_iter", f"""
execute unless data storage {ns}:temp _map_iter[0] run return fail

# Inject mode into the first entry for the macro
data modify storage {ns}:temp _map_entry set from storage {ns}:temp _map_iter[0]
data modify storage {ns}:temp _map_entry.mode set from storage {ns}:temp _map_select_mode

# Call shared entry
function {ns}:v{version}/shared/maps/select_entry with storage {ns}:temp _map_entry

# Advance
data remove storage {ns}:temp _map_iter[0]
scoreboard players add #map_idx {ns}.data 1
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter
""")

	## Map select entry (macro: mode, id, name, description)
	write_versioned_function("shared/maps/select_entry", f"""
$tellraw @s ["","  ",{{"text":""}},{{"text":"[$(name)]","color":"green","click_event":{{"action":"suggest_command","command":"/data modify storage {ns}:$(mode) game.map_id set value \\"$(id)\\""}},"hover_event":{{"action":"show_text","value":"Click to select '$(name)'"}}}},{{"text":" - $(description)","color":"gray"}}]
""")  # noqa: E501

