""" Where multiplayer grants XP: the two events that are not tied to a single gamemode.

Kills come through the shared `signals/on_kill` tag, so one listener covers all six modes. The match bonus
hangs off `multiplayer/on_game_end`, which `multiplayer/stop` fires while `mp.in_game` and the team scores are
both still valid — a few lines later they are wiped.

Objective XP (captures, hills, plants, defuses, round wins) is granted where the objective actually resolves,
inside each gamemode's own file, because most of those functions run as a marker rather than as a player and
the award has to sit at a precise point in the sequence.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from ..progression import Xp

# Constants
WINNER_TAG: str = "xp_winner"
""" Set on whoever took the match, just long enough for the bonus to be handed out.
FFA tags its own winner in `ffa/player_wins`; team modes are decided from the final score. """


# Functions
def generate_multiplayer_xp() -> None:
	""" Write the kill listener and the end-of-match bonus. """
	ns: str = Mem.ctx.project_id

	## @s = the killer. #mp_kill_headshot is already correct on BOTH death paths by the time this runs:
	## simulate_death reads it out of the damage payload, and vanilla_kill_credit (melee) zeroes it.
	## The state guard matters — this same signal fires for zombies and missions kills too.
	write_versioned_function("multiplayer/xp/on_kill", f"""
execute unless data storage {ns}:multiplayer game{{state:"active"}} run return fail
execute unless score @s {ns}.mp.in_game matches 1 run return fail

{Xp.give("mp", "kill")}
execute if score #mp_kill_headshot {ns}.data matches 1 run {Xp.give("mp", "headshot")}
""", tags=[f"{ns}:signals/on_kill"])

	## Fired from multiplayer/stop, before the ranked stats line reads xp_session and before mp.in_game is
	## cleared. No suffix of its own: this lands in the `+N XP` on each player's after-action line.
	write_versioned_function("multiplayer/xp/on_game_end", f"""
execute if score #red {ns}.mp.team > #blue {ns}.mp.team run tag @a[scores={{{ns}.mp.team=1}}] add {ns}.{WINNER_TAG}
execute if score #blue {ns}.mp.team > #red {ns}.mp.team run tag @a[scores={{{ns}.mp.team=2}}] add {ns}.{WINNER_TAG}

{Xp.give("mp", "match_win", f"@a[scores={{{ns}.mp.in_game=1}},tag={ns}.{WINNER_TAG}]")}
{Xp.give("mp", "match_loss", f"@a[scores={{{ns}.mp.in_game=1}},tag=!{ns}.{WINNER_TAG}]")}
tag @a remove {ns}.{WINNER_TAG}
""", tags=[f"{ns}:multiplayer/on_game_end"])
