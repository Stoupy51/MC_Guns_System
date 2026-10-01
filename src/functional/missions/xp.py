""" Where missions grants XP.

Missions has no level of its own, so everything pays into the Multiplayer pool.
Missions already runs on the multiplayer side (`mp.class`, `mp.team`, `mp.default`, the loadout and class functions),
and `progression/tick_player` shows the Multiplayer level outside Zombies, so a missions player watches that bar.

Two streams.
Kills ride the shared `signals/on_kill` tag, guarded on a live missions game so the three listeners never pay for each other's kills.
Completing the mission is paid from the victory function, on its per-player summary line.

Mission kills use their own award rows instead of `kill` and `headshot`: the Multiplayer kills challenge counts the `kill` row, and its nodes say "Kill N players".
"""
# Imports
from stewbeet import Mem, write_versioned_function

from ..progression import Xp


# Classes
class MissionsXp:
	""" The lines the victory function splices in, kept here with the rest of the missions XP. """

	# Functions
	@staticmethod
	def victory_suffix() -> str:
		""" Return the XP suffix appended to the victory summary's per-player line.

		No award prints a line of its own, and the summary already prints one per player, so the amount rides that.

		Returns:
			str: SNBT list component, ex: `[" ",{"text":"+50 XP","color":"gold"}]`
		"""
		return Xp.suffix("mp", "mission_complete")

	@staticmethod
	def victory_lines() -> str:
		""" Return the award granted to everyone who finished the mission.

		Spliced into `missions/victory` rather than appended, because that function ends by calling
		`missions/stop`, which clears `mi.in_game` and would leave an appended award selecting nobody.

		Returns:
			str: One command.
		"""
		ns: str = Mem.ctx.project_id
		return Xp.give("mp", "mission_complete", f"@a[scores={{{ns}.mi.in_game=1}}]")


# Functions
def generate_missions_xp() -> None:
	""" Write the kill listener. """
	ns: str = Mem.ctx.project_id

	## Run as the shooter. The state guard matters: multiplayer and zombies kills fire the same signal.
	## Headshots come from the payload, not #is_headshot, which the projectile path never resets (see zombies/xp).
	write_versioned_function("missions/xp/on_kill", f"""
execute unless data storage {ns}:missions game{{state:"active"}} run return fail
execute unless score @s {ns}.mi.in_game matches 1 run return fail

{Xp.give("mp", "mission_kill")}
execute if data storage {ns}:signals on_kill{{headshot:1}} run {Xp.give("mp", "mission_headshot")}
""", tags=[f"{ns}:signals/on_kill"])

