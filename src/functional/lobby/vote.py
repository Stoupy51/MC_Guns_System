""" The vote of each queue, from the Switch's: clickable options in chat, a countdown from the first vote, the most voted option wins.

A click runs `/trigger mgs.lobby.vote set <queue id * 10 + slot>`, so a click on another queue's message never counts here.
The slot a player picked is kept in `mgs.lobby.choice`, and only the players of the queue are counted.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from .queues import FIRST_ROUND_TICKS, MAX_SLOTS, PRESETS, SECOND_ROUND_TICKS, SPEED_UP_TICKS, Queue

# Constants
SLOTS: range = range(1, MAX_SLOTS + 1)


# Functions
def write_vote_helpers() -> None:
	""" Write the option lists shared by the three queues, kept in `mgs:lobby <mode>.options`. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	path: str = f"{ns}:v{version}/lobby/vote"

	## Macro: mode, and field, a list a map needs non-empty to be offered.
	write_versioned_function("lobby/vote/collect_maps", f"""
$data modify storage {ns}:temp _lv_iter set from storage {ns}:maps $(mode)
data modify storage {ns}:temp _lv_opts set value []
$execute if data storage {ns}:temp _lv_iter[0] run function {path}/collect_map {{field:"$(field)"}}
function {path}/trim_maps
$data modify storage {ns}:lobby $(mode).options set from storage {ns}:temp _lv_opts
""")

	write_versioned_function("lobby/vote/collect_map", f"""
$execute if data storage {ns}:temp _lv_iter[0].$(field)[0] run function {path}/add_map
data remove storage {ns}:temp _lv_iter[0]
$execute if data storage {ns}:temp _lv_iter[0] run function {path}/collect_map {{field:"$(field)"}}
""")

	write_versioned_function("lobby/vote/add_map", f"""
data modify storage {ns}:temp _lv_opt set value {{label:{{text:"",color:"aqua"}},hover:{{text:""}}}}
data modify storage {ns}:temp _lv_opt.label.text set from storage {ns}:temp _lv_iter[0].name
data modify storage {ns}:temp _lv_opt.hover.text set from storage {ns}:temp _lv_iter[0].description
data modify storage {ns}:temp _lv_opt.map_id set from storage {ns}:temp _lv_iter[0].id
data modify storage {ns}:temp _lv_opts append from storage {ns}:temp _lv_opt
""")

	## Random maps drop out until the Random slot fits.
	write_versioned_function("lobby/vote/trim_maps", f"""
execute store result score #lv_n {ns}.data if data storage {ns}:temp _lv_opts[]
execute if score #lv_n {ns}.data matches ..{MAX_SLOTS - 1} run return 0
scoreboard players remove #lv_n {ns}.data 1
execute store result storage {ns}:temp _lv_pick.max int 1 run scoreboard players get #lv_n {ns}.data
function {path}/drop_random with storage {ns}:temp _lv_pick
function {path}/trim_maps
""")
	write_versioned_function("lobby/vote/drop_random", f"""
$execute store result storage {ns}:temp _lv_pick.i int 1 run random value 0..$(max)
function {path}/drop_at with storage {ns}:temp _lv_pick
""")
	write_versioned_function("lobby/vote/drop_at", f"$data remove storage {ns}:temp _lv_opts[$(i)]")

	## Leaves the option count in #lv_slots.
	write_versioned_function("lobby/vote/finish_options", f"""
$execute store result score #lv_slots {ns}.data if data storage {ns}:lobby $(mode).options[]
$execute if score #lv_slots {ns}.data matches 2.. run data modify storage {ns}:lobby $(mode).options append value {{label:{{text:"Random",color:"light_purple"}},hover:{{text:"One of the options above, drawn at random"}},random:1b}}
$execute store result score #lv_slots {ns}.data if data storage {ns}:lobby $(mode).options[]
""")

	## Run with #lv_k holding the slot's votes. The draw only breaks ties, as one vote outweighs any draw.
	write_versioned_function("lobby/vote/weigh", f"""
scoreboard players operation #lv_k {ns}.data *= #100 {ns}.data
execute store result score #lv_r {ns}.data run random value 0..99
scoreboard players operation #lv_k {ns}.data += #lv_r {ns}.data
execute unless score #lv_k {ns}.data > #lv_best {ns}.data run return 0
scoreboard players operation #lv_best {ns}.data = #lv_k {ns}.data
$scoreboard players set #lv_win {ns}.data $(slot)
""")

	write_versioned_function("lobby/vote/pick_winner", f"$data modify storage {ns}:lobby $(mode).winner set from storage {ns}:lobby $(mode).options[$(i)]")
	write_versioned_function("lobby/vote/pick_random", f"""
$execute store result storage {ns}:temp _lv_pick.i int 1 run random value 0..$(max)
function {path}/pick_winner with storage {ns}:temp _lv_pick
""")


def write_queue_vote(queue: Queue) -> None:
	""" Write the vote of one queue: opening it, counting clicks, the countdown and launching the winner. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	mode, p, q = queue.mode, queue.prefix, queue.queue_id
	path: str = f"{ns}:v{version}/lobby/{mode}"
	members: str = queue.members
	is_multiplayer: bool = mode == "multiplayer"

	if is_multiplayer:
		options: str = f"data modify storage {ns}:lobby multiplayer.options set value []\n" + "".join(
			f"execute if score #lv_mp_count {ns}.data matches {preset.min_players}.. if data storage {ns}:maps multiplayer[].{preset.map_field}[0] "
			f"run data modify storage {ns}:lobby multiplayer.options append value {preset.option_snbt()}\n"
			for preset in PRESETS
		)
	else:
		options = f'function {ns}:v{version}/lobby/vote/collect_maps {{mode:"{mode}",field:"{queue.map_field}"}}'
	write_versioned_function(f"lobby/{mode}/open_vote", f"""
{options}
function {ns}:v{version}/lobby/vote/finish_options {{mode:"{mode}"}}
execute if score #lv_slots {ns}.data matches 0 run return run title {members} actionbar {{"text":"No {queue.label} map is ready to play.","color":"red"}}

scoreboard players operation #lv_{p}_slots {ns}.data = #lv_slots {ns}.data
scoreboard players set #lv_{p}_round {ns}.data 1
scoreboard players set #lv_{p}_timer {ns}.data {FIRST_ROUND_TICKS}
function {path}/begin_round
""")

	write_versioned_function(f"lobby/{mode}/begin_round", f"""
scoreboard players set {members} {ns}.lobby.choice 0
function {path}/count_votes
scoreboard players set #lv_{p}_dirty {ns}.data 0
execute as {members} at @s run playsound minecraft:block.note_block.pling ambient @s
execute as {members} run function {path}/message
""")

	counts: str = "\n".join(
		f"execute store result score #lv_{p}_vote_{i} {ns}.data if entity @a[scores={{{ns}.lobby.queue={q},{ns}.lobby.choice={i}}}]"
		for i in SLOTS
	)
	write_versioned_function(f"lobby/{mode}/count_votes", f"""
{counts}
execute store result score #lv_{p}_voters {ns}.data if entity @a[scores={{{ns}.lobby.queue={q},{ns}.lobby.choice=1..}}]
""")

	## The children inherit the click and the hover of the bracket.
	def option_line(i: int, *, voted: bool) -> str:
		mark: str = ',{"text":" ✔","color":"green"}' if voted else ""
		return (
			f'["  ",{{"text":"[","color":"yellow",'
			f'"click_event":{{"action":"run_command","command":"/trigger {ns}.lobby.vote set {q * 10 + i}"}},'
			f'"hover_event":{{"action":"show_text","value":{{"nbt":"{mode}.options[{i - 1}].hover","storage":"{ns}:lobby","interpret":true}}}},'
			f'"extra":[{{"nbt":"{mode}.options[{i - 1}].label","storage":"{ns}:lobby","interpret":true}},"] ",'
			f'{{"score":{{"name":"#lv_{p}_vote_{i}","objective":"{ns}.data"}},"color":"{"dark_aqua" if voted else "aqua"}"}}{mark}]}}]'
		)
	lines: str = "\n".join(
		f"execute if data storage {ns}:lobby {mode}.options[{i - 1}] {'if' if voted else 'unless'} score @s {ns}.lobby.choice matches {i} run tellraw @s {option_line(i, voted=voted)}"
		for i in SLOTS for voted in (False, True)
	)
	if is_multiplayer:
		header: str = f"""
execute if score #lv_mp_round {ns}.data matches 1 run tellraw @s ["\\n",{MGS_TAG},{{"text":"Vote for the next game mode:","color":"gold"}}]
execute if score #lv_mp_round {ns}.data matches 2 run tellraw @s ["\\n",{MGS_TAG},{{"text":"Vote for the map of ","color":"gold"}},{{"nbt":"multiplayer.preset.label","storage":"{ns}:lobby","interpret":true}},{{"text":":","color":"gold"}}]
"""
	else:
		header = f'tellraw @s ["\\n",{MGS_TAG},{{"text":"Vote for the next {queue.label} map:","color":"gold"}}]'
	write_versioned_function(f"lobby/{mode}/message", f"""
{header}
{lines}
""")

	## Each tick of a vote. The first round waits for a vote before counting down, the Multiplayer map round does not.
	write_versioned_function(f"lobby/{mode}/vote_tick", f"""
scoreboard players enable {members} {ns}.lobby.vote
execute as @a[scores={{{ns}.lobby.queue={q},{ns}.lobby.vote=1..}}] run function {path}/read_vote

execute if score #lv_{p}_round {ns}.data matches 1 if score #lv_{p}_voters {ns}.data matches 1.. run scoreboard players remove #lv_{p}_timer {ns}.data 1
execute if score #lv_{p}_round {ns}.data matches 2 run scoreboard players remove #lv_{p}_timer {ns}.data 1
execute if score #lv_{p}_timer {ns}.data matches {SPEED_UP_TICKS + 1}.. if score #lv_{p}_voters {ns}.data >= #lv_{p}_count {ns}.data run function {path}/speed_up
execute if score #lv_{p}_timer {ns}.data matches ..0 run function {path}/resolve
""")

	write_versioned_function(f"lobby/{mode}/read_vote", f"""
scoreboard players remove @s {ns}.lobby.vote {q * 10}
execute if score @s {ns}.lobby.vote matches 1.. if score @s {ns}.lobby.vote <= #lv_{p}_slots {ns}.data run scoreboard players operation @s {ns}.lobby.choice = @s {ns}.lobby.vote
scoreboard players set @s {ns}.lobby.vote 0
playsound minecraft:ui.button.click ambient @s

function {path}/count_votes
scoreboard players set #lv_{p}_dirty {ns}.data 1
""")

	write_versioned_function(f"lobby/{mode}/speed_up", f"""
scoreboard players set #lv_{p}_timer {ns}.data {SPEED_UP_TICKS}
execute as {members} at @s run playsound minecraft:entity.villager.celebrate ambient @s
tellraw {members} [{MGS_TAG},{{"text":"Everyone has voted, the vote ends in 5 seconds!","color":"aqua"}}]
""")

	## Once a second, so a burst of clicks sends one message: the new counts, and the countdown.
	write_versioned_function(f"lobby/{mode}/vote_second", f"""
function {path}/count_votes
execute if score #lv_{p}_dirty {ns}.data matches 1 as {members} run function {path}/message
scoreboard players set #lv_{p}_dirty {ns}.data 0

scoreboard players operation #lv_sec {ns}.data = #lv_{p}_timer {ns}.data
scoreboard players operation #lv_sec {ns}.data /= #20 {ns}.data
scoreboard players add #lv_sec {ns}.data 1
execute if score #lv_{p}_round {ns}.data matches 1 if score #lv_{p}_voters {ns}.data matches 0 run return run title {members} actionbar {{"text":"The countdown starts at the first vote.","color":"aqua"}}
title {members} actionbar [{{"text":"Vote ends in ","color":"aqua"}},{{"score":{{"name":"#lv_sec","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" s","color":"aqua"}}]
""")

	weighing: str = "\n".join(
		f"execute if score #lv_{p}_slots {ns}.data matches {i}.. run scoreboard players operation #lv_k {ns}.data = #lv_{p}_vote_{i} {ns}.data\n"
		f"execute if score #lv_{p}_slots {ns}.data matches {i}.. run function {ns}:v{version}/lobby/vote/weigh {{slot:{i}}}"
		for i in SLOTS
	)
	next_step: str = f"execute if score #lv_mp_round {ns}.data matches 1 run return run function {path}/map_round\n" if is_multiplayer else ""
	write_versioned_function(f"lobby/{mode}/resolve", f"""
scoreboard players set #lv_best {ns}.data -1
scoreboard players set #lv_win {ns}.data 1
{weighing}

data modify storage {ns}:temp _lv_pick set value {{mode:"{mode}"}}
scoreboard players remove #lv_win {ns}.data 1
execute store result storage {ns}:temp _lv_pick.i int 1 run scoreboard players get #lv_win {ns}.data
function {ns}:v{version}/lobby/vote/pick_winner with storage {ns}:temp _lv_pick

# Random is the last slot: it draws one of the slots before it.
scoreboard players operation #lv_n {ns}.data = #lv_{p}_slots {ns}.data
scoreboard players remove #lv_n {ns}.data 2
execute store result storage {ns}:temp _lv_pick.max int 1 run scoreboard players get #lv_n {ns}.data
execute if data storage {ns}:lobby {mode}.winner.random run function {ns}:v{version}/lobby/vote/pick_random with storage {ns}:temp _lv_pick

tellraw {members} [{MGS_TAG},{{"text":"Vote result: ","color":"gray"}},{{"nbt":"{mode}.winner.label","storage":"{ns}:lobby","interpret":true}}]
{next_step}function {path}/launch
""")

	if is_multiplayer:
		write_versioned_function("lobby/multiplayer/map_round", f"""
data modify storage {ns}:lobby multiplayer.preset set from storage {ns}:lobby multiplayer.winner
function {ns}:v{version}/lobby/vote/collect_maps with storage {ns}:lobby multiplayer.preset
function {ns}:v{version}/lobby/vote/finish_options {{mode:"multiplayer"}}
scoreboard players operation #lv_mp_slots {ns}.data = #lv_slots {ns}.data

# A single map needs no second vote.
execute if score #lv_mp_slots {ns}.data matches 1 run data modify storage {ns}:lobby multiplayer.winner set from storage {ns}:lobby multiplayer.options[0]
execute if score #lv_mp_slots {ns}.data matches 1 run return run function {path}/launch

scoreboard players set #lv_mp_round {ns}.data 2
scoreboard players set #lv_mp_timer {ns}.data {SECOND_ROUND_TICKS}
function {path}/begin_round
""")

	match_settings: str = "".join(
		f"data modify storage {ns}:multiplayer game.{key} set from storage {ns}:lobby multiplayer.preset.{key}\n"
		for key in ("gamemode", "score_limit", "time_limit")
	) if is_multiplayer else ""
	write_versioned_function(f"lobby/{mode}/launch", f"""
scoreboard players set #lv_{p}_round {ns}.data 0
{match_settings}data modify storage {ns}:{mode} game.map_id set from storage {ns}:lobby {mode}.winner.map_id

scoreboard players set {members} {queue.in_game} 1
execute as @r[scores={{{ns}.lobby.queue={q}}}] run function {ns}:v{version}/{mode}/start

# A refused start told its player why; the queue votes again.
execute if data storage {ns}:{mode} game{{state:"lobby"}} run scoreboard players set {members} {queue.in_game} 0
""")

	write_versioned_function(f"lobby/{mode}/cancel_vote", f"""
scoreboard players set #lv_{p}_round {ns}.data 0
scoreboard players set {members} {ns}.lobby.choice 0
tellraw {members} [{MGS_TAG},{{"text":"Not enough players left, the vote is cancelled.","color":"red"}}]
""")

