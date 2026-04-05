
# ruff: noqa: E501
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG


def generate_search_and_destroy() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## S&D Setup
	write_versioned_function("multiplayer/gamemodes/snd/setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Search & Destroy! Attackers plant, defenders defuse!","color":"yellow"}}]

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Round tracking
scoreboard players set #snd_round {ns}.data 1
scoreboard players set #snd_max_rounds {ns}.data 6
scoreboard players set #snd_red_wins {ns}.data 0
scoreboard players set #snd_blue_wins {ns}.data 0

# Red starts as attackers
scoreboard players set #snd_attackers {ns}.data 1

# Bomb state: 0=not planted, 1=planting, 2=planted, 3=defusing
scoreboard players set #snd_bomb_state {ns}.data 0
scoreboard players set #snd_bomb_timer {ns}.data 0

# Round timer (90 seconds = 1800 ticks)
scoreboard players set #snd_round_timer {ns}.data 1800

# Summon objective markers (relative → absolute)
data modify storage {ns}:temp _snd_iter set from storage {ns}:multiplayer game.map.search_and_destroy
execute if data storage {ns}:temp _snd_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/snd/summon_obj

# Start round
function {ns}:v{version}/multiplayer/gamemodes/snd/start_round
""")

	## S&D: Summon objective markers (relative → absolute)
	write_versioned_function("multiplayer/gamemodes/snd/summon_obj", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _snd_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _snd_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _snd_iter[0][2]
scoreboard players operation #rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _snd_pos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _snd_pos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _snd_pos.z double 1 run scoreboard players get #rz {ns}.data
function {ns}:v{version}/multiplayer/gamemodes/snd/summon_obj_at with storage {ns}:temp _snd_pos
data remove storage {ns}:temp _snd_iter[0]
execute if data storage {ns}:temp _snd_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/snd/summon_obj
""")

	write_versioned_function("multiplayer/gamemodes/snd/summon_obj_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.snd_obj","{ns}.gm_entity"]}}
$execute positioned $(x) $(y) $(z) run setblock ~ ~ ~ chest
$execute positioned $(x) $(y) $(z) run setblock ~ ~1 ~ barrier
""")

	## S&D: Start Round
	write_versioned_function("multiplayer/gamemodes/snd/start_round", f"""
# Announce round
tellraw @a [{MGS_TAG},{{"text":"────── Round ","color":"gold"}},{{"score":{{"name":"#snd_round","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" ──────","color":"gold"}}]

# Show which team attacks
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" attacks | "}},{{"text":"Blue","color":"blue"}},{{"text":" defends"}}]
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" attacks | "}},{{"text":"Red","color":"red"}},{{"text":" defends"}}]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Reset bomb state
scoreboard players set #snd_bomb_state {ns}.data 0
scoreboard players set #snd_bomb_timer {ns}.data 0

# Reset round timer
scoreboard players set #snd_round_timer {ns}.data 1800

# Tag alive players
tag @a[scores={{{ns}.mp.team=1..2}}] add {ns}.snd_alive

# Respawn all players at team spawns
execute as @a[scores={{{ns}.mp.team=1..2}}] at @s run function {ns}:v{version}/multiplayer/apply_class
""")

	## S&D Tick
	write_versioned_function("multiplayer/gamemodes/snd/tick", f"""
# Round timer
scoreboard players remove #snd_round_timer {ns}.data 1

# If timer runs out, defenders win
execute if score #snd_round_timer {ns}.data matches ..0 if score #snd_bomb_state {ns}.data matches ..1 run function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win

# If bomb planted, tick bomb timer (45 seconds = 900 ticks)
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players remove #snd_bomb_timer {ns}.data 1
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_bomb_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_explodes

# Check if all attackers are dead (defenders win)
execute store result score #snd_atk_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=1}}]
execute if score #snd_attackers {ns}.data matches 2 store result score #snd_atk_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=2}}]
execute if score #snd_atk_alive {ns}.data matches 0 if score #snd_bomb_state {ns}.data matches ..1 run function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win

# Check if all defenders are dead and bomb not planted (attackers win)
execute store result score #snd_def_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=2}}]
execute if score #snd_attackers {ns}.data matches 2 store result score #snd_def_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=1}}]
execute if score #snd_def_alive {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/attackers_win

# Particles at objectives
execute at @e[tag={ns}.snd_obj] run particle dust{{color:[1.0,0.6,0.0],scale:1.0}} ~ ~1 ~ 1.0 0.5 1.0 0 5

# Check planting (attacker near objective and sneaking)
execute if score #snd_bomb_state {ns}.data matches 0 as @a[tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking] at @s if entity @e[tag={ns}.snd_obj,distance=..3] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_plant

# Check defusing (defender near bomb and sneaking)
execute if score #snd_bomb_state {ns}.data matches 2 as @a[tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking] at @s if entity @e[tag={ns}.snd_bomb,distance=..3] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_defuse
""")

	## S&D: Plant attempt
	write_versioned_function("multiplayer/gamemodes/snd/try_plant", f"""
# Only attackers can plant
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 1 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 2 run return fail

# Start or continue planting (5 seconds = 100 ticks)
scoreboard players set #snd_bomb_state {ns}.data 1
scoreboard players add #snd_bomb_timer {ns}.data 1
title @s actionbar [{{"text":"Planting... ","color":"gold"}},{{"score":{{"name":"#snd_bomb_timer","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/100"}}]

# If planted
execute if score #snd_bomb_timer {ns}.data matches 100.. run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_planted
""")

	## S&D: Bomb planted
	write_versioned_function("multiplayer/gamemodes/snd/bomb_planted", f"""
scoreboard players set #snd_bomb_state {ns}.data 2
scoreboard players set #snd_bomb_timer {ns}.data 900

# Summon bomb entity at planter's position
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.snd_bomb","{ns}.gm_entity"]}}

tellraw @a [{MGS_TAG},{{"text":"💣 BOMB PLANTED!","color":"red","bold":true}}]
playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5
""")

	## S&D: Defuse attempt
	write_versioned_function("multiplayer/gamemodes/snd/try_defuse", f"""
# Only defenders can defuse
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 2 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 1 run return fail

# Defuse progress (7.5 seconds = 150 ticks)
scoreboard players set #snd_bomb_state {ns}.data 3
scoreboard players add #snd_bomb_timer {ns}.data 1
title @s actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#snd_bomb_timer","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/150"}}]

execute if score #snd_bomb_timer {ns}.data matches 150.. run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_defused
""")

	## S&D: Bomb defused → defenders win
	write_versioned_function("multiplayer/gamemodes/snd/bomb_defused", f"""
tellraw @a [{MGS_TAG},{{"text":"💣 BOMB DEFUSED!","color":"aqua","bold":true}}]
kill @e[tag={ns}.snd_bomb]
function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win
""")

	## S&D: Bomb explodes → attackers win
	write_versioned_function("multiplayer/gamemodes/snd/bomb_explodes", f"""
# Explosion effect at bomb
execute at @e[tag={ns}.snd_bomb] run particle minecraft:explosion_emitter ~ ~1 ~ 2 2 2 0 5
execute at @e[tag={ns}.snd_bomb] run playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2 0.8

# Simulate death for any players near the bomb (10 block radius)
execute at @e[tag={ns}.snd_bomb] as @a[distance=..10,gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run data modify storage {ns}:input with set value {{}}
execute at @e[tag={ns}.snd_bomb] as @a[distance=..10,gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run function {ns}:v{version}/multiplayer/simulate_death

tellraw @a [{MGS_TAG},{{"text":"💥 BOMB EXPLODED!","color":"red","bold":true}}]
kill @e[tag={ns}.snd_bomb]
function {ns}:v{version}/multiplayer/gamemodes/snd/attackers_win
""")

	## S&D: Attackers win round
	write_versioned_function("multiplayer/gamemodes/snd/attackers_win", f"""
execute if score #snd_attackers {ns}.data matches 1 run scoreboard players add #snd_red_wins {ns}.data 1
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" (Attackers) win the round!","color":"yellow"}}]
execute if score #snd_attackers {ns}.data matches 2 run scoreboard players add #snd_blue_wins {ns}.data 1
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" (Attackers) win the round!","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/snd/next_round
""")

	## S&D: Defenders win round
	write_versioned_function("multiplayer/gamemodes/snd/defenders_win", f"""
execute if score #snd_attackers {ns}.data matches 1 run scoreboard players add #snd_blue_wins {ns}.data 1
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" (Defenders) win the round!","color":"yellow"}}]
execute if score #snd_attackers {ns}.data matches 2 run scoreboard players add #snd_red_wins {ns}.data 1
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" (Defenders) win the round!","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/snd/next_round
""")

	## S&D: Next round or game over
	write_versioned_function("multiplayer/gamemodes/snd/next_round", f"""
# Clean round state
kill @e[tag={ns}.snd_bomb]
tag @a remove {ns}.snd_alive

# Check if either team won enough rounds (best of max_rounds)
scoreboard players set #snd_win_threshold {ns}.data 4
execute if score #snd_red_wins {ns}.data >= #snd_win_threshold {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #snd_blue_wins {ns}.data >= #snd_win_threshold {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}

# Swap sides at halftime (after round 3)
scoreboard players add #snd_round {ns}.data 1
execute if score #snd_round {ns}.data matches 4 if score #snd_attackers {ns}.data matches 1 run scoreboard players set #snd_attackers {ns}.data 2
execute if score #snd_round {ns}.data matches 4 if score #snd_attackers {ns}.data matches 2 run scoreboard players set #snd_attackers {ns}.data 1
execute if score #snd_round {ns}.data matches 4 run tellraw @a [{MGS_TAG},{{"text":"⚔ Sides swapped!","color":"gold"}}]
execute if score #snd_round {ns}.data matches 4 run playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
# Start next round (delay 3 seconds = 60 ticks via schedule)
schedule function {ns}:v{version}/multiplayer/gamemodes/snd/start_round 60t
""")

	## S&D Kill Hook: No team scoring from kills, only round wins
	write_versioned_function("multiplayer/gamemodes/snd/on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
# Remove snd_alive from dead player (dead players detected by death_count in on_respawn)
""")

	## S&D Death Hook: Mark dead (called from on_respawn override)
	write_versioned_function("multiplayer/gamemodes/snd/on_death", f"""
# Remove alive tag (no respawn in S&D)
tag @s remove {ns}.snd_alive
# Set to spectator mode
gamemode spectator @s
""")

	## S&D Cleanup
	write_versioned_function("multiplayer/gamemodes/snd/cleanup", f"""
execute at @e[tag={ns}.snd_obj] run fill ~ ~ ~ ~ ~1 ~ air
kill @e[tag={ns}.snd_obj]
kill @e[tag={ns}.snd_bomb]
tag @a remove {ns}.snd_alive
""")

