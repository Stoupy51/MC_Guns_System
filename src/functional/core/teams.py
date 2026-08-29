""" The vanilla teams every mode assigns players to.

Created at load rather than at game start: the Manage Players menu assigns a team before any game
exists, and a mid-game /reload can't leave them missing.
"""
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_load_file


# Classes
@dataclass(frozen=True)
class TeamDef:
	""" One vanilla team: its suffix under the project namespace and its display rules. """
	suffix: str
	color: str
	friendly_fire: bool
	nametag_visibility: str


# Constants
TEAMS: list[TeamDef] = [
	TeamDef(suffix="red",     color="red",      friendly_fire=False, nametag_visibility="hideForOtherTeams"),
	TeamDef(suffix="blue",    color="blue",     friendly_fire=False, nametag_visibility="hideForOtherTeams"),
	TeamDef(suffix="ffa",     color="yellow",   friendly_fire=True,  nametag_visibility="never"),
	TeamDef(suffix="zombies", color="yellow",   friendly_fire=False, nametag_visibility="hideForOtherTeams"),
	TeamDef(suffix="mi_mobs", color="dark_red", friendly_fire=True,  nametag_visibility="always"),
]
""" Every team shared across modes. The escort horde team lives with the escort code (it is AI-only). """


# Functions
def write_teams() -> None:
	ns: str = Mem.ctx.project_id

	lines: list[str] = ["# Shared vanilla teams"]
	for team in TEAMS:
		lines.append(f"team add {ns}.{team.suffix}")
		lines.append(f"team modify {ns}.{team.suffix} color {team.color}")
		lines.append(f"team modify {ns}.{team.suffix} friendlyFire {str(team.friendly_fire).lower()}")
		lines.append(f"team modify {ns}.{team.suffix} nametagVisibility {team.nametag_visibility}")
	write_load_file("\n".join(lines))

