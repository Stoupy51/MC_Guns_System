
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import btn


def generate_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	sep = '{"text":"============================================","color":"dark_gray"}'

	## Gamemode Configuration Menu
	def gamemode_btn(label: str, gamemode: str, color: str = "yellow") -> str:
		return btn(label, f'/data modify storage {ns}:multiplayer game.gamemode set value "{gamemode}"', color, f"Set gamemode to {label}")

	gm_title = '["",[{"text":"","color":"gold","bold":true},"       ⚙ ",{"text":"Multiplayer Setup"}," ⚙"]]'

	gm_btns = ",".join([
		gamemode_btn("FFA", "ffa", "green"),
		gamemode_btn("TDM", "tdm", "yellow"),
		gamemode_btn("CTF", "ctf", "red"),
	])
	gm_line = f'["",["","  ",{{"text":"Gamemode"}},": "],{gm_btns}]'

	sl_btns = ",".join([
		btn(str(n), f"/data modify storage {ns}:multiplayer game.score_limit set value {n}",
			"green" if n == 30 else "yellow", f"Set score limit to {n}")
		for n in [10, 20, 30, 50, 100]
	])
	sl_line = f'["",["","  ",{{"text":"Score Limit"}},": "],{sl_btns}]'

	tl_options = [("3min", 3600), ("5min", 6000), ("10min", 12000), ("15min", 18000), ("∞", 72000)]
	tl_btns = ",".join([
		btn(label, f"/data modify storage {ns}:multiplayer game.time_limit set value {ticks}",
			"green" if ticks == 12000 else "yellow", f"Set time limit to {label}")
		for label, ticks in tl_options
	])
	tl_line = f'["",["","  ",{{"text":"Time Limit"}},": "],{tl_btns}]'

	start_btn = btn("▶ START", f"/function {ns}:v{version}/multiplayer/start", "green", "Start the match")
	stop_btn = btn("■ STOP", f"/function {ns}:v{version}/multiplayer/stop", "red", "Stop the match")
	class_btn = btn("⚔ Classes", f"/function {ns}:v{version}/multiplayer/select_class", "aqua", "Select your class")
	team_btn_red = btn("Red", f"/function {ns}:v{version}/multiplayer/join_red", "red", "Join Red Team")
	team_btn_blue = btn("Blue", f"/function {ns}:v{version}/multiplayer/join_blue", "blue", "Join Blue Team")
	team_btn_auto = btn("Auto", f"/function {ns}:v{version}/multiplayer/auto_assign_team", "yellow", "Auto-balance assign")

	actions_line = f'["",["","  ",{{"text":"Actions"}},": "],{start_btn},{{"text":" "}},{stop_btn},{{"text":" "}},{class_btn}]'
	teams_line = f'["",["","  ",{{"text":"Join Team"}},": "],{team_btn_red},{{"text":" "}},{team_btn_blue},{{"text":" "}},{team_btn_auto}]'

	write_versioned_function("multiplayer/setup", f"""
tellraw @s {sep}
tellraw @s {gm_title}
tellraw @s {sep}
tellraw @s {gm_line}
tellraw @s {sl_line}
tellraw @s {tl_line}
tellraw @s ""
tellraw @s {teams_line}
tellraw @s {actions_line}
tellraw @s {sep}
""")
