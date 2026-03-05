
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

# Initialize team scores (only if not already set)
execute unless score #red {ns}.mp.team matches -2147483648.. run scoreboard players set #red {ns}.mp.team 0
execute unless score #blue {ns}.mp.team matches -2147483648.. run scoreboard players set #blue {ns}.mp.team 0

# Initialize game state (only if not yet set)
execute unless data storage {ns}:multiplayer game run data modify storage {ns}:multiplayer game set value {{state:"lobby",gamemode:"tdm",score_limit:30,time_limit:12000,map_id:"hijacked"}}

# Constants for timer math
scoreboard players set #20 {ns}.data 20
scoreboard players set #60 {ns}.data 60
""")

	## Signal function tags
	for event in ["register_maps", "register_classes", "on_game_start", "on_game_end"]:
		write_tag(f"multiplayer/{event}", Mem.ctx.data[ns].function_tags, [])

	## Game Start (requires a map to be loaded first)
	write_versioned_function("multiplayer/start",
f"""
# Prevent starting if already active
execute if data storage {ns}:multiplayer game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"Game already in progress!","color":"red"}}]

# Load the selected map (reads map_id from game storage)
function {ns}:v{version}/multiplayer/load_map_from_storage with storage {ns}:multiplayer game
execute unless score #map_load_found {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"No map found! Select a map first.","color":"red"}}]

# Copy loaded map data into game state
data modify storage {ns}:multiplayer game.map set from storage {ns}:temp map_load.result

# Initialize game
data modify storage {ns}:multiplayer game.state set value "active"

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

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set, otherwise show class dialog
execute as @a at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default
execute as @a at @s if score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/select_class

# Announce
tellraw @a ["",[{{"text":"","color":"gold","bold":true}},"⚔ ",{{"text":"Game Started"}},"! "],{{"text":"Pick your class!","color":"yellow"}}]
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
	write_versioned_function("multiplayer/stop",
f"""
# End game
data modify storage {ns}:multiplayer game.state set value "lobby"

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

# Clear in-game state
scoreboard players set @a {ns}.mp.in_game 0
scoreboard players set @a {ns}.mp.team 0
""")

	## Kill Tracking (Signal Listener) - now dispatches to gamemode
	write_versioned_function("multiplayer/on_kill_signal",
f"""
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
	write_versioned_function("multiplayer/team_wins",
f"""
# Announce winner
$tellraw @a ["",{{"text":"🏆 ","color":"gold"}},{{"text":"$(team) Team Wins!","color":"gold","bold":true}}]
tellraw @a ["",[{{"text":"","color":"gray"}},"  ",{{"text":"Final Score - Red"}},": "],{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"red"}},[{{"text":"","color":"gray"}}," ",{{"text":"vs Blue"}},": "],{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"blue"}}]

# End game
function {ns}:v{version}/multiplayer/stop
""")

	# ── Game Tick (runs once per server tick when game is active) ──
	write_tick_file(f"""
# Multiplayer game tick (only when active)
execute if data storage {ns}:multiplayer game{{state:"active"}} run function {ns}:v{version}/multiplayer/game_tick
""")

	write_versioned_function("multiplayer/game_tick",
f"""
# ── Timer ──
scoreboard players remove #mp_timer {ns}.data 1

# Timer display every second (20 ticks)
execute store result score #_tick_mod {ns}.data run scoreboard players get #mp_timer {ns}.data
scoreboard players operation #_tick_mod {ns}.data %= #20 {ns}.data
execute if score #_tick_mod {ns}.data matches 0 run function {ns}:v{version}/multiplayer/timer_display

# Time's up
execute if score #mp_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/time_up

# ── Boundary enforcement (for all in-game players) ──
execute as @a[scores={{{ns}.mp.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/multiplayer/check_bounds

# ── Out-of-bounds check ──
execute as @a[scores={{{ns}.mp.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag={ns}.oob_point,distance=..5] run function {ns}:v{version}/multiplayer/oob_kill

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

# Display (only show when < 30 seconds remain as warning)
execute if score #_timer_sec {ns}.data matches ..30 as @a[scores={{{ns}.mp.in_game=1}}] run title @s actionbar [{{"text":"⏱ ","color":"red"}},{{"score":{{"name":"#_timer_sec","objective":"{ns}.data"}},"color":"red"}},{{"text":"s","color":"red"}}]
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
execute store result score @s {ns}.mp.bx run data get entity @s Pos[0]
execute store result score @s {ns}.mp.by run data get entity @s Pos[1]
execute store result score @s {ns}.mp.bz run data get entity @s Pos[2]

# Check if outside boundaries (any axis out of range = OOB)
execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run function {ns}:v{version}/multiplayer/bounds_kill
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run function {ns}:v{version}/multiplayer/bounds_kill
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
