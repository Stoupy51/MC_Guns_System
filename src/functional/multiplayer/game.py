
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_tag, write_tick_file, write_versioned_function

from ..helpers import MGS_TAG


def generate_game() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Scoreboards & Storage Setup
	write_load_file(
f"""
## Multiplayer scoreboards
# Team assignment (1 = red, 2 = blue, 0 = none/spectator)
scoreboard objectives add {ns}.mp.team dummy
# Personal stats
scoreboard objectives add {ns}.mp.kills dummy
scoreboard objectives add {ns}.mp.deaths dummy
# Round timer (ticks remaining)
scoreboard objectives add {ns}.mp.timer dummy
# In-game tag scoreboard (1 = in active game)
scoreboard objectives add {ns}.mp.in_game dummy

# Boundary checking coords
scoreboard objectives add {ns}.mp.bx dummy
scoreboard objectives add {ns}.mp.by dummy
scoreboard objectives add {ns}.mp.bz dummy

# Class change detection (for prep phase)
scoreboard objectives add {ns}.mp.prev_class dummy

# Initialize team scores (only if not already set)
execute unless score #red {ns}.mp.team matches -2147483648.. run scoreboard players set #red {ns}.mp.team 0
execute unless score #blue {ns}.mp.team matches -2147483648.. run scoreboard players set #blue {ns}.mp.team 0

# Initialize game state (only if not yet set)
execute unless data storage {ns}:multiplayer game run data modify storage {ns}:multiplayer game set value {{state:"lobby",gamemode:"tdm",score_limit:30,time_limit:12000,map_id:"hijacked"}}

# Constants for timer math
scoreboard players set #10 {ns}.data 10
scoreboard players set #20 {ns}.data 20
scoreboard players set #60 {ns}.data 60
""")

	## Signal function tags
	for event in ["register_maps", "register_classes", "on_game_start", "on_game_end"]:
		write_tag(f"multiplayer/{event}", Mem.ctx.data[ns].function_tags, [])

	## Game Start (requires a map to be loaded first)
	write_versioned_function("multiplayer/start", f"""
# Prevent starting if already active or preparing
execute if data storage {ns}:multiplayer game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"Game already in progress!","color":"red"}}]
execute if data storage {ns}:multiplayer game{{state:"preparing"}} run return run tellraw @s [{MGS_TAG},{{"text":"Game already preparing!","color":"red"}}]

# Load the selected map (reads map_id from game storage)
function {ns}:v{version}/multiplayer/load_map_from_storage with storage {ns}:multiplayer game
execute unless score #map_load_found {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"No map found! Select a map first.","color":"red"}}]

# Copy loaded map data into game state
data modify storage {ns}:multiplayer game.map set from storage {ns}:temp map_load.result

# Initialize game
data modify storage {ns}:multiplayer game.state set value "preparing"

# Reset scores
scoreboard players set #red {ns}.mp.team 0
scoreboard players set #blue {ns}.mp.team 0
scoreboard players set @a {ns}.mp.kills 0
scoreboard players set @a {ns}.mp.deaths 0
scoreboard players set @a {ns}.mp.death_count 0

# Set timer from time_limit
execute store result score #mp_timer {ns}.data run data get storage {ns}:multiplayer game.time_limit

# Tag all non-spectator players as in-game
scoreboard players set @a {ns}.mp.in_game 1

# Set all in-game players to adventure and enable instant respawn
gamemode adventure @a[scores={{{ns}.mp.in_game=1}}]
gamerule immediate_respawn true

# Store base coordinates for offset
execute store result score #gm_base_x {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[2]

# Store boundary corners (relative) and convert to absolute
execute store result score #bound_x1 {ns}.data run data get storage {ns}:multiplayer game.map.boundaries[0][0]
execute store result score #bound_y1 {ns}.data run data get storage {ns}:multiplayer game.map.boundaries[0][1]
execute store result score #bound_z1 {ns}.data run data get storage {ns}:multiplayer game.map.boundaries[0][2]
execute store result score #bound_x2 {ns}.data run data get storage {ns}:multiplayer game.map.boundaries[1][0]
execute store result score #bound_y2 {ns}.data run data get storage {ns}:multiplayer game.map.boundaries[1][1]
execute store result score #bound_z2 {ns}.data run data get storage {ns}:multiplayer game.map.boundaries[1][2]
scoreboard players operation #bound_x1 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y1 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z1 {ns}.data += #gm_base_z {ns}.data
scoreboard players operation #bound_x2 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y2 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z2 {ns}.data += #gm_base_z {ns}.data

# Normalize boundaries (ensure x1 < x2, y1 < y2, z1 < z2)
function {ns}:v{version}/multiplayer/normalize_bounds

# Summon out-of-bounds markers
function {ns}:v{version}/multiplayer/summon_oob

# Summon spawn point markers (for smart spawn selection)
function {ns}:v{version}/multiplayer/summon_spawns

# Call register hooks (external datapacks can set up maps/classes)
function #{ns}:multiplayer/register_maps
function #{ns}:multiplayer/register_classes

# Signal game start
function #{ns}:multiplayer/on_game_start

# Run gamemode-specific setup
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/gamemodes/ffa/setup
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/gamemodes/tdm/setup
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/gamemodes/dom/setup
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/gamemodes/hp/setup
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/gamemodes/snd/setup

# Store score limit and compute initial timer values for sidebar
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute store result score #_timer_sec {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #_timer_sec {ns}.data /= #20 {ns}.data
execute store result score #_timer_min {ns}.data run scoreboard players get #_timer_sec {ns}.data
scoreboard players operation #_timer_min {ns}.data /= #60 {ns}.data
scoreboard players operation #_timer_mod {ns}.data = #_timer_sec {ns}.data
scoreboard players operation #_timer_mod {ns}.data %= #60 {ns}.data
scoreboard players operation #_timer_tens {ns}.data = #_timer_mod {ns}.data
scoreboard players operation #_timer_tens {ns}.data /= #10 {ns}.data
scoreboard players operation #_timer_ones {ns}.data = #_timer_mod {ns}.data
scoreboard players operation #_timer_ones {ns}.data %= #10 {ns}.data

# Create sidebar HUD
scoreboard objectives add {ns}.sidebar dummy
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/create_sidebar_ffa
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/create_sidebar_team {{title:"Team Deathmatch"}}
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/create_sidebar_team {{title:"Domination"}}
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/create_sidebar_team {{title:"Hardpoint"}}
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/create_sidebar_team {{title:"Search & Destroy"}}

# Show kills in player list (tab)
scoreboard objectives setdisplay list {ns}.mp.kills

# Teleport players to spawn points
function {ns}:v{version}/multiplayer/tp_all_to_spawns

# Freeze all players (no movement during prep)
effect give @a[scores={{{ns}.mp.in_game=1}}] darkness 25 255 true
effect give @a[scores={{{ns}.mp.in_game=1}}] blindness 25 255 true
effect give @a[scores={{{ns}.mp.in_game=1}}] night_vision 25 255 true
effect give @a[scores={{{ns}.mp.in_game=1}}] saturation infinite 255 true
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:jump_strength base set 0

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set
scoreboard players add @s {ns}.mp.class 0
execute as @a[scores={{{ns}.mp.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

# Show class selection dialog to EVERYONE (so they can change during prep)
execute as @a[scores={{{ns}.mp.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# Store current class for change detection during prep
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Schedule end of prep (10 seconds = 200 ticks)
schedule function {ns}:v{version}/multiplayer/end_prep 200t

# Announce
tellraw @a ["",[{{"text":"","color":"gold","bold":true}},"⚔ ",{{"text":"Preparing"}},"! "],{{"text":"Choose your class! Game starts in 10 seconds!","color":"yellow"}}]
""")

	## Load map from storage (reads map_id from game state and passes to load macro)
	write_versioned_function("multiplayer/load_map_from_storage", f"""
$function {ns}:v{version}/maps/multiplayer/load {{id:"$(map_id)",override:{{}}}}
""")

	## Normalize boundaries: ensure min < max for each axis
	write_versioned_function("multiplayer/normalize_bounds", f"""
# Swap x if needed
execute if score #bound_x1 {ns}.data > #bound_x2 {ns}.data run scoreboard players operation #_swap {ns}.data = #bound_x1 {ns}.data
execute if score #bound_x1 {ns}.data > #bound_x2 {ns}.data run scoreboard players operation #bound_x1 {ns}.data = #bound_x2 {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_x2 {ns}.data = #_swap {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players reset #_swap {ns}.data

# Swap y if needed
execute if score #bound_y1 {ns}.data > #bound_y2 {ns}.data run scoreboard players operation #_swap {ns}.data = #bound_y1 {ns}.data
execute if score #bound_y1 {ns}.data > #bound_y2 {ns}.data run scoreboard players operation #bound_y1 {ns}.data = #bound_y2 {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_y2 {ns}.data = #_swap {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players reset #_swap {ns}.data

# Swap z if needed
execute if score #bound_z1 {ns}.data > #bound_z2 {ns}.data run scoreboard players operation #_swap {ns}.data = #bound_z1 {ns}.data
execute if score #bound_z1 {ns}.data > #bound_z2 {ns}.data run scoreboard players operation #bound_z1 {ns}.data = #bound_z2 {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_z2 {ns}.data = #_swap {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players reset #_swap {ns}.data
""")

	## Game Stop
	write_versioned_function("multiplayer/stop", f"""
# End game
data modify storage {ns}:multiplayer game.state set value "lobby"

# Cancel scheduled prep end (in case game stopped during prep)
schedule clear {ns}:v{version}/multiplayer/end_prep

# Restore movement (in case stopped during prep)
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects (in case stopped during prep)
effect clear @a[scores={{{ns}.mp.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mp.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mp.in_game=1}}] night_vision

# Gamemode cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/gamemodes/ffa/cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/gamemodes/tdm/cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/gamemodes/dom/cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/gamemodes/hp/cleanup
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/gamemodes/snd/cleanup

# Kill gamemode entities
kill @e[tag={ns}.gm_entity]

# Signal game end
function #{ns}:multiplayer/on_game_end

# Announce scores
tellraw @a ["",[{{"text":"","color":"gold","bold":true}},"⚔ ",{{"text":"Game Over"}},"! "]]
tellraw @a ["",{{"text":"Red","color":"red"}},{{"text":": "}},{{"score":{{"name":"#red","objective":"{ns}.mp.team"}}}}," | ",{{"text":"Blue","color":"blue"}},{{"text":": "}},{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}}}}]

# Remove sidebar and list displays
scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.sidebar
scoreboard objectives setdisplay list

# Clear in-game state
scoreboard players set @a {ns}.mp.in_game 0
scoreboard players set @a {ns}.mp.team 0
""")

	## Kill Tracking (Signal Listener) - now dispatches to gamemode
	write_versioned_function("multiplayer/on_kill_signal", f"""
# Only process if multiplayer game is active
execute unless data storage {ns}:multiplayer game{{state:"active"}} run return fail

# Dispatch to gamemode-specific kill handler
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run return run function {ns}:v{version}/multiplayer/gamemodes/ffa/on_kill
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run return run function {ns}:v{version}/multiplayer/gamemodes/tdm/on_kill
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run return run function {ns}:v{version}/multiplayer/gamemodes/dom/on_kill
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run return run function {ns}:v{version}/multiplayer/gamemodes/hp/on_kill
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run return run function {ns}:v{version}/multiplayer/gamemodes/snd/on_kill
""", tags=[f"{ns}:signals/on_kill"])

	## Team Wins
	write_versioned_function("multiplayer/team_wins", f"""
# Announce winner
$tellraw @a ["",{{"text":"🏆 ","color":"gold"}},{{"text":"$(team) Team Wins!","color":"gold","bold":true}}]
tellraw @a ["",[{{"text":"","color":"gray"}},"  ",{{"text":"Final Score - Red"}},": "],{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"red"}},[{{"text":"","color":"gray"}}," ",{{"text":"vs Blue"}},": "],{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"blue"}}]

# End game
function {ns}:v{version}/multiplayer/stop
""")

	# ── Game Tick (runs once per server tick when game is active) ──
	write_tick_file(f"""
# Multiplayer game tick
execute if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/game_tick
execute if data storage {ns}:multiplayer game{{state:"preparing"}} run function {ns}:v{version}/multiplayer/prep_tick
""")

	write_versioned_function("multiplayer/game_tick", f"""
# ── Timer ──
scoreboard players remove #mp_timer {ns}.data 1

# Timer display every second (20 ticks)
execute store result score #_tick_mod {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #_tick_mod {ns}.data %= #20 {ns}.data
execute if score #_tick_mod {ns}.data matches 0 run function {ns}:v{version}/multiplayer/timer_display

# Time's up
execute if score #mp_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/time_up

# ── Boundary enforcement (skip players with respawn protection) ──
execute as @e[type=player,scores={{{ns}.mp.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/check_bounds

# ── Out-of-bounds check (skip players with respawn protection) ──
execute as @e[type=player,scores={{{ns}.mp.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag={ns}.oob_point,distance=..5] run function {ns}:v{version}/multiplayer/oob_kill

# ── Gamemode tick dispatch ──
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/gamemodes/ffa/tick
execute if data storage {ns}:multiplayer game{{gamemode:"tdm"}} run function {ns}:v{version}/multiplayer/gamemodes/tdm/tick
execute if data storage {ns}:multiplayer game{{gamemode:"dom"}} run function {ns}:v{version}/multiplayer/gamemodes/dom/tick
execute if data storage {ns}:multiplayer game{{gamemode:"hp"}} run function {ns}:v{version}/multiplayer/gamemodes/hp/tick
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run function {ns}:v{version}/multiplayer/gamemodes/snd/tick
""")

	## Timer display (actionbar timer in minutes:seconds for all in-game players)
	write_versioned_function("multiplayer/timer_display", f"""
# Convert ticks to seconds
execute store result score #_timer_sec {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #_timer_sec {ns}.data /= #20 {ns}.data
execute store result score #_timer_min {ns}.data run scoreboard players get #_timer_sec {ns}.data
scoreboard players operation #_timer_min {ns}.data /= #60 {ns}.data
scoreboard players operation #_timer_mod {ns}.data = #_timer_sec {ns}.data
scoreboard players operation #_timer_mod {ns}.data %= #60 {ns}.data

# Zero-padded seconds for sidebar
scoreboard players operation #_timer_tens {ns}.data = #_timer_mod {ns}.data
scoreboard players operation #_timer_tens {ns}.data /= #10 {ns}.data
scoreboard players operation #_timer_ones {ns}.data = #_timer_mod {ns}.data
scoreboard players operation #_timer_ones {ns}.data %= #10 {ns}.data

# Refresh sidebar with updated values
function #bs.sidebar:refresh {{objective:"{ns}.sidebar"}}
""")

	## Time up → determine winner
	write_versioned_function("multiplayer/time_up", f"""
# FFA: player with most kills wins
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run function {ns}:v{version}/multiplayer/ffa_time_up

# Team modes: team with more points wins
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #red {ns}.mp.team > #blue {ns}.mp.team run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #blue {ns}.mp.team > #red {ns}.mp.team run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} if score #red {ns}.mp.team = #blue {ns}.mp.team run function {ns}:v{version}/multiplayer/game_draw
""")

	## FFA time up: find player with most kills
	write_versioned_function("multiplayer/ffa_time_up", f"""
tellraw @a [{MGS_TAG},{{"text":"Time's up!","color":"gold"}}]
# Store max kills into a score
scoreboard players set #_max_kills {ns}.data 0
execute as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.kills > #_max_kills {ns}.data run scoreboard players operation #_max_kills {ns}.data = @s {ns}.mp.kills
# The player with that score wins
execute as @a[scores={{{ns}.mp.in_game=1}}] if score @s {ns}.mp.kills = #_max_kills {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/ffa/player_wins
""")

	## Game draw
	write_versioned_function("multiplayer/game_draw", f"""
tellraw @a ["",{{"text":"🤝 ","color":"gold"}},{{"text":"Draw!","color":"gold","bold":true}}]
function {ns}:v{version}/multiplayer/stop
""")

	## Boundary check (run as each in-game player at their position)
	write_versioned_function("multiplayer/check_bounds", f"""
# Get player position as integers
data modify storage {ns}:temp _player_pos set from entity @s Pos
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _player_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _player_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _player_pos[2]

# Check if outside boundaries (any axis out of range = OOB)
execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run function {ns}:v{version}/multiplayer/bounds_kill
""")

	## Kill player out of bounds
	write_versioned_function("multiplayer/bounds_kill", "kill @s")

	## OOB kill (player near an out-of-bounds marker)
	write_versioned_function("multiplayer/oob_kill", "kill @s")

	## Summon OOB markers from map data (relative → absolute)
	write_versioned_function("multiplayer/summon_oob", f"""
# Store base coordinates for offset
execute store result score #gm_base_x {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:multiplayer game.map.base_coordinates[2]

data modify storage {ns}:temp _oob_iter set from storage {ns}:multiplayer game.map.out_of_bounds
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/multiplayer/summon_oob_iter
""")
	write_versioned_function("multiplayer/summon_oob_iter", f"""
execute store result score #_rx {ns}.data run data get storage {ns}:temp _oob_iter[0][0]
execute store result score #_ry {ns}.data run data get storage {ns}:temp _oob_iter[0][1]
execute store result score #_rz {ns}.data run data get storage {ns}:temp _oob_iter[0][2]
scoreboard players operation #_rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _oob_pos.x double 1 run scoreboard players get #_rx {ns}.data
execute store result storage {ns}:temp _oob_pos.y double 1 run scoreboard players get #_ry {ns}.data
execute store result storage {ns}:temp _oob_pos.z double 1 run scoreboard players get #_rz {ns}.data
function {ns}:v{version}/multiplayer/summon_oob_at with storage {ns}:temp _oob_pos
data remove storage {ns}:temp _oob_iter[0]
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/multiplayer/summon_oob_iter
""")
	write_versioned_function("multiplayer/summon_oob_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.oob_point","{ns}.gm_entity"]}}
""")

	# ── Spawn Point Markers ───────────────────────────────────────

	## Summon spawn markers from map data (called at game start)
	write_versioned_function("multiplayer/summon_spawns", f"""
# Red spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:multiplayer game.map.spawning_points.red
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_red"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/multiplayer/summon_spawn_iter

# Blue spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:multiplayer game.map.spawning_points.blue
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_blue"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/multiplayer/summon_spawn_iter

# General spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:multiplayer game.map.spawning_points.general
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_general"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/multiplayer/summon_spawn_iter
""")

	write_versioned_function("multiplayer/summon_spawn_iter", f"""
# Read relative coords
execute store result score #_sx {ns}.data run data get storage {ns}:temp _spawn_iter[0][0]
execute store result score #_sy {ns}.data run data get storage {ns}:temp _spawn_iter[0][1]
execute store result score #_sz {ns}.data run data get storage {ns}:temp _spawn_iter[0][2]
execute store result score #_syaw {ns}.data run data get storage {ns}:temp _spawn_iter[0][3] 100

# Convert to absolute
scoreboard players operation #_sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_sz {ns}.data += #gm_base_z {ns}.data

# Store position + yaw for macro
execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #_sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #_sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #_sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #_syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

# Summon
function {ns}:v{version}/multiplayer/summon_spawn_at with storage {ns}:temp _spos

# Next
data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/multiplayer/summon_spawn_iter
""")

	write_versioned_function("multiplayer/summon_spawn_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.spawn_point","$(tag)","{ns}.gm_entity"],data:{{yaw:$(yaw)}}}}
""")

	# ── Smart Spawn Selection ─────────────────────────────────────

	## TP all players to spawn points at game start
	write_versioned_function("multiplayer/tp_all_to_spawns", f"""
# FFA: everyone uses general spawns
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}

# Team modes: TP by team
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}

# Players with no team: use general spawns
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} as @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=0}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}
""")

	## Pick best spawn: find spawn marker farthest from any enemy player (run as player)
	write_versioned_function("multiplayer/pick_spawn", f"""
# Mark this player as needing a spawn
tag @s add {ns}.spawn_pending

# Tag enemy players (for distance calculation — ignore teammates)
# In FFA or team=0: all in-game players are "enemies" for spawn distance
execute if score @s {ns}.mp.team matches 0 run tag @a[scores={{{ns}.mp.in_game=1}}] add {ns}.spawn_enemy
# In team modes: only tag players on different teams
execute if score @s {ns}.mp.team matches 1 run tag @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=2..}}] add {ns}.spawn_enemy
execute if score @s {ns}.mp.team matches 2 run tag @a[scores={{{ns}.mp.in_game=1,{ns}.mp.team=..1}}] add {ns}.spawn_enemy
# Never count self as an enemy
tag @s remove {ns}.spawn_enemy

# Tag candidate spawn markers of the right type
$tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type)] add {ns}.spawn_candidate

# Remove candidates that have an enemy player within 5 blocks
execute as @e[tag={ns}.spawn_candidate] at @s if entity @a[tag={ns}.spawn_enemy,distance=..5] run tag @s remove {ns}.spawn_candidate

# If all were removed (all spawns contested), re-tag all as candidates
$execute unless entity @e[tag={ns}.spawn_candidate] run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_$(type)] add {ns}.spawn_candidate

# If no enemies, pick random candidate directly (skip expensive distance calc)
execute unless entity @a[tag={ns}.spawn_enemy] run return run function {ns}:v{version}/multiplayer/pick_spawn_random

# Limit to X random candidates before distance computation (optimization)
tag @e[tag={ns}.spawn_candidate,sort=random,limit=32] add {ns}.spawn_final
tag @e[tag={ns}.spawn_candidate,tag=!{ns}.spawn_final] remove {ns}.spawn_candidate
tag @e[tag={ns}.spawn_final] remove {ns}.spawn_final

# Compute distance² to nearest enemy player for each candidate
execute as @e[tag={ns}.spawn_candidate] at @s run function {ns}:v{version}/multiplayer/spawn_calc_dist

# Find the maximum distance score
scoreboard players set #_best_dist {ns}.data 0
scoreboard players operation #_best_dist {ns}.data > @e[tag={ns}.spawn_candidate] {ns}.data

# Pick the first candidate with that best score and TP the pending player there
execute as @e[tag={ns}.spawn_candidate,sort=random] if score @s {ns}.data = #_best_dist {ns}.data run function {ns}:v{version}/multiplayer/tp_to_spawn

# Clean up
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
tag @a[tag={ns}.spawn_enemy] remove {ns}.spawn_enemy
""")

	## Pick random spawn (no enemies — skip distance calc entirely)
	write_versioned_function("multiplayer/pick_spawn_random", f"""
execute as @e[tag={ns}.spawn_candidate,sort=random,limit=1] run function {ns}:v{version}/multiplayer/tp_to_spawn

# Clean up
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
tag @a[tag={ns}.spawn_enemy] remove {ns}.spawn_enemy
""")

	## Calculate distance² from spawn marker to nearest enemy player (run as marker at marker)
	write_versioned_function("multiplayer/spawn_calc_dist", f"""
# Get marker position
execute store result score #_mx {ns}.data run data get entity @s Pos[0]
execute store result score #_my {ns}.data run data get entity @s Pos[1]
execute store result score #_mz {ns}.data run data get entity @s Pos[2]

# Get nearest enemy player position (expensive — caller limits candidates)
data modify storage {ns}:temp _nearest set from entity @p[tag={ns}.spawn_enemy] Pos
execute store result score #_px {ns}.data run data get storage {ns}:temp _nearest[0]
execute store result score #_py {ns}.data run data get storage {ns}:temp _nearest[1]
execute store result score #_pz {ns}.data run data get storage {ns}:temp _nearest[2]

# dx, dy, dz
scoreboard players operation #_mx {ns}.data -= #_px {ns}.data
scoreboard players operation #_my {ns}.data -= #_py {ns}.data
scoreboard players operation #_mz {ns}.data -= #_pz {ns}.data

# distance = dx + dy + dz
scoreboard players operation #_mx {ns}.data += #_my {ns}.data
scoreboard players operation #_mx {ns}.data += #_mz {ns}.data

# Store on entity
scoreboard players operation @s {ns}.data = #_mx {ns}.data
""")

	## TP player to chosen spawn marker (run as the marker)
	write_versioned_function("multiplayer/tp_to_spawn", f"""
# Store marker position and yaw for macro
execute store result storage {ns}:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage {ns}:temp _tp.yaw set from entity @s data.yaw

# TP the pending player
execute as @p[tag={ns}.spawn_pending] run function {ns}:v{version}/multiplayer/tp_player_at with storage {ns}:temp _tp
""")

	## TP macro (run as the player to TP)
	write_versioned_function("multiplayer/tp_player_at", "$tp @s $(x) $(y) $(z) $(yaw) 0")

	## Respawn TP: use general spawns on respawn to prevent spawn camping (run as the respawning player)
	write_versioned_function("multiplayer/respawn_tp", f"""
function {ns}:v{version}/multiplayer/pick_spawn {{type:"general"}}
""")

	# ── Sidebar HUD ───────────────────────────────────────────────

	# Build sidebar content components for reuse
	sb_timer = (
		f'[{{text:" ⏱ ",color:"yellow"}},'
		f'["",{{score:{{name:"#_timer_min",objective:"{ns}.data"}},color:"yellow"}},'
		f'{{text:":",color:"yellow"}},'
		f'{{score:{{name:"#_timer_tens",objective:"{ns}.data"}},color:"yellow"}},'
		f'{{score:{{name:"#_timer_ones",objective:"{ns}.data"}},color:"yellow"}}]]'
	)
	sb_red = f'[{{text:" 🔴 ",color:"red"}},{{text:"Red",color:"red"}}," ",{{score:{{name:"#red",objective:"{ns}.mp.team"}},color:"white"}}]'
	sb_blue = f'[{{text:" 🔵 ",color:"blue"}},{{text:"Blue",color:"blue"}}," ",{{score:{{name:"#blue",objective:"{ns}.mp.team"}},color:"white"}}]'
	sb_limit = f'[{{text:" First to ",color:"gray"}},{{score:{{name:"#score_limit",objective:"{ns}.data"}},color:"white"}}]'
	sb_spacer = '" "'

	## Team sidebar (TDM/DOM/HP/SND) — takes $(title) macro arg
	write_versioned_function("multiplayer/create_sidebar_team", f"""
$function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"$(title)",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_red},{sb_blue},{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	## FFA sidebar
	write_versioned_function("multiplayer/create_sidebar_ffa", f"""
function #bs.sidebar:create {{objective:"{ns}.sidebar",display_name:{{text:"Free For All",color:"gold",bold:true}},contents:[{sb_timer},{sb_spacer},{sb_limit}]}}
scoreboard objectives setdisplay sidebar {ns}.sidebar
""")

	# ── Shooting Block During Prep ────────────────────────────────

	## Prepend to right_click: block shooting during prep phase
	write_versioned_function("player/right_click", f"""
# Block shooting during multiplayer prep phase
execute if score @s {ns}.mp.in_game matches 1 if data storage {ns}:multiplayer game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)

	# ── Prep Phase ────────────────────────────────────────────────

	## Prep tick: during 10s warmup, detect class changes and apply immediately
	write_versioned_function("multiplayer/prep_tick", f"""
# Check for class changes and apply immediately
execute as @a[scores={{{ns}.mp.in_game=1}}] unless score @s {ns}.mp.class = @s {ns}.mp.prev_class unless score @s {ns}.mp.class matches 0 at @s run function {ns}:v{version}/multiplayer/apply_class
execute as @a[scores={{{ns}.mp.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class
""")

	## End prep: unfreeze players, transition to active
	write_versioned_function("multiplayer/end_prep", f"""
# Only if still preparing (game might have been stopped)
execute unless data storage {ns}:multiplayer game{{state:"preparing"}} run return fail

# Restore movement
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.mp.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects
effect clear @a[scores={{{ns}.mp.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mp.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mp.in_game=1}}] night_vision

# Re-apply permanent saturation for the active game
effect give @a[scores={{{ns}.mp.in_game=1}}] saturation infinite 255 true

# Set state to active
data modify storage {ns}:multiplayer game.state set value "active"

# Announce
tellraw @a [{{"text":"","color":"green","bold":true}},"⚔ ",{{"text":"GO! GO! GO!"}}]
""")

