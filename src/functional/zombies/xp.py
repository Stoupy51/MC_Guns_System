""" Where zombies grants XP.

Three streams need machinery and live here; the others are one-liners at the site that knows the event (a door, a perk, a power-up).

- Kills use the `totalKillCount` delta that `zombies/check_kill_points` computes, so gun, knife, trap and Nuke kills count, like points.
- Headshots come from the `signals/on_kill` payload, since the delta does not know where the bullet landed: a headshot kill pays base + bonus.
- Points spent come from `zb.points` dropping, not from the twelve purchase sites, which share no debit function; new purchases are covered for free.
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

	## Run as the shooter. Reads the signal payload, not #is_headshot, which the projectile path never resets;
	## that path writes `on_kill` as {}, so `headshot` is absent.
	write_versioned_function("zombies/xp/on_kill", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute unless score @s {ns}.zb.in_game matches 1 run return fail
execute unless data storage {ns}:signals on_kill{{headshot:1}} run return fail

{Xp.give("zb", "headshot")}
""", tags=[f"{ns}:signals/on_kill"])

	## Run per in-game player every tick from zombies/game_tick: usually two commands. Not in check_kill_points,
	## which returns early when there are no new kills.
	write_versioned_function("zombies/xp/track_points", f"""
execute if score @s {ns}.zb.points < @s {ns}.zb.xp_pts_prev run function {ns}:v{version}/zombies/xp/spend_delta
scoreboard players operation @s {ns}.zb.xp_pts_prev = @s {ns}.zb.points
""")

	## Points went down, so the difference was spent. A refund raises points and is never subtracted, so a refunded buy
	## still counts as spent (a few XP at most). The remainder carries in xp_spent_acc.
	write_versioned_function("zombies/xp/spend_delta", f"""
scoreboard players operation #xp_spent {ns}.data = @s {ns}.zb.xp_pts_prev
scoreboard players operation #xp_spent {ns}.data -= @s {ns}.zb.points
scoreboard players operation @s {ns}.zb.xp_spent_acc += #xp_spent {ns}.data

# Whole chunks convert, the rest carries.
scoreboard players operation #xp_gain {ns}.data = @s {ns}.zb.xp_spent_acc
scoreboard players operation #xp_gain {ns}.data /= #{POINTS_PER_XP} {ns}.data
execute if score #xp_gain {ns}.data matches 1.. run function {ns}:v{version}/zombies/xp/pay_spend
""")

	write_versioned_function("zombies/xp/pay_spend", f"""
scoreboard players operation #xp_spent {ns}.data = #xp_gain {ns}.data
scoreboard players operation #xp_spent {ns}.data *= #{POINTS_PER_XP} {ns}.data
scoreboard players operation @s {ns}.zb.xp_spent_acc -= #xp_spent {ns}.data

# No message: spending is a trickle with its own feedback.
{Xp.give("zb", "points_spent")}
""")

	## Fired by round_complete before its announce reads #xp_gain. The whole roster earns it, downed or not.
	write_versioned_function("zombies/xp/on_round_end", f"""
execute store result score #xp_gain {ns}.data run data get storage {ns}:zombies game.round
scoreboard players operation #xp_gain {ns}.data *= #{ROUND_XP} {ns}.data
{Xp.give("zb", "round_survived", f"@a[scores={{{ns}.zb.in_game=1}}]")}
""", tags=[f"{ns}:zombies/on_round_end"])

	## The kill XP, after check_kill_points' `return 0` for "no new kills".
	write_versioned_function("zombies/check_kill_points", f"""
# The same kills the points above paid for.
scoreboard players operation #xp_gain {ns}.data = #zb_kills_delta {ns}.data
scoreboard players operation #xp_gain {ns}.data *= #{ZB_AWARDS["kill"].amount} {ns}.data
{Xp.give("zb", "kill")}
""")

	write_versioned_function("zombies/game_tick", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/xp/track_points
""")

	## Paid once at the end, scaled by depth; written before game_over's Final Round line, which shows the amount.
	write_versioned_function("zombies/xp/on_game_over", f"""
scoreboard players operation #xp_gain {ns}.data = #final_round {ns}.data
scoreboard players operation #xp_gain {ns}.data *= #{GAME_OVER_XP} {ns}.data
{Xp.give("zb", "game_over", f"@a[scores={{{ns}.zb.in_game=1}}]")}
""")

