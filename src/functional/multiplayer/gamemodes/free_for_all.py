""" Free-for-all: every player scores on their own. """
# Imports
from ...helpers import MGS_TAG
from ...helpers.text import Text
from ..xp import WINNER_TAG
from .base import GameModeVariant


# Classes
class FreeForAll(GameModeVariant):
	""" Free-For-All: no teams, first player to the personal kill limit wins. """

	key = "ffa"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## No team colours; general spawns only.
		self.sub("setup", f"""
# Only red and blue leave: players stay on {ns}.ffa, which hides nametags and enables friendly fire.
team leave @a[team={ns}.red]
team leave @a[team={ns}.blue]
scoreboard players set @a {ns}.mp.team 0
tellraw @a [{MGS_TAG},{{"text":"Free-For-All! Everyone for themselves!","color":"yellow"}}]
""")

		self.sub("tick", f"""
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute as @a if score @s {ns}.mp.kills >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

		self.sub("player_wins", f"""
# FFA has no team score for multiplayer/xp/on_game_end, so the winner is marked here.
tag @s add {ns}.{WINNER_TAG}

tellraw @a ["","🏆 ",{Text.player(ns, "@s", color="gold", bold="true")}," ",{{"text":"wins!","color":"gold","bold":true}}]
tellraw @a ["","  ",{{"text":"Score: ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.mp.kills"}},"color":"yellow"}}," ",{{"text":"kills","color":"gray"}}]

function {ns}:v{version}/multiplayer/stop
""")

		## +1 personal score, no team score.
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1

function {ns}:v{version}/multiplayer/refresh_sidebar_ffa

execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score @s {ns}.mp.kills >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

		self.sub("cleanup", "# Nothing to clean up for FFA")

# Functions
def generate_free_for_all() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`FreeForAll`. """
	FreeForAll()()

