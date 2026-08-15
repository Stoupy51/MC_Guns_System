""" The feeds that cannot ride an award function.

Eleven of the sixteen chains hang off `progression/<side>/award_<key>`, which already runs as the earning
player. Two more borrow `xp_level` and need no feed at all. That leaves three, for three reasons:

- **Deepest round** is a high-water mark of a number that lives in storage, not on a player.
- **Missions** grants no XP at all, so it has no award function to ride. Its two counters come off the
  victory function, which has just finished computing `mgs.mi.kills` per player.

The three event challenges are here too. They are moments rather than totals, so they are granted rather
than watched.

Only the round-end listener is written here. The other two return their lines for the site to splice in,
because `generate_progression` runs before `main_missions` and `main_multiplayer` in `link.py`: anything
this package appended to their functions would land above the code computing the scores it reads.

Everything here runs once per round or once per mission. None of it is per tick.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from .catalog import Catalog
from .catalog.zombies import SOLO_ROUND

# Constants
ROSTER_SCORE: str = "#adv_roster"
""" How many players are still in the zombies game, counted once per round for the solo challenge. """


# Classes
class Hooks:
	""" The three sites that feed counters without going through an award function. """

	# Functions
	@staticmethod
	def grant(path: str, selector: str = "@s", guard: str = "") -> str:
		""" Return the single command granting one event challenge.

		Mirrors `Xp.give`'s shape on purpose, so the sites that call it read like every other award site.
		Granting an advancement a player already owns is a no-op, so no site needs a guard of its own.

		Args:
			path     (str): Unversioned advancement path, ex: "challenges/mi/flawless".
			selector (str): Who earns it; `@s` needs no `as` clause.
			guard    (str): Extra `execute` subcommands folded into the same command.
		Returns:
			str: One command, ex: `execute as @a[tag=x] run advancement grant @s only mgs:challenges/mi/flawless`
		"""
		call: str = f"advancement grant @s only {Mem.ctx.project_id}:{path}"
		clauses: str = " ".join(part for part in (guard, "" if selector == "@s" else f"as {selector}") if part)
		return f"execute {clauses} run {call}" if clauses else call

	@staticmethod
	def write_round_end() -> None:
		""" Write the round-end listener: the deepest-round mark and the solo challenge.

		Subscribes to the tag rather than appending to `zombies/round_complete`, so it is immune to the
		ordering that forces the other two hooks to be spliced by their sites. Runs once per cleared round
		for everyone still on the roster, downed or not, matching what the round bonus already pays.
		"""
		ns: str = Mem.ctx.project_id
		roster: str = f"@a[scores={{{ns}.zb.in_game=1}}]"
		best_round = Catalog.chain("zb", "best_round")
		solo = Catalog.event("zb", "solo_run")

		## The stat names the score it reads as a `<holder> <objective>` pair, which is exactly what both
		## `store result score` and `if score` want, so the fake player is written down in one place only.
		round_score: str = best_round.stat.source

		## `store result ... if entity` counts the matches, which is how "exactly one player" is asked for.
		## One roster scan per cleared round, nowhere near a hot path.
		write_versioned_function("zombies/adv/on_round_end", f"""
execute store result score {round_score} run data get storage {ns}:zombies game.round
execute as {roster} run {best_round.stat.line()}

# Solo run: exactly one player on the roster, deep enough to be worth saying so
execute store result score {ROSTER_SCORE} {ns}.data if entity {roster}
{Hooks.grant(Catalog.event_path(solo), roster, guard=f"if score {ROSTER_SCORE} {ns}.data matches 1 if score {round_score} matches {SOLO_ROUND}..")}
""", tags=[f"{ns}:zombies/on_round_end"])

	@staticmethod
	def mission_victory_lines() -> str:
		""" Return the block `missions/victory` splices in after it computes `mgs.mi.kills`.

		Both counters and the no-deaths challenge. A victory is the only mission ending that counts, and
		by this point the per-player kills are final and not yet reset.

		Returns:
			str: Three commands, one per line.
		"""
		ns: str = Mem.ctx.project_id
		roster: str = f"@a[scores={{{ns}.mi.in_game=1}}]"
		completed = Catalog.chain("mi", "completed")
		kills = Catalog.chain("mi", "kills")
		flawless = Catalog.event("mi", "flawless")
		return "\n".join((
			f"execute as {roster} run {completed.stat.line()}",
			f"execute as {roster} run {kills.stat.line()}",
			Hooks.grant(Catalog.event_path(flawless), f"@a[scores={{{ns}.mi.in_game=1,{ns}.mi.deaths=0}}]"),
		))

	@staticmethod
	def match_end_lines(winner_tag: str) -> str:
		""" Return the line `multiplayer/xp/on_game_end` splices in once it has tagged the winners.

		Args:
			winner_tag (str): The scratch tag that site puts on whoever took the match.
		Returns:
			str: One command.
		"""
		ns: str = Mem.ctx.project_id
		flawless = Catalog.event("mp", "flawless")
		return Hooks.grant(
			Catalog.event_path(flawless),
			f"@a[scores={{{ns}.mp.in_game=1,{ns}.mp.deaths=0}},tag={ns}.{winner_tag}]",
		)
