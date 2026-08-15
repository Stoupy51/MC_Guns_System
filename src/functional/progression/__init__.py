""" Cosmetic leveling, shared by Multiplayer and Zombies.

Purely visual: nothing is gated behind a level, there is no cap and no prestige. Each side keeps its own
independent level, shown on the vanilla XP bar and in front of the player's name in every message the pack
prints.

This package owns the curve and the display. The award *sites* live with the mode that fires them,
`multiplayer/xp.py` and `zombies/xp.py`, and the award *values* all live in `awards.py`. `Xp` itself is in
`xp.py` so the advancements package can pay through it without closing an import cycle.

[advancements] hangs the challenge tree off the same award functions: one advancement tab, three branches,
and counters fed from inside `award_<key>` so no award site is touched.
"""
# Imports
from stewbeet import (
	Mem,
	write_load_file,
	write_tag,
	write_tick_file,
	write_versioned_function,
)

from .advancements import Advancements, generate_advancements
from .curve import PARK_LEVEL, Curve
from .xp import EARNER_TAG, SIDES, TABLES, Xp

__all__ = ["EARNER_TAG", "SIDES", "TABLES", "Advancements", "Curve", "Xp", "generate_progression"]


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
		Curve.write_award_functions(ns, version, side, TABLES[side], Advancements.stat_lines(side))

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
	## awards.py safe: the totals are authoritative, so nobody loses progress when the curve moves under them.
	write_versioned_function("progression/recompute_all", f"""
execute as @a run function {ns}:v{version}/progression/mp/recompute
execute as @a run function {ns}:v{version}/progression/zb/recompute
""")

	## Challenges. Written last so the award functions it observes already exist, and because its tree
	## references the reward functions it is about to write.
	generate_advancements()
