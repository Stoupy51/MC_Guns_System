""" What happens the tick a challenge unlocks: pay the XP, say so, publish the event.

Vanilla runs these as the player who unlocked, once, when the advancement transitions to completed. There
is no guard against paying twice because there is nothing that could: the pack never grants a threshold
tier, and a completed advancement stops being evaluated.

The payout rides the `challenge` award row, which is `scaled`, so one row covers all 56 amounts and
`Xp.suffix` reads `#xp_gain` instead of a compile-time number. That also means `#xp_gain` has to be set
before the message is written, since a score component resolves when the command runs.

Top tiers broadcast, everything else is private. A chain's last node is the one worth the server hearing
about; the middle of a grind is not.
"""
# Imports
from stewbeet import Mem, write_tag, write_versioned_function

from ...helpers import MGS_TAG
from ...helpers.text import Text
from ..xp import Xp
from .catalog import CHAINS, EVENTS, Catalog
from .model import Chain, EventChallenge

# Constants
SIGNAL_TAG: str = "progression/on_challenge_unlock"
""" Published extension point, fired as the player who unlocked. Anything wanting to react to an unlock
subscribes instead of editing these functions, exactly like `progression/on_level_up`. """
AWARD_KEY: str = "challenge"
""" The row every challenge pays through, one per XP pool. """
SAVED_GAIN: str = "#adv_gain_prev"
""" Whatever `#xp_gain` held before a reward overwrote it with the tier's payout, put back on the way out.
An event challenge's reward runs nested inside the `advancement grant` at its site, so the site's own
`#xp_gain` has to survive the trip. """


# Classes
class Rewards:
	""" The generated reward functions, one per tier and one per event challenge. """

	# Functions
	@staticmethod
	def signal_lines(branch: str, chain_key: str, tier: int, side: str, xp: int) -> str:
		""" Return the lines publishing the unlock to subscribers.

		Args:
			branch    (str): Branch key.
			chain_key (str): Chain key, or the event challenge key.
			tier      (int): 1-based tier index, 0 for an event challenge.
			side      (str): XP pool that was paid.
			xp        (int): What it paid.
		Returns:
			str: Two commands, one per line.
		"""
		ns: str = Mem.ctx.project_id
		payload: str = f'{{branch:"{branch}",chain:"{chain_key}",tier:{tier},side:"{side}",xp:{xp}}}'
		return f"""data modify storage {ns}:signals on_challenge_unlock set value {payload}
function #{ns}:{SIGNAL_TAG}"""

	@staticmethod
	def body(branch: str, chain_key: str, tier: int, title: str, xp: int, broadcast: bool) -> str:
		""" Return the whole reward function for one unlocked node.

		Args:
			branch    (str):  Branch key, naming the XP pool through `Catalog.side`.
			chain_key (str):  Chain key, or the event challenge key.
			tier      (int):  1-based tier index, 0 for an event challenge.
			title     (str):  The node's title, repeated in the message.
			xp        (int):  What it pays.
			broadcast (bool): Whether the server sees it or only the player.
		Returns:
			str: The function body.
		"""
		ns: str = Mem.ctx.project_id
		side: str = Catalog.side(branch)
		label: str = f'{{"text":"{title}","color":"yellow"}}'

		## Xp.announce splits one message in two on a scratch tag so only the earner sees the amount, and
		## hands out the award itself. The private case cannot use it: it would still tellraw everyone else.
		if broadcast:
			announce: str = Xp.announce(
				side,
				AWARD_KEY,
				f'{MGS_TAG},{Text.player(ns, "@s", side=side, color="yellow")},{{"text":" unlocked ","color":"gray"}},{label},{{"text":"!","color":"gray"}}',
			)
		else:
			announce = "\n".join((
				f'tellraw @s [{MGS_TAG},{{"text":"🏆 ","color":"white"}},{{"text":"Challenge unlocked: ","color":"gray"}},{label},{Xp.suffix(side, AWARD_KEY)}]',
				Xp.give(side, AWARD_KEY),
			))

		## A threshold tier's reward runs in vanilla's tick phase, where nothing else is using #xp_gain. An
		## event challenge's runs nested inside the `advancement grant` at its site, mid-function, where
		## something might be: zombies/round_complete sets #xp_gain, fires the round-end tag, and only then
		## reads it back for its own suffix. Restoring it costs two commands on a path that runs once per
		## unlock, and means no site has to know this function exists.
		return f"""
# {title}: {xp} XP into the {side} pool
scoreboard players operation {SAVED_GAIN} {ns}.data = #xp_gain {ns}.data
scoreboard players set #xp_gain {ns}.data {xp}
{announce}
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

{Rewards.signal_lines(branch, chain_key, tier, side, xp)}
scoreboard players operation #xp_gain {ns}.data = {SAVED_GAIN} {ns}.data
"""

	@staticmethod
	def write_chain(chain: Chain) -> None:
		""" Write one reward function per tier of a chain.

		Args:
			chain (Chain): The chain.
		"""
		top: int = len(chain.tiers) - 1
		for index, tier in enumerate(chain.tiers):
			write_versioned_function(
				f"progression/adv/{chain.branch}/{chain.key}/reward_{index + 1}",
				Rewards.body(chain.branch, chain.key, index + 1, tier.title, tier.xp, broadcast=index == top),
			)

	@staticmethod
	def write_event(event: EventChallenge) -> None:
		""" Write the reward function for one event challenge.

		Args:
			event (EventChallenge): The challenge.
		"""
		write_versioned_function(
			f"progression/adv/{event.branch}/reward_{event.key}",
			Rewards.body(event.branch, event.key, 0, event.title, event.xp, broadcast=True),
		)

	@staticmethod
	def write_all() -> None:
		""" Write the signal tag and every reward function. """
		ns: str = Mem.ctx.project_id
		write_tag(SIGNAL_TAG, Mem.ctx.data[ns].function_tags, [])
		for chain in CHAINS:
			Rewards.write_chain(chain)
		for event in EVENTS:
			Rewards.write_event(event)
