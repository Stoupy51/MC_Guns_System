
# Imports
import json

from stewbeet import JsonDict, Mem, write_versioned_function

from .classes import CLASSES


def btn(label: str, command: str, color: str = "yellow", hover: str = "") -> str:
	""" Create a clickable button JSON component. """
	obj: JsonDict = {"text": f"[{label}]", "color": color, "click_event": {"action": "run_command", "command": command}}
	if hover:
		obj["hover_event"] = {"action": "show_text", "value": hover}
	return json.dumps(obj)


def generate_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	blank = '""'
	sep = '{"text":"============================================","color":"dark_gray"}'

	## ============================
	## Class Selection Menu
	## ============================
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

	write_versioned_function("multiplayer/select_class", f"""
tellraw @s {sep}
tellraw @s {title}
tellraw @s {sep}
{class_btns_lines}tellraw @s {sep}
""")

	## ============================
	## Gamemode Configuration Menu
	## ============================
	def gamemode_btn(label: str, gamemode: str, color: str = "yellow") -> str:
		return btn(label, f'/data modify storage {ns}:multiplayer game.gamemode set value "{gamemode}"', color, f"Set gamemode to {label}")

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

	start_btn = btn("▶ START", f"/function {ns}:v{version}/multiplayer/start", "green", "Start the match")
	stop_btn = btn("■ STOP", f"/function {ns}:v{version}/multiplayer/stop", "red", "Stop the match")
	class_btn = btn("⚔ Classes", f"/function {ns}:v{version}/multiplayer/select_class", "aqua", "Select your class")
	team_btn_red = btn("Red", f"/function {ns}:v{version}/multiplayer/join_red", "red", "Join Red Team")
	team_btn_blue = btn("Blue", f"/function {ns}:v{version}/multiplayer/join_blue", "blue", "Join Blue Team")
	team_btn_auto = btn("Auto", f"/function {ns}:v{version}/multiplayer/auto_assign_team", "yellow", "Auto-balance assign")

	actions_line = f'[{blank},{{"text":"  Actions: ","color":"white"}},{start_btn},{{"text":" "}},{stop_btn},{{"text":" "}},{class_btn}]'
	teams_line = f'[{blank},{{"text":"  Join Team: ","color":"white"}},{team_btn_red},{{"text":" "}},{team_btn_blue},{{"text":" "}},{team_btn_auto}]'

	write_versioned_function("multiplayer/setup", f"""
tellraw @s {sep}
tellraw @s {gm_title}
tellraw @s {sep}
tellraw @s {gm_line}
tellraw @s {sl_line}
tellraw @s {tl_line}
tellraw @s {blank}
tellraw @s {teams_line}
tellraw @s {actions_line}
tellraw @s {sep}
""")
