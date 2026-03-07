
# ruff: noqa: E501
# Missions Game System
# Cooperative PvE game mode: all enemies spawn at game start, players kill them all.
# Enemy positions and spawn functions are stored per-map via the editor.
# When all enemies are killed, the game ends with a performance score.

from stewbeet import Mem, write_load_file, write_tag, write_tick_file, write_versioned_function

from ..helpers import MGS_TAG


def generate_missions_game() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Scoreboards & Storage Setup
	write_load_file(
f"""
## Missions scoreboards
scoreboard objectives add {ns}.mi.in_game dummy
scoreboard objectives add {ns}.mi.timer dummy
scoreboard objectives add {ns}.mi.total_enemies dummy
scoreboard objectives add {ns}.mi.kills dummy
scoreboard objectives add {ns}.mi.deaths dummy

# Boundary checking coords (reuse mp prefix scores)
scoreboard objectives add {ns}.mp.bx dummy
scoreboard objectives add {ns}.mp.by dummy
scoreboard objectives add {ns}.mp.bz dummy

# Constants
scoreboard players set #20 {ns}.data 20
scoreboard players set #60 {ns}.data 60

# Initialize missions game state
execute unless data storage {ns}:missions game run data modify storage {ns}:missions game set value {{state:"lobby",map_id:""}}
""")

	## Signal function tags
	for event in ["on_mission_start", "on_mission_end"]:
		write_tag(f"missions/{event}", Mem.ctx.data[ns].function_tags, [])

	## Game Start
	write_versioned_function("missions/start", f"""
# Prevent starting if already active or preparing
execute if data storage {ns}:missions game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"Mission already in progress!","color":"red"}}]
execute if data storage {ns}:missions game{{state:"preparing"}} run return run tellraw @s [{MGS_TAG},{{"text":"Mission already preparing!","color":"red"}}]

# Check that a map is selected
execute if data storage {ns}:missions game{{map_id:""}} run return run tellraw @s [{MGS_TAG},{{"text":"No map selected! Use the setup menu to select a mission map.","color":"red"}}]

# Load the selected map
function {ns}:v{version}/missions/load_map_from_storage with storage {ns}:missions game
execute unless score #map_load_found {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"Map not found! Select a valid mission map.","color":"red"}}]

# Copy loaded map data into game state
data modify storage {ns}:missions game.map set from storage {ns}:temp map_load.result

# Set state to preparing
data modify storage {ns}:missions game.state set value "preparing"

# Reset scores
scoreboard players set @a {ns}.mi.in_game 0
scoreboard players set #mi_timer {ns}.data 0
scoreboard players set #mi_total_enemies {ns}.data 0
scoreboard players set @a {ns}.mi.kills 0
scoreboard players set @a {ns}.mi.deaths 0

# Tag all team 1 players as in-game (multiplayer support)
execute if entity @a[scores={{{ns}.mp.team=1}}] as @a[scores={{{ns}.mp.team=1}}] run scoreboard players set @s {ns}.mi.in_game 1
# Fallback: if no team system, tag all players
execute unless entity @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players set @a {ns}.mi.in_game 1

# Enable class menu for mission players
tag @a[scores={{{ns}.mi.in_game=1}}] add {ns}.give_class_menu

# Set gamerules
gamemode spectator @a[scores={{{ns}.mi.in_game=1}}]
gamerule immediate_respawn true
gamerule keep_inventory true

# Store base coordinates for offset
execute store result score #gm_base_x {ns}.data run data get storage {ns}:missions game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:missions game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:missions game.map.base_coordinates[2]

# Normalize and store boundaries
execute store result score #bound_x1 {ns}.data run data get storage {ns}:missions game.map.boundaries[0][0]
execute store result score #bound_y1 {ns}.data run data get storage {ns}:missions game.map.boundaries[0][1]
execute store result score #bound_z1 {ns}.data run data get storage {ns}:missions game.map.boundaries[0][2]
execute store result score #bound_x2 {ns}.data run data get storage {ns}:missions game.map.boundaries[1][0]
execute store result score #bound_y2 {ns}.data run data get storage {ns}:missions game.map.boundaries[1][1]
execute store result score #bound_z2 {ns}.data run data get storage {ns}:missions game.map.boundaries[1][2]
scoreboard players operation #bound_x1 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y1 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z1 {ns}.data += #gm_base_z {ns}.data
scoreboard players operation #bound_x2 {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #bound_y2 {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bound_z2 {ns}.data += #gm_base_z {ns}.data
function {ns}:v{version}/missions/normalize_bounds

# Forceload the mission area to ensure chunks are loaded
function {ns}:v{version}/missions/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #gm_base_z {ns}.data
execute as @a[scores={{{ns}.mi.in_game=1}}] run function {ns}:v{version}/missions/tp_to_base with storage {ns}:temp _tp

# Schedule preload completion after 1 second
schedule function {ns}:v{version}/missions/preload_complete 20t

# Announce
tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"Loading mission area...","color":"yellow"}}]
""")

	## Teleport to base coordinates (macro)
	write_versioned_function("missions/tp_to_base", """
$tp @s $(x) $(y) $(z)
""")

	## Preload complete → transition to prep phase
	write_versioned_function("missions/preload_complete", f"""
# Guard: only if still preparing
execute unless data storage {ns}:missions game{{state:"preparing"}} run return fail

# Switch to adventure mode
gamemode adventure @a[scores={{{ns}.mi.in_game=1}}]

# Summon OOB markers
function {ns}:v{version}/missions/summon_oob

# Summon spawn point markers
function {ns}:v{version}/missions/summon_spawns

# Signal mission start
function #{ns}:missions/on_mission_start

# Teleport all players to mission spawns
function {ns}:v{version}/missions/tp_all_to_spawns

# Freeze players during prep
effect give @a[scores={{{ns}.mi.in_game=1}}] darkness 25 255 true
effect give @a[scores={{{ns}.mi.in_game=1}}] blindness 25 255 true
effect give @a[scores={{{ns}.mi.in_game=1}}] night_vision 25 255 true
effect give @a[scores={{{ns}.mi.in_game=1}}] saturation infinite 255 true
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:jump_strength base set 0
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:waypoint_receive_range base reset

# Give loadout to players who already have a class
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# Auto-apply default custom loadout if no class set
scoreboard players add @s {ns}.mp.class 0
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

# Show class selection
execute as @a[scores={{{ns}.mi.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# Store current class for change detection
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Schedule end of prep (9 seconds remaining)
schedule function {ns}:v{version}/missions/end_prep 180t

# Announce
tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"Preparing! Choose your class! Mission starts in 9 seconds!","color":"yellow"}}]
""")

	## Load map from storage
	write_versioned_function("missions/load_map_from_storage", f"""
$function {ns}:v{version}/maps/missions/load {{id:"$(map_id)",override:{{}}}}
""")

	## Normalize boundaries (reuse multiplayer pattern)
	write_versioned_function("missions/normalize_bounds", f"""
execute if score #bound_x1 {ns}.data > #bound_x2 {ns}.data run scoreboard players operation #_swap {ns}.data = #bound_x1 {ns}.data
execute if score #bound_x1 {ns}.data > #bound_x2 {ns}.data run scoreboard players operation #bound_x1 {ns}.data = #bound_x2 {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_x2 {ns}.data = #_swap {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players reset #_swap {ns}.data

execute if score #bound_y1 {ns}.data > #bound_y2 {ns}.data run scoreboard players operation #_swap {ns}.data = #bound_y1 {ns}.data
execute if score #bound_y1 {ns}.data > #bound_y2 {ns}.data run scoreboard players operation #bound_y1 {ns}.data = #bound_y2 {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_y2 {ns}.data = #_swap {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players reset #_swap {ns}.data

execute if score #bound_z1 {ns}.data > #bound_z2 {ns}.data run scoreboard players operation #_swap {ns}.data = #bound_z1 {ns}.data
execute if score #bound_z1 {ns}.data > #bound_z2 {ns}.data run scoreboard players operation #bound_z1 {ns}.data = #bound_z2 {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players operation #bound_z2 {ns}.data = #_swap {ns}.data
execute if score #_swap {ns}.data matches -2147483648.. run scoreboard players reset #_swap {ns}.data
""")

	## Prep Tick (check for class changes during preparation)
	write_versioned_function("missions/prep_tick", f"""
# Detect class changes during prep
execute as @a[scores={{{ns}.mi.in_game=1}}] unless score @s {ns}.mp.prev_class = @s {ns}.mp.class at @s run function {ns}:v{version}/multiplayer/apply_class
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class
""")

	## End Prep → Start Mission (spawn all enemies)
	write_versioned_function("missions/end_prep", f"""
# Guard: only if still preparing
execute unless data storage {ns}:missions game{{state:"preparing"}} run return fail

# Transition to active
data modify storage {ns}:missions game.state set value "active"

# Restore movement
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects
effect clear @a[scores={{{ns}.mi.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mi.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mi.in_game=1}}] night_vision

# Keep saturation
effect give @a[scores={{{ns}.mi.in_game=1}}] saturation infinite 255 true

# Spawn all enemies from map data
function {ns}:v{version}/missions/spawn_all_enemies

# Give compass pointing to nearest enemy (hotbar slot 3)
execute as @a[scores={{{ns}.mi.in_game=1}}] run item replace entity @s hotbar.3 with compass[custom_data={{{ns}:{{compass:true}}}}]

# Reset mission timer (counts up)
scoreboard players set #mi_timer {ns}.data 0

# Announce
tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"GO! GO! GO! Kill all enemies!"}}]
""")

	## Spawn all enemies at once from map data
	write_versioned_function("missions/spawn_all_enemies", f"""
# Copy enemy list for iteration
data modify storage {ns}:temp _enemy_iter set from storage {ns}:missions game.map.enemies

# Start iteration
execute if data storage {ns}:temp _enemy_iter[0] run function {ns}:v{version}/missions/spawn_enemy_iter

# Tag all newly spawned armed mobs as mission enemies
execute as @e[tag={ns}.armed,tag=!{ns}.mission_enemy] run tag @s add {ns}.mission_enemy
execute as @e[tag={ns}.mission_enemy] run tag @s add {ns}.gm_entity

# Store total enemy count
execute store result score #mi_total_enemies {ns}.data if entity @e[tag={ns}.mission_enemy]

# Announce count
tellraw @a [{MGS_TAG},{{"score":{{"name":"#mi_total_enemies","objective":"{ns}.data"}},"color":"yellow"}}," ",{{"text":"enemies spawned!","color":"gray"}}]
""")

	## Spawn enemy iterator
	write_versioned_function("missions/spawn_enemy_iter", f"""
# Read relative position
execute store result score #_ex {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[0]
execute store result score #_ey {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[1]
execute store result score #_ez {ns}.data run data get storage {ns}:temp _enemy_iter[0].pos[2]

# Convert to absolute
scoreboard players operation #_ex {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_ey {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_ez {ns}.data += #gm_base_z {ns}.data

# Store absolute position for macro
execute store result storage {ns}:temp _epos.x double 1 run scoreboard players get #_ex {ns}.data
execute store result storage {ns}:temp _epos.y double 1 run scoreboard players get #_ey {ns}.data
execute store result storage {ns}:temp _epos.z double 1 run scoreboard players get #_ez {ns}.data

# Copy the function path
data modify storage {ns}:temp _epos.function set from storage {ns}:temp _enemy_iter[0].function

# Call the mob function at the absolute position
function {ns}:v{version}/missions/call_enemy_function with storage {ns}:temp _epos

# Next
data remove storage {ns}:temp _enemy_iter[0]
execute if data storage {ns}:temp _enemy_iter[0] run function {ns}:v{version}/missions/spawn_enemy_iter
""")

	## Call the stored mob function at a given position (macro)
	write_versioned_function("missions/call_enemy_function", """
$execute positioned $(x) $(y) $(z) run function $(function)
""")

	## Forceload / unload the mission boundary area
	write_versioned_function("missions/forceload_area", f"""
# Store boundary coords into storage for macro
execute store result storage {ns}:temp _fl.x1 int 1 run scoreboard players get #bound_x1 {ns}.data
execute store result storage {ns}:temp _fl.z1 int 1 run scoreboard players get #bound_z1 {ns}.data
execute store result storage {ns}:temp _fl.x2 int 1 run scoreboard players get #bound_x2 {ns}.data
execute store result storage {ns}:temp _fl.z2 int 1 run scoreboard players get #bound_z2 {ns}.data
function {ns}:v{version}/missions/forceload_add with storage {ns}:temp _fl
""")

	write_versioned_function("missions/forceload_add", """
$forceload add $(x1) $(z1) $(x2) $(z2)
""")

	write_versioned_function("missions/remove_forceload", f"""
# Store boundary coords into storage for macro
execute store result storage {ns}:temp _fl.x1 int 1 run scoreboard players get #bound_x1 {ns}.data
execute store result storage {ns}:temp _fl.z1 int 1 run scoreboard players get #bound_z1 {ns}.data
execute store result storage {ns}:temp _fl.x2 int 1 run scoreboard players get #bound_x2 {ns}.data
execute store result storage {ns}:temp _fl.z2 int 1 run scoreboard players get #bound_z2 {ns}.data
function {ns}:v{version}/missions/forceload_remove with storage {ns}:temp _fl
""")

	write_versioned_function("missions/forceload_remove", """
$forceload remove $(x1) $(z1) $(x2) $(z2)
""")

	## On Respawn (missions death handling - now with cooldown like multiplayer)
	write_versioned_function("missions/on_respawn", f"""
# Reset death counter & Increment mission death stats
scoreboard players set @s {ns}.mp.death_count 0
scoreboard players add @s {ns}.mi.deaths 1

# Set player to spectator mode for 3 seconds (60 ticks) before actual respawn
gamemode spectator @s
scoreboard players set @s {ns}.mp.spectate_timer 60

# Spectate a random alive in-game player
function {ns}:v{version}/missions/spectate_random_player

# Announce respawn delay to the dying player
title @s title [{{"text":"☠","color":"red"}}]
title @s subtitle [{{"text":"Respawning in 3 seconds...","color":"gray"}}]
""")

	## Spectate a random alive in-game player (fallback)
	write_versioned_function("missions/spectate_random_player", f"""
# Pick a random alive in-game player (not self, not spectator)
execute as @r[scores={{{ns}.mi.in_game=1}},gamemode=!spectator] run spectate @s @p[scores={{{ns}.mp.spectate_timer=1..}},sort=nearest]
""")

	## Actual respawn: called when spectate timer reaches 0
	write_versioned_function("missions/actual_respawn", f"""
# Stop spectating
spectate @s

# Switch back to adventure
gamemode adventure @s

# Teleport to random mission spawn point
function {ns}:v{version}/missions/respawn_tp

# Re-apply saturation
effect give @s saturation infinite 255 true

# Re-apply class loadout (lost on death)
execute unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# Re-give compass
item replace entity @s hotbar.3 with compass[custom_data={{{ns}:{{compass:true}}}}]
""")

	## Game Tick
	write_tick_file(f"""
# Missions game tick
execute if data storage {ns}:missions game{{state:"active"}} run function {ns}:v{version}/missions/game_tick
execute if data storage {ns}:missions game{{state:"preparing"}} run function {ns}:v{version}/missions/prep_tick
""")

	write_versioned_function("missions/game_tick", f"""
# ── Spectate Timer (3s respawn cooldown) ──
execute as @a[scores={{{ns}.mi.in_game=1,{ns}.mp.spectate_timer=1..}}] run scoreboard players remove @s {ns}.mp.spectate_timer 1
execute as @a[scores={{{ns}.mi.in_game=1,{ns}.mp.spectate_timer=0}},gamemode=spectator] at @s run function {ns}:v{version}/missions/actual_respawn

# Increment mission timer
scoreboard players add #mi_timer {ns}.data 1

# Boundary enforcement (skip spectators) & OOB Check
execute as @e[tag={ns}.mission_enemy] at @s run function {ns}:v{version}/missions/check_bounds
execute as @e[type=player,scores={{{ns}.mi.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/missions/check_bounds
execute as @e[type=player,scores={{{ns}.mi.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag={ns}.oob_point,distance=..5] run damage @s 10000 out_of_world

# Track enemy kills (total enemies - alive enemies)
execute store result score #_alive {ns}.data if entity @e[tag={ns}.mission_enemy]
scoreboard players operation #_mi_kills {ns}.data = #mi_total_enemies {ns}.data
scoreboard players operation #_mi_kills {ns}.data -= #_alive {ns}.data

# Update compass for all players (point to nearest enemy)
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s run function {ns}:v{version}/missions/update_compass
execute at @r[scores={{{ns}.mi.in_game=1}}] run kill @e[type=experience_orb,distance=..200]

# Check if all enemies are dead → victory
execute unless entity @e[tag={ns}.mission_enemy] run return run function {ns}:v{version}/missions/victory
""")

	## Boundary check
	write_versioned_function("missions/check_bounds", f"""
data modify storage {ns}:temp _player_pos set from entity @s Pos
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _player_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _player_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _player_pos[2]

execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run damage @s 10000 out_of_world
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run damage @s 10000 out_of_world
""")

	## Compass - points toward nearest enemy (runs as player at player)
	write_versioned_function("missions/update_compass", f"""
# Skip if no enemies remain
execute unless entity @e[tag={ns}.mission_enemy] run return fail

# Get nearest enemy position as ints
execute store result storage {ns}:temp _compass.x int 1 run data get entity @n[tag={ns}.mission_enemy] Pos[0]
execute store result storage {ns}:temp _compass.y int 1 run data get entity @n[tag={ns}.mission_enemy] Pos[1]
execute store result storage {ns}:temp _compass.z int 1 run data get entity @n[tag={ns}.mission_enemy] Pos[2]

# Update compass in hotbar slot 3
function {ns}:v{version}/missions/set_compass_target with storage {ns}:temp _compass
""")

	write_versioned_function("missions/set_compass_target", f"""
$item replace entity @s hotbar.3 with compass[lodestone_tracker={{target:{{pos:[I;$(x),$(y),$(z)],dimension:"minecraft:overworld"}},tracked:false}},custom_data={{{ns}:{{compass:true}}}}]
""")

	## Victory - all enemies killed!
	write_versioned_function("missions/victory", f"""
# Calculate time in seconds
scoreboard players operation #_mi_seconds {ns}.data = #mi_timer {ns}.data
scoreboard players operation #_mi_seconds {ns}.data /= #20 {ns}.data

# Calculate minutes and remaining seconds
scoreboard players operation #_mi_minutes {ns}.data = #_mi_seconds {ns}.data
scoreboard players operation #_mi_minutes {ns}.data /= #60 {ns}.data
scoreboard players operation #_mi_rem_sec {ns}.data = #_mi_seconds {ns}.data
scoreboard players operation #_mi_rem_sec {ns}.data %= #60 {ns}.data

# Title
title @a[scores={{{ns}.mi.in_game=1}}] times 10 80 20
title @a[scores={{{ns}.mi.in_game=1}}] title {{"text":"MISSION COMPLETE","color":"gold","bold":true}}
title @a[scores={{{ns}.mi.in_game=1}}] subtitle {{"text":"All enemies eliminated!","color":"green"}}

# Performance summary
tellraw @a ["","\\n",{{"text":"═══════ MISSION COMPLETE ═══════","color":"gold","bold":true}}]
tellraw @a ["",{{"text":"  ⏱ Time: ","color":"gray"}},{{"score":{{"name":"#_mi_minutes","objective":"{ns}.data"}},"color":"yellow"}},"m ",{{"score":{{"name":"#_mi_rem_sec","objective":"{ns}.data"}},"color":"yellow"}},"s"]
tellraw @a ["",{{"text":"  💀 Enemies killed: ","color":"gray"}},{{"score":{{"name":"#mi_total_enemies","objective":"{ns}.data"}},"color":"red"}}]

# Per-player stats
execute as @a[scores={{{ns}.mi.in_game=1}}] run tellraw @a ["",{{"text":"  🎖 ","color":"gray"}},{{"selector":"@s","color":"yellow"}}," — Kills: ",{{"score":{{"name":"@s","objective":"{ns}.mi.kills"}},"color":"green"}}," | Deaths: ",{{"score":{{"name":"@s","objective":"{ns}.mi.deaths"}},"color":"red"}}]

tellraw @a ["",{{"text":"═══════════════════════════════","color":"gold","bold":true}},"\\n"]

# End game
function {ns}:v{version}/missions/stop
""")

	## Game Stop
	write_versioned_function("missions/stop", f"""
# Set state to lobby
data modify storage {ns}:missions game.state set value "lobby"

# Cancel scheduled functions
schedule clear {ns}:v{version}/missions/end_prep

# Restore movement
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42

# Clear effects
effect clear @a[scores={{{ns}.mi.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mi.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mi.in_game=1}}] night_vision

# Remove compass from all players
clear @a[scores={{{ns}.mi.in_game=1}}] compass[custom_data~{{{ns}:{{compass:true}}}}]

# Kill all mission entities (enemies + markers)
kill @e[tag={ns}.mission_enemy]
kill @e[tag={ns}.gm_entity]

# Remove forceload
function {ns}:v{version}/missions/remove_forceload

# Signal mission end
function #{ns}:missions/on_mission_end

# Announce
tellraw @a [{MGS_TAG},{{"text":"Mission ended.","color":"red"}}]

# Reset in-game state
scoreboard players set @a {ns}.mi.in_game 0
scoreboard players set #mi_timer {ns}.data 0
scoreboard players set #mi_total_enemies {ns}.data 0
scoreboard players set @a {ns}.mi.kills 0
scoreboard players set @a {ns}.mi.deaths 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

	# ── Summon OOB markers ────────────────────────────────────────
	write_versioned_function("missions/summon_oob", f"""
execute store result score #gm_base_x {ns}.data run data get storage {ns}:missions game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:missions game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:missions game.map.base_coordinates[2]

data modify storage {ns}:temp _oob_iter set from storage {ns}:missions game.map.out_of_bounds
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/missions/summon_oob_iter
""")
	write_versioned_function("missions/summon_oob_iter", f"""
execute store result score #_rx {ns}.data run data get storage {ns}:temp _oob_iter[0][0]
execute store result score #_ry {ns}.data run data get storage {ns}:temp _oob_iter[0][1]
execute store result score #_rz {ns}.data run data get storage {ns}:temp _oob_iter[0][2]
scoreboard players operation #_rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _oob_pos.x double 1 run scoreboard players get #_rx {ns}.data
execute store result storage {ns}:temp _oob_pos.y double 1 run scoreboard players get #_ry {ns}.data
execute store result storage {ns}:temp _oob_pos.z double 1 run scoreboard players get #_rz {ns}.data
function {ns}:v{version}/missions/summon_oob_at with storage {ns}:temp _oob_pos
data remove storage {ns}:temp _oob_iter[0]
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/missions/summon_oob_iter
""")
	write_versioned_function("missions/summon_oob_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.oob_point","{ns}.gm_entity"]}}
""")

	# ── Spawn Point Markers ───────────────────────────────────────
	write_versioned_function("missions/summon_spawns", f"""
# Mission spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:missions game.map.spawning_points.mission
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_mission"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/missions/summon_spawn_iter
""")

	write_versioned_function("missions/summon_spawn_iter", f"""
execute store result score #_sx {ns}.data run data get storage {ns}:temp _spawn_iter[0][0]
execute store result score #_sy {ns}.data run data get storage {ns}:temp _spawn_iter[0][1]
execute store result score #_sz {ns}.data run data get storage {ns}:temp _spawn_iter[0][2]
execute store result score #_syaw {ns}.data run data get storage {ns}:temp _spawn_iter[0][3] 100

scoreboard players operation #_sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_sz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #_sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #_sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #_sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #_syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

function {ns}:v{version}/missions/summon_spawn_at with storage {ns}:temp _spos

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/missions/summon_spawn_iter
""")

	write_versioned_function("missions/summon_spawn_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.spawn_point","$(tag)","{ns}.gm_entity"],data:{{yaw:$(yaw)}}}}
""")

	# ── Smart Spawn Teleportation ─────────────────────────────────
	write_versioned_function("missions/tp_all_to_spawns", f"""
# Teleport all players to mission spawns (random selection)
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s run function {ns}:v{version}/missions/pick_spawn
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

	write_versioned_function("missions/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# Tag candidate spawns (exclude used)
tag @e[tag={ns}.spawn_point,tag={ns}.spawn_mission,tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# If all used, re-tag all
execute unless entity @e[tag={ns}.spawn_candidate] run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_mission] add {ns}.spawn_candidate

# Pick random candidate
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/missions/tp_to_spawn

# Cleanup
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

	write_versioned_function("missions/tp_to_spawn", f"""
execute store result storage {ns}:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage {ns}:temp _tp.yaw set from entity @s data.yaw

execute as @p[tag={ns}.spawn_pending] run function {ns}:v{version}/missions/tp_player_at with storage {ns}:temp _tp

execute unless data storage {ns}:missions game{{state:"active"}} run tag @s add {ns}.spawn_used
""")

	write_versioned_function("missions/tp_player_at", "$tp @s $(x) $(y) $(z) $(yaw) 0")

	## Respawn TP for missions (run as the respawning player)
	write_versioned_function("missions/respawn_tp", f"""
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_mission] run function {ns}:v{version}/missions/pick_spawn
""")
