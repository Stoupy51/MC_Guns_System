""" Where zombies grants XP.

Three streams need real machinery and live here; the rest are one-liners inserted at the site that already
knows the thing happened (a door opening, a perk landing, a power-up being picked up).

- **Kills** ride the `totalKillCount` delta `zombies/check_kill_points` already computes, so every kill type
  counts — gun, knife, trap, Nuke — exactly like the points economy does.
- **Headshots** cannot come from that delta, which knows nothing about where the bullet landed. They come off
  the `signals/on_kill` payload instead, so a headshot kill pays base + bonus and everything else pays base.
- **Points spent** is derived from `zb.points` DROPPING rather than from the twelve purchase sites, none of
  which share a debit function. Any purchase added later is covered for free.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from ..progression import Xp
from ..progression.awards import GAME_OVER_XP, POINTS_PER_XP, ROUND_XP, ZB_AWARDS


# Functions
def generate_zombies_xp() -> None:
	""" Write the headshot listener, the spend tracker and the round-survived bonus. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## @s = the shooter. Read off the signal payload, NOT off #is_headshot: the projectile path fires
	## on_kill without resetting that score, so it would still hold the last raycast's value. The payload is
	## safe because that path opens with `on_kill set value {}`, leaving `headshot` absent.
	write_versioned_function("zombies/xp/on_kill", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute unless score @s {ns}.zb.in_game matches 1 run return fail
execute unless data storage {ns}:signals on_kill{{headshot:1}} run return fail

{Xp.give("zb", "headshot")}
""", tags=[f"{ns}:signals/on_kill"])

	## Per in-game player, every tick, from zombies/game_tick. Two commands in the common case: the guard
	## fails and only the mirror runs. Deliberately NOT appended to check_kill_points, which returns early
	## when there are no new kills and would skip the tracking on most ticks.
	write_versioned_function("zombies/xp/track_points", f"""
execute if score @s {ns}.zb.points < @s {ns}.zb.xp_pts_prev run function {ns}:v{version}/zombies/xp/spend_delta
scoreboard players operation @s {ns}.zb.xp_pts_prev = @s {ns}.zb.points
""")

	## Points went down, so the difference was spent. A refund arrives as an INCREASE and is therefore never
	## counted back off — a refunded purchase reads as spent, which is worth at most a few XP and not worth
	## instrumenting eighteen call sites to avoid.
	## The remainder is carried in xp_spent_acc so nothing is lost to integer division.
	write_versioned_function("zombies/xp/spend_delta", f"""
scoreboard players operation #xp_spent {ns}.data = @s {ns}.zb.xp_pts_prev
scoreboard players operation #xp_spent {ns}.data -= @s {ns}.zb.points
scoreboard players operation @s {ns}.zb.xp_spent_acc += #xp_spent {ns}.data

# Convert whole chunks and keep the change
scoreboard players operation #xp_gain {ns}.data = @s {ns}.zb.xp_spent_acc
scoreboard players operation #xp_gain {ns}.data /= #{POINTS_PER_XP} {ns}.data
execute if score #xp_gain {ns}.data matches 1.. run function {ns}:v{version}/zombies/xp/pay_spend
""")

	write_versioned_function("zombies/xp/pay_spend", f"""
scoreboard players operation #xp_spent {ns}.data = #xp_gain {ns}.data
scoreboard players operation #xp_spent {ns}.data *= #{POINTS_PER_XP} {ns}.data
scoreboard players operation @s {ns}.zb.xp_spent_acc -= #xp_spent {ns}.data

# No message: spending already had its own feedback, and this is a trickle rather than an event
{Xp.give("zb", "points_spent")}
""")

	## Fired by zombies/round_complete BEFORE it announces the round, so #xp_gain is already set by the time
	## that announce reads it for its suffix. Everyone still on the roster earns it, downed or not.
	write_versioned_function("zombies/xp/on_round_end", f"""
execute store result score #xp_gain {ns}.data run data get storage {ns}:zombies game.round
scoreboard players operation #xp_gain {ns}.data *= #{ROUND_XP} {ns}.data
{Xp.give("zb", "round_survived", f"@a[scores={{{ns}.zb.in_game=1}}]")}
""", tags=[f"{ns}:zombies/on_round_end"])

	## The kill stream, appended to the function that already computed the delta. It sits after that
	## function's `return 0` for "no new kills", which is exactly where it belongs.
	write_versioned_function("zombies/check_kill_points", f"""
# XP for the same kills the points above were paid for
scoreboard players operation #xp_gain {ns}.data = #zb_kills_delta {ns}.data
scoreboard players operation #xp_gain {ns}.data *= #{ZB_AWARDS["kill"].amount} {ns}.data
{Xp.give("zb", "kill")}
""")

	## Hook the spend tracker into the per-player tick the economy already runs
	write_versioned_function("zombies/game_tick", f"""
# Progression: turn spent points into XP (see zombies/xp/track_points)
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/xp/track_points
""")

	## Paid once when the run ends, scaled by how deep it got. Written here rather than appended so it lands
	## before game_over's "Final Round" line, which carries the suffix.
	write_versioned_function("zombies/xp/on_game_over", f"""
scoreboard players operation #xp_gain {ns}.data = #final_round {ns}.data
scoreboard players operation #xp_gain {ns}.data *= #{GAME_OVER_XP} {ns}.data
{Xp.give("zb", "game_over", f"@a[scores={{{ns}.zb.in_game=1}}]")}
""")

