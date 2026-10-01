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

		Each pass announces the highest remaining score and drops that player from the candidates.

		Args:
			name: Base function path, e.g. "multiplayer/announce_stats".
			in_game_score: Score marking players in this game, e.g. "mp.in_game".
			rank_objective: Objective to sort by, descending, e.g. "mp.kills".
			line: The tellraw command to run as each player, in rank order.

		Returns:
			str: The lines to place where the ranked announcement should appear.
		"""
		cand: str = f"{ns}.stat_cand"

		write_versioned_function(f"{name}_iter", f"""
execute unless entity @a[tag={cand}] run return 0

# These objectives never go negative, so 0 is a safe floor.
scoreboard players set #stat_max {ns}.data 0
scoreboard players operation #stat_max {ns}.data > @a[tag={cand}] {ns}.{rank_objective}

# One player with that score; #stat_found keeps ties from printing at once.
scoreboard players set #stat_found {ns}.data 0
execute as @a[tag={cand}] if score @s {ns}.{rank_objective} = #stat_max {ns}.data if score #stat_found {ns}.data matches 0 run function {ns}:v{version}/{name}_one

# A candidate with no score matches nothing and would recurse forever, so stragglers are dropped.
execute if score #stat_found {ns}.data matches 0 run return run tag @a remove {cand}

# Depth is bounded by the player count.
function {ns}:v{version}/{name}_iter
""")

		write_versioned_function(f"{name}_one", f"""
# Run as the highest-scoring player not yet announced.
scoreboard players set #stat_found {ns}.data 1
tag @s remove {cand}
{line}
""")

		return f"""
tag @a[scores={{{ns}.{in_game_score}=1}}] add {cand}
function {ns}:v{version}/{name}_iter
tag @a remove {cand}
""".strip()

