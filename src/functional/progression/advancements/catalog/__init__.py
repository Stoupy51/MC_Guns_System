""" The whole catalog, assembled and checked.

`Catalog.validate` runs at generation time rather than at import time so a bad row fails the build with a
readable message instead of an import traceback. The checks exist because most of the ways to get this
data wrong are silent: a mistyped award key produces a chain nobody can ever complete, and a threshold
out of order strands a tier behind one that unlocks later.
"""
# Imports
from ...awards import MP_AWARDS, ZB_AWARDS, XpAward
from ..model import Branch, Chain, EventChallenge, StatKind
from .missions import MI_BRANCH, MI_CHAINS, MI_EVENTS
from .multiplayer import MP_BRANCH, MP_CHAINS, MP_EVENTS
from .zombies import ZB_BRANCH, ZB_CHAINS, ZB_EVENTS

# Constants
BRANCHES: tuple[Branch, ...] = (MP_BRANCH, MI_BRANCH, ZB_BRANCH)
""" The three sub-roots, in the order they should read on screen. """
CHAINS: tuple[Chain, ...] = MP_CHAINS + MI_CHAINS + ZB_CHAINS
""" Every threshold chain, 16 of them. """
EVENTS: tuple[EventChallenge, ...] = MP_EVENTS + MI_EVENTS + ZB_EVENTS
""" Every challenge granted by a command, 3 of them. """
ROOT_PATH: str = "challenges"
""" Unversioned on purpose: an advancement id is state in the player's world, so a version segment would
wipe every unlock on every pack update and then re-pay the entire catalog on the next tick. """


# Classes
class Catalog:
	""" Lookups over the catalog, and the build-time checks that keep it honest. """

	# Functions
	@staticmethod
	def branch(key: str) -> Branch:
		""" Return the branch with that key.

		Args:
			key (str): Branch key, ex: "mi".
		Returns:
			Branch: The matching branch.

		Examples:
			>>> Catalog.branch("mi").side
			'mp'
		"""
		return next(branch for branch in BRANCHES if branch.key == key)

	@staticmethod
	def side(branch_key: str) -> str:
		""" Return the XP pool a branch pays into.

		Args:
			branch_key (str): Branch key, ex: "mi".
		Returns:
			str: `mp` or `zb`.

		Examples:
			>>> Catalog.side("zb")
			'zb'
		"""
		return Catalog.branch(branch_key).side

	@staticmethod
	def chain(branch_key: str, key: str) -> Chain:
		""" Return one chain by branch and key.

		Args:
			branch_key (str): Branch key, ex: "zb".
			key        (str): Chain key, ex: "best_round".
		Returns:
			Chain: The matching chain.

		Examples:
			>>> Catalog.chain("zb", "best_round").stat.kind.value
			'max_score'
		"""
		return next(chain for chain in CHAINS if chain.branch == branch_key and chain.key == key)

	@staticmethod
	def event(branch_key: str, key: str) -> EventChallenge:
		""" Return one event challenge by branch and key.

		Args:
			branch_key (str): Branch key, ex: "mi".
			key        (str): Challenge key, ex: "flawless".
		Returns:
			EventChallenge: The matching challenge.

		Examples:
			>>> Catalog.event("mi", "flawless").xp
			300
		"""
		return next(event for event in EVENTS if event.branch == branch_key and event.key == key)

	@staticmethod
	def awards(side: str) -> dict[str, XpAward]:
		""" Return the award table for one XP pool.

		Args:
			side (str): `mp` or `zb`.
		Returns:
			dict[str, XpAward]: That side's table.
		"""
		return MP_AWARDS if side == "mp" else ZB_AWARDS

	@staticmethod
	def tier_path(chain: Chain, index: int) -> str:
		""" Return the unversioned advancement path of one tier.

		Args:
			chain (Chain): The chain.
			index (int):   0-based tier index.
		Returns:
			str: ex: "challenges/zb/kills_2"

		Examples:
			>>> Catalog.tier_path(CHAINS[0], 1)
			'challenges/mp/kills_2'
		"""
		return f"{ROOT_PATH}/{chain.branch}/{chain.key}_{index + 1}"

	@staticmethod
	def event_path(event: EventChallenge) -> str:
		""" Return the unversioned advancement path of one event challenge.

		Args:
			event (EventChallenge): The challenge.
		Returns:
			str: ex: "challenges/mi/flawless"
		"""
		return f"{ROOT_PATH}/{event.branch}/{event.key}"

	@staticmethod
	def validate() -> None:
		""" Fail the build on any catalog mistake that would otherwise be silent.

		Raises:
			ValueError: With the offending chain or challenge named.
		"""
		branch_keys: set[str] = {branch.key for branch in BRANCHES}
		seen_objectives: dict[str, str] = {}
		seen_paths: set[str] = set()

		for chain in CHAINS:
			label: str = f"chain {chain.branch}/{chain.key}"
			if chain.branch not in branch_keys:
				raise ValueError(f"{label}: unknown branch")
			if not chain.tiers:
				raise ValueError(f"{label}: no tiers")

			## Thresholds must strictly ascend: the tree parents each tier onto the previous one, so an
			## out-of-order row would leave a tier unlocking before the node it hangs from.
			thresholds: list[int] = [tier.threshold for tier in chain.tiers]
			if thresholds != sorted(set(thresholds)):
				raise ValueError(f"{label}: thresholds must strictly ascend, got {thresholds}")

			## Two rows sharing a title produce two nodes nobody can tell apart, and the toast for the
			## second one reads as a bug rather than a reward.
			titles: list[str] = [tier.title for tier in chain.tiers]
			if len(set(titles)) != len(titles):
				raise ValueError(f"{label}: duplicate tier titles, got {titles}")

			## The tree is read left to right, so a chain that is much shorter than its neighbours leaves a
			## ragged column. Ten is the shape the catalog is tuned for.
			if len(chain.tiers) < 5:
				raise ValueError(f"{label}: only {len(chain.tiers)} tiers, which makes the tree vertical again")

			stat = chain.stat
			if not stat.owned:
				if stat.sources or stat.source:
					raise ValueError(f"{label}: a borrowed stat is never written, so it takes no sources")
			else:
				## One owned objective per chain. Two chains sharing a counter would each pay for the
				## other's progress, which is never what the catalog means.
				if stat.objective in seen_objectives:
					raise ValueError(f"{label}: objective {stat.objective} already used by {seen_objectives[stat.objective]}")
				seen_objectives[stat.objective] = label

				needs_source: bool = stat.kind in (StatKind.COUNT_SCORE, StatKind.MAX_SCORE)
				if needs_source and not stat.source:
					raise ValueError(f"{label}: {stat.kind.value} needs a source score")
				if not needs_source and stat.source:
					raise ValueError(f"{label}: count_one reads no source score")

				## A mistyped award key is the failure this whole method exists for: the chain would
				## generate cleanly, show up in game, and never move.
				table: dict[str, XpAward] = Catalog.awards(Catalog.side(chain.branch))
				for key in stat.sources:
					if key not in table:
						raise ValueError(f"{label}: award key {key!r} is not in the {Catalog.side(chain.branch)} table")

			for index in range(len(chain.tiers)):
				seen_paths.add(Catalog.tier_path(chain, index))

		for event in EVENTS:
			label = f"challenge {event.branch}/{event.key}"
			if event.branch not in branch_keys:
				raise ValueError(f"{label}: unknown branch")
			path: str = Catalog.event_path(event)
			if path in seen_paths:
				raise ValueError(f"{label}: path {path} collides with a chain tier")
			seen_paths.add(path)
