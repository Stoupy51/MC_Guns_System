""" Player stats per mode, kept as scores and copied into `mgs:stats` at login and at the end of a game.

Spec: `specs/011-player-stats-leaderboards`. Nothing here runs every tick.
Counters ride the award functions and the event sites, and the time and roster ride `progression/tick_player`, once a second.
Storage is written at login, at a game end and when a stats page opens.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..multiplayer.gamemodes.dispatch import GAMEMODES
from .boards import write_boards
from .catalog import MODES
from .identity import write_identity
from .menus import write_stats_menus
from .snapshot import write_snapshot


# Functions
def generate_stats() -> None:
	""" Write the identity, the recording, the dialogs and the admin reset. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	write_identity()
	write_snapshot()
	write_stats_menus()
	write_boards()

	objectives: list[str] = [stat.objective for mode in MODES for stat in mode.stats]
	objectives += [f"{ns}.st.mp.{gamemode}.{key}" for gamemode in GAMEMODES for key in ("games", "wins")]
	resets: str = "\n".join(f"$scoreboard players reset $(name) {objective}" for objective in objectives)
	write_versioned_function("stats/admin/reset", f"""
data modify storage {ns}:temp _st_one set value {{}}
$data modify storage {ns}:temp _st_one.uuid set from storage {ns}:stats known[$(i)]
function {ns}:v{version}/stats/admin/reset_uuid with storage {ns}:temp _st_one
""")
	write_versioned_function("stats/admin/reset_uuid", f"""
$data modify storage {ns}:temp _st_one.name set from storage {ns}:stats players."$(uuid)".name
function {ns}:v{version}/stats/admin/reset_name with storage {ns}:temp _st_one
""")
	write_versioned_function("stats/admin/reset_name", f"""
{resets}
$function {ns}:v{version}/stats/snapshot/player {{uuid:$(uuid),name:"$(name)"}}
$tellraw @s [{MGS_TAG},{{"text":"Stats reset for ","color":"yellow"}},{{"text":"$(name)","color":"white"}}]
""")

