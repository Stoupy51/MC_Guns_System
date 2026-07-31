""" Cosmetic leveling, shared by Multiplayer and Zombies.

Purely visual: nothing is gated behind a level, there is no cap and no prestige. Each side keeps its own
independent level, shown on the vanilla XP bar and in front of the player's name in every message the pack
prints.

This package owns the curve and the display. The award *sites* live with the mode that fires them —
`multiplayer/xp.py` and `zombies/xp.py` — and the award *values* all live in `awards.py`.
"""
# Imports
from stewbeet import Mem, write_load_file, write_tag, write_tick_file, write_versioned_function

from .awards import MP_AWARDS, ZB_AWARDS, XpAward
from .curve import PARK_LEVEL, Curve

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
			side     (str): `mp` or `zb`.
			key      (str): Row key in that side's table.
			selector (str): Who earns it; `@s` needs no `as` clause.
			guard    (str): Extra `execute` subcommands folded into the same command as `selector`.
		Returns:
			str: One command.
		"""
		return Curve.award_call(Mem.ctx.project_id, Mem.ctx.project_version, side, key, selector, guard)

	@staticmethod
	def announce(side: str, key: str, body: str, earner: str = "@s", audience: str = "@a") -> str:
		""" Award XP and broadcast the event, with the amount visible only to whoever earned it.

		A tellraw is one atomic message and a score component resolves in the executor's context rather
		than per recipient, so one line cannot say "+20 XP" to only some of the people reading it. The
		message is therefore emitted twice, split on a temporary tag: the earners get the suffix, everyone
		else gets the identical line without it.

		Args:
			side     (str): `mp` or `zb`.
			key      (str): Row key in that side's table.
			body     (str): The message's components, WITHOUT the enclosing brackets.
			earner   (str): Who earned it, ex: "@s" or "@a[tag=mgs.demo_atk]".
			audience (str): Who sees the message at all.
		Returns:
			str: Four commands, one per line.
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

		Used by the round-win functions: a round always pays the winning side more than the losing one, and
		neither ever gets nothing, so there is no plain unsuffixed copy of the line at all.

		Args:
			side     (str): `mp` or `zb`.
			body     (str): The message's components, WITHOUT the enclosing brackets.
			win_key  (str): Row key for the winning side's award.
			winners  (str): Selector for the winning side.
			loss_key (str): Row key for the losing side's award.
			losers   (str): Selector for the losing side.
			guard    (str): `execute` subcommands every line is gated on, ex: "if score #x mgs.data matches 1".
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
			side  (str): `mp` or `zb`.
			key   (str): Row key in that side's table.
			color (str): Colour of the suffix.
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


# Functions
def generate_progression() -> None:
	""" Write the objectives, the curve functions for both sides, the bar macro and the re-assert tick. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## All dummy, so they live in level.dat and survive reloads, restarts and the player being offline.
	## multiplayer/start and zombies/stop reset their objectives by explicit name, so none of these are
	## caught by a mode's per-match wipe. xp_session is the exception and is cleared in multiplayer/start.
	write_load_file(f"""
# Progression scoreboards (xp_total is authoritative; xp_level and xp_prog are caches derived from it)
scoreboard objectives add {ns}.mp.xp_total dummy
scoreboard objectives add {ns}.mp.xp_level dummy
scoreboard objectives add {ns}.mp.xp_prog dummy
scoreboard objectives add {ns}.mp.xp_session dummy
scoreboard objectives add {ns}.zb.xp_total dummy
scoreboard objectives add {ns}.zb.xp_level dummy
scoreboard objectives add {ns}.zb.xp_prog dummy
scoreboard objectives add {ns}.zb.xp_pts_prev dummy
scoreboard objectives add {ns}.zb.xp_spent_acc dummy
""")

	## Published so anything that wants to react to a level up subscribes instead of editing the feedback
	## function. Fired as the player who levelled, with the side in `storage {ns}:signals on_level_up`.
	write_tag("progression/on_level_up", Mem.ctx.data[ns].function_tags, [])

	for side, label in SIDES.items():
		Curve.write(ns, version, side, label)
		Curve.write_award_functions(ns, version, side, TABLES[side])

	## The bar trick, shared by both sides. Order is everything: `xp set <n> points` scales n by the cost of
	## the CURRENT level, so the level has to be parked at 130 (cost exactly 1012) before the fill is written,
	## and only then set to what the player should see.
	write_versioned_function("progression/apply_bar", f"""
xp set @s {PARK_LEVEL} levels
$xp set @s $(points) points
$xp set @s $(level) levels
""")

	## Re-assert the bar once a second. There is no event for "the client's XP changed", and a stray orb or a
	## furnace would otherwise leave someone showing a level they never earned, so this is the self-heal.
	## Multiplayer already kills loose orbs during a match; this covers the lobby and everything else.
	write_versioned_function("progression/tick_player", f"""
execute unless score @s {ns}.mp.xp_level matches 1.. run function {ns}:v{version}/progression/mp/init
execute unless score @s {ns}.zb.xp_level matches 1.. run function {ns}:v{version}/progression/zb/init

# Zombies owns the bar while its game is running; multiplayer and the lobby show the multiplayer level.
execute if score @s {ns}.zb.in_game matches 1 run return run function {ns}:v{version}/progression/zb/refresh_bar
function {ns}:v{version}/progression/mp/refresh_bar
""")

	write_tick_file(f"""
# Progression: re-assert every player's XP bar once a second (see progression/tick_player)
scoreboard players operation #xp_sec_tick {ns}.data = #total_tick {ns}.data
scoreboard players operation #xp_sec_tick {ns}.data %= #20 {ns}.data
execute if score #xp_sec_tick {ns}.data matches 0 as @a run function {ns}:v{version}/progression/tick_player
""")

	## Admin entry point: rebuild every player's level from the XP they banked. This is what makes retuning
	## awards.py safe — the totals are authoritative, so nobody loses progress when the curve moves under them.
	write_versioned_function("progression/recompute_all", f"""
execute as @a run function {ns}:v{version}/progression/mp/recompute
execute as @a run function {ns}:v{version}/progression/zb/recompute
""")
