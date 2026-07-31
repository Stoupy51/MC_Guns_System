""" Demolition's round structure: two halves, then a sudden-death overtime.

Each side attacks exactly once. An attacking side wins its half only by destroying **both** sites before
the clock runs out; anything less is a defensive hold. If the two halves split 1-1 — or if both defences
held, 0-0, which the official rules do not cover and which is treated the same way here — a third round
decides it: both bomb sites turn neutral, everyone is armed, and the first detonation takes the match.

CoD runs that decider on one dedicated neutral site. This mode has no map data for such a point and will
not invent one: the two bomb sites the map already defines are authored, playable, and exactly the right
kind of place, so overtime simply opens both of them to both teams instead.
"""
# ruff: noqa: E501
# Imports
from .....helpers import MGS_TAG
from ...base import GameModeVariant
from .sites_state import DemoSites

# Constants
ROUND_TICKS: int = 3600
""" 3:00 per half. Longer than a Search & Destroy round because the attackers have to destroy two sites
rather than plant one, and every death is a respawn rather than the end of their round.
NOT a sourced value — tune in game. """
OVERTIME_TICKS: int = 3600
""" 3:00 for the decider. Expiring means nobody detonated anything, which is a draw. """
ROUNDS_PER_MATCH: int = 2
""" Halves in regulation, one per side. """
OVERTIME_ROUND: int = ROUNDS_PER_MATCH + 1
""" Round number the sudden-death round runs as; `demo_round` reaching past it means it expired. """


# Classes
class DemoRounds:
	""" Opening and closing Demolition rounds, and running the overtime decider. """

	# Functions
	@staticmethod
	def write(variant: GameModeVariant) -> None:
		""" Write `start_round`, the two win functions, `next_round`, `swap_sides` and the overtime pair. """
		ns, version = variant.ns, variant.version

		## Demolition: Start Round
		variant.sub("start_round", f"""
# Guard: only while the game is running (a scheduled call may fire after the game ended)
execute if data storage {ns}:multiplayer game{{state:"lobby"}} run return fail
execute if data storage {ns}:multiplayer game{{state:"ended"}} run return fail

# Announce round
tellraw @a [{MGS_TAG},{{"text":"────── Round ","color":"gold"}},{{"score":{{"name":"#demo_round","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" ──────","color":"gold"}}]
execute if score #demo_round {ns}.data matches ..{ROUNDS_PER_MATCH} if score #demo_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" attacks both sites | "}},{{"text":"Blue","color":"blue"}},{{"text":" defends"}}]
execute if score #demo_round {ns}.data matches ..{ROUNDS_PER_MATCH} if score #demo_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" attacks both sites | "}},{{"text":"Red","color":"red"}},{{"text":" defends"}}]
execute if score #demo_round {ns}.data matches {OVERTIME_ROUND}.. run tellraw @a [{MGS_TAG},"⚡ ",{{"text":"OVERTIME — both sites are neutral, first detonation wins!","color":"gold","bold":true}}]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Every site back to intact
{DemoSites.reset_lines(variant)}

# Clock. Regulation and overtime differ only in length; both stop while a bomb is down.
execute if score #demo_round {ns}.data matches ..{ROUNDS_PER_MATCH} run scoreboard players set #demo_timer {ns}.data {ROUND_TICKS}
execute if score #demo_round {ns}.data matches {OVERTIME_ROUND}.. run scoreboard players set #demo_timer {ns}.data {OVERTIME_TICKS}
scoreboard players operation #mp_timer {ns}.data = #demo_timer {ns}.data

# Who is carrying a bomb. Every attacker is, on every respawn, which is why Demolition needs none of the
# carry/drop/pickup machinery S&D has — the tag IS the bomb. In overtime BOTH sides get it.
tag @a remove {ns}.demo_atk
execute if score #demo_round {ns}.data matches ..{ROUNDS_PER_MATCH} if score #demo_attackers {ns}.data matches 1 run tag @a[scores={{{ns}.mp.team=1}}] add {ns}.demo_atk
execute if score #demo_round {ns}.data matches ..{ROUNDS_PER_MATCH} if score #demo_attackers {ns}.data matches 2 run tag @a[scores={{{ns}.mp.team=2}}] add {ns}.demo_atk
execute if score #demo_round {ns}.data matches {OVERTIME_ROUND}.. run tag @a[scores={{{ns}.mp.team=1..2}}] add {ns}.demo_atk

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
execute if score #demo_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" destroyed both sites!","color":"yellow"}}]
execute if score #demo_attackers {ns}.data matches 2 run scoreboard players add #blue {ns}.mp.team 1
execute if score #demo_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" destroyed both sites!","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/demo/next_round
""")

		## Demolition: the clock ran out with something still standing
		variant.sub("defenders_win", f"""
execute unless score #demo_round_active {ns}.data matches 1 run return fail
scoreboard players set #demo_round_active {ns}.data 0

execute if score #demo_attackers {ns}.data matches 1 run scoreboard players add #blue {ns}.mp.team 1
execute if score #demo_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" held the sites!","color":"yellow"}}]
execute if score #demo_attackers {ns}.data matches 2 run scoreboard players add #red {ns}.mp.team 1
execute if score #demo_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" held the sites!","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/demo/next_round
""")

		## Demolition: overtime detonation — the planting team takes the match (#demo_last_owner is set by
		## site_destroyed, before this is called, because the site marker is gone from that context by then)
		variant.sub("overtime_won", f"""
execute unless score #demo_round_active {ns}.data matches 1 run return fail
scoreboard players set #demo_round_active {ns}.data 0

execute if score #demo_last_owner {ns}.data matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score #demo_last_owner {ns}.data matches 2 run scoreboard players add #blue {ns}.mp.team 1
execute if score #demo_last_owner {ns}.data matches 1 run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #demo_last_owner {ns}.data matches 2 run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}

# Nobody owned it (should be unreachable): treat it as the draw an expired overtime would have been
function {ns}:v{version}/multiplayer/game_draw
""")

		## Demolition: the overtime clock ran out with the neutral site still standing — nobody earned it
		variant.sub("overtime_expired", f"""
execute unless score #demo_round_active {ns}.data matches 1 run return fail
scoreboard players set #demo_round_active {ns}.data 0

tellraw @a [{MGS_TAG},"⚡ ",{{"text":"Overtime expired — nobody detonated the site.","color":"gray"}}]
function {ns}:v{version}/multiplayer/game_draw
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

# Both halves played: a leader takes the match, a tie plays the decider. Overtime needs no setup of its
# own — start_round already restores both sites and arms both teams once the round number says so.
execute if score #demo_round {ns}.data matches {OVERTIME_ROUND} if score #red {ns}.mp.team > #blue {ns}.mp.team run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #demo_round {ns}.data matches {OVERTIME_ROUND} if score #blue {ns}.mp.team > #red {ns}.mp.team run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
execute if score #demo_round {ns}.data matches {OVERTIME_ROUND} run return run schedule function {ns}:v{version}/multiplayer/gamemodes/demo/start_round 60t

# Overtime itself expired without a detonation
function {ns}:v{version}/multiplayer/game_draw
""")

		## Demolition: halftime. The only structural change in the whole match — overtime alters no
		## geometry and no sides, which is why it needs no function of its own.
		variant.sub("swap_sides", f"""
execute if score #demo_attackers {ns}.data matches 1 run scoreboard players set #demo_attackers {ns}.data 2
execute unless score #demo_attackers {ns}.data matches 2 run scoreboard players set #demo_attackers {ns}.data 1
tellraw @a [{MGS_TAG},"⚔ ",{{"text":"Sides swapped!","color":"gold"}}]
playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
""")
