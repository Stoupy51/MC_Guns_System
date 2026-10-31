""" Who a player is: their UUID keys `mgs:stats`, and a new name takes over the scores of the old one. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .catalog import PERSISTENT_OBJECTIVES


# Functions
def write_identity() -> None:
	""" Write the login check, the first login and the rename.

	The UUID int array, rendered by a macro as `[I;a,b,c,d]`, is the compound key: `players."[I;a,b,c,d]"`.
	"""
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## custom:leave_game counts the disconnections, so a rejoin and a first join both find it different from 0.
	write_load_file(f"scoreboard objectives add {ns}.st.login custom:leave_game")
	write_versioned_function("progression/tick_player", f"execute unless score @s {ns}.st.login matches 0 run function {ns}:v{version}/stats/login", prepend=True)

	## The levels are initialised here too: this runs before `progression/tick_player` does it, and the snapshot copies them.
	write_versioned_function("stats/login", f"""
scoreboard players set @s {ns}.st.login 0
execute unless score @s {ns}.mp.xp_level matches 1.. run function {ns}:v{version}/progression/mp/init
execute unless score @s {ns}.zb.xp_level matches 1.. run function {ns}:v{version}/progression/zb/init

function {ns}:v{version}/players/read_name
data modify storage {ns}:temp _st set value {{}}
data modify storage {ns}:temp _st.uuid set from entity @s UUID
data modify storage {ns}:temp _st.name set from storage {ns}:temp _name
function {ns}:v{version}/stats/login_as with storage {ns}:temp _st
""")

	write_versioned_function("stats/login_as", f"""
$execute unless data storage {ns}:stats players."$(uuid)" run function {ns}:v{version}/stats/first_login with storage {ns}:temp _st

# A rename leaves the entry's name behind the current one.
$data modify storage {ns}:temp _st.old set from storage {ns}:stats players."$(uuid)".name
data modify storage {ns}:temp _st.cmp set from storage {ns}:temp _st.old
execute store success score #st_renamed {ns}.data run data modify storage {ns}:temp _st.cmp set from storage {ns}:temp _st.name
execute if score #st_renamed {ns}.data matches 1 run function {ns}:v{version}/stats/rename with storage {ns}:temp _st

$data modify storage {ns}:stats players."$(uuid)".name set value "$(name)"
$function {ns}:v{version}/stats/snapshot/player {{uuid:$(uuid),name:"$(name)"}}
function {ns}:v{version}/stats/board/levels with storage {ns}:temp _st
function {ns}:v{version}/stats/board/refresh_holograms
""")

	## The entry holds the current name, so a player whose scores predate this feature is backfilled by the snapshot that follows.
	write_versioned_function("stats/first_login", f"""
$data modify storage {ns}:stats players."$(uuid)" set value {{name:"$(name)"}}
execute store result score @s {ns}.st.index run data get storage {ns}:stats known
$data modify storage {ns}:stats known append value $(uuid)
""")

	## An unset source would copy as 0, so only the scores the old name has move, and the SUID Bookshelf just gave stays when there is none to restore.
	copies: str = "\n".join(
		f"$execute if score $(old) {objective} matches -2147483648.. run scoreboard players operation $(name) {objective} = $(old) {objective}"
		for objective in PERSISTENT_OBJECTIVES
	)
	write_versioned_function("stats/rename", f"""
{copies}
$scoreboard players reset $(old)
""")

