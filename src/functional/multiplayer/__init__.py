
# ruff: noqa: E501
# Imports
import json

from stewbeet import JsonDict, Mem, write_function, write_load_file, write_tag, write_versioned_function

from .classes import CLASSES


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Scoreboards & Storage Setup
	## ============================
	write_load_file(
f"""
## Multiplayer scoreboards
# Team assignment (1 = red, 2 = blue, 0 = none/spectator)
scoreboard objectives add {ns}.mp.team dummy
# Personal stats
scoreboard objectives add {ns}.mp.kills dummy
scoreboard objectives add {ns}.mp.deaths dummy
# Round timer (ticks remaining)
scoreboard objectives add {ns}.mp.timer dummy

# Initialize team scores (only if not already set)
execute unless score #red {ns}.mp.team matches -2147483648.. run scoreboard players set #red {ns}.mp.team 0
execute unless score #blue {ns}.mp.team matches -2147483648.. run scoreboard players set #blue {ns}.mp.team 0

# Initialize game state
data modify storage {ns}:multiplayer game set value {{state:"lobby",gamemode:"tdm",score_limit:30,time_limit:12000}}
""")

	## ============================
	## Signal function tags
	## ============================
	for event in ["register_maps", "register_classes", "on_game_start", "on_game_end"]:
		write_tag(f"multiplayer/{event}", Mem.ctx.data[ns].function_tags, [])

	## ============================
	## Default Class Registration
	## ============================
	for class_id, class_data in CLASSES.items():
		class_json: str = json.dumps(class_data)
		write_load_file(f"data modify storage {ns}:multiplayer classes.{class_id} set value {class_json}")

	## ============================
	## Per-class loadout functions
	## ============================
	for class_id, class_data in CLASSES.items():
		commands: str = f"""
# Apply class: {class_data['name']} - {class_data['lore']}
clear @s

# Give main weapon
loot give @s loot {ns}:i/{class_data['main']['gun']}
"""
		for _ in range(class_data["main"].get("mag_count", 0)):
			commands += f"loot give @s loot {ns}:i/{class_data['main']['mag']}\n"

		if "secondary" in class_data:
			commands += f"\n# Give secondary weapon\nloot give @s loot {ns}:i/{class_data['secondary']['gun']}\n"
			for _ in range(class_data["secondary"].get("mag_count", 0)):
				commands += f"loot give @s loot {ns}:i/{class_data['secondary']['mag']}\n"

		if "equipment" in class_data:
			commands += "\n# Give equipment\n"
			for item_id, count in class_data["equipment"].items():
				for _ in range(count):
					commands += f"loot give @s loot {ns}:i/{item_id}\n"

		write_versioned_function(f"multiplayer/class/{class_id}", commands)

	## ============================
	## Class Selection Menu
	## ============================
	def btn(label: str, command: str, color: str = "yellow", hover: str = "") -> str:
		""" Create a clickable button JSON component. """
		obj: JsonDict = {"text": f"[{label}]", "color": color, "click_event": {"action": "run_command", "command": command}}
		if hover:
			obj["hover_event"] = {"action": "show_text", "value": hover}
		return json.dumps(obj)

	sep = '{"text":"============================================","color":"dark_gray"}'
	blank = '""'
	title = f'[{blank},{{"text":"       ⚔ Select Your Class ⚔","color":"gold","bold":true}}]'

	class_btns_lines: str = ""
	for class_id, class_data in CLASSES.items():
		name: str = class_data["name"]
		lore: str = class_data["lore"]
		main_gun: str = class_data["main"]["gun"].upper().replace("_", " ")
		secondary_gun: str = class_data.get("secondary", {}).get("gun", "").upper().replace("_", " ")
		hover_text: str = f"{lore}\nMain: {main_gun}\nSecondary: {secondary_gun}"
		btn_json: str = btn(name, f"/function {ns}:v{version}/multiplayer/class/{class_id}", "green", hover_text)
		lore_json = f'{{"text":" {lore}","color":"gray","italic":true}}'
		class_btns_lines += f"tellraw @s [{blank},{btn_json},{lore_json}]\n"

	write_function(f"{ns}:multiplayer/select_class",
f"""tellraw @s {sep}
tellraw @s {title}
tellraw @s {sep}
{class_btns_lines}tellraw @s {sep}
""")

	## ============================
	## Team Management
	## ============================
	write_versioned_function("multiplayer/join_red",
f"""
scoreboard players set @s {ns}.mp.team 1
team join {ns}.red @s
tellraw @s [{blank},{{"text":"You joined ","color":"white"}},{{"text":"Red Team","color":"red","bold":true}}]
""")
	write_versioned_function("multiplayer/join_blue",
f"""
scoreboard players set @s {ns}.mp.team 2
team join {ns}.blue @s
tellraw @s [{blank},{{"text":"You joined ","color":"white"}},{{"text":"Blue Team","color":"blue","bold":true}}]
""")

	write_versioned_function("multiplayer/auto_assign_team",
f"""
# Count players on each team
execute store result score #red_count {ns}.data if entity @a[scores={{{ns}.mp.team=1}}]
execute store result score #blue_count {ns}.data if entity @a[scores={{{ns}.mp.team=2}}]

# Assign to team with fewer players (red if tied)
execute if score #red_count {ns}.data <= #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_red
execute if score #red_count {ns}.data > #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_blue
""")

	# Team setup in load
	write_load_file(
f"""
# Create teams
execute unless score #mp_teams_created {ns}.data matches 1 run team add {ns}.red
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red color red
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red friendlyFire false
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red nametagVisibility hideForOtherTeams
execute unless score #mp_teams_created {ns}.data matches 1 run team add {ns}.blue
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue color blue
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue friendlyFire false
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue nametagVisibility hideForOtherTeams
scoreboard players set #mp_teams_created {ns}.data 1
""")

	## ============================
	## Game Start / Stop
	## ============================
	write_function(f"{ns}:multiplayer/start",
f"""
# Initialize game
data modify storage {ns}:multiplayer game.state set value "active"

# Reset scores
scoreboard players set #red {ns}.mp.team 0
scoreboard players set #blue {ns}.mp.team 0
scoreboard players set @a {ns}.mp.kills 0
scoreboard players set @a {ns}.mp.deaths 0

# Set timer from time_limit
execute store result score #mp_timer {ns}.data run data get storage {ns}:multiplayer game.time_limit
scoreboard players operation @a {ns}.mp.timer = #mp_timer {ns}.data

# Call register hooks (external datapacks can set up maps/classes)
function #{ns}:multiplayer/register_maps
function #{ns}:multiplayer/register_classes

# Signal game start
function #{ns}:multiplayer/on_game_start

# Announce
tellraw @a [{blank},{{"text":"⚔ Game Started! ","color":"gold","bold":true}},{{"text":"Good luck!","color":"yellow"}}]
""")

	write_function(f"{ns}:multiplayer/stop",
f"""
# End game
data modify storage {ns}:multiplayer game.state set value "lobby"

# Signal game end
function #{ns}:multiplayer/on_game_end

# Announce scores
tellraw @a [{blank},{{"text":"⚔ Game Over! ","color":"gold","bold":true}}]
tellraw @a [{blank},{{"text":"  Red: ","color":"red"}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"white"}},{{"text":" | Blue: ","color":"blue"}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"white"}}]

# Clear teams
scoreboard players set @a {ns}.mp.team 0
""")

	## ============================
	## Gamemode Configuration Menu
	## ============================
	def gamemode_btn(label: str, gamemode: str, color: str = "yellow") -> str:
		return btn(label, f'/data modify storage {ns}:multiplayer game.gamemode set value "{gamemode}"', color, f"Set gamemode to {label}")

	gm_sep = sep
	gm_title = f'[{blank},{{"text":"       ⚙ Multiplayer Setup ⚙","color":"gold","bold":true}}]'

	gm_btns = ",".join([
		gamemode_btn("FFA", "ffa", "green"),
		gamemode_btn("TDM", "tdm", "yellow"),
		gamemode_btn("CTF", "ctf", "red"),
	])
	gm_line = f'[{blank},{{"text":"  Gamemode: ","color":"white"}},{gm_btns}]'

	sl_btns = ",".join([
		btn(str(n), f"/data modify storage {ns}:multiplayer game.score_limit set value {n}",
			"green" if n == 30 else "yellow", f"Set score limit to {n}")
		for n in [10, 20, 30, 50, 100]
	])
	sl_line = f'[{blank},{{"text":"  Score Limit: ","color":"white"}},{sl_btns}]'

	tl_options = [("3min", 3600), ("5min", 6000), ("10min", 12000), ("15min", 18000), ("∞", 72000)]
	tl_btns = ",".join([
		btn(label, f"/data modify storage {ns}:multiplayer game.time_limit set value {ticks}",
			"green" if ticks == 12000 else "yellow", f"Set time limit to {label}")
		for label, ticks in tl_options
	])
	tl_line = f'[{blank},{{"text":"  Time Limit: ","color":"white"}},{tl_btns}]'

	start_btn = btn("▶ START", f"/function {ns}:multiplayer/start", "green", "Start the match")
	stop_btn = btn("■ STOP", f"/function {ns}:multiplayer/stop", "red", "Stop the match")
	class_btn = btn("⚔ Classes", f"/function {ns}:multiplayer/select_class", "aqua", "Select your class")
	team_btn_red = btn("Red", f"/function {ns}:v{version}/multiplayer/join_red", "red", "Join Red Team")
	team_btn_blue = btn("Blue", f"/function {ns}:v{version}/multiplayer/join_blue", "blue", "Join Blue Team")
	team_btn_auto = btn("Auto", f"/function {ns}:v{version}/multiplayer/auto_assign_team", "yellow", "Auto-balance assign")

	actions_line = f'[{blank},{{"text":"  Actions: ","color":"white"}},{start_btn},{{"text":" "}},{stop_btn},{{"text":" "}},{class_btn}]'
	teams_line = f'[{blank},{{"text":"  Join Team: ","color":"white"}},{team_btn_red},{{"text":" "}},{team_btn_blue},{{"text":" "}},{team_btn_auto}]'

	write_function(f"{ns}:multiplayer/setup",
f"""tellraw @s {gm_sep}
tellraw @s {gm_title}
tellraw @s {gm_sep}
tellraw @s {gm_line}
tellraw @s {sl_line}
tellraw @s {tl_line}
tellraw @s {blank}
tellraw @s {teams_line}
tellraw @s {actions_line}
tellraw @s {gm_sep}
""")

	## ============================
	## Dynamic Map Registration
	## ============================
	write_versioned_function("multiplayer/register_map",
f"""
# Append map from mgs:input multiplayer.map to the maps list
# Expected format: {{name:"map_name", spawns:{{red:[x,y,z], blue:[x,y,z]}}, flags:{{red:[x,y,z], blue:[x,y,z]}}}}
data modify storage {ns}:multiplayer maps append from storage {ns}:input multiplayer.map
""")

	## ============================
	## Kill Tracking (Signal Listener)
	## ============================
	write_versioned_function("multiplayer/on_kill_signal",
f"""
# Only process if multiplayer game is active
execute unless data storage {ns}:multiplayer game{{state:"active"}} run return fail

# @s = killer player at this point
scoreboard players add @s {ns}.mp.kills 1

# Update team score based on killer's team
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1

# Check win condition (score limit)
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score #red {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
""", tags=[f"{ns}:signals/on_kill"])

	write_versioned_function("multiplayer/team_wins",
f"""
# Announce winner
$tellraw @a [{blank},{{"text":"🏆 ","color":"gold"}},{{"text":"$(team) Team Wins!","color":"gold","bold":true}}]
tellraw @a [{blank},{{"text":"  Final Score — Red: ","color":"white"}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"red"}},{{"text":" vs Blue: ","color":"gray"}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"blue"}}]

# End game
function {ns}:multiplayer/stop
""")

