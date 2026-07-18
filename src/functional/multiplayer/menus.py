
# ruff: noqa: E501
# Imports

from stewbeet import Mem, write_versioned_function

from ..helpers import dialog_function, dialog_run_btn, dialog_show_btn, register_dialog, register_value_picker


def generate_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ---- Value pickers (each opens from the setup dialog; Back returns there) ----
	# Gamemode
	gm_data = [("FFA", "ffa", "green"), ("TDM", "tdm", "yellow"), ("DOM", "dom", "aqua"), ("HP", "hp", "dark_purple"), ("S&D", "snd", "gold")]
	gamemode_opts = [
		(label, f'/data modify storage {ns}:multiplayer game.gamemode set value "{gm}"', color, f"Set gamemode to {label}")
		for label, gm, color in gm_data
	]
	register_value_picker("multiplayer/setup/gamemode", "Gamemode", "Choose the multiplayer gamemode", gamemode_opts, back_dialog="multiplayer/setup")

	# Score Limit
	score_limit_opts = [
		(str(n), f"/data modify storage {ns}:multiplayer game.score_limit set value {n}", "green" if n == 50 else "yellow", f"Set score limit to {n}")
		for n in [10, 20, 30, 50, 100, 200, 300, 500]
	]
	register_value_picker("multiplayer/setup/score_limit", "Score Limit", "Set the score needed to win", score_limit_opts, back_dialog="multiplayer/setup")

	# Time Limit
	tl_data = [("3min", 3600), ("5min", 6000), ("10min", 12000), ("15min", 18000), ("∞", 72000)]
	time_limit_opts = [
		(label, f"/data modify storage {ns}:multiplayer game.time_limit set value {ticks}", "green" if ticks == 12000 else "yellow", f"Set time limit to {label}")
		for label, ticks in tl_data
	]
	register_value_picker("multiplayer/setup/time_limit", "Time Limit", "Set the match time limit", time_limit_opts, back_dialog="multiplayer/setup")

	## ---- Main multiplayer setup dialog ----
	setup_actions = [
		dialog_show_btn(f"{ns}:multiplayer/setup/gamemode", "🎮 Gamemode", "Choose the multiplayer gamemode"),
		dialog_show_btn(f"{ns}:multiplayer/setup/score_limit", "🏆 Score Limit", "Set the score needed to win"),
		dialog_show_btn(f"{ns}:multiplayer/setup/time_limit", "⏱ Time Limit", "Set the match time limit"),
		dialog_run_btn("🗺 Select Map", f"/function {ns}:v{version}/multiplayer/map_select", "Browse and select a map", "aqua"),
		dialog_run_btn("▶ START", f"/function {ns}:v{version}/multiplayer/start", "Start the match", "green"),
		dialog_run_btn("■ STOP", f"/function {ns}:v{version}/multiplayer/stop", "Stop the match", "red"),
		dialog_run_btn("⚔ Classes", f"/function {ns}:v{version}/multiplayer/select_class", "Select your class", "aqua"),
		dialog_run_btn("+ Join", f"/function {ns}:v{version}/multiplayer/join_game", "Join the ongoing game as a late joiner", "yellow"),
		dialog_run_btn("Red Team", f"/function {ns}:v{version}/multiplayer/join_red", "Join Red Team", "red"),
		dialog_run_btn("Blue Team", f"/function {ns}:v{version}/multiplayer/join_blue", "Join Blue Team", "blue"),
		dialog_run_btn("Auto Team", f"/execute as @a[sort=random] run function {ns}:v{version}/multiplayer/auto_assign_team", "Auto-balance across Red/Blue (in FFA, seats everyone on the single FFA team)", "yellow"),
		dialog_run_btn("👥 Manage Players", f"/function {ns}:v{version}/players/list_multiplayer", "Assign players to Red/Blue teams", "dark_aqua"),
	]
	register_dialog("multiplayer/setup", {
		"type": "minecraft:multi_action",
		"title": ["", "⚙ ", {"text": "Multiplayer Setup", "color": "gold", "bold": True}, " ⚙"],
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Configure the match, then Start", "color": "gray"}}],
		"actions": setup_actions,
		"columns": 2,
		"exit_action": {
			"label": {"text": "◀ Back", "color": "gray"},
			"tooltip": {"text": "Return to the configuration menu"},
			"action": {"type": "run_command", "command": f"/function {dialog_function('config')}"},
		},
	})

	# /function .../multiplayer/setup now opens the dialog
	write_versioned_function("multiplayer/setup", f"function {dialog_function('multiplayer/setup')}")

	## Map selection menu: build a dialog listing all available multiplayer maps
	write_versioned_function("multiplayer/map_select", f"""
# Build the base map-select dialog (empty actions), then append one button per map
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🗺 ",{{text:"Select Map",color:"aqua",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"Click a map to select it",color:"gray"}}}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{{label:{{text:"◀ Back",color:"gray"}},tooltip:{{text:"Return to setup"}},action:{{type:"run_command",command:"/function {ns}:v{version}/multiplayer/setup"}}}}}}

# Copy maps list and iterate (select_entry appends one button per map)
data modify storage {ns}:temp _map_iter set from storage {ns}:maps multiplayer
scoreboard players set #map_idx {ns}.data 0
data modify storage {ns}:temp _map_select_mode set value "multiplayer"
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage {ns}:temp dialog.actions[0] run data modify storage {ns}:temp dialog.actions append value {{label:{{text:"No maps registered",color:"red"}},tooltip:{{text:"Create one in the map editor first"}},action:{{type:"run_command",command:"/function {ns}:v{version}/multiplayer/setup"}}}}

# Show the completed dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
