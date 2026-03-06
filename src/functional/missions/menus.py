
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import btn


def generate_missions_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	sep = '{"text":"============================================","color":"dark_gray"}'

	## Missions Setup Menu
	setup_title = '[{"text":"","color":"aqua","bold":true},"       🎯 ",{"text":"Missions Setup"}," 🎯"]'

	# Map selection button
	map_select_btn = btn("Select Map", f"/function {ns}:v{version}/missions/map_select", "aqua", "Browse and select a mission map")
	map_line = f'["",["","  ",{{"text":"Map"}},": "],{map_select_btn}]'

	# Action buttons
	start_btn = btn("▶ START", f"/function {ns}:v{version}/missions/start", "green", "Start the mission")
	stop_btn = btn("■ STOP", f"/function {ns}:v{version}/missions/stop", "red", "Stop the mission")
	class_btn = btn("⚔ Classes", f"/function {ns}:v{version}/multiplayer/select_class", "aqua", "Select your class")

	actions_line = f'["",["","  ",{{"text":"Actions"}},": "],{start_btn},{{"text":" "}},{stop_btn},{{"text":" "}},{class_btn}]'

	write_versioned_function("missions/setup", f"""
tellraw @s {sep}
tellraw @s {setup_title}
tellraw @s {sep}
tellraw @s {map_line}
tellraw @s ""
tellraw @s {actions_line}
tellraw @s {sep}
""")

	## Map selection menu: list all available mission maps
	write_versioned_function("missions/map_select", f"""
tellraw @s {sep}
tellraw @s [{{"text":"","color":"aqua","bold":true}},"  🗺 ",{{"text":"Select Mission Map"}}]
tellraw @s {sep}

# Copy maps list for iteration
data modify storage {ns}:temp _map_iter set from storage {ns}:maps missions
scoreboard players set #_map_idx {ns}.data 0
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/missions/map_select_entry with storage {ns}:temp _map_iter[0]

execute unless data storage {ns}:maps missions[0] run tellraw @s [{{"text":"  No mission maps! Create one in the map editor first.","color":"red"}}]
tellraw @s {sep}
""")

	## Map select entry (recursive macro)
	write_versioned_function("missions/map_select_entry", f"""
$tellraw @s ["",{{"text":"  "}},{{"text":"[$(name)]","color":"green","click_event":{{"action":"run_command","command":"/data modify storage {ns}:missions game.map_id set value \\"$(id)\\""}},"hover_event":{{"action":"show_text","value":"Click to select '$(name)'"}}}},{{"text":" - $(description)","color":"gray"}}]

data remove storage {ns}:temp _map_iter[0]
scoreboard players add #_map_idx {ns}.data 1
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/missions/map_select_entry with storage {ns}:temp _map_iter[0]
""")  # noqa: E501
