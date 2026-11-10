""" Ending a game and the ranked end-of-match stats. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers.lifecycle import GameLifecycle
from ...helpers.ranked import RankedStats
from ...helpers.text import Text
from ..gamemodes.dispatch import gm_dispatch


# Functions
def write_multiplayer_stop() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## The line ends with the match XP, including the win or loss bonus that multiplayer/xp/on_game_end (in the on_game_end tag) adds first.
	mp_stat_line: str = (
		f'tellraw @a[scores={{{ns}.mp.in_game=1}}] ["","  ",{Text.player(ns, "@s")},{{"text":" ➤ ","color":"dark_gray"}},'
		f'{{"score":{{"name":"@s","objective":"{ns}.mp.kills"}},"color":"green"}},'
		'{"text":" kills","color":"gray"},{"text":" · ","color":"dark_gray"},'
		f'{{"score":{{"name":"@s","objective":"{ns}.mp.deaths"}},"color":"red"}},'
		'{"text":" deaths","color":"gray"},{"text":" · ","color":"dark_gray"},'
		f'{{"text":"+","color":"gold"}},{{"score":{{"name":"@s","objective":"{ns}.mp.xp_session"}},"color":"gold"}},'
		'{"text":" XP","color":"gold"}]'
	)
	mp_ranked_stats: str = RankedStats.write_ranked_stats_functions(
		ns, version, "multiplayer/announce_stats", "mp.in_game", "mp.kills", mp_stat_line
	)

	## Run by every win path once it has announced. A win path can run inside the kill signal, halfway through the victim's simulate_death,
	## so multiplayer/end waits for the next game_tick: the deciding kill pays its XP and its victim is reset with everyone else.
	write_versioned_function("multiplayer/request_end", f"""
scoreboard players operation #mp_end_tick {ns}.data = #total_tick {ns}.data

# Inside a kill, the death logged next is the final kill (see kill_cam/on_death).
execute if entity @a[tag={ns}.temp_victim] run scoreboard players set #kc_final {ns}.data 1
""")

	## Run by game_tick once an end is requested: the kill cam when a player kill ended the match, then stop.
	write_versioned_function("multiplayer/end", f"""
data modify storage {ns}:multiplayer game.state set value "ended"
execute unless function {ns}:v{version}/multiplayer/kill_cam/start run function {ns}:v{version}/multiplayer/stop
""")

	write_versioned_function("multiplayer/stop", f"""
function {ns}:v{version}/multiplayer/kill_cam/cleanup

# Map scripts only run during a match, so the leave script comes before the lobby state.
execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/shared/maps/call_script_at_base {{mode:"multiplayer",script:"leave"}}

data modify storage {ns}:multiplayer game.state set value "lobby"
scoreboard players set #mp_end_tick {ns}.data 0
schedule clear {ns}:v{version}/multiplayer/end_prep

# Mode cleanup before the multiplayer_entity sweep: S&D restores its sites with `execute at @e[tag=snd_obj] run fill`,
# which needs the markers to still exist.
{gm_dispatch(ns, version, "cleanup")}
kill @e[tag={ns}.multiplayer_entity]
function #{ns}:multiplayer/on_game_end

{GameLifecycle.regen_disable_lines(ns, f"@a[scores={{{ns}.mp.in_game=1}}]")}

# Team scores mean nothing in FFA; player_wins announces the winner.
tellraw @a[scores={{{ns}.mp.in_game=1}}] ["","⚔ ",[{{"text":"","color":"gold","bold":true}},{{"text":"Game Over"}},"! "]]
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} run tellraw @a[scores={{{ns}.mp.in_game=1}}] ["",{{"text":"Red","color":"red"}},{{"text":": "}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}}}}," | ",{{"text":"Blue","color":"blue"}},{{"text":": "}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}}}}]

# Best first; the bare selector shows the team colour, which still applies until reset_player below.
{mp_ranked_stats}

scoreboard objectives setdisplay sidebar.team.red
scoreboard objectives setdisplay sidebar.team.blue
scoreboard objectives setdisplay sidebar.team.gold
scoreboard objectives remove {ns}.sidebar
scoreboard objectives setdisplay list

execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/multiplayer/reset_player
scoreboard players set #mp_has_boundary {ns}.data 0
""")

	## Run as each match player by stop, and at login for one who left as a spectator (dead, or watching the kill cam) and missed it.
	write_versioned_function("multiplayer/reset_player", f"""
attribute @s minecraft:movement_speed base reset
attribute @s minecraft:jump_strength base reset
attribute @s minecraft:waypoint_receive_range base reset
effect clear @s darkness
effect clear @s blindness
effect clear @s night_vision
gamemode adventure @s[gamemode=spectator]

# The deciding kill's victim still shows its respawn countdown.
title @s clear

team leave @s
function {ns}:v{version}/lobby/return
scoreboard players set @s {ns}.mp.team 0
scoreboard players set @s {ns}.mp.spectate_timer 0
scoreboard players set @s {ns}.mp.in_game 0
tag @s remove {ns}.give_class_menu
tag @s remove {ns}.kc_viewer
""")
	write_versioned_function("stats/login", f"""
execute if entity @s[gamemode=spectator,scores={{{ns}.mp.in_game=1}}] if data storage {ns}:multiplayer game{{state:"lobby"}} run function {ns}:v{version}/multiplayer/reset_player
""")

