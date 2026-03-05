
#> mgs:v5.0.0/multiplayer/start
#
# @within	???
#

# Prevent starting if already active or preparing
execute if data storage mgs:multiplayer game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.game_already_in_progress","color":"red"}]
execute if data storage mgs:multiplayer game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.game_already_preparing","color":"red"}]

# Load the selected map (reads map_id from game storage)
function mgs:v5.0.0/multiplayer/load_map_from_storage with storage mgs:multiplayer game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.no_map_found_select_a_map_first","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:multiplayer game.map set from storage mgs:temp map_load.result

# Initialize game
data modify storage mgs:multiplayer game.state set value "preparing"

# Reset scores
scoreboard players set #red mgs.mp.team 0
scoreboard players set #blue mgs.mp.team 0
scoreboard players set @a mgs.mp.kills 0
scoreboard players set @a mgs.mp.deaths 0
scoreboard players set @a mgs.mp.death_count 0
scoreboard players set @a mgs.mp.respawn_prot 0

# Set timer from time_limit
execute store result score #mp_timer mgs.data run data get storage mgs:multiplayer game.time_limit

# Tag all non-spectator players as in-game
scoreboard players set @a mgs.mp.in_game 1

# Set all in-game players to adventure and enable instant respawn
gamemode adventure @a[scores={mgs.mp.in_game=1}]
gamerule immediate_respawn true

# Store base coordinates for offset
execute store result score #gm_base_x mgs.data run data get storage mgs:multiplayer game.map.base_coordinates[0]
execute store result score #gm_base_y mgs.data run data get storage mgs:multiplayer game.map.base_coordinates[1]
execute store result score #gm_base_z mgs.data run data get storage mgs:multiplayer game.map.base_coordinates[2]

# Store boundary corners (relative) and convert to absolute
execute store result score #bound_x1 mgs.data run data get storage mgs:multiplayer game.map.boundaries[0][0]
execute store result score #bound_y1 mgs.data run data get storage mgs:multiplayer game.map.boundaries[0][1]
execute store result score #bound_z1 mgs.data run data get storage mgs:multiplayer game.map.boundaries[0][2]
execute store result score #bound_x2 mgs.data run data get storage mgs:multiplayer game.map.boundaries[1][0]
execute store result score #bound_y2 mgs.data run data get storage mgs:multiplayer game.map.boundaries[1][1]
execute store result score #bound_z2 mgs.data run data get storage mgs:multiplayer game.map.boundaries[1][2]
scoreboard players operation #bound_x1 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y1 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z1 mgs.data += #gm_base_z mgs.data
scoreboard players operation #bound_x2 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y2 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z2 mgs.data += #gm_base_z mgs.data

# Normalize boundaries (ensure x1 < x2, y1 < y2, z1 < z2)
function mgs:v5.0.0/multiplayer/normalize_bounds

# Summon out-of-bounds markers
function mgs:v5.0.0/multiplayer/summon_oob

# Summon spawn point markers (for smart spawn selection)
function mgs:v5.0.0/multiplayer/summon_spawns

# Call register hooks (external datapacks can set up maps/classes)
function #mgs:multiplayer/register_maps
function #mgs:multiplayer/register_classes

# Signal game start
function #mgs:multiplayer/on_game_start

# Run gamemode-specific setup
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.0.0/multiplayer/gamemodes/ffa/setup
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.0.0/multiplayer/gamemodes/tdm/setup
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.0.0/multiplayer/gamemodes/dom/setup
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.0.0/multiplayer/gamemodes/hp/setup
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.0.0/multiplayer/gamemodes/snd/setup

# Store score limit and compute initial timer values for sidebar
execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute store result score #_timer_sec mgs.data run scoreboard players get #mp_timer mgs.data
scoreboard players operation #_timer_sec mgs.data /= #20 mgs.data
execute store result score #_timer_min mgs.data run scoreboard players get #_timer_sec mgs.data
scoreboard players operation #_timer_min mgs.data /= #60 mgs.data
scoreboard players operation #_timer_mod mgs.data = #_timer_sec mgs.data
scoreboard players operation #_timer_mod mgs.data %= #60 mgs.data
scoreboard players operation #_timer_tens mgs.data = #_timer_mod mgs.data
scoreboard players operation #_timer_tens mgs.data /= #10 mgs.data
scoreboard players operation #_timer_ones mgs.data = #_timer_mod mgs.data
scoreboard players operation #_timer_ones mgs.data %= #10 mgs.data

# Create sidebar HUD
scoreboard objectives add mgs.sidebar dummy
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.0.0/multiplayer/create_sidebar_ffa
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.0.0/multiplayer/create_sidebar_team {title:"Team Deathmatch"}
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.0.0/multiplayer/create_sidebar_team {title:"Domination"}
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.0.0/multiplayer/create_sidebar_team {title:"Hardpoint"}
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.0.0/multiplayer/create_sidebar_team {title:"Search & Destroy"}

# Show kills in player list (tab)
scoreboard objectives setdisplay list mgs.mp.kills

# Teleport players to spawn points
function mgs:v5.0.0/multiplayer/tp_all_to_spawns

# Freeze all players (no movement during prep)
effect give @a[scores={mgs.mp.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.mp.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.mp.in_game=1}] night_vision 25 255 true
effect give @a[scores={mgs.mp.in_game=1}] saturation infinite 255 true
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base set 0

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a at @s unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set
execute as @a at @s if score @s mgs.mp.class matches 0 if score @s mgs.mp.default matches 1.. run function mgs:v5.0.0/multiplayer/auto_apply_default

# Show class selection dialog to EVERYONE (so they can change during prep)
execute as @a run function mgs:v5.0.0/multiplayer/select_class

# Store current class for change detection during prep
execute as @a run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

# Schedule end of prep (10 seconds = 200 ticks)
schedule function mgs:v5.0.0/multiplayer/end_prep 200t

# Announce
tellraw @a ["",[{"text":"","color":"gold","bold":true},"⚔ ",{"translate": "mgs.preparing"},"! "],{"translate": "mgs.choose_your_class_game_starts_in_10_seconds","color":"yellow"}]

