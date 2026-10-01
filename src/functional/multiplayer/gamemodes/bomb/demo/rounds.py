""" Demolition's round structure: two halves, then a tie-break round when they split.

Each side attacks once, and wins its half only by destroying **both** sites before the clock runs out.
Anything less is a defensive hold, so every round awards exactly one point and regulation ends 2-0 or 1-1.

A 1-1 goes to a third round played like the first two: one attacking side, one defending side, both sites to destroy.
Per the [CoD Wiki](https://callofduty.fandom.com/wiki/Demolition_(Game_Mode)), the team with the most kills **defends** it.
That favours maps easier to hold than to take, and it is the rule as written.
A kill tie leaves Red attacking, the same fallback as `BombSites.write_side_picking`.
"""
# Imports
from .....helpers import MGS_TAG
from ...base import GameModeVariant
from ..round_xp import RoundXp
from .sites_state import DemoSites

# Constants
ROUND_TICKS: int = 3600
""" 3:00 per round, longer than Search & Destroy: two sites to destroy instead of one plant, and deaths respawn.
Not a sourced value, tune it in game.
"""
ROUNDS_PER_MATCH: int = 2
""" Rounds in regulation, one attack per side. """
TIEBREAK_ROUND: int = ROUNDS_PER_MATCH + 1
""" Round number the decider runs as, played only when regulation ends level. """


# Classes
class DemoRounds:
	""" Opening and closing Demolition rounds, and choosing the sides of the tie-break round. """

	# Functions
	@staticmethod
	def write(variant: GameModeVariant) -> None:
		""" Write `start_round`, the two win functions, `next_round`, `swap_sides` and `pick_tiebreak_sides`. """
		ns, version = variant.ns, variant.version

		variant.sub("start_round", f"""
# A scheduled call may fire after the game ended.
execute if data storage {ns}:multiplayer game{{state:"lobby"}} run return fail
execute if data storage {ns}:multiplayer game{{state:"ended"}} run return fail

# The decider is announced as such but plays like any round.
tellraw @a [{MGS_TAG},{{"text":"Round ","color":"gold"}},{{"score":{{"name":"#demo_round","objective":"{ns}.data"}},"color":"yellow"}}]
execute if score #demo_round {ns}.data matches {TIEBREAK_ROUND}.. run tellraw @a [{MGS_TAG},{{"text":"⚡ ","color":"white"}},{{"text":"TIE-BREAK ROUND: most kills defends!","color":"gold","bold":true}}]
execute if score #demo_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" attacks both sites | "}},{{"text":"Blue","color":"blue"}},{{"text":" defends"}}]
execute if score #demo_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" attacks both sites | "}},{{"text":"Red","color":"red"}},{{"text":" defends"}}]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

{DemoSites.reset_lines(variant)}

# Same length every round; it stops while a bomb is down, hence this mode owns #mp_timer.
scoreboard players set #demo_timer {ns}.data {ROUND_TICKS}
scoreboard players operation #mp_timer {ns}.data = #demo_timer {ns}.data

# Every attacker carries a bomb on every respawn, so no carry, drop or pickup machinery: the tag is the bomb.
tag @a remove {ns}.demo_atk
execute if score #demo_attackers {ns}.data matches 1 run tag @a[scores={{{ns}.mp.team=1}}] add {ns}.demo_atk
execute if score #demo_attackers {ns}.data matches 2 run tag @a[scores={{{ns}.mp.team=2}}] add {ns}.demo_atk

# Spectators are pulled out and their countdown cleared, so a death from the last round cannot respawn them mid-round.
execute as @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator]
scoreboard players set @a[scores={{{ns}.mp.team=1..2}}] {ns}.mp.spectate_timer 0
execute as @a[scores={{{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute as @a[scores={{{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
execute as @a[scores={{{ns}.mp.team=1..2}}] at @s run function {ns}:v{version}/multiplayer/apply_class

# Last, once the sites are intact and everyone is placed.
scoreboard players set #demo_round_active {ns}.data 1
""")

		## The attacking side destroyed everything.
		variant.sub("attackers_win", f"""
# Closes the round once: the last destruction and a clock expiry can land on the same tick.
execute unless score #demo_round_active {ns}.data matches 1 run return fail
scoreboard players set #demo_round_active {ns}.data 0

execute if score #demo_attackers {ns}.data matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score #demo_attackers {ns}.data matches 2 run scoreboard players add #blue {ns}.mp.team 1
{RoundXp.result_lines(ns, "#demo_attackers", attackers_won=True, note="destroyed both sites!")}
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/demo/next_round
""")

		## The clock ran out with something still standing.
		variant.sub("defenders_win", f"""
execute unless score #demo_round_active {ns}.data matches 1 run return fail
scoreboard players set #demo_round_active {ns}.data 0

execute if score #demo_attackers {ns}.data matches 1 run scoreboard players add #blue {ns}.mp.team 1
execute if score #demo_attackers {ns}.data matches 2 run scoreboard players add #red {ns}.mp.team 1
{RoundXp.result_lines(ns, "#demo_attackers", attackers_won=False, note="held the sites!")}
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/demo/next_round
""")

		variant.sub("next_round", f"""
# Also reset here: the tick does not drive #mp_timer between rounds.
scoreboard players set #mp_timer {ns}.data {ROUND_TICKS}
tag @a remove {ns}.demo_atk

scoreboard players add #demo_round {ns}.data 1

# End of the first half: swap sides.
execute if score #demo_round {ns}.data matches {ROUNDS_PER_MATCH} run function {ns}:v{version}/multiplayer/gamemodes/demo/swap_sides
execute if score #demo_round {ns}.data matches {ROUNDS_PER_MATCH} run return run schedule function {ns}:v{version}/multiplayer/gamemodes/demo/start_round 60t

# Each round awards one point, so this ends the match on 2-0, or on 2-1 after the decider; only 1-1 falls through.
execute if score #red {ns}.mp.team > #blue {ns}.mp.team run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team > #red {ns}.mp.team run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}

# Still level: the decider, its defending side chosen by kills.
execute if score #demo_round {ns}.data matches {TIEBREAK_ROUND} run function {ns}:v{version}/multiplayer/gamemodes/demo/pick_tiebreak_sides
execute if score #demo_round {ns}.data matches {TIEBREAK_ROUND} run return run schedule function {ns}:v{version}/multiplayer/gamemodes/demo/start_round 60t

# Unreachable: every round awards a point.
function {ns}:v{version}/multiplayer/game_draw
""")

		## Halftime: the only place sides are swapped rather than computed.
		variant.sub("swap_sides", f"""
execute if score #demo_attackers {ns}.data matches 1 run scoreboard players set #demo_attackers {ns}.data 2
execute unless score #demo_attackers {ns}.data matches 2 run scoreboard players set #demo_attackers {ns}.data 1
tellraw @a [{MGS_TAG},{{"text":"⚔ ","color":"white"}},{{"text":"Sides swapped!","color":"gold"}}]
playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
""")

		## The team with most kills defends, so this replaces swap_sides and can give one side two attacks in a row.
		## Announced in full, since it decides the match and nobody sees the tally.
		variant.sub("pick_tiebreak_sides", f"""
# mp.kills is per player and only zeroed by multiplayer/start.
scoreboard players set #demo_kills_red {ns}.data 0
scoreboard players set #demo_kills_blue {ns}.data 0
execute as @a[scores={{{ns}.mp.team=1}}] run scoreboard players operation #demo_kills_red {ns}.data += @s {ns}.mp.kills
execute as @a[scores={{{ns}.mp.team=2}}] run scoreboard players operation #demo_kills_blue {ns}.data += @s {ns}.mp.kills

# A tie leaves Red attacking, like the side-picking fallback.
scoreboard players set #demo_attackers {ns}.data 1
execute if score #demo_kills_red {ns}.data > #demo_kills_blue {ns}.data run scoreboard players set #demo_attackers {ns}.data 2

# start_round announces the defenders, so only the tie case is spelled out.
tellraw @a [{MGS_TAG},{{"text":"Kills: ","color":"gray"}},{{"text":"Red ","color":"red"}},{{"score":{{"name":"#demo_kills_red","objective":"{ns}.data"}},"color":"white"}},{{"text":" - ","color":"gray"}},{{"text":"Blue ","color":"blue"}},{{"score":{{"name":"#demo_kills_blue","objective":"{ns}.data"}},"color":"white"}}]
execute if score #demo_kills_red {ns}.data = #demo_kills_blue {ns}.data run tellraw @a [{MGS_TAG},{{"text":"Kills are level, so ","color":"yellow"}},{{"text":"Blue","color":"blue"}},{{"text":" defends.","color":"yellow"}}]
""")

