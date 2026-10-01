""" The Search & Destroy round structure: opening a round, closing it, and who took the match. """
# Imports
from .....helpers import MGS_TAG
from ...base import GameModeVariant
from ..round_xp import RoundXp

# Constants
ROUND_TICKS: int = 3000
""" 2:30 to take the bomb across the map and plant it, the classic CoD round length.
Longer than a Counter-Strike round because the attackers start by walking to the bomb, not by buying. """
WIN_ROUNDS: int = 4
""" Round wins needed to take the match, so a match lasts between 4 and 7 rounds.
There is deliberately no cap on the round number: "first to 4" is the CoD rule, and a 3-3 match has to
play a seventh round to produce a winner. """
ROUNDS_PER_HALF: int = 3
""" Rounds a side spends attacking before the swap. """
HALFTIME_ROUND: int = ROUNDS_PER_HALF + 1
""" The round the sides swap on, i.e. the first round of the second half. """


# Classes
class SndRounds:
	""" Round lifecycle for Search & Destroy. """

	# Functions
	@staticmethod
	def write(variant: GameModeVariant) -> None:
		""" Write `start_round`, `attackers_win`, `defenders_win` and `next_round`. """
		ns, version = variant.ns, variant.version

		variant.sub("start_round", f"""
# A scheduled call may fire after the game ended.
execute if data storage {ns}:multiplayer game{{state:"lobby"}} run return fail
execute if data storage {ns}:multiplayer game{{state:"ended"}} run return fail

tellraw @a [{MGS_TAG},{{"text":"Round ","color":"gold"}},{{"score":{{"name":"#snd_round","objective":"{ns}.data"}},"color":"yellow"}}]

execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" attacks | "}},{{"text":"Blue","color":"blue"}},{{"text":" defends"}}]
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" attacks | "}},{{"text":"Red","color":"red"}},{{"text":" defends"}}]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

scoreboard players set #snd_bomb_state {ns}.data 0
scoreboard players set #snd_bomb_timer {ns}.data 0
scoreboard players set #snd_plant_progress {ns}.data 0
scoreboard players set #snd_defuse_progress {ns}.data 0

# The HUD clock too, so the 3 s gap already shows 2:30.
scoreboard players set #snd_round_timer {ns}.data {ROUND_TICKS}
scoreboard players set #mp_timer {ns}.data {ROUND_TICKS}

# S&D deaths skip the respawn countdown.
execute as @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator]

tag @a[scores={{{ns}.mp.team=1..2}},gamemode=!spectator] add {ns}.snd_alive

execute as @a[scores={{{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute as @a[scores={{{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
execute as @a[scores={{{ns}.mp.team=1..2}}] at @s run function {ns}:v{version}/multiplayer/apply_class

# One bomb per round, held by nobody: collecting it gives the defenders time to set up, unlike a Counter-Strike round.
tag @a remove {ns}.snd_carrier
kill @e[tag={ns}.snd_loose]
kill @e[tag={ns}.snd_carrier_label]
execute if score #snd_attackers {ns}.data matches 1 at @e[tag={ns}.spawn_red,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb
execute if score #snd_attackers {ns}.data matches 2 at @e[tag={ns}.spawn_blue,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb

# A map with only general spawns would otherwise start the round with no bomb.
execute unless entity @e[tag={ns}.snd_loose_at] at @e[tag={ns}.spawn_point,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb

# Last, once everyone is tagged and placed: until then the tick judges nothing, so the gap is never read as a wipe.
scoreboard players set #snd_round_active {ns}.data 1
""")

		variant.sub("attackers_win", f"""
# Closes the round once: several end conditions can land on the same tick and each calls here.
execute unless score #snd_round_active {ns}.data matches 1 run return fail
scoreboard players set #snd_round_active {ns}.data 0

execute if score #snd_attackers {ns}.data matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 2 run scoreboard players add #blue {ns}.mp.team 1
{RoundXp.result_lines(ns, "#snd_attackers", attackers_won=True, note="(Attackers) win the round!")}
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/snd/next_round
""")

		variant.sub("defenders_win", f"""
# Same single-shot guard: the defuse takes this path, and the wiped-looking alive tags would be judged again each tick.
execute unless score #snd_round_active {ns}.data matches 1 run return fail
scoreboard players set #snd_round_active {ns}.data 0

execute if score #snd_attackers {ns}.data matches 1 run scoreboard players add #blue {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 2 run scoreboard players add #red {ns}.mp.team 1
{RoundXp.result_lines(ns, "#snd_attackers", attackers_won=False, note="(Defenders) win the round!")}
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/snd/next_round
""")

		variant.sub("next_round", f"""
# The win function already cleared #snd_round_active, so the cleared snd_alive tags are not read as a wipe.
# The HUD clock resets here too: the tick does not drive it between rounds.
scoreboard players set #mp_timer {ns}.data {ROUND_TICKS}
kill @e[tag={ns}.snd_bomb]
kill @e[tag={ns}.snd_bomb_vis]
kill @e[tag={ns}.snd_bomb_hud]
kill @e[tag={ns}.snd_loose]
kill @e[tag={ns}.snd_carrier_label]
tag @a remove {ns}.snd_carrier
tag @a remove {ns}.snd_alive

# Threshold set in setup, also read by the sidebar.
execute if score #red {ns}.mp.team >= #snd_win_threshold {ns}.data run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #snd_win_threshold {ns}.data run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}

# Sides swap at halftime.
scoreboard players add #snd_round {ns}.data 1
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} if score #snd_attackers {ns}.data matches 1 run scoreboard players set #snd_attackers {ns}.data 2
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} if score #snd_attackers {ns}.data matches 2 run scoreboard players set #snd_attackers {ns}.data 1
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} run tellraw @a [{MGS_TAG},{{"text":"⚔ ","color":"white"}},{{"text":"Sides swapped!","color":"gold"}}]
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} run playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
# 3 s later.
schedule function {ns}:v{version}/multiplayer/gamemodes/snd/start_round 60t
""")

