""" What happens the tick a challenge unlocks: pay the XP, say so, publish the event.

Vanilla runs these as the player who unlocked, once, when the advancement transitions to completed.
Granting an advancement the player already has does nothing, so nothing can pay twice.

The payout rides the `challenge` award row, which is `scaled`, so one row covers all 56 amounts and `Xp.suffix` reads `#xp_gain` instead of a compile-time number.
`#xp_gain` is therefore set before the message is written, since a score component resolves when the command runs.

Every unlock is announced to the whole server, with the XP amount shown only to the earner.
"""
# Imports
import json

from stewbeet import Mem, write_tag, write_versioned_function

from ...helpers import MGS_TAG
from ...helpers.text import Text
from ..xp import EARNER_TAG, Xp
from .catalog import CHAINS, EVENTS, Catalog
from .model import Chain, EventChallenge

# Constants
SIGNAL_TAG: str = "progression/on_challenge_unlock"
""" Published extension point, fired as the player who unlocked. Anything wanting to react to an unlock
subscribes instead of editing these functions, exactly like `progression/on_level_up`. """
AWARD_KEY: str = "challenge"
""" The row every challenge pays through, one per XP pool. """
SAVED_GAIN: str = "#adv_gain_prev"
""" Whatever `#xp_gain` held before a reward overwrote it with the payout, put back on the way out.
A reward runs nested inside the `advancement grant` that unlocked it, so the caller's `#xp_gain` has to survive the trip.
"""


# Classes
class Rewards:
	""" One reward macro per XP pool, called by a one-line function per tier and per event challenge. """

	# Functions
	@staticmethod
	def macro_body(side: str) -> str:
		""" The reward commands for one XP pool, filled by each unlock's title, description, XP and signal ids. """
		ns: str = Mem.ctx.project_id
		hover: str = '{"action":"show_text","value":[$(title),"\\n",$(description)]}'

		def message(*parts: str) -> str:
			return f'{{"text":"","hover_event":{hover},"extra":[{MGS_TAG},{{"text":"🏆 ","color":"white"}},{",".join(parts)}]}}'

		## Everyone hears about every unlock; only the earner sees the amount.
		earner_tag: str = f"{ns}.{EARNER_TAG}"
		payload: str = '{branch:"$(branch)",chain:"$(chain)",tier:$(tier),side:"' + side + '",xp:$(xp)}'

		## A reward runs inside the `advancement grant` that unlocked it, where #xp_gain may be in use (zombies/round_complete reads it back after the round-end tag).
		return f"""
scoreboard players operation {SAVED_GAIN} {ns}.data = #xp_gain {ns}.data
$scoreboard players set #xp_gain {ns}.data $(xp)
tag @s add {earner_tag}
$tellraw @a[tag=!{earner_tag}] {message(Text.player(ns, "@s", side=side, color="yellow"), '{"text":" unlocked challenge: ","color":"gray"}', "$(title)")}
tag @s remove {earner_tag}
$tellraw @s {message('{"text":"Challenge unlocked: ","color":"gray"}', "$(title)", Xp.suffix(side, AWARD_KEY))}
{Xp.give(side, AWARD_KEY)}
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1

$data modify storage {ns}:signals on_challenge_unlock set value {payload}
function #{ns}:{SIGNAL_TAG}
scoreboard players operation #xp_gain {ns}.data = {SAVED_GAIN} {ns}.data
"""

	@staticmethod
	def call(path: str, branch: str, chain_key: str, tier: int, title: str, description: str, xp: int) -> None:
		""" Write the reward function `path`, one call to its XP pool's macro.

		Args:
			tier: 1-based tier index, 0 for an event challenge.
		"""
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		def snbt(component: str) -> str:
			return "'" + component.replace("\\", "\\\\").replace("'", "\\'") + "'"

		title_json: str = f'{{"text":{json.dumps(title, ensure_ascii=False)},"color":"yellow"}}'
		description_json: str = f'{{"text":{json.dumps(description, ensure_ascii=False)},"color":"gray"}}'
		args: str = f'{{title:{snbt(title_json)},description:{snbt(description_json)},xp:{xp},branch:"{branch}",chain:"{chain_key}",tier:{tier}}}'
		write_versioned_function(path, f"function {ns}:v{version}/progression/adv/reward_{Catalog.side(branch)} {args}")

	@staticmethod
	def write_chain(chain: Chain) -> None:
		""" Write one reward function per tier of a chain. """
		for index, tier in enumerate(chain.tiers):
			path: str = f"progression/adv/{chain.branch}/{chain.key}/reward_{index + 1}"
			Rewards.call(path, chain.branch, chain.key, index + 1, tier.title, chain.description_of(index), tier.xp)

	@staticmethod
	def write_event(event: EventChallenge) -> None:
		""" Write the reward function for one event challenge. """
		path: str = f"progression/adv/{event.branch}/reward_{event.key}"
		Rewards.call(path, event.branch, event.key, 0, event.title, event.description, event.xp)

	@staticmethod
	def write_all() -> None:
		""" Write the signal tag and every reward function. """
		ns: str = Mem.ctx.project_id
		write_tag(SIGNAL_TAG, Mem.ctx.data[ns].function_tags, [])
		for side in sorted({Catalog.side(branch) for branch in (*(c.branch for c in CHAINS), *(e.branch for e in EVENTS))}):
			write_versioned_function(f"progression/adv/reward_{side}", Rewards.macro_body(side))
		for chain in CHAINS:
			Rewards.write_chain(chain)
		for event in EVENTS:
			Rewards.write_event(event)

