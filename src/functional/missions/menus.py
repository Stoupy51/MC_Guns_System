
# Imports

from ..helpers import btn
from ..generator import McfunctionGenerator


class MenusGenerator(McfunctionGenerator):
    """ Generates the menus datapack functions. """

    def generate(self) -> None:
    	ns: str = self.ns
    	version: str = self.version
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
    	teams_btn = btn("👥 Roster", f"/function {ns}:v{version}/multiplayer/show_teams", "dark_aqua", "Show which players have team assignments")
    	join_btn = btn("+ Join", f"/function {ns}:v{version}/missions/join_game", "yellow", "Join the ongoing mission as a late joiner")

    	actions_line = f'["",["","  ",{{"text":"Actions"}},": "],{start_btn}," ",{stop_btn}," ",{class_btn}," ",{teams_btn}," ",{join_btn}]'

    	self.func("missions/setup", f"""
tellraw @s {sep}
tellraw @s {setup_title}
tellraw @s {sep}
tellraw @s {map_line}
tellraw @s ""
tellraw @s {actions_line}
tellraw @s {sep}
""")

    	## Map selection menu: list all available mission maps
    	self.func("missions/map_select", f"""
tellraw @s {sep}
tellraw @s [{{"text":"","color":"aqua","bold":true}},"  🗺 ",{{"text":"Select Mission Map"}}]
tellraw @s {sep}

# Copy maps list for iteration
data modify storage {ns}:temp _map_iter set from storage {ns}:maps missions
scoreboard players set #map_idx {ns}.data 0
data modify storage {ns}:temp _map_select_mode set value "missions"
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter

execute unless data storage {ns}:maps missions[0] run tellraw @s ["  ",{{"text":"No mission maps! Create one in the map editor first.","color":"red"}}]
tellraw @s {sep}
""")


def generate_missions_menus() -> None:
	""" Module-level entry (preserved signature); delegates to :class:`MenusGenerator`. """
	MenusGenerator()()


