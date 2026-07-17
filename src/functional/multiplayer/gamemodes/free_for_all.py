
# Imports
from ...helpers import MGS_TAG
from .base import GameModeVariant


class FreeForAll(GameModeVariant):
	""" Free-For-All: no teams, first player to the personal kill limit wins. """

	key = "ffa"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## FFA Setup: Remove team coloring, use general spawns only
		self.sub("setup", f"""
# Clear leftover red/blue assignments only — players must STAY on the {ns}.ffa team
# (it carries nametagVisibility never + friendlyFire true; a bare 'team leave @a' made nametags visible)
team leave @a[team={ns}.red]
team leave @a[team={ns}.blue]
scoreboard players set @a {ns}.mp.team 0
tellraw @a [{MGS_TAG},{{"text":"Free-For-All! Everyone for themselves!","color":"yellow"}}]
""")

		## FFA Tick: Check personal score limit
		self.sub("tick", f"""
# Check each player's kill count against score limit
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute as @a if score @s {ns}.mp.kills >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

		## FFA Player Wins
		self.sub("player_wins", f"""
# Announce winner using player's name
tellraw @a ["","🏆 ",{{"selector":"@s","color":"gold","bold":true}}," ",{{"text":"wins!","color":"gold","bold":true}}]
tellraw @a ["","  ",{{"text":"Score: ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.mp.kills"}},"color":"yellow"}}," ",{{"text":"kills","color":"gray"}}]

# End game
function {ns}:v{version}/multiplayer/stop
""")

		## FFA Kill Hook: +1 personal score (no team score)
		self.sub("on_kill", f"""
# Only personal kill tracking (no team scoring)
scoreboard players add @s {ns}.mp.kills 1

# Refresh FFA sidebar with updated rankings
function {ns}:v{version}/multiplayer/refresh_sidebar_ffa

# Check win
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score @s {ns}.mp.kills >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

		## FFA Cleanup: Re-allow team joining
		self.sub("cleanup", "# Nothing to clean up for FFA")


def generate_free_for_all() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`FreeForAll`. """
	FreeForAll()()
