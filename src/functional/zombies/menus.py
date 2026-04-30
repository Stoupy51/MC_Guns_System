
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
	teams_btn = btn("👥 Roster", f"/function {ns}:v{version}/multiplayer/show_teams", "dark_aqua", "Show which players have team assignments")
	join_btn = btn("+ Join", f"/function {ns}:v{version}/zombies/join_game", "yellow", "Join the ongoing zombies game as a late joiner")

	actions_line = f'["",["","  ",{{"text":"Actions"}},": "],{start_btn}," ",{stop_btn}," ",{teams_btn}," ",{join_btn}]'

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
scoreboard players set #map_idx {ns}.data 0
data modify storage {ns}:temp _map_select_mode set value "zombies"
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter

execute unless data storage {ns}:maps zombies[0] run tellraw @s ["  ",{{"text":"No zombies maps! Create one in the map editor first.","color":"red"}}]
tellraw @s {sep}
""")



