""" Starting a round and the zombie/dog count curves that size it. """
# Imports
from stewbeet import Mem, write_versioned_function

# Constants
EARLY_ROUND_ZOMBIES: dict[int, int] = {1: 5, 2: 6, 3: 8, 4: 9, 5: 11, 6: 12, 7: 13, 8: 15, 9: 16}
""" Zombies per player for rounds 1-9, replacing the standard `round + 7` base while it is still steep.
The ramp lands on 16 at round 9 and hands over to `round + 7` = 17 at round 10 with no step or drop.
"""


# Functions
def write_round_start() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/start_round", f"""
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data 1
execute store result storage {ns}:zombies game.round int 1 run scoreboard players get #zb_round {ns}.data

# Dog round: every 5th round from 5, only on maps with special spawn markers.
scoreboard players set #zb_dog_round {ns}.data 0
scoreboard players operation #zb_dog_mod {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_dog_mod {ns}.data %= #5 {ns}.data
execute if score #zb_has_special {ns}.data matches 1 if score #zb_round {ns}.data matches 5.. if score #zb_dog_mod {ns}.data matches 0 run scoreboard players set #zb_dog_round {ns}.data 1

# Clamped at 4, used by both round-size formulas.
execute store result score #zb_player_count {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute if score #zb_player_count {ns}.data matches 5.. run scoreboard players set #zb_player_count {ns}.data 4

execute if score #zb_dog_round {ns}.data matches 0 run function {ns}:v{version}/zombies/calc_round_count_zombies
execute if score #zb_dog_round {ns}.data matches 1 run function {ns}:v{version}/zombies/calc_round_count_dogs

# zb_to_spawn counts down as they spawn; the power-up drop chance needs the total (see powerups/check_drop).
scoreboard players operation #zb_round_total {ns}.data = #zb_to_spawn {ns}.data

function {ns}:v{version}/zombies/calc_spawn_timer

# No game-over check for 3 s.
scoreboard players set #zb_round_grace {ns}.data 60
scoreboard players set #zb_nobody_ticks {ns}.data 0

scoreboard players set #zb_stuck_timer {ns}.data 0
scoreboard players set #zb_glow_timer {ns}.data 0

# Its counter survives between matches and would trip recovery early.
scoreboard players set #zb_wd_ticks {ns}.data 0

function #{ns}:zombies/on_round_start

function {ns}:v{version}/zombies/refresh_sidebar

execute if score #zb_dog_round {ns}.data matches 0 run tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" has begun!","color":"red"}}]
execute if score #zb_dog_round {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/round_start_generic ambient @s ~ ~ ~ 0.3 1.0

# Dog rounds have their own announcement and howl instead of the round jingle.
execute if score #zb_dog_round {ns}.data matches 1 run tellraw @a ["",{{"text":"","color":"dark_red","bold":true}},"🐺 ",{{"text":"Round ","color":"dark_red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" — the hounds are loose!","color":"dark_red"}}]
execute if score #zb_dog_round {ns}.data matches 1 as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound minecraft:entity.wolf.howl ambient @s ~ ~ ~ 1.0 0.6
""")

	early_round_lines: str = "\n".join(
		f"execute if score #zb_round {ns}.data matches {round_num} run scoreboard players set #zb_to_spawn {ns}.data {count}"
		for round_num, count in EARLY_ROUND_ZOMBIES.items()
	)

	## min(256, min(96, 7 + round) x min(4, players)); EARLY_ROUND_ZOMBIES replaces the base below round 10 as a warmup.
	## Solo: r1 5, r5 11, r10 17, r20 27, r40 47, 96 from r41. 4+ players: r1 20, r5 44, r10 68, r20 108, r40 188, 256 from r41.
	write_versioned_function("zombies/calc_round_count_zombies", f"""
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players add #zb_to_spawn {ns}.data 7

# Rounds 1-9 use the eased ramp, which meets the formula at round 10.
{early_round_lines}
execute if score #zb_to_spawn {ns}.data matches 97.. run scoreboard players set #zb_to_spawn {ns}.data 96
scoreboard players operation #zb_to_spawn {ns}.data *= #zb_player_count {ns}.data
execute if score #zb_to_spawn {ns}.data matches 257.. run scoreboard players set #zb_to_spawn {ns}.data 256
""")

	## min(48, min(12, 4 + round / 3) x min(4, players)): short bursts, not another attrition wave.
	## Solo: r5 5, r10 7, r20 10, 12 from r25. 4+ players: r5 20, r10 28, r20 40, 48 from r25.
	write_versioned_function("zombies/calc_round_count_dogs", f"""
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data /= #3 {ns}.data
scoreboard players add #zb_to_spawn {ns}.data 4
execute if score #zb_to_spawn {ns}.data matches 13.. run scoreboard players set #zb_to_spawn {ns}.data 12
scoreboard players operation #zb_to_spawn {ns}.data *= #zb_player_count {ns}.data
execute if score #zb_to_spawn {ns}.data matches 49.. run scoreboard players set #zb_to_spawn {ns}.data 48

# Hounds come in packs scaled by players (solo 3, 4 players 6), refilled as they die (BO).
scoreboard players operation #zb_dog_cap {ns}.data = #zb_player_count {ns}.data
scoreboard players add #zb_dog_cap {ns}.data 2

# The guaranteed Max Ammo of this round.
scoreboard players set #zb_dog_ammo_done {ns}.data 0
""")

