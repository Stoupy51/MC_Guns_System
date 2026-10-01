""" Challenges: one advancement tab, three branches, 56 nodes, each paying XP.

A tier is a `minecraft:impossible` advancement, granted by its chain's check function whenever the counter moves (see [hooks.py]).
A `minecraft:tick` criterion per tier would cost one score check per unearned tier, per player, per tick.
A catch-up runs every check once per player after each load, so a retuned threshold unlocks for everyone who already qualifies.

The counters ride the award functions the XP system already generates, so no award site is touched.
Only three feeds need their own code (see [hooks.py]), and three challenges are granted at their site because a moment is not a total.

Advancement paths carry no version.
An advancement id is state in the player's world, so a version segment would wipe every unlock on every pack update and then re-pay the whole catalog.
"""
# Imports
from stewbeet import Mem, write_load_file

from .catalog import CHAINS, EVENTS, Catalog
from .hooks import Hooks
from .model import Chain
from .rewards import Rewards
from .tree import Tree

__all__ = ["Advancements", "Catalog", "generate_advancements"]


# Classes
class Advancements:
	""" What the rest of the pack calls.
	Two entry points: the lines an award function carries, and the command an event site runs. """

	# Functions
	@staticmethod
	def stat_lines(side: str) -> dict[str, str]:
		""" Return the extra lines each award function of one XP pool has to carry.

		`Curve.write_award_functions` takes this and splices it in. It never learns what a challenge is,
		which is what keeps the dependency one-way and the progression package free of an import cycle.

		Args:
			side: `mp` or `zb`.
		Returns:
			dict[str, str]: Award key -> the counter lines for it, for the awards that feed a chain.
		"""
		lines: dict[str, list[str]] = {}
		for chain in CHAINS:
			## A borrowed stat is already maintained, and a chain fed by a dedicated hook has no award to ride; both have empty `sources`.
			if Catalog.side(chain.branch) != side:
				continue
			for key in chain.stat.sources:
				lines.setdefault(key, []).extend((chain.stat.line(), Hooks.check_call(chain)))
		return {key: "\n".join(bumps) for key, bumps in lines.items()}

	@staticmethod
	def grant(branch: str, key: str, selector: str = "@s", guard: str = "") -> str:
		""" Return the single command granting one event challenge.

		Args:
			branch: Branch key, ex: "mi".
			key: Challenge key, ex: "flawless".
			selector: Who earns it; `@s` needs no `as` clause.
			guard: Extra `execute` subcommands folded into the same command.
		Returns:
			str: One command.
		"""
		return Hooks.grant(Catalog.event_path(Catalog.event(branch, key)), selector, guard)

	@staticmethod
	def mission_victory_lines() -> str:
		""" Return the block `missions/victory` splices in after it computes `mgs.mi.kills`.

		Returns:
			str: Three commands, one per line.
		"""
		return Hooks.mission_victory_lines()

	@staticmethod
	def match_end_lines(winner_tag: str) -> str:
		""" Return the line `multiplayer/xp/on_game_end` splices in once it has tagged the winners.

		Args:
			winner_tag: The scratch tag that site puts on whoever took the match.
		Returns:
			str: One command.
		"""
		return Hooks.match_end_lines(winner_tag)


# Functions
def generate_advancements() -> None:
	""" Write the counters, the tree, the reward functions and the round-end listener. """
	Catalog.validate()

	ns: str = Mem.ctx.project_id
	owned: list[Chain] = [chain for chain in CHAINS if chain.stat.owned]

	## Dummy, so they survive reloads, restarts and offline players; the `adv` segment keeps them out of every per-match wipe (which clears by name).
	## A missing score reads as 0, the right start.
	declarations: str = "\n".join(
		f"scoreboard objectives add {chain.stat.objective} dummy"
		for chain in owned
	)
	write_load_file(f"""
# {len(owned)} challenge counters; the level chains read {ns}.mp.xp_level and {ns}.zb.xp_level.
{declarations}
""")

	Tree.write_all()
	Rewards.write_all()
	Hooks.write_round_end()
	Hooks.write_unlocks()

	## Every event challenge must be granted somewhere; a missing grant fails the build.
	for event in EVENTS:
		if not event.site:
			raise ValueError(f"challenge {event.branch}/{event.key}: no site named, so nothing can ever grant it")

