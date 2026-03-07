
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG


def generate_free_for_all() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## FFA Setup: Remove team coloring, use general spawns only
	write_versioned_function("multiplayer/gamemodes/ffa/setup", f"""
# Reset all teams (no teams in FFA)
team leave @a
scoreboard players set @a {ns}.mp.team 0
tellraw @a [{MGS_TAG},{{"text":"Free-For-All! Everyone for themselves!","color":"yellow"}}]
""")

	## FFA Tick: Check personal score limit
	write_versioned_function("multiplayer/gamemodes/ffa/tick", f"""
# Check each player's kill count against score limit
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute as @a if score @s {ns}.mp.kills >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

	## FFA Player Wins
	write_versioned_function("multiplayer/gamemodes/ffa/player_wins", f"""
# Announce winner using player's name
tellraw @a ["",{{"text":"🏆 ","color":"gold"}},{{"selector":"@s","color":"gold","bold":true}},{{"text":" wins!","color":"gold","bold":true}}]
tellraw @a ["",{{"text":"  Score: ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.mp.kills"}},"color":"yellow"}},{{"text":" kills","color":"gray"}}]

# End game
function {ns}:v{version}/multiplayer/stop
""")

	## FFA Kill Hook: +1 personal score (no team score)
	write_versioned_function("multiplayer/gamemodes/ffa/on_kill", f"""
# Only personal kill tracking (no team scoring)
scoreboard players add @s {ns}.mp.kills 1

# Refresh FFA sidebar with updated rankings
function {ns}:v{version}/multiplayer/refresh_sidebar_ffa

# Check win
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score @s {ns}.mp.kills >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

	## FFA Cleanup: Re-allow team joining
	write_versioned_function("multiplayer/gamemodes/ffa/cleanup", "# Nothing to clean up for FFA")
