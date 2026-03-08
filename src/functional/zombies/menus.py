
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import btn


def generate_zombies_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	sep = '{"text":"============================================","color":"dark_gray"}'

	## Zombies Setup Menu
	setup_title = '[{"text":"","color":"dark_green","bold":true},"       🧟 ",{"text":"Zombies Setup"}," 🧟"]'

	# Map selection button
	map_select_btn = btn("Select Map", f"/function {ns}:v{version}/zombies/map_select", "dark_green", "Browse and select a zombies map")
	map_line = f'["",["","  ",{{"text":"Map"}},": "],{map_select_btn}]'

	# Action buttons
	start_btn = btn("▶ START", f"/function {ns}:v{version}/zombies/start", "green", "Start the zombies game")
	stop_btn = btn("■ STOP", f"/function {ns}:v{version}/zombies/stop", "red", "Stop the zombies game")

	actions_line = f'["",["","  ",{{"text":"Actions"}},": "],{start_btn}," ",{stop_btn}]'

	write_versioned_function("zombies/setup", f"""
tellraw @s {sep}
tellraw @s {setup_title}
tellraw @s {sep}
tellraw @s {map_line}
tellraw @s ""
tellraw @s {actions_line}
tellraw @s {sep}
""")

	## Map selection menu: list all available zombies maps
	write_versioned_function("zombies/map_select", f"""
tellraw @s {sep}
tellraw @s [{{"text":"","color":"dark_green","bold":true}},"  🗺 ",{{"text":"Select Zombies Map"}}]
tellraw @s {sep}

# Copy maps list for iteration
data modify storage {ns}:temp _map_iter set from storage {ns}:maps zombies
scoreboard players set #_map_idx {ns}.data 0
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/zombies/map_select_entry with storage {ns}:temp _map_iter[0]

execute unless data storage {ns}:maps zombies[0] run tellraw @s [{{"text":"  No zombies maps! Create one in the map editor first.","color":"red"}}]
tellraw @s {sep}
""")

	## Map select entry (recursive macro)
	write_versioned_function("zombies/map_select_entry", f"""
$tellraw @s ["",{{"text":"  "}},{{"text":"[$(name)]","color":"green","click_event":{{"action":"run_command","command":"/data modify storage {ns}:zombies game.map_id set value \\"$(id)\\""}},"hover_event":{{"action":"show_text","value":"Click to select '$(name)'"}}}},{{"text":" - $(description)","color":"gray"}}]

data remove storage {ns}:temp _map_iter[0]
scoreboard players add #_map_idx {ns}.data 1
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/zombies/map_select_entry with storage {ns}:temp _map_iter[0]
""")  # noqa: E501

