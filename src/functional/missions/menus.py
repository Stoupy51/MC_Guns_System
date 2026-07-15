
# ruff: noqa: E501
# Imports

from stewbeet import Mem, write_versioned_function

from ..helpers import dialog_run_btn, register_dialog


def generate_missions_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Main missions setup dialog
	setup_actions = [
		dialog_run_btn("🗺 Select Map", f"/function {ns}:v{version}/missions/map_select", "Browse and select a mission map", "aqua"),
		dialog_run_btn("▶ START", f"/function {ns}:v{version}/missions/start", "Start the mission", "green"),
		dialog_run_btn("■ STOP", f"/function {ns}:v{version}/missions/stop", "Stop the mission", "red"),
		dialog_run_btn("⚔ Classes", f"/function {ns}:v{version}/multiplayer/select_class", "Select your class", "aqua"),
		dialog_run_btn("👥 Manage Players", f"/function {ns}:v{version}/players/list_missions", "Add or remove players from the mission", "dark_aqua"),
		dialog_run_btn("+ Join", f"/function {ns}:v{version}/missions/join_game", "Join the ongoing mission as a late joiner", "yellow"),
	]
	register_dialog("missions/setup", {
		"type": "minecraft:multi_action",
		"title": {"text": "🎯 Missions Setup 🎯", "color": "aqua", "bold": True},
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Pick a map, then Start", "color": "gray"}}],
		"actions": setup_actions,
		"columns": 2,
		"exit_action": {
			"label": {"text": "◀ Back", "color": "gray"},
			"tooltip": {"text": "Return to the game modes menu"},
			"action": {"type": "show_dialog", "dialog": f"{ns}:config/modes"},
		},
	})

	# /function .../missions/setup now opens the dialog
	write_versioned_function("missions/setup", f"dialog show @s {ns}:missions/setup")

	## Map selection menu: build a dialog listing all available mission maps
	write_versioned_function("missions/map_select", f"""
# Build the base map-select dialog (empty actions), then append one button per map
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:{{text:"🗺 Select Mission Map",color:"aqua",bold:true}},body:[{{type:"minecraft:plain_message",contents:{{text:"Click a map to select it",color:"gray"}}}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{{label:{{text:"◀ Back",color:"gray"}},tooltip:{{text:"Return to setup"}},action:{{type:"show_dialog",dialog:"{ns}:missions/setup"}}}}}}

# Copy maps list and iterate (select_entry appends one button per map)
data modify storage {ns}:temp _map_iter set from storage {ns}:maps missions
scoreboard players set #map_idx {ns}.data 0
data modify storage {ns}:temp _map_select_mode set value "missions"
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage {ns}:temp dialog.actions[0] run data modify storage {ns}:temp dialog.actions append value {{label:{{text:"No mission maps",color:"red"}},tooltip:{{text:"Create one in the map editor first"}},action:{{type:"show_dialog",dialog:"{ns}:missions/setup"}}}}

# Show the completed dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
