""" Where missions grants XP.

Missions has no level of its own, so everything here pays into the Multiplayer pool. That is not a
shortcut: missions already runs on the multiplayer side (`mp.class`, `mp.team`, `mp.default`, the
multiplayer loadout and class functions), and `progression/tick_player` shows the Multiplayer level
everywhere outside a Zombies game, so a missions player is watching their Multiplayer bar the whole time.

Two streams. **Kills** ride the shared `signals/on_kill` tag, the same one multiplayer and zombies listen
to, guarded on the missions game actually being live so the three listeners never pay for each other's
kills. **Completing the mission** is granted from the victory function, whose per-player summary line the
amount rides on rather than printing a message of its own.

Mission kills use their own award rows instead of `kill` and `headshot`, because the Multiplayer kills
challenge counts the `kill` row and its nodes say "Kill N players".
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

		No award ever prints a line of its own, and the summary already prints one per player, so the
		amount rides that instead of adding a message nobody asked for.

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

	## @s = the shooter. The state guard matters: this signal fires for multiplayer and zombies kills too,
	## and all three listeners sit on the same tag.
	## Headshots come off the payload rather than #is_headshot, for the reason zombies/xp/on_kill spells
	## out: the projectile path fires on_kill without resetting that score.
	write_versioned_function("missions/xp/on_kill", f"""
execute unless data storage {ns}:missions game{{state:"active"}} run return fail
execute unless score @s {ns}.mi.in_game matches 1 run return fail

{Xp.give("mp", "mission_kill")}
execute if data storage {ns}:signals on_kill{{headshot:1}} run {Xp.give("mp", "mission_headshot")}
""", tags=[f"{ns}:signals/on_kill"])
