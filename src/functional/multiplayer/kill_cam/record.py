""" Recording: the window that opens once one streak could end the match, its frames, and the deaths and shots inside it.

A sample never reads player NBT: one marker with a fixed UUID is teleported to the player and its own `Pos` and `Rotation` are copied.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from .shared import MAX_CHAIN, PROBE_UUID, PROBE_UUID_NBT, RECORD_TICKS


# Functions
def write_kill_cam_recording() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	kc: str = f"{ns}:v{version}/multiplayer/kill_cam"
	modes: str = " ".join(f'unless data storage {ns}:multiplayer game{{gamemode:"{mode}"}}' for mode in ("ffa", "tdm", "snd"))

	## Run when a match goes active, at each death while the window is closed and at each Search and Destroy round start.
	write_versioned_function("multiplayer/kill_cam/check_window", f"""
# The other modes end on points, sites or the clock.
execute {modes} run return fail

# The lead: FFA's best player or the best team, against the score limit minus one full chain, or one round win short in S&D.
scoreboard players set #kc_lead {ns}.data 0
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run scoreboard players operation #kc_lead {ns}.data > @a[scores={{{ns}.mp.in_game=1}}] {ns}.mp.kills
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} run scoreboard players operation #kc_lead {ns}.data > #red {ns}.mp.team
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} run scoreboard players operation #kc_lead {ns}.data > #blue {ns}.mp.team

execute store result score #kc_threshold {ns}.data run data get storage {ns}:multiplayer game.score_limit
scoreboard players remove #kc_threshold {ns}.data {MAX_CHAIN}
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run scoreboard players operation #kc_threshold {ns}.data = #snd_win_threshold {ns}.data
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run scoreboard players remove #kc_threshold {ns}.data 1

execute if score #kc_lead {ns}.data >= #kc_threshold {ns}.data run function {kc}/open
""")

	write_versioned_function("multiplayer/kill_cam/open", f"""
scoreboard players set #kc_window {ns}.data 1
data modify storage {ns}:kill_cam frames set value []
data modify storage {ns}:kill_cam deaths set value []
data remove storage {ns}:kill_cam pending_shots
""")

	## Also run when a Search and Destroy round ends without ending the match.
	write_versioned_function("multiplayer/kill_cam/close", f"""
scoreboard players set #kc_window {ns}.data 0
data remove storage {ns}:kill_cam frames
data remove storage {ns}:kill_cam deaths
data remove storage {ns}:kill_cam pending_shots
""")

	## One frame per game tick while the window is open, keyed by its tick.
	write_versioned_function("multiplayer/kill_cam/record", f"""
data modify storage {ns}:kill_cam frames append value {{s:[]}}
execute store result storage {ns}:kill_cam frames[-1].t int 1 run scoreboard players get #total_tick {ns}.data
execute if data storage {ns}:kill_cam pending_shots[0] run data modify storage {ns}:kill_cam frames[-1].shots set from storage {ns}:kill_cam pending_shots
data remove storage {ns}:kill_cam pending_shots

# The probe stays where the last sample left it, which a player leaving can unload.
execute unless entity {PROBE_UUID} at @r[scores={{{ns}.mp.in_game=1}},gamemode=!spectator] run function {kc}/summon_probe
execute as @a[scores={{{ns}.mp.in_game=1}},gamemode=!spectator] at @s run function {kc}/sample

execute if data storage {ns}:kill_cam frames[{RECORD_TICKS}] run function {kc}/trim
""")

	write_versioned_function("multiplayer/kill_cam/summon_probe", f"""
summon minecraft:marker ~ ~ ~ {{UUID:{PROBE_UUID_NBT},Tags:["{ns}.kill_cam","{ns}.multiplayer_entity"]}}
""")

	## Run as a live match player, at them.
	write_versioned_function("multiplayer/kill_cam/sample", f"""
tp {PROBE_UUID} ~ ~ ~ ~ ~
data modify storage {ns}:kill_cam frames[-1].s append value {{}}
execute store result storage {ns}:kill_cam frames[-1].s[-1].id int 1 run scoreboard players get @s bs.id
data modify storage {ns}:kill_cam frames[-1].s[-1].p set from entity {PROBE_UUID} Pos
data modify storage {ns}:kill_cam frames[-1].s[-1].r set from entity {PROBE_UUID} Rotation
execute if predicate {ns}:v{version}/is_sneaking run data modify storage {ns}:kill_cam frames[-1].s[-1].sneak set value 1b
""")

	write_versioned_function("multiplayer/kill_cam/trim", f"""
data remove storage {ns}:kill_cam frames[0]
execute store result score #kc_oldest {ns}.data run data get storage {ns}:kill_cam frames[0].t
execute if data storage {ns}:kill_cam deaths[0] run function {kc}/trim_deaths
""")

	## Drops the deaths before #kc_oldest, which no frame can show.
	write_versioned_function("multiplayer/kill_cam/trim_deaths", f"""
execute store result score #kc_t {ns}.data run data get storage {ns}:kill_cam deaths[0].t
execute if score #kc_t {ns}.data >= #kc_oldest {ns}.data run return 0
data remove storage {ns}:kill_cam deaths[0]
execute if data storage {ns}:kill_cam deaths[0] run function {kc}/trim_deaths
""")

	## Run as the shooter. Mob shots and other modes' players fire the same signal.
	write_versioned_function("multiplayer/kill_cam/on_shoot", f"""
execute unless score #kc_window {ns}.data matches 1 run return fail
execute unless entity @s[type=player,scores={{{ns}.mp.in_game=1}}] run return fail
data modify storage {ns}:kill_cam pending_shots append value {{}}
execute store result storage {ns}:kill_cam pending_shots[-1].id int 1 run scoreboard players get @s bs.id
data modify storage {ns}:kill_cam pending_shots[-1].snd set from storage {ns}:signals on_shoot.weapon.sounds.fire
""", tags=[f"{ns}:signals/on_shoot"])

	write_versioned_function("multiplayer/end_prep", f"""
# A score limit within one chain records from the start.
function {kc}/check_window
""")

	## Ahead of the Search and Destroy branch of enter_death_spectate, which returns, while {ns}.temp_killer is still on the killer.
	write_versioned_function("multiplayer/enter_death_spectate", f"function {kc}/on_death", prepend=True)
	write_versioned_function("multiplayer/kill_cam/on_death", f"""
execute unless score #kc_window {ns}.data matches 1 run return run function {kc}/check_window

# Once the match is decided only its deciding kill is logged, #kc_final going from 1 to 2 (see multiplayer/request_end).
execute if score #mp_end_tick {ns}.data matches 1.. unless score #kc_final {ns}.data matches 1 run return fail
execute if score #kc_final {ns}.data matches 1 run scoreboard players set #kc_final {ns}.data 2

data modify storage {ns}:kill_cam deaths append value {{}}
execute store result storage {ns}:kill_cam deaths[-1].t int 1 run scoreboard players get #total_tick {ns}.data
execute store result storage {ns}:kill_cam deaths[-1].victim int 1 run scoreboard players get @s bs.id
execute as @a[tag={ns}.temp_killer,limit=1] store result storage {ns}:kill_cam deaths[-1].killer int 1 run scoreboard players get @s bs.id
""")

