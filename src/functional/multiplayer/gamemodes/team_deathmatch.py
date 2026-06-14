
# Imports
from ...helpers import MGS_TAG
from .base import GameModeVariant


class TeamDeathmatch(GameModeVariant):
	""" Team Deathmatch: first team to the score limit wins. Kills are scored by the
	shared on_kill signal in game.py (kill -> +1 team -> check limit). """

	key = "tdm"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## TDM Setup
		self.sub("setup", f"""
# Auto-assign players with no team so team scores can increment
execute as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=0}}] run function {ns}:v{version}/multiplayer/auto_assign_team

tellraw @a [{MGS_TAG},{{"text":"Team Deathmatch! First team to the score limit wins!","color":"yellow"}}]
""")

		## TDM Tick: Already handled by on_kill_signal in game.py (kill → +1 team → check limit)
		self.sub("tick", "# TDM scoring handled by kill signal")

		## TDM Kill Hook
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
execute if score @s {ns}.mp.team matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players add #blue {ns}.mp.team 1

# Refresh sidebar to show updated team scores
function #bs.sidebar:refresh {{objective:"{ns}.sidebar"}}

# Check win condition
function {ns}:v{version}/multiplayer/check_team_win
""")

		## TDM Cleanup
		self.sub("cleanup", "# Nothing to clean up for TDM")


def generate_team_deathmatch() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`TeamDeathmatch`. """
	TeamDeathmatch()()
