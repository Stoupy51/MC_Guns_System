
#> mgs:v5.0.0/missions/start
#
# @within	???
#

# Prevent starting if already active or preparing
execute if data storage mgs:missions game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mission_already_in_progress","color":"red"}]
execute if data storage mgs:missions game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mission_already_preparing","color":"red"}]

# Check that a map is selected
execute if data storage mgs:missions game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.no_map_selected_use_the_setup_menu_to_select_a_mission_map","color":"red"}]

# Load the selected map
function mgs:v5.0.0/missions/load_map_from_storage with storage mgs:missions game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.map_not_found_select_a_valid_mission_map","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:missions game.map set from storage mgs:temp map_load.result

# Initialize enemy config defaults if missing
execute unless data storage mgs:missions game.map.enemy_config run data modify storage mgs:missions game.map.enemy_config set value {level_1:{entity:"pillager",hp:20},level_2:{entity:"pillager",hp:40},level_3:{entity:"pillager",hp:60},level_4:{entity:"pillager",hp:80}}

# Set state to preparing
data modify storage mgs:missions game.state set value "preparing"

# Reset scores
scoreboard players set @a mgs.mi.in_game 0
scoreboard players set #mi_level mgs.data 0
scoreboard players set #mi_enemies mgs.data 0

# Tag all players as in-game
scoreboard players set @a mgs.mi.in_game 1

# Enable class menu for mission players
tag @a[scores={mgs.mi.in_game=1}] add mgs.give_class_menu

# Set gamerules
gamemode adventure @a[scores={mgs.mi.in_game=1}]
gamerule immediate_respawn true
gamerule keep_inventory true

# Store base coordinates for offset
execute store result score #gm_base_x mgs.data run data get storage mgs:missions game.map.base_coordinates[0]
execute store result score #gm_base_y mgs.data run data get storage mgs:missions game.map.base_coordinates[1]
execute store result score #gm_base_z mgs.data run data get storage mgs:missions game.map.base_coordinates[2]

# Normalize and store boundaries
execute store result score #bound_x1 mgs.data run data get storage mgs:missions game.map.boundaries[0][0]
execute store result score #bound_y1 mgs.data run data get storage mgs:missions game.map.boundaries[0][1]
execute store result score #bound_z1 mgs.data run data get storage mgs:missions game.map.boundaries[0][2]
execute store result score #bound_x2 mgs.data run data get storage mgs:missions game.map.boundaries[1][0]
execute store result score #bound_y2 mgs.data run data get storage mgs:missions game.map.boundaries[1][1]
execute store result score #bound_z2 mgs.data run data get storage mgs:missions game.map.boundaries[1][2]
scoreboard players operation #bound_x1 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y1 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z1 mgs.data += #gm_base_z mgs.data
scoreboard players operation #bound_x2 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y2 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z2 mgs.data += #gm_base_z mgs.data
function mgs:v5.0.0/missions/normalize_bounds

# Summon OOB markers
function mgs:v5.0.0/missions/summon_oob

# Summon spawn point markers
function mgs:v5.0.0/missions/summon_spawns

# Signal mission start
function #mgs:missions/on_mission_start

# Teleport all players to mission spawns
function mgs:v5.0.0/missions/tp_all_to_spawns

# Freeze players during prep
effect give @a[scores={mgs.mi.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.mi.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.mi.in_game=1}] night_vision 25 255 true
effect give @a[scores={mgs.mi.in_game=1}] saturation infinite 255 true
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:jump_strength base set 0

# Give loadout to players who already have a class
execute as @a[scores={mgs.mi.in_game=1}] at @s unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# Auto-apply default custom loadout if no class set
scoreboard players add @s mgs.mp.class 0
execute as @a[scores={mgs.mi.in_game=1}] at @s if score @s mgs.mp.class matches 0 if score @s mgs.mp.default matches 1.. run function mgs:v5.0.0/multiplayer/auto_apply_default

# Show class selection
execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.0.0/multiplayer/select_class

# Store current class for change detection
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

# Schedule end of prep (10 seconds)
schedule function mgs:v5.0.0/missions/end_prep 200t

# Announce
tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate": "mgs.preparing_choose_your_class_mission_starts_in_10_seconds","color":"yellow"}]

