""" Ending a game and the ranked end-of-match stats. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers.lifecycle import GameLifecycle
from ...helpers.ranked import RankedStats
from ..gamemodes.dispatch import gm_dispatch


# Functions
def write_multiplayer_stop() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Game Stop
	mp_stat_line: str = (
		'tellraw @a ["","  ",{"selector":"@s"},{"text":" ➤ ","color":"dark_gray"},'
		f'{{"score":{{"name":"@s","objective":"{ns}.mp.kills"}},"color":"green"}},'
		'{"text":" kills","color":"gray"},{"text":" · ","color":"dark_gray"},'
		f'{{"score":{{"name":"@s","objective":"{ns}.mp.deaths"}},"color":"red"}},'
		'{"text":" deaths","color":"gray"}]'
	)
	mp_ranked_stats: str = RankedStats.write_ranked_stats_functions(
		ns, version, "multiplayer/announce_stats", "mp.in_game", "mp.kills", mp_stat_line
	)

	write_versioned_function("multiplayer/stop", f"""
# Various cleanup to go back to lobby
data modify storage {ns}:multiplayer game.state set value "lobby"
schedule clear {ns}:v{version}/multiplayer/end_prep
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:jump_strength base reset
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base reset
effect clear @a[scores={{{ns}.mp.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mp.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mp.in_game=1}}] night_vision
gamemode adventure @a[scores={{{ns}.mp.in_game=1}},gamemode=spectator]
kill @e[tag={ns}.gm_entity]
{gm_dispatch(ns, version, "cleanup")}
function #{ns}:multiplayer/on_game_end

{GameLifecycle.regen_disable_lines(ns)}

# Announce scores (team scores are meaningless in FFA — the winner is announced by player_wins)
tellraw @a ["","⚔ ",[{{"text":"","color":"gold","bold":true}},{{"text":"Game Over"}},"! "]]
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} run tellraw @a ["",{{"text":"Red","color":"red"}},{{"text":": "}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}}}}," | ",{{"text":"Blue","color":"blue"}},{{"text":": "}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}}}}]

# Per-player match stats, best first. The name is a bare selector component so it renders in the
# player's team colour; this runs before the team leave below, while that colour still applies.
{mp_ranked_stats}

# Remove sidebar and list displays and leave teams
scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.sidebar
scoreboard objectives setdisplay list
team leave @a[team={ns}.red]
team leave @a[team={ns}.blue]
team leave @a[team={ns}.ffa]

# Call map leave script for each in-game player (state is still active/preparing here)
execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/shared/maps/call_script_at_base {{script:"leave"}}

scoreboard players set @a {ns}.mp.in_game 0
scoreboard players set @a {ns}.mp.team 0
scoreboard players set @a {ns}.mp.spectate_timer 0
scoreboard players set #mp_has_boundary {ns}.data 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

