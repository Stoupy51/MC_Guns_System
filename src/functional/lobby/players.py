""" Players around the queues: joining one, going back to the lobby, and logging back in. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...config.catalogs import TRIG_LOBBY_LEAVE
from ..helpers import MGS_TAG
from .queues import AWAY_SECONDS, Queue, queues


# Functions
def write_queue_players(queue: Queue) -> None:
	""" Write how a player joins and leaves one queue, and its check of every second. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	mode, p, q = queue.mode, queue.prefix, queue.queue_id
	path: str = f"{ns}:v{version}/lobby/{mode}"
	members: str = queue.members
	running: str = f'unless data storage {ns}:{mode} game{{state:"lobby"}}'

	write_versioned_function(f"lobby/{mode}/join", f"""
execute unless score #public_lobby {ns}.config matches 1 run return fail
execute if score @s {ns}.lobby.queue matches {q} run return run tellraw @s [{MGS_TAG},{{"text":"You are already in the {queue.label} queue.","color":"yellow"}}]

function {ns}:v{version}/lobby/leave_games
scoreboard players set @s {ns}.lobby.queue {q}
scoreboard players set @s {ns}.lobby.choice 0
scoreboard players set @s {ns}.lobby.vote 0
tellraw @s [{MGS_TAG},{{"text":"You joined the {queue.label} queue.","color":"green"}}]
execute if score #lv_{p}_round {ns}.data matches 1.. run function {path}/message
""")

	## Run as a player of this mode's game. The last one out ends it, so the queue can vote again.
	write_versioned_function(f"lobby/{mode}/leave", f"""
{queue.leave_lines.strip()}
tellraw @a[scores={{{queue.in_game}=1}}] [{MGS_TAG},{{"selector":"@s"}},{{"text":" went back to the lobby.","color":"gray"}}]
execute unless entity @a[scores={{{queue.in_game}=1}}] {running} run function {ns}:v{version}/{mode}/stop
""")

	late_joins: str = "\n".join(
		f'execute if data storage {ns}:{mode} game{{state:"{state}"}} as {members} unless score @s {queue.in_game} matches 1 run function {ns}:v{version}/{mode}/join_game'
		for state in queue.joinable_states
	)
	write_versioned_function(f"lobby/{mode}/second", f"""
execute store result score #lv_{p}_count {ns}.data if entity {members}
{late_joins}

execute if score #lv_{p}_round {ns}.data matches 1.. unless score #lv_{p}_count {ns}.data matches {queue.min_players}.. run function {path}/cancel_vote
execute unless score #lv_{p}_round {ns}.data matches 1.. if score #lv_{p}_count {ns}.data matches {queue.min_players}.. if data storage {ns}:{mode} game{{state:"lobby"}} run function {path}/open_vote
execute if score #lv_{p}_round {ns}.data matches 1.. run function {path}/vote_second
execute unless score #lv_{p}_round {ns}.data matches 1.. unless score #lv_{p}_count {ns}.data matches {queue.min_players}.. if data storage {ns}:{mode} game{{state:"lobby"}} run title {members} actionbar [{{"text":"Waiting for players: ","color":"aqua"}},{{"score":{{"name":"#lv_{p}_count","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{queue.min_players}","color":"yellow"}}]

# A game nobody is online in waits {AWAY_SECONDS // 60} minutes for them, then frees the mode.
execute unless entity @a[scores={{{queue.in_game}=1}}] {running} run scoreboard players add #lv_{p}_empty {ns}.data 1
execute if entity @a[scores={{{queue.in_game}=1}}] run scoreboard players set #lv_{p}_empty {ns}.data 0
execute if data storage {ns}:{mode} game{{state:"lobby"}} run scoreboard players set #lv_{p}_empty {ns}.data 0
execute if score #lv_{p}_empty {ns}.data matches {AWAY_SECONDS}.. run function {ns}:v{version}/{mode}/stop
""")


def write_lobby_players() -> None:
	""" Write the lobby clock, the login check, the way back to the lobby and its chat and menu buttons. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	path: str = f"{ns}:v{version}/lobby"
	all_queues: list[Queue] = queues()

	write_versioned_function("lobby/tick", "\n".join((
		*(f"execute if score #lv_{queue.prefix}_round {ns}.data matches 1.. run function {path}/{queue.mode}/vote_tick" for queue in all_queues),
		f"scoreboard players add #lv_tick {ns}.data 1",
		f"execute if score #lv_tick {ns}.data matches 20.. run function {path}/second",
	)))

	## Everyone online gets the current second, so a player who does not have it has just logged in.
	## First in the player tick: the modes' own rejoin checks then find the player already sorted out.
	write_versioned_function("player/tick", f"execute if score #public_lobby {ns}.config matches 1 unless score @s {ns}.lobby.seen = #now {ns}.lobby.seen run function {path}/login", prepend=True)
	write_versioned_function("lobby/second", "\n".join((
		f"scoreboard players set #lv_tick {ns}.data 0",
		f"scoreboard players add #now {ns}.lobby.seen 1",
		f"scoreboard players operation @a {ns}.lobby.seen = #now {ns}.lobby.seen",
		"",
		*(f"function {path}/{queue.mode}/second" for queue in all_queues),
	)))

	playing: str = "\n".join(
		f'execute if score @s {queue.in_game} matches 1 unless data storage {ns}:{queue.mode} game{{state:"lobby"}} run scoreboard players set #lv_playing {ns}.data 1'
		for queue in all_queues
	)
	write_versioned_function("lobby/login", f"""
scoreboard players operation #lv_away {ns}.data = #now {ns}.lobby.seen
scoreboard players operation #lv_away {ns}.data -= @s {ns}.lobby.seen
execute unless score @s {ns}.lobby.seen matches -2147483648.. run scoreboard players set #lv_away {ns}.data {AWAY_SECONDS + 1}
scoreboard players operation @s {ns}.lobby.seen = #now {ns}.lobby.seen

scoreboard players set #lv_playing {ns}.data 0
{playing}
execute if score #lv_playing {ns}.data matches 1 if score #lv_away {ns}.data matches ..{AWAY_SECONDS} run return 0

# Away too long: out of the queue too. Back from a game that ended while away: still queued.
execute if score #lv_away {ns}.data matches {AWAY_SECONDS + 1}.. run scoreboard players set @s {ns}.lobby.queue 0
function {path}/leave_games
execute if score #lv_in_game {ns}.data matches 0 run function {path}/return
""")

	in_game_flags: str = "\n".join(f"execute if score @s {queue.in_game} matches 1 run scoreboard players set #lv_in_game {ns}.data 1" for queue in all_queues)
	leaves: str = "\n".join(f"execute if score @s {queue.in_game} matches 1 run function {path}/{queue.mode}/leave" for queue in all_queues)
	## #lv_in_game tells whether a game's own reset already sent the player to the lobby.
	write_versioned_function("lobby/leave_games", f"""
scoreboard players set #lv_in_game {ns}.data 0
{in_game_flags}
{leaves}
scoreboard players set @s {ns}.lobby.choice 0
""")

	write_versioned_function("lobby/send_home", f"""
execute unless score #public_lobby {ns}.config matches 1 run return fail
scoreboard players set @s {ns}.lobby.queue 0
function {path}/leave_games
execute if score #lv_in_game {ns}.data matches 0 run function {path}/return
""")

	## Every game's reset sends its players through lobby/return.
	write_versioned_function("lobby/return", f"execute if score #public_lobby {ns}.config matches 1 if data storage {ns}:config lobby.dimension run function {path}/arrive")
	write_versioned_function("lobby/arrive", f"""
clear @s[gamemode=!creative]
effect clear @s
function {ns}:v{version}/player/fx_reset
function {path}/welcome
""")

	def mode_button(queue: Queue) -> str:
		return (
			f'{{"text":"","color":"{queue.color}",'
			f'"click_event":{{"action":"run_command","command":"/trigger {ns}.player.config set {TRIG_LOBBY_LEAVE + queue.queue_id}"}},'
			f'"hover_event":{{"action":"show_text","value":"Join the {queue.label} queue"}},'
			f'"extra":["[{queue.emoji} ",{{"text":"{queue.label}"}}," ",{{"score":{{"name":"#lv_{queue.prefix}_count","objective":"{ns}.data"}}}},"]"]}}'
		)
	leave_button: str = (
		f'{{"text":"","color":"yellow",'
		f'"click_event":{{"action":"run_command","command":"/trigger {ns}.player.config set {TRIG_LOBBY_LEAVE}"}},'
		f'"extra":["[🏠 ",{{"text":"Leave the queue"}},"]"]}}'
	)
	counts: str = "\n".join(f"execute store result score #lv_{queue.prefix}_count {ns}.data if entity {queue.members}" for queue in all_queues)
	write_versioned_function("lobby/welcome", f"""
{counts}
tellraw @s ["",{MGS_TAG},{{"text":"Play: ","color":"gray"}},{'," ",'.join(mode_button(queue) for queue in all_queues)}]
execute if score @s {ns}.lobby.queue matches 1.. run tellraw @s ["",{MGS_TAG},{{"text":"You stay in your queue for the next game. ","color":"gray"}},{leave_button}]
tellraw @s ["",{MGS_TAG},{{"text":"Menu, class and stats: ","color":"gray"}},{{"keybind":"key.quickActions","color":"yellow"}}]
""")

	## Appended to the Player Settings dialog being built in mgs:temp dialog.
	buttons: str = "\n".join(
		f'execute unless score @s {ns}.lobby.queue matches {queue.queue_id} run data modify storage {ns}:temp dialog.actions append value '
		f'{{label:["","{queue.emoji} ",{{text:"Play {queue.label}",color:"{queue.color}",bold:true}}],tooltip:{{text:"Join the {queue.label} queue, vote, then play"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_LOBBY_LEAVE + queue.queue_id}"}}}}'
		for queue in all_queues
	)
	write_versioned_function("lobby/menu_buttons", f"""
{buttons}
data modify storage {ns}:temp dialog.actions append value {{label:["","🏠 ",{{text:"Back to Lobby",color:"yellow",bold:true}}],tooltip:{{text:"Leave your queue and your game"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_LOBBY_LEAVE}"}}}}
""")

