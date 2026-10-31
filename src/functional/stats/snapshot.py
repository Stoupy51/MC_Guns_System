""" Recording: the counters each award feeds, the time and roster of a running game, and the copy of the scores into `mgs:stats`. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ..multiplayer.gamemodes.dispatch import GAMEMODES
from .catalog import MODES, StatMode


# Functions
def write_snapshot() -> None:
	""" Write the counters, the per-second time and roster, the end-of-game hooks and the snapshot. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	owned: list[str] = [stat.objective for mode in MODES for stat in mode.stats if stat.owned]
	per_gamemode: list[str] = [f"{ns}.st.mp.{gamemode}.{key}" for gamemode in GAMEMODES for key in ("games", "wins")]
	write_load_file("\n".join(
		[f"scoreboard objectives add {objective} dummy" for objective in (*owned, *per_gamemode, f"{ns}.st.index")]
		+ [f"scoreboard objectives add {ns}.st.{mode.key}.game_id dummy" for mode in MODES]
		+ [f"execute unless score #st_{mode.key}_game {ns}.data matches 0.. run scoreboard players set #st_{mode.key}_game {ns}.data 0" for mode in MODES]
	))

	## Appended after `settle`: a counter has no say in the level the award pushes.
	for mode in MODES:
		for stat in mode.stats:
			for source in stat.sources:
				write_versioned_function(f"progression/{mode.award_side}/award_{source}", f"scoreboard players add @s {stat.objective} 1")
	write_versioned_function("progression/mp/award_match_win", f"function {ns}:v{version}/stats/mp/gamemode_win with storage {ns}:multiplayer game")
	write_versioned_function("progression/mp/award_match_loss", f"function {ns}:v{version}/stats/mp/gamemode_game with storage {ns}:multiplayer game")
	write_versioned_function("stats/mp/gamemode_game", f"$scoreboard players add @s {ns}.st.mp.$(gamemode).games 1")
	write_versioned_function("stats/mp/gamemode_win", f"""
$scoreboard players add @s {ns}.st.mp.$(gamemode).games 1
$scoreboard players add @s {ns}.st.mp.$(gamemode).wins 1
""")

	for mode in MODES:
		write_mode_recording(ns, version, mode)

	## Run once per cleared round, for the whole roster, like the round XP.
	write_versioned_function("stats/zb/on_round_end", f"scoreboard players add @a[scores={{{ns}.zb.in_game=1}}] {ns}.st.zb.rounds 1", tags=[f"{ns}:zombies/on_round_end"])

	## Only a mission that ran counts: missions/stop also ends one still in its lobby.
	write_versioned_function("stats/mi/on_mission_end", f"""
execute if score #mi_timer {ns}.data matches 1.. run scoreboard players add @a[scores={{{ns}.mi.in_game=1}}] {ns}.st.mi.games 1
function {ns}:v{version}/stats/mi/game_end
""", tags=[f"{ns}:missions/on_mission_end"])
	write_versioned_function("stats/zb/on_game_end", f"function {ns}:v{version}/stats/zb/game_end", tags=[f"{ns}:zombies/on_game_end"])
	write_versioned_function("stats/mp/on_game_end", f"function {ns}:v{version}/stats/mp/game_end", tags=[f"{ns}:multiplayer/on_game_end"])

	write_snapshot_player(ns, version)

	## Macro {uuid, name, map_id}, once per roster player at a game end, after their snapshot.
	board: str = f"{ns}:v{version}/stats/board"
	write_versioned_function("stats/mp/player_end", f"function {board}/levels with storage {ns}:temp _st_one")
	write_versioned_function("stats/zb/player_end", f"""
function {board}/levels with storage {ns}:temp _st_one
function {board}/zb_round with storage {ns}:temp _st_one
""")
	write_versioned_function("stats/mi/player_end", f"""
function {board}/levels with storage {ns}:temp _st_one
execute if score #st_mi_won {ns}.data matches 1 run function {board}/mi_time with storage {ns}:temp _st_one
""")
	write_versioned_function("missions/victory", f"scoreboard players set #st_mi_won {ns}.data 1", prepend=True)
	write_versioned_function("stats/mi/on_mission_end", f"scoreboard players set #st_mi_won {ns}.data 0")


def write_mode_recording(ns: str, version: str, mode: StatMode) -> None:
	""" Write one mode's second (time and roster) and its game end (snapshot of the roster, offline players included). """
	write_versioned_function("progression/tick_player", (
		f'execute if score @s {mode.in_game} matches 1 if data storage {ns}:{mode.storage} game{{state:"active"}} '
		f"run function {ns}:v{version}/stats/{mode.key}/second"
	), prepend=True)

	## The game id tells this game's roster from the last one, whatever its players did offline in between.
	write_versioned_function(f"stats/{mode.key}/second", f"""
scoreboard players add @s {ns}.st.{mode.key}.time 1
execute unless score @s {ns}.st.{mode.key}.game_id = #st_{mode.key}_game {ns}.data run function {ns}:v{version}/stats/{mode.key}/join_roster
""")
	write_versioned_function(f"stats/{mode.key}/join_roster", f"""
scoreboard players operation @s {ns}.st.{mode.key}.game_id = #st_{mode.key}_game {ns}.data
data modify storage {ns}:stats rosters.{mode.key} append from entity @s UUID
""")

	write_versioned_function(f"stats/{mode.key}/game_end", f"""
data modify storage {ns}:temp _st_roster set from storage {ns}:stats rosters.{mode.key}
execute store result score #lb_n {ns}.data run data get storage {ns}:temp _st_roster
data modify storage {ns}:temp _st_map set from storage {ns}:{mode.storage} game.map_id
function {ns}:v{version}/stats/snapshot/roster_next {{mode:"{mode.key}"}}
function {ns}:v{version}/stats/board/refresh_holograms

data remove storage {ns}:stats rosters.{mode.key}
scoreboard players add #st_{mode.key}_game {ns}.data 1
""")


def write_snapshot_player(ns: str, version: str) -> None:
	""" Write the copy of one player's scores, read by name so it works offline, and the roster walk calling it. """
	write_versioned_function("stats/snapshot/roster_next", f"""
execute unless data storage {ns}:temp _st_roster[0] run return 0

data modify storage {ns}:temp _st_one set value {{}}
data modify storage {ns}:temp _st_one.uuid set from storage {ns}:temp _st_roster[0]
function {ns}:v{version}/stats/snapshot/by_uuid with storage {ns}:temp _st_one
data modify storage {ns}:temp _st_one.map_id set from storage {ns}:temp _st_map
$function {ns}:v{version}/stats/$(mode)/player_end with storage {ns}:temp _st_one

data remove storage {ns}:temp _st_roster[0]
$function {ns}:v{version}/stats/snapshot/roster_next {{mode:"$(mode)"}}
""")
	write_versioned_function("stats/snapshot/by_uuid", f"""
$data modify storage {ns}:temp _st_one.name set from storage {ns}:stats players."$(uuid)".name
function {ns}:v{version}/stats/snapshot/player with storage {ns}:temp _st_one
""")

	## An unset score fails `scoreboard players get`, which stores 0.
	def copy(path: str, objective: str) -> str:
		return f'$execute store result storage {ns}:stats players."$(uuid)".{path} int 1 run scoreboard players get $(name) {objective}'

	lines: list[str] = [copy(f"{mode.key}.{stat.key}", stat.objective) for mode in MODES for stat in mode.stats]
	lines += [copy(f"mp.modes.{gamemode}.{key}", f"{ns}.st.mp.{gamemode}.{key}") for gamemode in GAMEMODES for key in ("games", "wins")]
	lines += [copy(f"level.{side}", f"{ns}.{side}.xp_level") for side in ("mp", "zb")]
	write_versioned_function("stats/snapshot/player", "\n".join(lines))

