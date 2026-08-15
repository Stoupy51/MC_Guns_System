""" What a challenge is, as data.

Five dataclasses and one enum. The generator reads nothing else: the tree, the criteria, the reward
functions, the counter lines and the objective declarations are all derived from a `Chain` or an
`EventChallenge`.

A `Branch` carries both a `key` and a `side` because the tree and the XP system disagree on how many
things there are. The screen wants three branches; progression has two pools. Missions is the one where
they differ, and it pays into `mp`.
"""
# Imports
from dataclasses import dataclass
from enum import Enum


# Classes
class StatKind(Enum):
	""" How a stat moves when its event fires. Picks the command shape, nothing else. """
	COUNT_ONE = "count_one"
	""" The event happened once. """
	COUNT_SCORE = "count_score"
	""" The event happened `Stat.source` times. """
	MAX_SCORE = "max_score"
	""" High-water mark of `Stat.source`. """


@dataclass(frozen=True)
class Branch:
	""" One sub-root of the single MGS tab.

	Examples:
		>>> Branch(key="mi", side="mp", title="Missions", description="", icon="minecraft:compass").side
		'mp'
	"""
	key: str
	""" Path and objective segment: `mp`, `mi` or `zb`. """
	side: str
	""" Which XP pool its payouts go into, `mp` or `zb`. Missions is `mp`, everything else matches `key`. """
	title: str
	""" Shown on the branch root. """
	description: str
	""" Shown on the branch root. """
	icon: str
	""" Item id. """


@dataclass(frozen=True)
class Stat:
	""" The number a chain reads.

	Either an objective this feature owns and feeds, or one the pack already maintains. A borrowed stat
	is never written here: `owned=False` means no objective is declared and no counter line is emitted.

	Examples:
		>>> Stat(objective="mgs.zb.xp_level", owned=False).owned
		False
		>>> Stat(objective="mgs.adv.zb.kills", kind=StatKind.COUNT_SCORE, sources=("kill",), source="#zb_kills_delta mgs.data").sources
		('kill',)
	"""
	objective: str
	""" Full objective name. Owned stats are `mgs.adv.<branch>.<key>`. """
	owned: bool = True
	""" False when the pack already declares and maintains it. """
	kind: StatKind = StatKind.COUNT_ONE
	""" Ignored when `owned` is False. """
	sources: tuple[str, ...] = ()
	""" Award keys whose generated function carries the counter line. Empty when a dedicated hook feeds it. """
	source: str = ""
	""" `<holder> <objective>` read by COUNT_SCORE and MAX_SCORE, ex: `#zb_kills_delta mgs.data`. """
	unit: str = ""
	""" What one point of the counter means, for whoever writes the tier descriptions, ex: "100 points". """
	note: str = ""
	""" Why this stat exists, for whoever reads the catalog next. """

	def line(self) -> str:
		""" Return the single command moving this counter.

		Returns:
			str: One command, or "" for a borrowed stat.

		Examples:
			>>> Stat(objective="mgs.adv.zb.revives").line()
			'scoreboard players add @s mgs.adv.zb.revives 1'
			>>> Stat(objective="mgs.adv.zb.best_round", kind=StatKind.MAX_SCORE, source="#adv_round mgs.data").line()
			'scoreboard players operation @s mgs.adv.zb.best_round > #adv_round mgs.data'
		"""
		if not self.owned:
			return ""
		if self.kind is StatKind.COUNT_ONE:
			return f"scoreboard players add @s {self.objective} 1"
		operator: str = "+=" if self.kind is StatKind.COUNT_SCORE else ">"
		return f"scoreboard players operation @s {self.objective} {operator} {self.source}"


@dataclass(frozen=True)
class Tier:
	""" One advancement with a threshold, unlocked by vanilla when the counter qualifies.

	A chain is ten rows long, so a row spells out only what is genuinely its own: how far along it sits,
	what it pays, and what it is called. The description, the icon and the frame come from the chain
	unless the row overrides them, which keeps a ten-row table readable instead of ten near-copies.
	"""
	threshold: int
	""" Becomes `{"min": threshold}` in the criterion. """
	xp: int
	""" Paid once, through the `challenge` award row. """
	title: str
	""" Shown in the toast and on the node. """
	icon: str = ""
	""" Item id. Empty falls back to the chain's icon. """
	description: str = ""
	""" Empty falls back to the chain's template with the threshold filled in. """
	frame: str = ""
	""" Empty derives from the row's position: the last is `challenge`, the two before it `goal`. """
	hidden: bool = False
	""" Reserved for later secret entries. """


@dataclass(frozen=True)
class Chain:
	""" One line of a branch: an ordered set of tiers over a single stat. """
	key: str
	""" Path segment, giving `mgs:challenges/<branch>/<key>_<n>`. """
	branch: str
	""" Branch key. """
	stat: Stat
	""" The number this chain reads. """
	icon: str
	""" Fallback icon for rows that do not name their own. """
	description: str
	""" Fallback description template, with `{count}` where the threshold goes, ex: "Kill {count} zombies". """
	tiers: tuple[Tier, ...]
	""" Strictly ascending by threshold. """

	def icon_of(self, index: int) -> str:
		""" Return the icon one row should display.

		Args:
			index (int): 0-based tier index.
		Returns:
			str: The row's own icon, or the chain's.
		"""
		return self.tiers[index].icon or self.icon

	def description_of(self, index: int) -> str:
		""" Return the description one row should display.

		The threshold is formatted with thousands separators, because "Kill 50000 zombies" is a worse
		sentence than "Kill 50,000 zombies" and every chain would otherwise write its own.

		Args:
			index (int): 0-based tier index.
		Returns:
			str: The row's own description, or the chain's template filled in.

		Examples:
			>>> chain = Chain(key="k", branch="zb", stat=Stat(objective="o"), icon="i", description="Kill {count} zombies", tiers=(Tier(threshold=50000, xp=1, title="t"),))
			>>> chain.description_of(0)
			'Kill 50,000 zombies'
		"""
		tier: Tier = self.tiers[index]
		return tier.description or self.description.format(count=f"{tier.threshold:,}")

	def frame_of(self, index: int) -> str:
		""" Return the frame one row should display.

		Vanilla's own visual grammar: most of a chain is plain tasks, it tightens into two goals, and the
		last node is a challenge. Derived rather than written out, so a chain cannot end on a task by
		accident.

		Args:
			index (int): 0-based tier index.
		Returns:
			str: `task`, `goal` or `challenge`.

		Examples:
			>>> chain = Chain(key="k", branch="zb", stat=Stat(objective="o"), icon="i", description="", tiers=tuple(Tier(threshold=n, xp=1, title="t") for n in range(10)))
			>>> [chain.frame_of(i) for i in (0, 6, 7, 8, 9)]
			['task', 'task', 'goal', 'goal', 'challenge']
		"""
		explicit: str = self.tiers[index].frame
		if explicit:
			return explicit
		last: int = len(self.tiers) - 1
		if index == last:
			return "challenge"
		return "goal" if index >= last - 2 else "task"


@dataclass(frozen=True)
class EventChallenge:
	""" A challenge with no threshold, granted by the code that detects the moment.

	Its criterion is `minecraft:impossible`, so the single `advancement grant` at `site` is the only way in.
	"""
	key: str
	""" Path segment, giving `mgs:challenges/<branch>/<key>`. """
	branch: str
	""" Branch key. """
	xp: int
	""" Paid once. """
	title: str
	""" Shown in the toast and on the node. """
	description: str
	""" What the player has to do. """
	icon: str
	""" Item id. """
	site: str
	""" Where the grant is inserted, for whoever reads the catalog next. """
	frame: str = "challenge"
	""" Event challenges are all `challenge` in the first pass. """
	hidden: bool = False
	""" Reserved for later secret entries. """
