
#> mgs:v5.0.0/multiplayer/start
#
# @within	???
#

# Prevent starting if already active
execute if data storage mgs:multiplayer game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.game_already_in_progress","color":"red"}]

# Load the selected map (reads map_id from game storage)
function mgs:v5.0.0/multiplayer/load_map_from_storage with storage mgs:multiplayer game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.no_map_found_select_a_map_first","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:multiplayer game.map set from storage mgs:temp map_load.result

# Initialize game
data modify storage mgs:multiplayer game.state set value "active"

# Reset scores
scoreboard players set #red mgs.mp.team 0
scoreboard players set #blue mgs.mp.team 0
scoreboard players set @a mgs.mp.kills 0
scoreboard players set @a mgs.mp.deaths 0
scoreboard players set @a mgs.mp.death_count 0

# Set timer from time_limit
execute store result score #mp_timer mgs.data run data get storage mgs:multiplayer game.time_limit

# Tag all non-spectator players as in-game
scoreboard players set @a mgs.mp.in_game 1

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

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a at @s unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set, otherwise show class dialog
execute as @a at @s if score @s mgs.mp.class matches 0 if score @s mgs.mp.default matches 1.. run function mgs:v5.0.0/multiplayer/auto_apply_default
execute as @a at @s if score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/select_class

# Announce
tellraw @a ["",[{"text":"","color":"gold","bold":true},"⚔ ",{"translate": "mgs.game_started"},"! "],{"translate": "mgs.pick_your_class","color":"yellow"}]

