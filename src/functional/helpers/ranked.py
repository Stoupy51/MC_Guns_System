""" The end-of-match stat lines a ranked game reports. """
# Imports
from stewbeet import write_versioned_function


# Classes
class RankedStats:
	""" The end-of-match stat lines a ranked game reports. """

	# Functions
	@staticmethod
	def write_ranked_stats_functions(ns: str, version: str, name: str, in_game_score: str, rank_objective: str, line: str) -> str:
		""" Generate the function pair that announces every in-game player once, highest score first.

		Players come out of a selector in arbitrary order, so end-of-game stats used to be listed in
		whatever order the entity list happened to hold. This repeatedly takes the highest remaining
		score instead, announcing one player per pass and dropping them from the candidate set.

		Args:
			ns             (str): The project namespace.
			version        (str): The project version, used to build the function paths.
			name           (str): Base function path, e.g. "multiplayer/announce_stats".
			in_game_score  (str): Score marking players in this game, e.g. "mp.in_game".
			rank_objective (str): Objective to sort by, descending, e.g. "mp.kills".
			line           (str): The tellraw command to run as each player, in rank order.

		Returns:
			str: The lines to place where the ranked announcement should appear.
		"""
		cand: str = f"{ns}.stat_cand"

		write_versioned_function(f"{name}_iter", f"""
# Stop once every player has been announced
execute unless entity @a[tag={cand}] run return 0

# Highest score still unannounced (these objectives never go negative, so 0 is a safe floor)
scoreboard players set #stat_max {ns}.data 0
scoreboard players operation #stat_max {ns}.data > @a[tag={cand}] {ns}.{rank_objective}

# Announce exactly one player holding that score; #stat_found keeps ties from all printing at once
scoreboard players set #stat_found {ns}.data 0
execute as @a[tag={cand}] if score @s {ns}.{rank_objective} = #stat_max {ns}.data if score #stat_found {ns}.data matches 0 run function {ns}:v{version}/{name}_one

# Termination guarantee: a candidate with no score at all matches nothing, so no tag would be
# removed and this function would recurse until the server died. Drop the stragglers and stop.
execute if score #stat_found {ns}.data matches 0 run return run tag @a remove {cand}

# Recurse for the next player down. Depth is bounded by the player count.
function {ns}:v{version}/{name}_iter
""")

		write_versioned_function(f"{name}_one", f"""
# @s = the highest-scoring player not yet announced
scoreboard players set #stat_found {ns}.data 1
tag @s remove {cand}
{line}
""")

		return f"""
tag @a[scores={{{ns}.{in_game_score}=1}}] add {cand}
function {ns}:v{version}/{name}_iter
tag @a remove {cand}
""".strip()

