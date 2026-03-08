
# ruff: noqa: E501
# Zombies Game System
# Wave-based survival mode with zombie spawning, points, perks, mystery box, wallbuys, doors, and traps.
# Map definitions are dynamic (stored in storage, registered via function tags).

from stewbeet import Mem, write_load_file, write_tag, write_tick_file, write_versioned_function

from ..helpers import MGS_TAG


def generate_zombies_game() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Scoreboards & Storage Setup
	write_load_file(
f"""
## Zombies scoreboards
scoreboard objectives add {ns}.zb.in_game dummy
scoreboard objectives add {ns}.zb.points dummy
scoreboard objectives add {ns}.zb.kills dummy
scoreboard objectives add {ns}.zb.downs dummy

# Perk scoreboards
# zb.passive: 0=none, 1=points_x1.2, 2=powerup_x1.5
# zb.ability: 0=none, 1=coward, 2=guardian
# Ability cooldown (0 = ready, 1+ = on cooldown in rounds remaining)
scoreboard objectives add {ns}.zb.passive dummy
scoreboard objectives add {ns}.zb.ability dummy
scoreboard objectives add {ns}.zb.ability_cd dummy
scoreboard objectives add {ns}.zb.perk.juggernog dummy
scoreboard objectives add {ns}.zb.perk.speed_cola dummy
scoreboard objectives add {ns}.zb.perk.double_tap dummy
scoreboard objectives add {ns}.zb.perk.quick_revive dummy
# TODO: more perks?

# Constants
scoreboard players set #20 {ns}.data 20
scoreboard players set #60 {ns}.data 60
scoreboard players set #100 {ns}.data 100
scoreboard players set #150 {ns}.data 150
scoreboard players set #4 {ns}.data 4

# Initialize zombies game state
execute unless data storage {ns}:zombies game run data modify storage {ns}:zombies game set value {{state:"lobby",map_id:"",round:0}}

# Initialize mystery box base pool (can be extended via function tag)
execute unless data storage {ns}:zombies mystery_box_pool run data modify storage {ns}:zombies mystery_box_pool set value []

# Config: points per kill, points per hit
execute unless score #zb_points_kill {ns}.config matches 1.. run scoreboard players set #zb_points_kill {ns}.config 100
execute unless score #zb_points_hit {ns}.config matches 1.. run scoreboard players set #zb_points_hit {ns}.config 10
execute unless score #zb_mystery_box_price {ns}.config matches 1.. run scoreboard players set #zb_mystery_box_price {ns}.config 950
""")

	## Signal function tags
	for event in ["register_maps", "register_mystery_box_item", "on_round_start", "on_round_end", "on_game_start", "on_game_end"]:
		write_tag(f"zombies/{event}", Mem.ctx.data[ns].function_tags, [])

	## Game Start
	write_versioned_function("zombies/start", f"""
# Prevent starting if already active or preparing
execute if data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"Zombies game already in progress!","color":"red"}}]
execute if data storage {ns}:zombies game{{state:"preparing"}} run return run tellraw @s [{MGS_TAG},{{"text":"Zombies game already preparing!","color":"red"}}]

# Check that a map is selected
execute unless data storage {ns}:zombies game.map_id run return run tellraw @s [{MGS_TAG},{{"text":"No map selected! Use the setup menu to select a zombies map.","color":"red"}}]
execute if data storage {ns}:zombies game{{map_id:""}} run return run tellraw @s [{MGS_TAG},{{"text":"No map selected! Use the setup menu to select a zombies map.","color":"red"}}]

# Load the selected map
function {ns}:v{version}/zombies/load_map_from_storage with storage {ns}:zombies game
execute unless score #map_load_found {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"Map not found! Select a valid zombies map.","color":"red"}}]

# Copy loaded map data into game state
data modify storage {ns}:zombies game.map set from storage {ns}:temp map_load.result

# Set state to preparing
data modify storage {ns}:zombies game.state set value "preparing"

# Reset scores
scoreboard players set @a {ns}.zb.in_game 0
scoreboard players set @a {ns}.zb.points 500
scoreboard players set @a {ns}.zb.kills 0
scoreboard players set @a {ns}.zb.downs 0
scoreboard players set @a {ns}.zb.passive 0
scoreboard players set @a {ns}.zb.ability 0
scoreboard players set @a {ns}.zb.ability_cd 0

# Tag all players as in-game
scoreboard players set @a {ns}.zb.in_game 1

# Reset death counters and spectate timers to prevent false triggers
scoreboard players set @a {ns}.mp.death_count 0
scoreboard players set @a {ns}.mp.spectate_timer 0

# Set gamerules
gamemode spectator @a[scores={{{ns}.zb.in_game=1}}]
gamerule immediate_respawn true
gamerule keep_inventory true

# Initialize round to 0 (first round will be 1)
data modify storage {ns}:zombies game.round set value 0

# Store base coordinates for offset
execute store result score #gm_base_x {ns}.data run data get storage {ns}:zombies game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:zombies game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:zombies game.map.base_coordinates[2]

# Check if map has boundaries defined
scoreboard players set #zb_has_bounds {ns}.data 0
execute if data storage {ns}:zombies game.map.boundaries[0] run scoreboard players set #zb_has_bounds {ns}.data 1

# Normalize and store boundaries (only if defined)
execute if score #zb_has_bounds {ns}.data matches 1 store result score #bound_x1 {ns}.data run data get storage {ns}:zombies game.map.boundaries[0][0]
execute if score #zb_has_bounds {ns}.data matches 1 store result score #bound_y1 {ns}.data run data get storage {ns}:zombies game.map.boundaries[0][1]
execute if score #zb_has_bounds {ns}.data matches 1 store result score #bound_z1 {ns}.data run data get storage {ns}:zombies game.map.boundaries[0][2]
execute if score #zb_has_bounds {ns}.data matches 1 store result score #bound_x2 {ns}.data run data get storage {ns}:zombies game.map.boundaries[1][0]
execute if score #zb_has_bounds {ns}.data matches 1 store result score #bound_y2 {ns}.data run data get storage {ns}:zombies game.map.boundaries[1][1]
execute if score #zb_has_bounds {ns}.data matches 1 store result score #bound_z2 {ns}.data run data get storage {ns}:zombies game.map.boundaries[1][2]
execute if score #zb_has_bounds {ns}.data matches 1 run scoreboard players operation #bound_x1 {ns}.data += #gm_base_x {ns}.data
execute if score #zb_has_bounds {ns}.data matches 1 run scoreboard players operation #bound_y1 {ns}.data += #gm_base_y {ns}.data
execute if score #zb_has_bounds {ns}.data matches 1 run scoreboard players operation #bound_z1 {ns}.data += #gm_base_z {ns}.data
execute if score #zb_has_bounds {ns}.data matches 1 run scoreboard players operation #bound_x2 {ns}.data += #gm_base_x {ns}.data
execute if score #zb_has_bounds {ns}.data matches 1 run scoreboard players operation #bound_y2 {ns}.data += #gm_base_y {ns}.data
execute if score #zb_has_bounds {ns}.data matches 1 run scoreboard players operation #bound_z2 {ns}.data += #gm_base_z {ns}.data
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/zombies/normalize_bounds

# Forceload the area (only if bounds defined)
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/zombies/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #gm_base_z {ns}.data
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/tp_to_base with storage {ns}:temp _tp

# Register custom maps and mystery box items (extension points)
function #{ns}:zombies/register_maps
function #{ns}:zombies/register_mystery_box_item

# Schedule preload completion after 1 second
schedule function {ns}:v{version}/zombies/preload_complete 20t

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Loading zombies map...","color":"yellow"}}]
""")

	## Teleport to base coordinates (macro)
	write_versioned_function("zombies/tp_to_base", """
$tp @s $(x) $(y) $(z)
""")

	## Load map from storage
	write_versioned_function("zombies/load_map_from_storage", f"""
$function {ns}:v{version}/maps/zombies/load {{id:"$(map_id)",override:{{}}}}
""")

	## Normalize boundaries (reuse same logic as multiplayer/missions)
	write_versioned_function("zombies/normalize_bounds", f"""
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

	## Preload complete → transition to prep phase
	write_versioned_function("zombies/preload_complete", f"""
# Guard: only if still preparing
execute unless data storage {ns}:zombies game{{state:"preparing"}} run return fail

# Switch to adventure mode
gamemode adventure @a[scores={{{ns}.zb.in_game=1}}]

# Summon OOB markers (only if map has out_of_bounds data)
execute if data storage {ns}:zombies game.map.out_of_bounds run function {ns}:v{version}/zombies/summon_oob

# Summon spawn point markers for players
function {ns}:v{version}/zombies/summon_spawns

# Signal zombies game start
function #{ns}:zombies/on_game_start

# Teleport all players to player spawns
function {ns}:v{version}/zombies/tp_all_to_spawns

# Freeze players during prep
effect give @a[scores={{{ns}.zb.in_game=1}}] darkness 25 255 true
effect give @a[scores={{{ns}.zb.in_game=1}}] blindness 25 255 true
effect give @a[scores={{{ns}.zb.in_game=1}}] night_vision 25 255 true
effect give @a[scores={{{ns}.zb.in_game=1}}] saturation infinite 255 true
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base set 0

# Give starting weapon (M1911) to all players
clear @a[scores={{{ns}.zb.in_game=1}}]
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run loot give @s loot {ns}:i/m1911

# Show zombies perk selection menu
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/passive_ability_menu

# Schedule end of prep (9 seconds remaining)
schedule function {ns}:v{version}/zombies/end_prep 180t

# Initialize sidebar
function {ns}:v{version}/zombies/create_sidebar

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Preparing! Choose your perk! Round 1 starts in 9 seconds!","color":"yellow"}}]
""")

	## Prep Tick (no class to detect, just wait)
	write_versioned_function("zombies/prep_tick", """
# Nothing to process during prep (perk selection is instant via chat click)
""")

	## End Prep → Start Round 1
	write_versioned_function("zombies/end_prep", f"""
# Guard: only if still preparing
execute unless data storage {ns}:zombies game{{state:"preparing"}} run return fail

# Transition to active
data modify storage {ns}:zombies game.state set value "active"

# Restore movement
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects
effect clear @a[scores={{{ns}.zb.in_game=1}}] darkness
effect clear @a[scores={{{ns}.zb.in_game=1}}] blindness
effect clear @a[scores={{{ns}.zb.in_game=1}}] night_vision

# Keep saturation
effect give @a[scores={{{ns}.zb.in_game=1}}] saturation infinite 255 true

# Start round 1
function {ns}:v{version}/zombies/start_round
""")

	# ── Round System ──────────────────────────────────────────────

	## Start a new round
	write_versioned_function("zombies/start_round", f"""
# Increment round number
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data 1
execute store result storage {ns}:zombies game.round int 1 run scoreboard players get #zb_round {ns}.data

# Calculate zombies to spawn this round: base formula = round * 4 + (player_count - 1) * 2
execute store result score #zb_player_count {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
scoreboard players remove #zb_player_count {ns}.data 1
scoreboard players operation #zb_player_count {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data *= #4 {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data += #zb_player_count {ns}.data

# Store zombies to spawn and remaining count
scoreboard players operation #zb_remaining {ns}.data = #zb_to_spawn {ns}.data

# Set spawn timer (spawn a zombie every 2 seconds = 40 ticks)
scoreboard players set #zb_spawn_timer {ns}.data 20

# Grace period: don't check game over for 3 seconds (60 ticks)
scoreboard players set #zb_round_grace {ns}.data 60

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 40 10
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"Round ","color":"red","bold":true}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}}]

# Signal round start
function #{ns}:zombies/on_round_start

# Refresh sidebar
function {ns}:v{version}/zombies/refresh_sidebar

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" has begun!","color":"red"}}]
""")

	## Spawn a single zombie at a random zombie spawn point
	write_versioned_function("zombies/spawn_zombie", f"""
# Pick a random zombie spawn point (relative coordinates)
data modify storage {ns}:temp _zs_iter set from storage {ns}:zombies game.map.spawning_points.zombies

# Count available spawn points
execute store result score #_zs_count {ns}.data run data get storage {ns}:zombies game.map.spawning_points.zombies
execute if score #_zs_count {ns}.data matches ..0 run return fail

# Pick random index
execute store result score #_zs_idx {ns}.data run random value 0..100
scoreboard players operation #_zs_idx {ns}.data %= #_zs_count {ns}.data

# Iterate to that index
function {ns}:v{version}/zombies/spawn_zombie_at_idx
""")

	## Iterate to selected index and spawn
	write_versioned_function("zombies/spawn_zombie_at_idx", f"""
execute if score #_zs_idx {ns}.data matches 1.. run data remove storage {ns}:temp _zs_iter[0]
execute if score #_zs_idx {ns}.data matches 1.. run scoreboard players remove #_zs_idx {ns}.data 1
execute if score #_zs_idx {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_zombie_at_idx

# Now at the right index, read position
execute if score #_zs_idx {ns}.data matches 0 run function {ns}:v{version}/zombies/do_spawn_zombie
""")

	## Actually spawn the zombie at the chosen position
	write_versioned_function("zombies/do_spawn_zombie", f"""
# Read relative position
execute store result score #_zx {ns}.data run data get storage {ns}:temp _zs_iter[0][0]
execute store result score #_zy {ns}.data run data get storage {ns}:temp _zs_iter[0][1]
execute store result score #_zz {ns}.data run data get storage {ns}:temp _zs_iter[0][2]

# Convert to absolute
scoreboard players operation #_zx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_zy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_zz {ns}.data += #gm_base_z {ns}.data

# Store absolute position for macro
execute store result storage {ns}:temp _zpos.x double 1 run scoreboard players get #_zx {ns}.data
execute store result storage {ns}:temp _zpos.y double 1 run scoreboard players get #_zy {ns}.data
execute store result storage {ns}:temp _zpos.z double 1 run scoreboard players get #_zz {ns}.data

# Determine zombie level based on round
# Rounds 1-5: level 1, 6-10: level 2, 11-15: level 3, 16+: level 4
execute if score #zb_round {ns}.data matches ..5 run data modify storage {ns}:temp _zpos.level set value "1"
execute if score #zb_round {ns}.data matches 6..10 run data modify storage {ns}:temp _zpos.level set value "2"
execute if score #zb_round {ns}.data matches 11..15 run data modify storage {ns}:temp _zpos.level set value "3"
execute if score #zb_round {ns}.data matches 16.. run data modify storage {ns}:temp _zpos.level set value "4"

# Spawn the zombie
function {ns}:v{version}/zombies/summon_zombie_at with storage {ns}:temp _zpos
""")

	## Summon zombie at absolute position (macro)
	write_versioned_function("zombies/summon_zombie_at", f"""
# Summon a regular zombie (not armed)
$summon minecraft:zombie $(x) $(y) $(z) {{Tags:["{ns}.zombie_round","{ns}.gm_entity","{ns}.nukable"],CanPickUpLoot:false,PersistenceRequired:true}}

# Scale health based on round level
$execute as @e[tag={ns}.zombie_round,tag=!{ns}.zb_scaled,limit=1,sort=nearest] run function {ns}:v{version}/zombies/scale_zombie {{level:"$(level)"}}
""")

	write_versioned_function("zombies/scale_zombie", f"""
tag @s add {ns}.zb_scaled

$scoreboard players set #_zb_level {ns}.data $(level)

# Level 1: default 20 HP (rounds 1-5) — no changes needed
# Level 2: 30 HP (rounds 6-10)
execute if score #_zb_level {ns}.data matches 2 run attribute @s minecraft:max_health base set 30
execute if score #_zb_level {ns}.data matches 2 run data modify entity @s Health set value 30f

# Level 3: 40 HP (rounds 11-15)
execute if score #_zb_level {ns}.data matches 3 run attribute @s minecraft:max_health base set 40
execute if score #_zb_level {ns}.data matches 3 run data modify entity @s Health set value 40f

# Level 4: 60 HP (rounds 16+)
execute if score #_zb_level {ns}.data matches 4 run attribute @s minecraft:max_health base set 60
execute if score #_zb_level {ns}.data matches 4 run data modify entity @s Health set value 60f

# Increase speed slightly at higher levels
execute if score #_zb_level {ns}.data matches 3 run attribute @s minecraft:movement_speed base set 0.26
execute if score #_zb_level {ns}.data matches 4 run attribute @s minecraft:movement_speed base set 0.30
""")

	# ── Game Tick ─────────────────────────────────────────────────

	write_tick_file(f"""
# Zombies game tick
execute if data storage {ns}:zombies game{{state:"active"}} run function {ns}:v{version}/zombies/game_tick
execute if data storage {ns}:zombies game{{state:"preparing"}} run function {ns}:v{version}/zombies/prep_tick
""")

	write_versioned_function("zombies/game_tick", f"""
# ── Spectate Timer (3s respawn cooldown) ──
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.mp.spectate_timer=1..}}] run scoreboard players remove @s {ns}.mp.spectate_timer 1
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.mp.spectate_timer=0}},gamemode=spectator] at @s run function {ns}:v{version}/zombies/actual_respawn

# ── Zombie Spawning (if there are still zombies to spawn) ──
execute if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_tick

# ── Boundary enforcement (skip spectators, only if map has bounds) ──
execute if score #zb_has_bounds {ns}.data matches 1 as @e[tag={ns}.zombie_round] at @s run function {ns}:v{version}/zombies/check_bounds
execute if score #zb_has_bounds {ns}.data matches 1 as @e[type=player,scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/zombies/check_bounds

# ── Check round completion ──
execute store result score #_zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
execute if score #_zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 run function {ns}:v{version}/zombies/round_complete

# ── Check game over (all players down/spectator, but not during first 3 seconds) ──
execute if score #zb_round_grace {ns}.data matches 1.. run scoreboard players remove #zb_round_grace {ns}.data 1
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #_zb_alive_players {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. if score #_zb_alive_players {ns}.data matches 0 run function {ns}:v{version}/zombies/game_over

# ── Points display on actionbar (every 10 ticks) ──
execute store result score #_zb_tick_mod {ns}.data run random value 0..0
execute if score #_zb_tick_mod {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:v{version}/zombies/show_points_actionbar

# ── Refresh sidebar every second (20 ticks) ──
scoreboard players add #zb_sidebar_timer {ns}.data 1
execute if score #zb_sidebar_timer {ns}.data matches 20.. run scoreboard players set #zb_sidebar_timer {ns}.data 0
execute if score #zb_sidebar_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/refresh_sidebar
""")

	## Spawn tick: spawn zombies on a timer
	write_versioned_function("zombies/spawn_tick", f"""
# Decrease spawn timer
scoreboard players remove #zb_spawn_timer {ns}.data 1
execute if score #zb_spawn_timer {ns}.data matches 1.. run return 0

# Reset timer (spawn every 2 seconds)
scoreboard players set #zb_spawn_timer {ns}.data 40

# Spawn a zombie
function {ns}:v{version}/zombies/spawn_zombie

# Decrease count to spawn
scoreboard players remove #zb_to_spawn {ns}.data 1
""")

	## Boundary checks (reuse pattern from missions)
	write_versioned_function("zombies/check_bounds", f"""
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

	## Show points on actionbar
	write_versioned_function("zombies/show_points_actionbar", f"""
title @s actionbar [{{"text":"💰 ","color":"gold"}},{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"yellow"}},{{"text":" points","color":"gray"}}]
""")

	# ── Round Completion ──────────────────────────────────────────

	write_versioned_function("zombies/round_complete", f"""
# Signal round end
function #{ns}:zombies/on_round_end

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 40 10
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"Round Complete!","color":"green","bold":true}}]

# Give all players 500 bonus points for surviving the round
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run scoreboard players add @s {ns}.zb.points 500

# Announce
execute store result score #_completed_round {ns}.data run data get storage {ns}:zombies game.round
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#_completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! +500 points. Next round in 10 seconds...","color":"green"}}]

# Schedule next round after 10 seconds
schedule function {ns}:v{version}/zombies/start_round 200t
""")

	# ── Death & Respawn ───────────────────────────────────────────

	## On Respawn (zombies death handling - with cooldown)
	write_versioned_function("zombies/on_respawn", f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Increment down count
scoreboard players add @s {ns}.zb.downs 1

# Set player to spectator mode for 5 seconds (100 ticks) before actual respawn
gamemode spectator @s
scoreboard players set @s {ns}.mp.spectate_timer 100

# Spectate a random alive in-game player
function {ns}:v{version}/zombies/spectate_random_player

# Announce
title @s title [{{"text":"\\u2620","color":"red"}}]
title @s subtitle [{{"text":"Respawning in 5 seconds...","color":"gray"}}]
""")

	## Spectate a random alive in-game player
	write_versioned_function("zombies/spectate_random_player", f"""
execute as @r[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run spectate @s @p[scores={{{ns}.mp.spectate_timer=1..}},sort=nearest]
""")

	## Actual respawn: called when spectate timer reaches 0
	write_versioned_function("zombies/actual_respawn", f"""
# Stop spectating
spectate @s

# Switch back to adventure
gamemode adventure @s

# Teleport to random player spawn
function {ns}:v{version}/zombies/respawn_tp

# Re-apply saturation
effect give @s saturation infinite 255 true

# Re-give M1911 on respawn
loot give @s loot {ns}:i/m1911
""")

	## Add player tick hook for zombies death detection
	write_versioned_function("player/tick", f"""
# Zombies: detect respawn
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/zombies/on_respawn
""")

	# ── Game Over ─────────────────────────────────────────────────

	write_versioned_function("zombies/game_over", f"""
# Set state to ended
data modify storage {ns}:zombies game.state set value "ended"

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 80 20
title @a[scores={{{ns}.zb.in_game=1}}] title {{"text":"GAME OVER","color":"dark_red","bold":true}}

# Calculate final round
execute store result score #_final_round {ns}.data run data get storage {ns}:zombies game.round

# Performance summary
tellraw @a ["","\\n",{{"text":"═══════ GAME OVER ═══════","color":"dark_red","bold":true}}]
tellraw @a ["",{{"text":"  🧟 Final Round: ","color":"gray"}},{{"score":{{"name":"#_final_round","objective":"{ns}.data"}},"color":"red","bold":true}}]

# Per-player stats
execute as @a[scores={{{ns}.zb.in_game=1}}] run tellraw @a ["",{{"text":"  🎖 ","color":"gray"}},{{"selector":"@s","color":"yellow"}}," — Kills: ",{{"score":{{"name":"@s","objective":"{ns}.zb.kills"}},"color":"green"}}," | Downs: ",{{"score":{{"name":"@s","objective":"{ns}.zb.downs"}},"color":"red"}}," | Points: ",{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"gold"}}]

tellraw @a ["",{{"text":"═════════════════════════","color":"dark_red","bold":true}},"\\n"]

# Signal game end
function #{ns}:zombies/on_game_end

# End game after 5 seconds
schedule function {ns}:v{version}/zombies/stop 100t
""")

	# ── Game Stop ─────────────────────────────────────────────────

	write_versioned_function("zombies/stop", f"""
# Set state to lobby
data modify storage {ns}:zombies game.state set value "lobby"

# Cancel scheduled functions
schedule clear {ns}:v{version}/zombies/end_prep
schedule clear {ns}:v{version}/zombies/start_round

# Restore movement
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base set 0.42

# Clear effects
effect clear @a[scores={{{ns}.zb.in_game=1}}] darkness
effect clear @a[scores={{{ns}.zb.in_game=1}}] blindness
effect clear @a[scores={{{ns}.zb.in_game=1}}] night_vision

# Restore adventure mode for spectating players
gamemode adventure @a[scores={{{ns}.zb.in_game=1}},gamemode=spectator]

# Kill all zombies mode entities
kill @e[tag={ns}.zombie_round]
kill @e[tag={ns}.gm_entity]

# Remove forceload (only if bounds were set)
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/zombies/remove_forceload

# Remove sidebar
scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.zb_sidebar

# Announce
tellraw @a [{MGS_TAG},{{"text":"Zombies game ended.","color":"red"}}]

# Reset in-game state
scoreboard players set @a {ns}.zb.in_game 0
scoreboard players set @a {ns}.zb.points 0
scoreboard players set @a {ns}.zb.kills 0
scoreboard players set @a {ns}.zb.downs 0
scoreboard players set @a {ns}.zb.passive 0
scoreboard players set @a {ns}.zb.ability 0
scoreboard players set @a {ns}.zb.ability_cd 0
scoreboard players set @a {ns}.mp.spectate_timer 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

	# ── Kill Points ───────────────────────────────────────────────
	# Hook into the on_kill signal to add points when killing zombies
	write_versioned_function("zombies/on_kill_signal", f"""
# Only process if zombies game is active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Award kill points (with passive bonus if applicable)
scoreboard players operation @s {ns}.zb.points += #zb_points_kill {ns}.config

# Apply x1.2 points passive: add 20% extra (100 * 0.2 = 20 extra points per kill)
execute if score @s {ns}.zb.passive matches 1 run scoreboard players add @s {ns}.zb.points 20

scoreboard players add @s {ns}.zb.kills 1
""", tags=[f"{ns}:signals/on_kill"])

	# ── Passive & Ability Dialogs ─────────────────────────────────

	# Trigger values for zombies perks (dispatched in player_config.py)
	TRIG_ZB_PASSIVE_1 = 6   # x1.2 points
	TRIG_ZB_PASSIVE_2 = 7   # x1.5 powerups
	TRIG_ZB_ABILITY_1 = 8   # Coward
	TRIG_ZB_ABILITY_2 = 9   # Guardian

	write_versioned_function("zombies/passive_ability_menu", f"""
# Show the passive selection dialog (ability dialog is shown after)
dialog show @s {{type:"minecraft:multi_action",title:{{text:"Zonweeb Passive",color:"dark_green"}},body:{{type:"minecraft:plain_message",contents:{{text:"Choose a passive effect for this game.",color:"gray"}}}},columns:1,after_action:"close",exit_action:{{label:"Skip"}},actions:[{{label:[{{"text":"💰 ","color":"gold"}},{{"text":"x1.2 Points"}}],tooltip:{{text:"Earn 20% more points from kills (permanent)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_PASSIVE_1}"}}}},{{label:[{{"text":"⏱ ","color":"aqua"}},{{"text":"x1.5 Powerups"}}],tooltip:{{text:"All powerup durations last 50% longer"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_PASSIVE_2}"}}}}]}}
""")

	write_versioned_function("zombies/ability_menu", f"""
# Show the ability selection dialog
dialog show @s {{type:"minecraft:multi_action",title:{{text:"Zonweeb Ability",color:"dark_green"}},body:{{type:"minecraft:plain_message",contents:{{text:"Choose an ability for this game.",color:"gray"}}}},columns:1,after_action:"close",exit_action:{{label:"Skip"}},actions:[{{label:[{{"text":"🏃 ","color":"yellow"}},{{"text":"Coward"}}],tooltip:{{text:"TP to spawn when under 50% HP (1 round cooldown)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_ABILITY_1}"}}}},{{label:[{{"text":"🛡 ","color":"green"}},{{"text":"Guardian"}}],tooltip:{{text:"Summon an Iron Golem ally at round start (1 round cooldown)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_ABILITY_2}"}}}}]}}
""")

	# Passive selection (called via trigger dispatch, then show ability dialog)
	write_versioned_function("zombies/perks/set_passive_1", f"""
scoreboard players set @s {ns}.zb.passive 1
tellraw @s [{MGS_TAG},{{"text":"Passive set: ","color":"gray"}},{{"text":"x1.2 Points","color":"gold"}}]
function {ns}:v{version}/zombies/ability_menu
""")

	write_versioned_function("zombies/perks/set_passive_2", f"""
scoreboard players set @s {ns}.zb.passive 2
tellraw @s [{MGS_TAG},{{"text":"Passive set: ","color":"gray"}},{{"text":"x1.5 Powerups","color":"aqua"}}]
function {ns}:v{version}/zombies/ability_menu
""")

	# Ability selection (called via trigger dispatch)
	write_versioned_function("zombies/perks/set_ability_1", f"""
scoreboard players set @s {ns}.zb.ability 1
scoreboard players set @s {ns}.zb.ability_cd 0
tellraw @s [{MGS_TAG},{{"text":"Ability set: ","color":"gray"}},{{"text":"Coward","color":"yellow"}},{{"text":" (TP to spawn when below 50% HP)","color":"gray"}}]
""")

	write_versioned_function("zombies/perks/set_ability_2", f"""
scoreboard players set @s {ns}.zb.ability 2
scoreboard players set @s {ns}.zb.ability_cd 0
tellraw @s [{MGS_TAG},{{"text":"Ability set: ","color":"gray"}},{{"text":"Guardian","color":"green"}},{{"text":" (Summon an Iron Golem ally)","color":"gray"}}]
""")

	# ── Ability Tick (check and trigger abilities) ────────────────

	write_versioned_function("zombies/ability_tick", f"""
# Coward: TP to spawn when under 50% health (10 HP out of 20), cooldown not active
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability=1,{ns}.zb.ability_cd=0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/perks/check_coward
""")

	write_versioned_function("zombies/perks/check_coward", f"""
# Check health: 10 HP = 50% of default 20 HP max
execute store result score #_hp {ns}.data run data get entity @s Health 1
execute if score #_hp {ns}.data matches ..10 run function {ns}:v{version}/zombies/perks/trigger_coward
""")

	# Coward: actually teleport to spawn
	write_versioned_function("zombies/perks/trigger_coward", f"""
# Teleport to a player spawn point
function {ns}:v{version}/zombies/respawn_tp

# Set cooldown (1 round)
scoreboard players set @s {ns}.zb.ability_cd 1

# Effects
effect give @s speed 5 1 true
effect give @s regeneration 5 1 true

# Announce
title @s actionbar [{{"text":"🏃 Coward activated! Teleported to safety!","color":"yellow"}}]
""")

	# Guardian: summon iron golem when the round starts (if ability is ready)
	write_versioned_function("zombies/perks/check_guardian", f"""
# Check guardian ability for all players with it ready
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability=2,{ns}.zb.ability_cd=0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/perks/trigger_guardian
""")

	write_versioned_function("zombies/perks/trigger_guardian", f"""
# Summon an Iron Golem ally near the player
summon minecraft:iron_golem ~ ~ ~ {{Tags:["{ns}.guardian_golem","{ns}.gm_entity"],PlayerCreated:0b,CustomName:'"\\u00a72Guardian"'}}

# Set cooldown (1 round)
scoreboard players set @s {ns}.zb.ability_cd 1

# Announce
title @s actionbar [{{"text":"🛡 Guardian activated! Iron Golem summoned!","color":"green"}}]
""")

	# Reduce ability cooldowns at the start of each round
	write_versioned_function("zombies/perks/reduce_cooldowns", f"""
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability_cd=1..}}] run scoreboard players remove @s {ns}.zb.ability_cd 1
""")

	# Hook ability tick into game_tick
	write_versioned_function("zombies/game_tick", f"""
# Ability tick
function {ns}:v{version}/zombies/ability_tick
""")

	# Hook cooldown reduction and guardian into round start
	write_versioned_function("zombies/start_round", f"""
# Reduce ability cooldowns
function {ns}:v{version}/zombies/perks/reduce_cooldowns

# Check guardian ability (summon golem at round start)
function {ns}:v{version}/zombies/perks/check_guardian
""")



	# ── Forceload ─────────────────────────────────────────────────

	write_versioned_function("zombies/forceload_area", f"""
execute store result storage {ns}:temp _fl.x1 int 1 run scoreboard players get #bound_x1 {ns}.data
execute store result storage {ns}:temp _fl.z1 int 1 run scoreboard players get #bound_z1 {ns}.data
execute store result storage {ns}:temp _fl.x2 int 1 run scoreboard players get #bound_x2 {ns}.data
execute store result storage {ns}:temp _fl.z2 int 1 run scoreboard players get #bound_z2 {ns}.data
function {ns}:v{version}/zombies/forceload_add with storage {ns}:temp _fl
""")

	write_versioned_function("zombies/forceload_add", """
$forceload add $(x1) $(z1) $(x2) $(z2)
""")

	write_versioned_function("zombies/remove_forceload", f"""
execute store result storage {ns}:temp _fl.x1 int 1 run scoreboard players get #bound_x1 {ns}.data
execute store result storage {ns}:temp _fl.z1 int 1 run scoreboard players get #bound_z1 {ns}.data
execute store result storage {ns}:temp _fl.x2 int 1 run scoreboard players get #bound_x2 {ns}.data
execute store result storage {ns}:temp _fl.z2 int 1 run scoreboard players get #bound_z2 {ns}.data
function {ns}:v{version}/zombies/forceload_remove with storage {ns}:temp _fl
""")

	write_versioned_function("zombies/forceload_remove", """
$forceload remove $(x1) $(z1) $(x2) $(z2)
""")

	# ── OOB Markers ───────────────────────────────────────────────

	write_versioned_function("zombies/summon_oob", f"""
execute store result score #gm_base_x {ns}.data run data get storage {ns}:zombies game.map.base_coordinates[0]
execute store result score #gm_base_y {ns}.data run data get storage {ns}:zombies game.map.base_coordinates[1]
execute store result score #gm_base_z {ns}.data run data get storage {ns}:zombies game.map.base_coordinates[2]

data modify storage {ns}:temp _oob_iter set from storage {ns}:zombies game.map.out_of_bounds
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/zombies/summon_oob_iter
""")

	write_versioned_function("zombies/summon_oob_iter", f"""
execute store result score #_rx {ns}.data run data get storage {ns}:temp _oob_iter[0][0]
execute store result score #_ry {ns}.data run data get storage {ns}:temp _oob_iter[0][1]
execute store result score #_rz {ns}.data run data get storage {ns}:temp _oob_iter[0][2]
scoreboard players operation #_rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _oob_pos.x double 1 run scoreboard players get #_rx {ns}.data
execute store result storage {ns}:temp _oob_pos.y double 1 run scoreboard players get #_ry {ns}.data
execute store result storage {ns}:temp _oob_pos.z double 1 run scoreboard players get #_rz {ns}.data
function {ns}:v{version}/zombies/summon_oob_at with storage {ns}:temp _oob_pos
data remove storage {ns}:temp _oob_iter[0]
execute if data storage {ns}:temp _oob_iter[0] run function {ns}:v{version}/zombies/summon_oob_iter
""")

	write_versioned_function("zombies/summon_oob_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.oob_point","{ns}.gm_entity"]}}
""")

	# ── Spawn Point Markers ───────────────────────────────────────

	write_versioned_function("zombies/summon_spawns", f"""
# Player spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.players
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb_player"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter
""")

	write_versioned_function("zombies/summon_spawn_iter", f"""
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

function {ns}:v{version}/zombies/summon_spawn_at with storage {ns}:temp _spos

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter
""")

	write_versioned_function("zombies/summon_spawn_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.spawn_point","$(tag)","{ns}.gm_entity"],data:{{yaw:$(yaw)}}}}
""")

	# ── Smart Spawn Selection ─────────────────────────────────────

	write_versioned_function("zombies/tp_all_to_spawns", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/pick_spawn
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

	write_versioned_function("zombies/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# Tag candidate spawns (exclude used)
tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# If all used, re-tag all
execute unless entity @e[tag={ns}.spawn_candidate] run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player] add {ns}.spawn_candidate

# Pick random candidate
execute as @n[tag={ns}.spawn_candidate,sort=random] run function {ns}:v{version}/zombies/tp_to_spawn

# Cleanup
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

	write_versioned_function("zombies/tp_to_spawn", f"""
execute store result storage {ns}:temp _tp.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _tp.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _tp.z double 1 run data get entity @s Pos[2]
data modify storage {ns}:temp _tp.yaw set from entity @s data.yaw

execute as @p[tag={ns}.spawn_pending] run function {ns}:v{version}/zombies/tp_player_at with storage {ns}:temp _tp

execute unless data storage {ns}:zombies game{{state:"active"}} run tag @s add {ns}.spawn_used
""")

	write_versioned_function("zombies/tp_player_at", "$tp @s $(x) $(y) $(z) $(yaw) 0")

	## Respawn TP for zombies
	write_versioned_function("zombies/respawn_tp", f"""
execute if entity @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player] run function {ns}:v{version}/zombies/pick_spawn
""")

	# ── Sidebar HUD ───────────────────────────────────────────────

	write_versioned_function("zombies/create_sidebar", f"""
scoreboard objectives add {ns}.zb_sidebar dummy
function {ns}:v{version}/zombies/refresh_sidebar
scoreboard objectives setdisplay sidebar {ns}.zb_sidebar
""")

	write_versioned_function("zombies/refresh_sidebar", f"""
# Count alive zombies
execute store result score #_zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
scoreboard players operation #_zb_total {ns}.data = #_zb_alive {ns}.data
scoreboard players operation #_zb_total {ns}.data += #zb_to_spawn {ns}.data

function #bs.sidebar:create {{objective:"{ns}.zb_sidebar",display_name:{{text:"🧟 Zombies",color:"dark_green",bold:true}},contents:[{{text:" Round: ",extra:[{{score:{{name:"#zb_round",objective:"{ns}.data"}},color:"gold"}}],color:"red"}},{{text:" Zombies: ",extra:[{{score:{{name:"#_zb_total",objective:"{ns}.data"}},color:"red"}}],color:"gray"}}," "]}}
""")

	# ── Block shooting during prep ────────────────────────────────

	write_versioned_function("player/right_click", f"""
# Block shooting during zombies prep phase
execute if score @s {ns}.zb.in_game matches 1 if data storage {ns}:zombies game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)
