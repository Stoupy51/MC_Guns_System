
# ruff: noqa: E501
# Missions Game System
# Cooperative PvE game mode: players fight through 4 levels of enemies.
# Each level spawns enemies at predefined positions from the map editor.
# Clearing all enemies in a level advances to the next level.
# Completing all 4 levels = mission success.

from stewbeet import Mem, write_load_file, write_tag, write_tick_file, write_versioned_function

from ..helpers import MGS_TAG


def generate_missions_game() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Scoreboards & Storage Setup
	write_load_file(
f"""
## Missions scoreboards
# In-game flag (1 = active in mission)
scoreboard objectives add {ns}.mi.in_game dummy
# Current wave/level (1-4)
scoreboard objectives add {ns}.mi.level dummy
# Enemies remaining in current level
scoreboard objectives add {ns}.mi.enemies dummy
# Timer (ticks remaining, used for spawn delay between levels)
scoreboard objectives add {ns}.mi.timer dummy

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

# Initialize enemy config defaults if missing
execute unless data storage {ns}:missions game.map.enemy_config run data modify storage {ns}:missions game.map.enemy_config set value {{level_1:{{entity:"pillager",hp:20}},level_2:{{entity:"pillager",hp:40}},level_3:{{entity:"pillager",hp:60}},level_4:{{entity:"pillager",hp:80}}}}

# Set state to preparing
data modify storage {ns}:missions game.state set value "preparing"

# Reset scores
scoreboard players set @a {ns}.mi.in_game 0
scoreboard players set #mi_level {ns}.data 0
scoreboard players set #mi_enemies {ns}.data 0

# Tag all players as in-game
scoreboard players set @a {ns}.mi.in_game 1

# Enable class menu for mission players
tag @a[scores={{{ns}.mi.in_game=1}}] add {ns}.give_class_menu

# Set gamerules
gamemode adventure @a[scores={{{ns}.mi.in_game=1}}]
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

# Give loadout to players who already have a class
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

# Auto-apply default custom loadout if no class set
scoreboard players add @s {ns}.mp.class 0
execute as @a[scores={{{ns}.mi.in_game=1}}] at @s if score @s {ns}.mp.class matches 0 if score @s {ns}.mp.default matches 1.. run function {ns}:v{version}/multiplayer/auto_apply_default

# Show class selection
execute as @a[scores={{{ns}.mi.in_game=1}}] run function {ns}:v{version}/multiplayer/select_class

# Store current class for change detection
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mp.prev_class = @s {ns}.mp.class

# Schedule end of prep (10 seconds)
schedule function {ns}:v{version}/missions/end_prep 200t

# Announce
tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"Preparing! Choose your class! Mission starts in 10 seconds!","color":"yellow"}}]
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

	## End Prep → Start Level 1
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

# Announce
tellraw @a ["",{{"text":"","color":"aqua","bold":true}},"🎯 ",{{"text":"GO! GO! GO!"}}]

# Start level 1
scoreboard players set #mi_level {ns}.data 1
function {ns}:v{version}/missions/spawn_level
""")

	## Spawn enemies for the current level
	write_versioned_function("missions/spawn_level", f"""
# Announce current level
execute if score #mi_level {ns}.data matches 1 run tellraw @a ["",{{"text":"","color":"green","bold":true}},"  ▶ ",{{"text":"Level 1"}}]
execute if score #mi_level {ns}.data matches 2 run tellraw @a ["",{{"text":"","color":"yellow","bold":true}},"  ▶ ",{{"text":"Level 2"}}]
execute if score #mi_level {ns}.data matches 3 run tellraw @a ["",{{"text":"","color":"gold","bold":true}},"  ▶ ",{{"text":"Level 3"}}]
execute if score #mi_level {ns}.data matches 4 run tellraw @a ["",{{"text":"","color":"red","bold":true}},"  ▶ ",{{"text":"Level 4"}}]

# Store base coordinates for offset
execute store result score #gm_base_x {ns}.data run data get storage {ns}:missions game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:missions game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:missions game.map.base_coordinates[2]

# Reset enemy count
scoreboard players set #mi_enemies {ns}.data 0

# Dispatch to level-specific spawner
execute if score #mi_level {ns}.data matches 1 run function {ns}:v{version}/missions/spawn_level_1
execute if score #mi_level {ns}.data matches 2 run function {ns}:v{version}/missions/spawn_level_2
execute if score #mi_level {ns}.data matches 3 run function {ns}:v{version}/missions/spawn_level_3
execute if score #mi_level {ns}.data matches 4 run function {ns}:v{version}/missions/spawn_level_4

# Give a random gun to all enemies that don't have any gun
execute as @e[tag={ns}.mission_enemy] unless items entity @s weapon.mainhand * run function {ns}:v{version}/utils/random_weapon {{slot:"weapon.mainhand"}}
""")

	## Per-level spawn functions
	for level in range(1, 5):
		write_versioned_function(f"missions/spawn_level_{level}", f"""
# Copy enemy positions for iteration
data modify storage {ns}:temp _enemy_iter set from storage {ns}:missions game.map.enemies.level_{level}

# Copy enemy config for this level
data modify storage {ns}:temp _enemy_config set from storage {ns}:missions game.map.enemy_config.level_{level}

# Iterate and spawn
execute if data storage {ns}:temp _enemy_iter[0] run function {ns}:v{version}/missions/spawn_enemy_iter
""")

	## Spawn enemy iterator (reusable across levels)
	write_versioned_function("missions/spawn_enemy_iter", f"""
# Read relative coordinates
execute store result score #_ex {ns}.data run data get storage {ns}:temp _enemy_iter[0][0]
execute store result score #_ey {ns}.data run data get storage {ns}:temp _enemy_iter[0][1]
execute store result score #_ez {ns}.data run data get storage {ns}:temp _enemy_iter[0][2]

# Convert to absolute
scoreboard players operation #_ex {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_ey {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_ez {ns}.data += #gm_base_z {ns}.data

# Store for macro
execute store result storage {ns}:temp _epos.x double 1 run scoreboard players get #_ex {ns}.data
execute store result storage {ns}:temp _epos.y double 1 run scoreboard players get #_ey {ns}.data
execute store result storage {ns}:temp _epos.z double 1 run scoreboard players get #_ez {ns}.data

# Copy entity type and HP from config
data modify storage {ns}:temp _epos.entity set from storage {ns}:temp _enemy_config.entity
data modify storage {ns}:temp _epos.hp set from storage {ns}:temp _enemy_config.hp

# Summon
function {ns}:v{version}/missions/summon_enemy with storage {ns}:temp _epos

# Increment enemy count
scoreboard players add #mi_enemies {ns}.data 1

# Next
data remove storage {ns}:temp _enemy_iter[0]
execute if data storage {ns}:temp _enemy_iter[0] run function {ns}:v{version}/missions/spawn_enemy_iter
""")

	## Summon a single enemy at position (macro)
	write_versioned_function("missions/summon_enemy", f"""
$summon $(entity) $(x) $(y) $(z) {{Tags:["{ns}.mission_enemy","{ns}.gm_entity"],DeathLootTable:"minecraft:empty",attributes:[{{id:"minecraft:max_health",base:$(hp)}}],Health:$(hp)f}}
""")

	## Game Tick
	write_tick_file(f"""
# Missions game tick
execute if data storage {ns}:missions game{{state:"active"}} run function {ns}:v{version}/missions/game_tick
execute if data storage {ns}:missions game{{state:"preparing"}} run function {ns}:v{version}/missions/prep_tick
""")

	write_versioned_function("missions/game_tick", f"""
# Boundary enforcement (skip players with respawn protection)
execute as @e[type=player,scores={{{ns}.mi.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/missions/check_bounds

# OOB check
execute as @e[type=player,scores={{{ns}.mi.in_game=1,{ns}.mp.death_count=0}},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag={ns}.oob_point,distance=..5] run kill @s

# Check if all enemies are dead (level transition)
execute unless entity @e[tag={ns}.mission_enemy] if score #mi_level {ns}.data matches 1..4 run function {ns}:v{version}/missions/level_cleared
""")

	## Boundary check
	write_versioned_function("missions/check_bounds", f"""
data modify storage {ns}:temp _player_pos set from entity @s Pos
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _player_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _player_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _player_pos[2]

execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run kill @s
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run kill @s
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run kill @s
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run kill @s
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run kill @s
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run kill @s
""")

	## Level Cleared → advance or win
	write_versioned_function("missions/level_cleared", f"""
# Check if all 4 levels are done
execute if score #mi_level {ns}.data matches 4 run return run function {ns}:v{version}/missions/victory

# Announce
execute if score #mi_level {ns}.data matches 1 run tellraw @a ["",{{"text":"","color":"green","bold":true}},"  ✔ ",{{"text":"Level 1 Cleared!"}}]
execute if score #mi_level {ns}.data matches 2 run tellraw @a ["",{{"text":"","color":"yellow","bold":true}},"  ✔ ",{{"text":"Level 2 Cleared!"}}]
execute if score #mi_level {ns}.data matches 3 run tellraw @a ["",{{"text":"","color":"gold","bold":true}},"  ✔ ",{{"text":"Level 3 Cleared!"}}]

# Advance to next level after short delay (3 seconds)
scoreboard players add #mi_level {ns}.data 1
schedule function {ns}:v{version}/missions/spawn_level 60t
""")

	## Victory!
	write_versioned_function("missions/victory", f"""
tellraw @a ["",{{"text":"","color":"gold","bold":true}},"🏆 ",{{"text":"Mission Complete!"}}]
tellraw @a [{MGS_TAG},{{"text":"All levels cleared! Well done!","color":"green"}}]

# End game
function {ns}:v{version}/missions/stop
""")

	## Game Stop
	write_versioned_function("missions/stop", f"""
# Set state to lobby
data modify storage {ns}:missions game.state set value "lobby"

# Cancel scheduled functions
schedule clear {ns}:v{version}/missions/end_prep
schedule clear {ns}:v{version}/missions/spawn_level

# Restore movement
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42

# Clear effects
effect clear @a[scores={{{ns}.mi.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mi.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mi.in_game=1}}] night_vision

# Kill all mission entities (enemies + markers)
kill @e[tag={ns}.mission_enemy]
kill @e[tag={ns}.gm_entity]

# Signal mission end
function #{ns}:missions/on_mission_end

# Announce
tellraw @a [{MGS_TAG},{{"text":"Mission ended.","color":"red"}}]

# Reset in-game state
scoreboard players set @a {ns}.mi.in_game 0
scoreboard players set #mi_level {ns}.data 0
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
execute as @e[tag={ns}.spawn_candidate,sort=random,limit=1] run function {ns}:v{version}/missions/tp_to_spawn

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
