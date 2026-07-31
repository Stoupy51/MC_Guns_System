""" Demolition's round structure: two halves, then a tie-break round when they split.

Each side attacks exactly once. An attacking side wins its half only by destroying **both** sites before
the clock runs out, and anything less is a defensive hold, so every round awards exactly one point and
regulation always ends 2-0 or 1-1.

A 1-1 goes to a third round played exactly like the first two — one attacking side, one defending side,
both sites to destroy. Per the [CoD Wiki](https://callofduty.fandom.com/wiki/Demolition_(Game_Mode)) the
side that **defends** it is whichever team has the most kills.
That is knowingly an advantage on maps easier to hold than to take, and it is the rule as written.
A kill tie leaves Red attacking, the same fallback `BombSites.write_side_picking` uses.
"""
# ruff: noqa: E501
# Imports
from .....helpers import MGS_TAG
from ...base import GameModeVariant
from ..round_xp import RoundXp
from .sites_state import DemoSites

# Constants
ROUND_TICKS: int = 3600
""" 3:00 per round. Longer than a Search & Destroy round because the attackers have to destroy two sites
rather than plant one, and every death is a respawn rather than the end of their round.
NOT a sourced value — tune in game. """
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

		## Demolition: Start Round
		variant.sub("start_round", f"""
# Guard: only while the game is running (a scheduled call may fire after the game ended)
execute if data storage {ns}:multiplayer game{{state:"lobby"}} run return fail
execute if data storage {ns}:multiplayer game{{state:"ended"}} run return fail

# Announce round. The decider is announced as one, but plays like any other round.
tellraw @a [{MGS_TAG},{{"text":"────── Round ","color":"gold"}},{{"score":{{"name":"#demo_round","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" ──────","color":"gold"}}]
execute if score #demo_round {ns}.data matches {TIEBREAK_ROUND}.. run tellraw @a [{MGS_TAG},"⚡ ",{{"text":"TIE-BREAK ROUND — most kills defends!","color":"gold","bold":true}}]
execute if score #demo_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" attacks both sites | "}},{{"text":"Blue","color":"blue"}},{{"text":" defends"}}]
execute if score #demo_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" attacks both sites | "}},{{"text":"Red","color":"red"}},{{"text":" defends"}}]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Every site back to intact
{DemoSites.reset_lines(variant)}

# Clock, same length every round; it stops while a bomb is down, which is why this mode owns #mp_timer.
scoreboard players set #demo_timer {ns}.data {ROUND_TICKS}
scoreboard players operation #mp_timer {ns}.data = #demo_timer {ns}.data

# Who is carrying a bomb. Every attacker is, on every respawn, which is why Demolition needs none of the
# carry/drop/pickup machinery S&D has — the tag IS the bomb.
tag @a remove {ns}.demo_atk
execute if score #demo_attackers {ns}.data matches 1 run tag @a[scores={{{ns}.mp.team=1}}] add {ns}.demo_atk
execute if score #demo_attackers {ns}.data matches 2 run tag @a[scores={{{ns}.mp.team=2}}] add {ns}.demo_atk

# Everyone alive and back at their spawns. Mid-respawn spectators are pulled out of it and their countdown
# is cleared, so a death from the previous round cannot respawn them a second time mid-round.
execute as @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator]
scoreboard players set @a[scores={{{ns}.mp.team=1..2}}] {ns}.mp.spectate_timer 0
execute as @a[scores={{{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute as @a[scores={{{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
execute as @a[scores={{{ns}.mp.team=1..2}}] at @s run function {ns}:v{version}/multiplayer/apply_class

# Open the round LAST, once the sites are intact and everyone is placed
scoreboard players set #demo_round_active {ns}.data 1
""")

		## Demolition: the attacking side destroyed everything
		variant.sub("attackers_win", f"""
# Close the round exactly once: the last site's destruction and a clock expiry can land on the same tick
execute unless score #demo_round_active {ns}.data matches 1 run return fail
scoreboard players set #demo_round_active {ns}.data 0

execute if score #demo_attackers {ns}.data matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score #demo_attackers {ns}.data matches 2 run scoreboard players add #blue {ns}.mp.team 1
{RoundXp.result_lines(ns, "#demo_attackers", attackers_won=True, note="destroyed both sites!")}
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/demo/next_round
""")

		## Demolition: the clock ran out with something still standing
		variant.sub("defenders_win", f"""
execute unless score #demo_round_active {ns}.data matches 1 run return fail
scoreboard players set #demo_round_active {ns}.data 0

execute if score #demo_attackers {ns}.data matches 1 run scoreboard players add #blue {ns}.mp.team 1
execute if score #demo_attackers {ns}.data matches 2 run scoreboard players add #red {ns}.mp.team 1
{RoundXp.result_lines(ns, "#demo_attackers", attackers_won=False, note="held the sites!")}
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/demo/next_round
""")

		## Demolition: what happens after a round closes
		variant.sub("next_round", f"""
# The clock is reset here as well as in start_round: the tick stops driving #mp_timer between rounds, so
# the 3s gap would otherwise sit on the expired value.
scoreboard players set #mp_timer {ns}.data {ROUND_TICKS}
tag @a remove {ns}.demo_atk

scoreboard players add #demo_round {ns}.data 1

# End of the first half: swap sides and play the second
execute if score #demo_round {ns}.data matches {ROUNDS_PER_MATCH} run function {ns}:v{version}/multiplayer/gamemodes/demo/swap_sides
execute if score #demo_round {ns}.data matches {ROUNDS_PER_MATCH} run return run schedule function {ns}:v{version}/multiplayer/gamemodes/demo/start_round 60t

# Regulation is over. Every round awards exactly one point, so this closes the match on 2-0 here and on
# 2-1 after the decider; only a 1-1 falls through.
execute if score #red {ns}.mp.team > #blue {ns}.mp.team run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team > #red {ns}.mp.team run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}

# Still level: play the decider, its defending side chosen by kills
execute if score #demo_round {ns}.data matches {TIEBREAK_ROUND} run function {ns}:v{version}/multiplayer/gamemodes/demo/pick_tiebreak_sides
execute if score #demo_round {ns}.data matches {TIEBREAK_ROUND} run return run schedule function {ns}:v{version}/multiplayer/gamemodes/demo/start_round 60t

# Level after the decider (should be unreachable: a round that awards no point cannot happen)
function {ns}:v{version}/multiplayer/game_draw
""")

		## Demolition: halftime, the only place sides are swapped rather than computed
		variant.sub("swap_sides", f"""
execute if score #demo_attackers {ns}.data matches 1 run scoreboard players set #demo_attackers {ns}.data 2
execute unless score #demo_attackers {ns}.data matches 2 run scoreboard players set #demo_attackers {ns}.data 1
tellraw @a [{MGS_TAG},"⚔ ",{{"text":"Sides swapped!","color":"gold"}}]
playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
""")

		## Demolition: the decider's sides. The team with the most kills defends, so the other one attacks —
		## which is why this replaces swap_sides rather than following it, and can hand the same side two
		## attacks in a row. Announced in full because it decides the match and nobody can see the tally.
		variant.sub("pick_tiebreak_sides", f"""
# Match kill totals: mp.kills is per player and zeroed by multiplayer/start, never between rounds
scoreboard players set #demo_kills_red {ns}.data 0
scoreboard players set #demo_kills_blue {ns}.data 0
execute as @a[scores={{{ns}.mp.team=1}}] run scoreboard players operation #demo_kills_red {ns}.data += @s {ns}.mp.kills
execute as @a[scores={{{ns}.mp.team=2}}] run scoreboard players operation #demo_kills_blue {ns}.data += @s {ns}.mp.kills

# Most kills defends. A tie leaves Red attacking, matching the side-picking fallback.
scoreboard players set #demo_attackers {ns}.data 1
execute if score #demo_kills_red {ns}.data > #demo_kills_blue {ns}.data run scoreboard players set #demo_attackers {ns}.data 2

# The tally, then the tie fallback only: who defends is already announced by start_round, but "most kills"
# says nothing about a tie, so that one case is spelled out.
tellraw @a [{MGS_TAG},{{"text":"Kills: ","color":"gray"}},{{"text":"Red ","color":"red"}},{{"score":{{"name":"#demo_kills_red","objective":"{ns}.data"}},"color":"white"}},{{"text":" - ","color":"gray"}},{{"text":"Blue ","color":"blue"}},{{"score":{{"name":"#demo_kills_blue","objective":"{ns}.data"}},"color":"white"}}]
execute if score #demo_kills_red {ns}.data = #demo_kills_blue {ns}.data run tellraw @a [{MGS_TAG},{{"text":"Kills are level, so ","color":"yellow"}},{{"text":"Blue","color":"blue"}},{{"text":" defends.","color":"yellow"}}]
""")
