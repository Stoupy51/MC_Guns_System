""" Starting a round and the zombie/dog count curves that size it. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_round_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Round System.

	## Start a new round
	write_versioned_function("zombies/start_round", f"""
# Increment round number
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data 1
execute store result storage {ns}:zombies game.round int 1 run scoreboard players get #zb_round {ns}.data

# Dog round: every 5th round from 5 on, and only on maps that placed special spawn markers
scoreboard players set #zb_dog_round {ns}.data 0
scoreboard players operation #zb_dog_mod {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_dog_mod {ns}.data %= #5 {ns}.data
execute if score #zb_has_special {ns}.data matches 1 if score #zb_round {ns}.data matches 5.. if score #zb_dog_mod {ns}.data matches 0 run scoreboard players set #zb_dog_round {ns}.data 1

# Player count, clamped at 4, drives both round-size formulas
execute store result score #zb_player_count {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute if score #zb_player_count {ns}.data matches 5.. run scoreboard players set #zb_player_count {ns}.data 4

# Enemy count for this round — see each subfunction for its curve
execute if score #zb_dog_round {ns}.data matches 0 run function {ns}:v{version}/zombies/calc_round_count_zombies
execute if score #zb_dog_round {ns}.data matches 1 run function {ns}:v{version}/zombies/calc_round_count_dogs

# Snapshot the round's total zombie count (zb_to_spawn is decremented as they spawn).
# Used by the power-up drop chance: min(5%, 2/total_round_zombies).
scoreboard players operation #zb_round_total {ns}.data = #zb_to_spawn {ns}.data

# Calculate initial spawn timer and batch size for this round
function {ns}:v{version}/zombies/calc_spawn_timer

# Grace period: don't check game over for 3 seconds (60 ticks)
scoreboard players set #zb_round_grace {ns}.data 60

# Reset stuck zombie glow timers
scoreboard players set #zb_stuck_timer {ns}.data 0
scoreboard players set #zb_glow_timer {ns}.data 0

# Reset the freeze watchdog: its counter survives between matches and would trip recovery early
scoreboard players set #zb_wd_ticks {ns}.data 0

# Signal round start
function #{ns}:zombies/on_round_start

# Refresh sidebar
function {ns}:v{version}/zombies/refresh_sidebar

# Announce
execute if score #zb_dog_round {ns}.data matches 0 run tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" has begun!","color":"red"}}]
execute if score #zb_dog_round {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/round_start_generic ambient @s ~ ~ ~ 0.3 1.0

# Dog rounds get their own announcement + howl instead of the usual round jingle
execute if score #zb_dog_round {ns}.data matches 1 run tellraw @a ["",{{"text":"","color":"dark_red","bold":true}},"🐺 ",{{"text":"Round ","color":"dark_red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" — the hounds are loose!","color":"dark_red"}}]
execute if score #zb_dog_round {ns}.data matches 1 as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound minecraft:entity.wolf.howl ambient @s ~ ~ ~ 1.0 0.6
""")

	## Standard round size: min(256, min(96, 7 + round) * min(4, player_count))
	## Solo player: r1=8,  r5=12, r10=17, r20=27,  r40=47,  r41+ caps at 96
	## 4+ players:  r1=32, r5=48, r10=68, r20=108, r40=188, r41+ caps at 256
	write_versioned_function("zombies/calc_round_count_zombies", f"""
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players add #zb_to_spawn {ns}.data 7
execute if score #zb_to_spawn {ns}.data matches 97.. run scoreboard players set #zb_to_spawn {ns}.data 96
scoreboard players operation #zb_to_spawn {ns}.data *= #zb_player_count {ns}.data
execute if score #zb_to_spawn {ns}.data matches 257.. run scoreboard players set #zb_to_spawn {ns}.data 256
""")

	## Dog round size: min(48, min(12, 4 + round/3) * min(4, player_count)).
	## Far below the zombie curve on purpose: short frantic bursts, not another attrition wave.
	## Solo player: r5=5,  r10=7,  r20=10, r25+ caps at 12
	## 4+ players:  r5=20, r10=28, r20=40, r25+ caps at 48
	write_versioned_function("zombies/calc_round_count_dogs", f"""
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data /= #3 {ns}.data
scoreboard players add #zb_to_spawn {ns}.data 4
execute if score #zb_to_spawn {ns}.data matches 13.. run scoreboard players set #zb_to_spawn {ns}.data 12
scoreboard players operation #zb_to_spawn {ns}.data *= #zb_player_count {ns}.data
execute if score #zb_to_spawn {ns}.data matches 49.. run scoreboard players set #zb_to_spawn {ns}.data 48

# Concurrent pack size: BO sends hounds in packs of 2-4 scaled by players, refilled as they die,
# rather than releasing the round's whole count at once. Solo 3 -> 4 players 6.
scoreboard players operation #zb_dog_cap {ns}.data = #zb_player_count {ns}.data
scoreboard players add #zb_dog_cap {ns}.data 2

# Arm this round's guaranteed Max Ammo
scoreboard players set #zb_dog_ammo_done {ns}.data 0
""")

