
# ruff: noqa: E501
# Zombies Game System
# Wave-based survival mode with zombie spawning, points, perks, mystery box, wallbuys, doors, and traps.
# Map definitions are dynamic (stored in storage, registered via function tags).
from stewbeet import Mem, write_load_file, write_tag, write_tick_file, write_versioned_function

from ..helpers import MGS_TAG, game_start_guards, regen_disable_lines, regen_enable_lines


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

# Spawn point group_id scoreboard
scoreboard objectives add {ns}.zb.spawn.gid dummy

# Sidebar rank scoreboard
scoreboard objectives add {ns}.zb.sb_rank dummy

# Initialize zombies game state
execute unless data storage {ns}:zombies game run data modify storage {ns}:zombies game set value {{state:"lobby",map_id:"",round:0}}

# Initialize mystery box base pool (can be extended via function tag)
execute unless data storage {ns}:zombies mystery_box_pool run data modify storage {ns}:zombies mystery_box_pool set value []

# Config: points per kill, points per hit
# TODO: ZB points hit not used
execute unless score #zb_points_kill {ns}.config matches 1.. run scoreboard players set #zb_points_kill {ns}.config 50
execute unless score #zb_points_hit {ns}.config matches 1.. run scoreboard players set #zb_points_hit {ns}.config 10
execute unless score #zb_mystery_box_price {ns}.config matches 1.. run scoreboard players set #zb_mystery_box_price {ns}.config 950
""")

	## Signal function tags
	for event in ["register_maps", "register_mystery_box_item", "on_round_start", "on_round_end", "on_game_start", "on_game_end"]:
		write_tag(f"zombies/{event}", Mem.ctx.data[ns].function_tags, [])

	## Game Start
	write_versioned_function("zombies/start", f"""
# Prevent starting if already active or preparing
{game_start_guards(ns, "zombies", "Zombies game")}

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

# Disable natural regeneration, enable custom regen system
{regen_enable_lines(ns)}

# Set gamerules
gamemode spectator @a[scores={{{ns}.zb.in_game=1}}]
gamerule immediate_respawn true
gamerule keep_inventory true

# Initialize round to 0 (first round will be 1)
data modify storage {ns}:zombies game.round set value 0

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"zombies"}}

# Check if map has boundaries defined
scoreboard players set #zb_has_bounds {ns}.data 0
execute if data storage {ns}:zombies game.map.boundaries[0] run scoreboard players set #zb_has_bounds {ns}.data 1

# Normalize and store boundaries (only if defined)
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/load_bounds {{mode:"zombies"}}

# Forceload the area (only if bounds defined)
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #gm_base_z {ns}.data
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

# Register custom maps and mystery box items (extension points)
function #{ns}:zombies/register_maps
function #{ns}:zombies/register_mystery_box_item

# Schedule preload completion after 1 second
schedule function {ns}:v{version}/zombies/preload_complete 20t

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Loading zombies map...","color":"yellow"}}]
""")

	## Load map from storage
	write_versioned_function("zombies/load_map_from_storage", f"""
$function {ns}:v{version}/shared/maps/load {{id:"$(map_id)",mode:"zombies",override:{{}}}}
""")

	## Preload complete → transition to prep phase
	write_versioned_function("zombies/preload_complete", f"""
# Guard: only if still preparing
execute unless data storage {ns}:zombies game{{state:"preparing"}} run return fail

# Switch to adventure mode
gamemode adventure @a[scores={{{ns}.zb.in_game=1}}]

# Summon OOB markers (only if map has out_of_bounds data)
execute if data storage {ns}:zombies game.map.out_of_bounds run function {ns}:v{version}/shared/summon_oob {{mode:"zombies"}}

# Summon spawn point markers for players
function {ns}:v{version}/zombies/summon_spawns

# Signal zombies game start
function #{ns}:zombies/on_game_start

# Run map-defined start commands after entity/setup summons
execute if data storage {ns}:zombies game.map.start_commands[0] run function {ns}:v{version}/shared/run_start_commands {{mode:"zombies"}}

# Teleport all players to player spawns
function {ns}:v{version}/zombies/tp_all_to_spawns

# Freeze players during prep
effect give @a[scores={{{ns}.zb.in_game=1}}] darkness 25 255 true
effect give @a[scores={{{ns}.zb.in_game=1}}] blindness 25 255 true
effect give @a[scores={{{ns}.zb.in_game=1}}] night_vision 25 255 true
effect give @a[scores={{{ns}.zb.in_game=1}}] saturation infinite 255 true
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base set 0

# Give starting loadout to all players
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/inventory/give_starting_loadout

# Show zombies perk selection menu
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/passive_ability_menu

# Schedule end of prep (10 seconds remaining)
schedule function {ns}:v{version}/zombies/end_prep 200t

# Initialize sidebar
function {ns}:v{version}/zombies/create_sidebar

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Preparing! Choose your perk! Round 1 starts in 10 seconds!","color":"yellow"}}]
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
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base reset

# Clear prep effects
effect clear @a[scores={{{ns}.zb.in_game=1}}] darkness
effect clear @a[scores={{{ns}.zb.in_game=1}}] blindness
effect clear @a[scores={{{ns}.zb.in_game=1}}] night_vision

# Keep saturation
effect give @a[scores={{{ns}.zb.in_game=1}}] saturation infinite 255 true

# Start round 1
function {ns}:v{version}/zombies/start_round
""")



	# Game Tick ─────────────────────────────────────────────────

	write_tick_file(f"""
# Zombies game tick
execute if data storage {ns}:zombies game{{state:"active"}} run function {ns}:v{version}/zombies/game_tick
execute if data storage {ns}:zombies game{{state:"preparing"}} run function {ns}:v{version}/zombies/prep_tick
""")

	write_versioned_function("zombies/game_tick", f"""
# Revive system tick (process downed players)
function {ns}:v{version}/zombies/revive/tick

# Zombie Spawning (if there are still zombies to spawn)
execute if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_tick

# Boundary enforcement (skip spectators, only if map has bounds)
execute if score #zb_has_bounds {ns}.data matches 1 as @e[tag={ns}.zombie_round] at @s run function {ns}:v{version}/zombies/check_bounds
execute if score #zb_has_bounds {ns}.data matches 1 as @e[type=player,scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/zombies/check_bounds

# Check round completion
execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 run function {ns}:v{version}/zombies/round_complete

# Check game over (all players downed or spectator means no one can revive)
execute if score #zb_round_grace {ns}.data matches 1.. run scoreboard players remove #zb_round_grace {ns}.data 1
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #zb_alive_players {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_alive_players {ns}.data matches 0 run function {ns}:v{version}/zombies/game_over

# Refresh sidebar every second (20 ticks)
scoreboard players add #zb_sidebar_timer {ns}.data 1
execute if score #zb_sidebar_timer {ns}.data matches 20.. run scoreboard players set #zb_sidebar_timer {ns}.data 0
execute if score #zb_sidebar_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/refresh_sidebar

# Cleanup
kill @e[type=experience_orb]
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



	# Death & Respawn ───────────────────────────────────────────

	## On Respawn (zombies death handling → enter downed state)
	write_versioned_function("zombies/on_respawn", f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Increment down count
scoreboard players add @s {ns}.zb.downs 1

# Enter downed state (revive system)
function {ns}:v{version}/zombies/revive/on_down
""")

	## Add player tick hook for zombies death detection
	write_versioned_function("player/tick", f"""
# Zombies: detect respawn
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/zombies/on_respawn
""")

	# Game Over ─────────────────────────────────────────────────

	write_versioned_function("zombies/game_over", f"""
# Set state to ended
data modify storage {ns}:zombies game.state set value "ended"

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 80 20
title @a[scores={{{ns}.zb.in_game=1}}] title {{"text":"GAME OVER","color":"dark_red","bold":true}}

# Calculate final round
execute store result score #final_round {ns}.data run data get storage {ns}:zombies game.round

# Performance summary
tellraw @a ["","\\n",{{"text":"═══════ GAME OVER ═══════","color":"dark_red","bold":true}}]
tellraw @a ["","  ",{{"text":"🧟 Final Round: ","color":"gray"}},{{"score":{{"name":"#final_round","objective":"{ns}.data"}},"color":"red","bold":true}}]

# Per-player stats
execute as @a[scores={{{ns}.zb.in_game=1}}] run tellraw @a ["","  ",{{"text":"🎖 ","color":"gray"}},{{"selector":"@s","color":"yellow"}}," — Kills: ",{{"score":{{"name":"@s","objective":"{ns}.zb.kills"}},"color":"green"}}," | Downs: ",{{"score":{{"name":"@s","objective":"{ns}.zb.downs"}},"color":"red"}}," | Points: ",{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"gold"}}]

tellraw @a ["",{{"text":"═════════════════════════","color":"dark_red","bold":true}},"\\n"]

# Signal game end
function #{ns}:zombies/on_game_end

# End game after 5 seconds
schedule function {ns}:v{version}/zombies/stop 100t
""")

	# Game Stop ─────────────────────────────────────────────────

	write_versioned_function("zombies/stop", f"""
# Set state to lobby
data modify storage {ns}:zombies game.state set value "lobby"

# Cancel scheduled functions
schedule clear {ns}:v{version}/zombies/end_prep
schedule clear {ns}:v{version}/zombies/start_round

# Restore movement
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:max_health base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base reset

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
execute if score #zb_has_bounds {ns}.data matches 1 run function {ns}:v{version}/shared/remove_forceload

# Remove sidebar
scoreboard objectives setdisplay sidebar
scoreboard objectives remove {ns}.zb_sidebar
{regen_disable_lines(ns)}
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

	# Kill Points ───────────────────────────────────────────────
	# Hook into the on_kill signal to add points when killing zombies
	write_versioned_function("zombies/on_kill_signal", f"""
# Only process if zombies game is active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Award kill points (with passive bonus if applicable)
scoreboard players operation @s {ns}.zb.points += #zb_points_kill {ns}.config

# Apply x1.2 points passive: add 20% extra
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation #additional {ns}.data = #zb_points_kill {ns}.config
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation #additional {ns}.data /= #5 {ns}.data
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation @s {ns}.zb.points += #additional {ns}.data

scoreboard players add @s {ns}.zb.kills 1
""", tags=[f"{ns}:signals/on_kill"])





	# Spawn Point Markers ───────────────────────────────────────

	write_versioned_function("zombies/summon_spawns", f"""
# Player spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.players
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb_player"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Zombie spawns
data modify storage {ns}:temp _spawn_iter set from storage {ns}:zombies game.map.spawning_points.zombies
data modify storage {ns}:temp _spawn_tag set value "{ns}.spawn_zb"
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter

# Tag group 0 spawns as unlocked (starting area)
scoreboard players set #unlock_gid {ns}.data 0
execute as @e[tag={ns}.spawn_point] if score @s {ns}.zb.spawn.gid = #unlock_gid {ns}.data run tag @s add {ns}.spawn_unlocked
""")

	write_versioned_function("zombies/summon_spawn_iter", f"""
# Read position from compound format
execute store result score #sx {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[0]
execute store result score #sy {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[1]
execute store result score #sz {ns}.data run data get storage {ns}:temp _spawn_iter[0].pos[2]
execute store result score #syaw {ns}.data run data get storage {ns}:temp _spawn_iter[0].rotation[0] 100

scoreboard players operation #sx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #sy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #sz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #sx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #sy {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #sz {ns}.data
execute store result storage {ns}:temp _spos.yaw double 0.01 run scoreboard players get #syaw {ns}.data
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_tag

function {ns}:v{version}/zombies/summon_spawn_at with storage {ns}:temp _spos

# Set group_id score on newly spawned marker (default 0 if not defined)
scoreboard players set @n[tag={ns}.new_spawn] {ns}.zb.spawn.gid 0
execute store result score @n[tag={ns}.new_spawn] {ns}.zb.spawn.gid run data get storage {ns}:temp _spawn_iter[0].group_id
tag @n[tag={ns}.new_spawn] remove {ns}.new_spawn

data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/zombies/summon_spawn_iter
""")

	write_versioned_function("zombies/summon_spawn_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.spawn_point","$(tag)","{ns}.gm_entity","{ns}.new_spawn"],data:{{yaw:$(yaw)}}}}
""")

	# Smart Spawn Selection ─────────────────────────────────────

	write_versioned_function("zombies/tp_all_to_spawns", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/pick_spawn
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
""")

	write_versioned_function("zombies/pick_spawn", f"""
tag @s add {ns}.spawn_pending

# Tag candidate spawns (unlocked, exclude used)
tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked,tag=!{ns}.spawn_used] add {ns}.spawn_candidate

# If all used, re-tag all unlocked
execute unless entity @e[tag={ns}.spawn_candidate] run tag @e[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate

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

	# Sidebar HUD ───────────────────────────────────────────────

	write_versioned_function("zombies/create_sidebar", f"""
scoreboard objectives add {ns}.zb_sidebar dummy
function {ns}:v{version}/zombies/refresh_sidebar
scoreboard objectives setdisplay sidebar {ns}.zb_sidebar
""")

	write_versioned_function("zombies/refresh_sidebar", f"""
# Count alive zombies
execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
scoreboard players operation #zb_total {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_total {ns}.data += #zb_to_spawn {ns}.data
execute if score #zb_total {ns}.data matches ..-1 run scoreboard players set #zb_total {ns}.data 0

# Initialize sidebar contents
data modify storage {ns}:temp zb_sb set value [[{{text:"Round",color:"red"}},{{score:{{name:"#zb_round",objective:"{ns}.data"}},color:"gold"}}],[{{text:"Zombies",color:"red"}},{{score:{{name:"#zb_total",objective:"{ns}.data"}},color:"gold"}}]," "]

# Rank players for sidebar display
scoreboard players set @a {ns}.zb.sb_rank 0
tag @a[scores={{{ns}.zb.in_game=1}}] add {ns}.zb_sb_cand
function {ns}:v{version}/zombies/sidebar_rank_players

# Build sidebar via macro
function {ns}:v{version}/zombies/build_sidebar with storage {ns}:temp
""")

	# Rank players and append to sidebar (up to 8 players)
	sidebar_rank_code = ""
	for i in range(1, 9):
		sidebar_rank_code += f"""
execute unless entity @a[tag={ns}.zb_sb_cand] run return 0
execute as @r[tag={ns}.zb_sb_cand] run scoreboard players set @s {ns}.zb.sb_rank {i}
tag @a[scores={{{ns}.zb.sb_rank={i}}}] remove {ns}.zb_sb_cand
data modify storage {ns}:temp zb_sb append value [{{selector:"@a[scores={{{ns}.zb.sb_rank={i}}}]",color:"green"}},{{score:{{name:"@a[scores={{{ns}.zb.sb_rank={i}}}]",objective:"{ns}.zb.points"}},color:"yellow"}}]
"""
	sidebar_rank_code += f"\ntag @a remove {ns}.zb_sb_cand\n"
	write_versioned_function("zombies/sidebar_rank_players", sidebar_rank_code)

	write_versioned_function("zombies/build_sidebar", f"""
$function #bs.sidebar:create {{objective:"{ns}.zb_sidebar",display_name:{{text:"Zombies",color:"dark_green",bold:true}},contents:$(zb_sb)}}
""")

	# Block shooting during prep ────────────────────────────────

	write_versioned_function("player/right_click", f"""
# Block shooting during zombies prep phase
execute if score @s {ns}.zb.in_game matches 1 if data storage {ns}:zombies game{{state:"preparing"}} run return run scoreboard players set @s {ns}.pending_clicks 0
""", prepend=True)
