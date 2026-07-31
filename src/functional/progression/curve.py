""" The level curve, and every function that reads or writes it.

Linear cost: level 1 costs 50 XP and each level costs 10 more than the last.

	xp_required(L)    = LEVEL_BASE + LEVEL_STEP * L
	total_to_reach(L) = (L - 1) * (LEVEL_STEP // 2 * L + LEVEL_BASE)

`xp_total` is the source of truth; `xp_level` and `xp_prog` are caches derived from it. Awards update all
three incrementally because some fire once per second, but `recompute` can rebuild the caches from the total
alone — which is what makes retuning awards.py safe on a live server.

Inverting `total_to_reach` needs a square root. Rather than pull in `#bs.math:sqrt` and fight rounding at the
level boundary, `bisect` binary-searches the level: 14 frames covers every level the XP cap allows, exactly.
"""
# ruff: noqa: E501
# Imports
from stewbeet import write_versioned_function

from ..helpers import MGS_TAG
from .awards import XpAward

# Constants
LEVEL_BASE: int = 40
""" Constant term of the per-level cost. With LEVEL_STEP=10 this puts level 1 at 50 XP. """
LEVEL_STEP: int = 10
""" How much more each level costs than the one before it. """
XP_TOTAL_CAP: int = 1_000_000_000
""" Hard ceiling on `xp_total`, ~level 14,141.
Nothing about the pacing gets a player near it (level 1000 is already ~14,000 matches), but it keeps every
intermediate multiplication in the bar and bisect math inside int32. """
BISECT_HI: int = 16384
""" Exclusive upper bound for the level search, a power of two so the halving is even.
total_to_reach(16384) is 1.34e9: above XP_TOTAL_CAP, so the bracket always holds, and still inside int32. """
BAR_SCALE: int = 1011
""" Full-scale value for the XP bar fill.
The trick is to park the level at 130, where vanilla's cost is exactly 9*130-158 = 1012 points, set the
fill in those units, then set the real level back. 1012 would roll over into level 131, so the top of the
scale is 1011. """
PARK_LEVEL: int = 130
""" Level whose vanilla XP cost (1012) the bar fill is expressed in. Never displayed — it exists for one
command, between the two `xp set ... levels` calls in `apply_bar`. """


# Classes
class Curve:
	""" Reads and writes of the level curve, generated once per side (`mp` / `zb`). """

	# Functions
	@staticmethod
	def xp_required_lines(ns: str, side: str, dest: str = "#xp_req") -> str:
		""" Return the lines putting `xp_required(@s's level)` into `dest`.

		Args:
			ns   (str): Project namespace.
			side (str): `mp` or `zb`, naming the objective trio.
			dest (str): Fake player to write the result to.
		Returns:
			str: Three commands, one per line.
		"""
		return f"""scoreboard players operation {dest} {ns}.data = @s {ns}.{side}.xp_level
scoreboard players operation {dest} {ns}.data *= #{LEVEL_STEP} {ns}.data
scoreboard players add {dest} {ns}.data {LEVEL_BASE}"""

	@staticmethod
	def total_to_reach_lines(ns: str, src: str, dest: str) -> str:
		""" Return the lines putting `total_to_reach(src)` into `dest`.

		`(L - 1) * (5L + 40)`, ordered so the multiply happens last: at the top of the search range that
		product is 1.34e9, and doing it in any other order overflows on the way there.

		Args:
			ns   (str): Project namespace.
			src  (str): Fake player holding the level to evaluate.
			dest (str): Fake player to write the result to.
		Returns:
			str: Five commands, one per line.
		"""
		return f"""scoreboard players operation {dest} {ns}.data = {src} {ns}.data
scoreboard players operation {dest} {ns}.data *= #{LEVEL_STEP // 2} {ns}.data
scoreboard players add {dest} {ns}.data {LEVEL_BASE}
scoreboard players operation #xp_lvl_m1 {ns}.data = {src} {ns}.data
scoreboard players remove #xp_lvl_m1 {ns}.data 1
scoreboard players operation {dest} {ns}.data *= #xp_lvl_m1 {ns}.data"""

	@staticmethod
	def write_award_functions(ns: str, version: str, side: str, awards: dict[str, XpAward]) -> None:
		""" Write one `award_<key>` function per row, so every call site is a single command.

		Award sites are scattered across gamemode functions where `@s` is often a marker rather than a
		player, so they need an `execute as <players> run` wrapper. Giving each award its own function keeps
		that wrapper to one line instead of four, which is what makes inserting it mid-function readable.

		Args:
			ns      (str):                Project namespace.
			version (str):                Project version.
			side    (str):                `mp` or `zb`.
			awards  (dict[str, XpAward]): That side's table.
		"""
		# xp_session feeds the end-of-match report, so only multiplayer keeps one.
		targets: list[str] = ["xp_total", "xp_prog"] + (["xp_session"] if side == "mp" else [])
		for key, award in awards.items():
			# Scaled rows carry their value in a score; flat ones are a literal the codegen already knows.
			if award.scaled:
				bumps = [f"scoreboard players operation @s {ns}.{side}.{target} += #xp_gain {ns}.data" for target in targets]
			else:
				bumps = [f"scoreboard players add @s {ns}.{side}.{target} {award.amount}" for target in targets]
			body: str = "\n".join(bumps)
			write_versioned_function(f"progression/{side}/award_{key}", f"""
# {award.note}
{body}
function {ns}:v{version}/progression/{side}/settle
""")

	@staticmethod
	def award_call(ns: str, version: str, side: str, key: str, selector: str = "@s", guard: str = "") -> str:
		""" Return the single command granting one award to whoever `selector` matches.

		`guard` is folded into the same `execute` as `selector` rather than being wrapped around the call,
		which is what keeps award sites from generating `execute <guard> run execute as <sel> run ...`.

		Args:
			ns       (str): Project namespace.
			version  (str): Project version.
			side     (str): `mp` or `zb`.
			key      (str): Row key in that side's table.
			selector (str): Who earns it; `@s` needs no `as` clause.
			guard    (str): Extra `execute` subcommands, ex: "if score #hp_red mgs.data matches 1..".
		Returns:
			str: One command.

		Examples:
			>>> Curve.award_call("mgs", "1.0", "mp", "kill")
			'function mgs:v1.0/progression/mp/award_kill'
			>>> Curve.award_call("mgs", "1.0", "mp", "kill", "@a", "if score #x mgs.data matches 1")
			'execute if score #x mgs.data matches 1 as @a run function mgs:v1.0/progression/mp/award_kill'
		"""
		call: str = f"function {ns}:v{version}/progression/{side}/award_{key}"
		clauses: str = " ".join(part for part in (guard, "" if selector == "@s" else f"as {selector}") if part)
		return f"execute {clauses} run {call}" if clauses else call

	@staticmethod
	def write(ns: str, version: str, side: str, label: str) -> None:
		""" Write every curve function for one side.

		Args:
			ns      (str): Project namespace.
			version (str): Project version.
			side    (str): `mp` or `zb`, naming both the objectives and the function folder.
			label   (str): Human name for the level-up message, ex: "Multiplayer".
		"""
		base: str = f"{ns}:v{version}/progression/{side}"

		## First contact with a player: level 1 is the floor the entire curve is written against, so a
		## missing score is not the same as level 0 and must never be treated as one.
		write_versioned_function(f"progression/{side}/init", f"""
scoreboard players add @s {ns}.{side}.xp_total 0
scoreboard players add @s {ns}.{side}.xp_prog 0
scoreboard players set @s {ns}.{side}.xp_level 1

# Banked XP with no level means either a first run after this system shipped or a retune of awards.py.
# Either way the total is the only trustworthy number, so rebuild the caches from it.
execute if score @s {ns}.{side}.xp_total matches 1.. run function {base}/recompute
function {base}/refresh_bar
""")

		## Everything an award has to do after moving the scores. Called once per award, never per level.
		write_versioned_function(f"progression/{side}/settle", f"""
# XP only ever goes up, and the cap is far past anything reachable — it exists so the bar and bisect
# multiplications cannot overflow.
execute if score @s {ns}.{side}.xp_total matches {XP_TOTAL_CAP}.. run scoreboard players set @s {ns}.{side}.xp_total {XP_TOTAL_CAP}
execute unless score @s {ns}.{side}.xp_level matches 1.. run scoreboard players set @s {ns}.{side}.xp_level 1

# Drain the progress into levels, then announce ONCE however many levels that turned out to be: a single
# large award can cross twenty boundaries at low level, and twenty chat lines is not a reward.
scoreboard players operation #xp_lvl_before {ns}.data = @s {ns}.{side}.xp_level
function {base}/level_check
execute if score @s {ns}.{side}.xp_level > #xp_lvl_before {ns}.data run function {base}/level_up_feedback

function {base}/refresh_bar
""")

		## Recursion depth is bounded by the largest single award: ~20 frames for a full zombies game-over
		## bonus landing on a level-1 player, and 1 for everything else.
		write_versioned_function(f"progression/{side}/level_check", f"""
{Curve.xp_required_lines(ns, side)}
execute if score @s {ns}.{side}.xp_prog >= #xp_req {ns}.data run function {base}/level_up
""")

		write_versioned_function(f"progression/{side}/level_up", f"""
scoreboard players operation @s {ns}.{side}.xp_prog -= #xp_req {ns}.data
scoreboard players add @s {ns}.{side}.xp_level 1
function {base}/level_check
""")

		## Deliberately not a `title @s actionbar`: the actionbar belongs to the Smithed library, which
		## merges this with whatever the ammo counter is already showing instead of stomping it.
		## The tag at the end is the public extension point — anything that wants to react to a level up
		## (a cosmetic unlock, a broadcast at milestones) subscribes to it instead of editing this.
		write_versioned_function(f"progression/{side}/level_up_feedback", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⬆ ","color":"gold"}},{{"text":"{label} level ","color":"gold","bold":true}},{{"score":{{"name":"@s","objective":"{ns}.{side}.xp_level"}},"color":"yellow","bold":true}}],priority:"override",freeze:60}}
function #smithed.actionbar:message
tellraw @s [{MGS_TAG},{{"text":"⬆ ","color":"gold"}},{{"text":"{label} level up! You are now level ","color":"yellow"}},{{"score":{{"name":"@s","objective":"{ns}.{side}.xp_level"}},"color":"gold","bold":true}},{{"text":".","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1.2

# @s = the player who levelled; #xp_lvl_before still holds the level they came from
data modify storage {ns}:signals on_level_up set value {{side:"{side}"}}
function #{ns}:progression/on_level_up
""")

		## The bar. Uninitialised players are skipped rather than defaulted: writing a level of 0 would
		## divide by the cost of a level that does not exist.
		write_versioned_function(f"progression/{side}/refresh_bar", f"""
execute unless score @s {ns}.{side}.xp_level matches 1.. run return 0

{Curve.xp_required_lines(ns, side)}
scoreboard players operation #xp_bar {ns}.data = @s {ns}.{side}.xp_prog
scoreboard players operation #xp_bar {ns}.data *= #{BAR_SCALE} {ns}.data
scoreboard players operation #xp_bar {ns}.data /= #xp_req {ns}.data

execute store result storage {ns}:temp _xp.points int 1 run scoreboard players get #xp_bar {ns}.data
execute store result storage {ns}:temp _xp.level int 1 run scoreboard players get @s {ns}.{side}.xp_level
function {ns}:v{version}/progression/apply_bar with storage {ns}:temp _xp
""")

		## Rebuild level and progress from the total. Run this after changing any value in awards.py: every
		## player keeps the XP they banked and their level is re-derived from the new curve.
		write_versioned_function(f"progression/{side}/recompute", f"""
execute unless score @s {ns}.{side}.xp_total matches 0.. run scoreboard players set @s {ns}.{side}.xp_total 0
execute if score @s {ns}.{side}.xp_total matches {XP_TOTAL_CAP}.. run scoreboard players set @s {ns}.{side}.xp_total {XP_TOTAL_CAP}

# Bracket the answer, then halve. Invariant: total_to_reach(#xp_lo) <= xp_total < total_to_reach(#xp_hi).
scoreboard players set #xp_lo {ns}.data 1
scoreboard players set #xp_hi {ns}.data {BISECT_HI}
function {base}/bisect

# #xp_lo is the level; whatever the level does not account for is the progress into it
scoreboard players operation @s {ns}.{side}.xp_level = #xp_lo {ns}.data
{Curve.total_to_reach_lines(ns, "#xp_lo", "#xp_need")}
scoreboard players operation @s {ns}.{side}.xp_prog = @s {ns}.{side}.xp_total
scoreboard players operation @s {ns}.{side}.xp_prog -= #xp_need {ns}.data

function {base}/refresh_bar
""")

		## Integer division is what makes this terminate: once the bounds are adjacent, (lo + lo+1)/2 == lo,
		## so the equality check below is reached in at most log2(BISECT_HI) = 14 frames.
		write_versioned_function(f"progression/{side}/bisect", f"""
scoreboard players operation #xp_mid {ns}.data = #xp_lo {ns}.data
scoreboard players operation #xp_mid {ns}.data += #xp_hi {ns}.data
scoreboard players operation #xp_mid {ns}.data /= #2 {ns}.data
execute if score #xp_mid {ns}.data = #xp_lo {ns}.data run return 0

{Curve.total_to_reach_lines(ns, "#xp_mid", "#xp_need")}
execute if score @s {ns}.{side}.xp_total >= #xp_need {ns}.data run scoreboard players operation #xp_lo {ns}.data = #xp_mid {ns}.data
execute if score @s {ns}.{side}.xp_total < #xp_need {ns}.data run scoreboard players operation #xp_hi {ns}.data = #xp_mid {ns}.data
function {base}/bisect
""")
