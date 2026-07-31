""" The Search & Destroy round structure: opening a round, closing it, and who took the match. """
# Imports
from .....helpers import MGS_TAG
from ...base import GameModeVariant

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

		## S&D: Start Round
		variant.sub("start_round", f"""
# Guard: only while the game is running (a scheduled call may fire after the game ended)
execute if data storage {ns}:multiplayer game{{state:"lobby"}} run return fail
execute if data storage {ns}:multiplayer game{{state:"ended"}} run return fail

# Announce round
tellraw @a [{MGS_TAG},{{"text":"────── Round ","color":"gold"}},{{"score":{{"name":"#snd_round","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" ──────","color":"gold"}}]

# Show which team attacks
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" attacks | "}},{{"text":"Blue","color":"blue"}},{{"text":" defends"}}]
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" attacks | "}},{{"text":"Red","color":"red"}},{{"text":" defends"}}]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Reset bomb state and channel progress
scoreboard players set #snd_bomb_state {ns}.data 0
scoreboard players set #snd_bomb_timer {ns}.data 0
scoreboard players set #snd_plant_progress {ns}.data 0
scoreboard players set #snd_defuse_progress {ns}.data 0

# Reset round timer (and the HUD clock it drives, so the 3s gap already shows the fresh 2:30)
scoreboard players set #snd_round_timer {ns}.data {ROUND_TICKS}
scoreboard players set #mp_timer {ns}.data {ROUND_TICKS}

# Restore players who died last round (S&D deaths skip the respawn countdown)
execute as @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator]

# Tag alive players
tag @a[scores={{{ns}.mp.team=1..2}},gamemode=!spectator] add {ns}.snd_alive

# Teleport everyone to their team spawns and re-apply class loadouts
execute as @a[scores={{{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute as @a[scores={{{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
execute as @a[scores={{{ns}.mp.team=1..2}}] at @s run function {ns}:v{version}/multiplayer/apply_class

# Drop a fresh bomb in front of the attacking team. There is exactly ONE bomb per round and nobody starts
# holding it, so the attackers' first job is to collect it — that walk is what gives the defenders time
# to set up, and it is the main thing that separates this from a Counter-Strike round.
tag @a remove {ns}.snd_carrier
kill @e[tag={ns}.snd_loose]
kill @e[tag={ns}.snd_carrier_label]
execute if score #snd_attackers {ns}.data matches 1 at @e[tag={ns}.spawn_red,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb
execute if score #snd_attackers {ns}.data matches 2 at @e[tag={ns}.spawn_blue,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb

# Safety net: a map defining only general spawns would otherwise open the round with no bomb anywhere,
# which the attackers could never win. Any spawn point is better than none.
execute unless entity @e[tag={ns}.snd_loose_at] at @e[tag={ns}.spawn_point,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb

# Open the round LAST, once everyone is alive-tagged and placed. Until this is 1 the tick judges nothing,
# so the gap between rounds can never be mistaken for a team wipe.
scoreboard players set #snd_round_active {ns}.data 1
""")

		## S&D: Attackers win round
		variant.sub("attackers_win", f"""
# Close the round exactly once. Several end conditions can come true on the same tick (a defuse that
# also wipes a side, a timeout landing with the last kill), and each one calls in here.
execute unless score #snd_round_active {ns}.data matches 1 run return fail
scoreboard players set #snd_round_active {ns}.data 0

execute if score #snd_attackers {ns}.data matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" (Attackers) win the round!","color":"yellow"}}]
execute if score #snd_attackers {ns}.data matches 2 run scoreboard players add #blue {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" (Attackers) win the round!","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/snd/next_round
""")

		## S&D: Defenders win round
		variant.sub("defenders_win", f"""
# Same single-shot guard as attackers_win — this is the path the defuse takes, and the defuse used to be
# immediately followed by four attacker wins as the wiped-looking alive tags were judged tick after tick.
execute unless score #snd_round_active {ns}.data matches 1 run return fail
scoreboard players set #snd_round_active {ns}.data 0

execute if score #snd_attackers {ns}.data matches 1 run scoreboard players add #blue {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" (Defenders) win the round!","color":"yellow"}}]
execute if score #snd_attackers {ns}.data matches 2 run scoreboard players add #red {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" (Defenders) win the round!","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/snd/next_round
""")

		## S&D: Next round or game over
		variant.sub("next_round", f"""
# Clean round state. #snd_round_active was already cleared by the win function that got us here, which is
# what stops the tick from judging the cleared snd_alive tags below as a wipe.
# The HUD clock is reset here and not only in start_round: the tick stops driving it while no round is
# running, so the 3s gap would otherwise sit on the expired timer or the leftover fuse.
scoreboard players set #mp_timer {ns}.data {ROUND_TICKS}
kill @e[tag={ns}.snd_bomb]
kill @e[tag={ns}.snd_bomb_vis]
kill @e[tag={ns}.snd_bomb_hud]
kill @e[tag={ns}.snd_loose]
kill @e[tag={ns}.snd_carrier_label]
tag @a remove {ns}.snd_carrier
tag @a remove {ns}.snd_alive

# Check if either team reached the round-win threshold (set in setup, also read by the sidebar)
execute if score #red {ns}.mp.team >= #snd_win_threshold {ns}.data run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #snd_win_threshold {ns}.data run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}

# Swap sides at halftime
scoreboard players add #snd_round {ns}.data 1
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} if score #snd_attackers {ns}.data matches 1 run scoreboard players set #snd_attackers {ns}.data 2
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} if score #snd_attackers {ns}.data matches 2 run scoreboard players set #snd_attackers {ns}.data 1
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} run tellraw @a [{MGS_TAG},"⚔ ",{{"text":"Sides swapped!","color":"gold"}}]
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} run playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
# Start next round (delay 3 seconds = 60 ticks via schedule)
schedule function {ns}:v{version}/multiplayer/gamemodes/snd/start_round 60t
""")
