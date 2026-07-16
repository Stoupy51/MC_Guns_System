
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import dialog_function, dialog_run_btn, dialog_show_btn, register_dialog, register_value_picker


def generate_zombies_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Variant picker (Vanilla = classic CoD zombies, Zonweeb = passives/abilities/special zombies)
	variant_opts = [
		("Vanilla", f'/data modify storage {ns}:zombies game.variant set value "vanilla"', "yellow", "Classic CoD zombies: no passives, abilities, or special zombies"),
		("Zonweeb", f'/data modify storage {ns}:zombies game.variant set value "zonweeb"', "green", "Full experience: passives, abilities, and special zombies"),
	]
	register_value_picker("zombies/setup/variant", "Variant", "Choose the zombies experience", variant_opts, back_dialog="zombies/setup")

	## Main zombies setup dialog
	setup_actions = [
		dialog_run_btn("🗺 Select Map", f"/function {ns}:v{version}/zombies/map_select", "Browse and select a zombies map", "dark_green"),
		dialog_show_btn(f"{ns}:zombies/setup/variant", "🧬 Variant", "Choose the zombies experience"),
		dialog_run_btn("▶ START", f"/function {ns}:v{version}/zombies/start", "Start the zombies game", "green"),
		dialog_run_btn("■ STOP", f"/function {ns}:v{version}/zombies/stop", "Stop the zombies game", "red"),
		dialog_run_btn("👥 Manage Players", f"/function {ns}:v{version}/players/list_zombies", "Add or remove players from the zombies game", "dark_aqua"),
		dialog_run_btn("+ Join", f"/function {ns}:v{version}/zombies/join_game", "Join the ongoing zombies game as a late joiner", "yellow"),
	]
	register_dialog("zombies/setup", {
		"type": "minecraft:multi_action",
		"title": ["", "🧟 ", {"text": "Zombies Setup", "color": "dark_green", "bold": True}, " 🧟"],
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Pick a map and variant, then Start", "color": "gray"}}],
		"actions": setup_actions,
		"columns": 2,
		"exit_action": {
			"label": {"text": "◀ Back", "color": "gray"},
			"tooltip": {"text": "Return to the game modes menu"},
			"action": {"type": "run_command", "command": f"/function {dialog_function('config/modes')}"},
		},
	})

	# /function .../zombies/setup now opens the dialog
	write_versioned_function("zombies/setup", f"function {dialog_function('zombies/setup')}")

	## Map selection menu: build a dialog listing all available zombies maps
	write_versioned_function("zombies/map_select", f"""
# Build the base map-select dialog (empty actions), then append one button per map
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🗺 ",{{text:"Select Zombies Map",color:"dark_green",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"Click a map to select it",color:"gray"}}}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{{label:{{text:"◀ Back",color:"gray"}},tooltip:{{text:"Return to setup"}},action:{{type:"run_command",command:"/function {ns}:v{version}/zombies/setup"}}}}}}

# Copy maps list and iterate (select_entry appends one button per map)
data modify storage {ns}:temp _map_iter set from storage {ns}:maps zombies
scoreboard players set #map_idx {ns}.data 0
data modify storage {ns}:temp _map_select_mode set value "zombies"
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage {ns}:temp dialog.actions[0] run data modify storage {ns}:temp dialog.actions append value {{label:{{text:"No zombies maps",color:"red"}},tooltip:{{text:"Create one in the map editor first"}},action:{{type:"run_command",command:"/function {ns}:v{version}/zombies/setup"}}}}

# Show the completed dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
