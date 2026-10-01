""" The whole catalog, assembled and checked.

`Catalog.validate` runs at generation time rather than at import time so a bad row fails the build with a readable message instead of an import traceback.
The checks exist because most of the ways to get this data wrong are silent: a mistyped award key produces a chain nobody can ever complete, and a threshold out of order strands a tier behind one that unlocks later.
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
wipe every unlock on every pack update and then re-pay the entire catalog. """


# Classes
class Catalog:
	""" Lookups over the catalog, and the build-time checks that keep it honest. """

	# Functions
	@staticmethod
	def branch(key: str) -> Branch:
		""" Return the branch with that key.

		Args:
			key: Branch key, ex: "mi".
		Returns:
			Branch: The matching branch.

		>>> Catalog.branch("mi").side
		'mp'
		"""
		return next(branch for branch in BRANCHES if branch.key == key)

	@staticmethod
	def side(branch_key: str) -> str:
		""" Return the XP pool a branch pays into.

		Args:
			branch_key: Branch key, ex: "mi".
		Returns:
			str: `mp` or `zb`.

		>>> Catalog.side("zb")
		'zb'
		"""
		return Catalog.branch(branch_key).side

	@staticmethod
	def chain(branch_key: str, key: str) -> Chain:
		""" Return one chain by branch and key.

		Args:
			branch_key: Branch key, ex: "zb".
			key: Chain key, ex: "best_round".
		Returns:
			Chain: The matching chain.

		>>> Catalog.chain("zb", "best_round").stat.kind.value
		'max_score'
		"""
		return next(chain for chain in CHAINS if chain.branch == branch_key and chain.key == key)

	@staticmethod
	def event(branch_key: str, key: str) -> EventChallenge:
		""" Return one event challenge by branch and key.

		Args:
			branch_key: Branch key, ex: "mi".
			key: Challenge key, ex: "flawless".
		Returns:
			EventChallenge: The matching challenge.

		>>> Catalog.event("mi", "flawless").xp
		300
		"""
		return next(event for event in EVENTS if event.branch == branch_key and event.key == key)

	@staticmethod
	def awards(side: str) -> dict[str, XpAward]:
		""" Return the award table for one XP pool.

		Args:
			side: `mp` or `zb`.
		Returns:
			dict[str, XpAward]: That side's table.
		"""
		return MP_AWARDS if side == "mp" else ZB_AWARDS

	@staticmethod
	def tier_path(chain: Chain, index: int) -> str:
		""" Return the unversioned advancement path of one tier.

		Args:
			index: 0-based tier index.
		Returns:
			str: ex: "challenges/zb/kills_2"

		>>> Catalog.tier_path(CHAINS[0], 1)
		'challenges/mp/kills_2'
		"""
		return f"{ROOT_PATH}/{chain.branch}/{chain.key}_{index + 1}"

	@staticmethod
	def event_path(event: EventChallenge) -> str:
		""" Return the unversioned advancement path of one event challenge.

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
		seen_objectives: dict[str, str] = {}
		for chain in CHAINS:
			label: str = f"chain {chain.branch}/{chain.key}"
			Catalog.validate_tiers(chain, label)
			Catalog.validate_stat(chain, label, seen_objectives)

		seen_paths: set[str] = {Catalog.tier_path(chain, index) for chain in CHAINS for index in range(len(chain.tiers))}
		for event in EVENTS:
			label = f"challenge {event.branch}/{event.key}"
			if event.branch not in {branch.key for branch in BRANCHES}:
				raise ValueError(f"{label}: unknown branch")
			path: str = Catalog.event_path(event)
			if path in seen_paths:
				raise ValueError(f"{label}: path {path} collides with a chain tier")
			seen_paths.add(path)

	@staticmethod
	def validate_tiers(chain: Chain, label: str) -> None:
		""" Check a chain's branch and the shape of its tier list.

		Raises:
			ValueError: With `label` naming the chain.
		"""
		if chain.branch not in {branch.key for branch in BRANCHES}:
			raise ValueError(f"{label}: unknown branch")
		if not chain.tiers:
			raise ValueError(f"{label}: no tiers")

		## The tree parents each tier on the previous one, so an out-of-order threshold would unlock a tier before its parent node.
		thresholds: list[int] = [tier.threshold for tier in chain.tiers]
		if thresholds != sorted(set(thresholds)):
			raise ValueError(f"{label}: thresholds must strictly ascend, got {thresholds}")

		## Two nodes with the same title cannot be told apart, and the second toast reads as a bug.
		titles: list[str] = [tier.title for tier in chain.tiers]
		if len(set(titles)) != len(titles):
			raise ValueError(f"{label}: duplicate tier titles, got {titles}")

		## The tree reads left to right, so a much shorter chain leaves a ragged column; ten is the tuned shape.
		if len(chain.tiers) < 5:
			raise ValueError(f"{label}: only {len(chain.tiers)} tiers, which makes the tree vertical again")

	@staticmethod
	def validate_stat(chain: Chain, label: str, seen_objectives: dict[str, str]) -> None:
		""" Check that a chain's stat is fed the way its kind reads it.

		Args:
			seen_objectives: Owned objectives of the chains checked so far, mapped to their label; this one is added.
		Raises:
			ValueError: With `label` naming the chain.
		"""
		stat = chain.stat
		if not stat.owned:
			if stat.sources or stat.source:
				raise ValueError(f"{label}: a borrowed stat is never written, so it takes no sources")
			return

		## Two chains sharing a counter would each pay for the other's progress.
		if stat.objective in seen_objectives:
			raise ValueError(f"{label}: objective {stat.objective} already used by {seen_objectives[stat.objective]}")
		seen_objectives[stat.objective] = label

		needs_source: bool = stat.kind in (StatKind.COUNT_SCORE, StatKind.MAX_SCORE)
		if needs_source and not stat.source:
			raise ValueError(f"{label}: {stat.kind.value} needs a source score")
		if not needs_source and stat.source:
			raise ValueError(f"{label}: count_one reads no source score")

		## A mistyped award key would build cleanly, show in game and never move.
		side: str = Catalog.side(chain.branch)
		unknown: list[str] = [key for key in stat.sources if key not in Catalog.awards(side)]
		if unknown:
			raise ValueError(f"{label}: award key {unknown[0]!r} is not in the {side} table")

