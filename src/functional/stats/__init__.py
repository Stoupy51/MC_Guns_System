""" Player stats per mode, kept as scores and copied into `mgs:stats` at login and at the end of a game.

Nothing here runs every tick but the three commands of each leaderboard command block.
Counters ride the award functions and the event sites, and the time and roster ride `progression/tick_player`, once a second.
Storage is written at login, at a game end and when a stats page opens.
"""
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .boards import write_boards
from .catalog import PERSISTENT_OBJECTIVES
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

	kept: set[str] = {"bs.id", "mgs.st.index", "mgs.mp.pid"}
	resets: str = "\n".join(f"$scoreboard players reset $(name) {objective}" for objective in PERSISTENT_OBJECTIVES if objective not in kept)
	write_load_file(f"scoreboard objectives add {ns}.st.reset dummy")
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
$scoreboard players set $(name) {ns}.mp.xp_level 1
$scoreboard players set $(name) {ns}.zb.xp_level 1
$function {ns}:v{version}/stats/board/forget {{uuid:$(uuid)}}
$execute as $(name) run function {ns}:v{version}/progression/mp/init
$execute as $(name) run function {ns}:v{version}/progression/zb/init
$execute if entity $(name) run advancement revoke $(name) everything
$execute unless entity $(name) run scoreboard players set $(name) {ns}.st.reset 1
$function {ns}:v{version}/stats/snapshot/player {{uuid:$(uuid),name:"$(name)"}}
$tellraw @s [{MGS_TAG},{{"text":"Fully reset: ","color":"yellow"}},{{"text":"$(name)","color":"white"}}]
""")

