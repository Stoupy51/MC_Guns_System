""" What an award site calls.

Both modes' hook files go through here so no site names an amount. Lives in its own module rather than in
the package `__init__` because the advancements package needs it too, and importing it from the package
root would close a cycle: `__init__` pulls in `advancements`, which pulls in the reward writer, which
pays through `Xp`.
"""
# Imports
from stewbeet import Mem

from .awards import MP_AWARDS, ZB_AWARDS, XpAward
from .curve import Curve

# Constants
SIDES: dict[str, str] = {"mp": "Multiplayer", "zb": "Zombies"}
""" Objective/folder prefix mapped to the name used in that side's level-up message. """
TABLES: dict[str, dict[str, XpAward]] = {"mp": MP_AWARDS, "zb": ZB_AWARDS}
""" Which award table belongs to which side. """
EARNER_TAG: str = "xp_earner"
""" Scratch tag marking who earned the award currently being announced, so `Xp.announce` can send the
suffixed and unsuffixed copies of one message to two different audiences. Never persists past its own call. """


# Classes
class Xp:
	""" What an award site calls. Both modes' hook files go through here so no site names an amount. """

	# Functions
	@staticmethod
	def give(side: str, key: str, selector: str = "@s", guard: str = "") -> str:
		""" Return the single command granting one award.

		Args:
			side: `mp` or `zb`.
			key: Row key in that side's table.
			selector: Who earns it; `@s` needs no `as` clause.
			guard: Extra `execute` subcommands folded into the same command as `selector`.
		Returns:
			str: One command.
		"""
		return Curve.award_call(Mem.ctx.project_id, Mem.ctx.project_version, side, key, selector, guard)

	@staticmethod
	def announce(side: str, key: str, body: str, earner: str = "@s", audience: str = "@a") -> str:
		""" Award XP and broadcast the event, with the amount visible only to whoever earned it.

		A score component resolves for the executor, not per reader, so the line is sent twice, split on a temporary tag.
		Earners get the suffix, everyone else the same line without it.

		Args:
			side: `mp` or `zb`.
			key: Row key in that side's table.
			body: The message's components, WITHOUT the enclosing brackets.
			earner: Who earned it, ex: "@s" or "@a[tag=mgs.demo_atk]".
			audience: Who sees the message at all.
		Returns:
			str: Six commands, one per line.
		"""
		ns: str = Mem.ctx.project_id
		tag: str = f"{ns}.{EARNER_TAG}"
		# Splice the exclusion into whatever selector the caller already wrote
		others: str = f"{audience[:-1]},tag=!{tag}]" if audience.endswith("]") else f"{audience}[tag=!{tag}]"
		return f"""tag @a remove {tag}
tag {earner} add {tag}
tellraw {others} [{body}]
tellraw @a[tag={tag}] [{body},{Xp.suffix(side, key)}]
{Xp.give(side, key, f"@a[tag={tag}]")}
tag @a remove {tag}"""

	@staticmethod
	def announce_teams(
		side: str, body: str, win_key: str, winners: str, loss_key: str, losers: str, guard: str = "",
	) -> str:
		""" Award and announce a result where BOTH audiences earn, each seeing their own amount.

		Round wins pay both sides, the winners more, so no reader gets the line without an amount.

		Args:
			side: `mp` or `zb`.
			body: The message's components, WITHOUT the enclosing brackets.
			win_key: Row key for the winning side's award.
			winners: Selector for the winning side.
			loss_key: Row key for the losing side's award.
			losers: Selector for the losing side.
			guard: `execute` subcommands every line is gated on, ex: "if score #x mgs.data matches 1".
		Returns:
			str: Four commands, one per line.
		"""
		# The guard goes INTO Xp.give for the award lines rather than around them, so they stay one execute
		# each instead of `execute <guard> run execute as <sel> run ...`.
		prefix: str = f"execute {guard} run " if guard else ""
		return "\n".join((
			f'{prefix}tellraw {winners} [{body},{Xp.suffix(side, win_key)}]',
			f'{prefix}tellraw {losers} [{body},{Xp.suffix(side, loss_key, color="gray")}]',
			Xp.give(side, win_key, winners, guard=guard),
			Xp.give(side, loss_key, losers, guard=guard),
		))

	@staticmethod
	def suffix(side: str, key: str, color: str = "gold") -> str:
		""" Return the text component appended to the message this award rides on.

		No award ever prints a line of its own, so this is how the amount reaches the player. A scaled
		award has no compile-time number and reads `#xp_gain` instead.

		Args:
			side: `mp` or `zb`.
			key: Row key in that side's table.
		Returns:
			str: SNBT list component, ex: `[" ",{"text":"+10 XP","color":"gold"}]`
		"""
		ns: str = Mem.ctx.project_id
		award: XpAward = TABLES[side][key]
		if award.scaled:
			return (
				f'[" ",{{"text":"+","color":"{color}"}}'
				f',{{"score":{{"name":"#xp_gain","objective":"{ns}.data"}},"color":"{color}"}}'
				f',{{"text":" XP","color":"{color}"}}]'
			)
		return f'[" ",{{"text":"{award.suffix_text}","color":"{color}"}}]'

