
#> mgs:v5.0.0/zombies/start
#
# @within	???
#

# Prevent starting if already active or preparing
execute if data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.zombies_game_already_in_progress","color":"red"}]
execute if data storage mgs:zombies game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.zombies_game_already_preparing","color":"red"}]

# Check that a map is selected
execute unless data storage mgs:zombies game.map_id run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.no_map_selected_use_the_setup_menu_to_select_a_zombies_map","color":"red"}]
execute if data storage mgs:zombies game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.no_map_selected_use_the_setup_menu_to_select_a_zombies_map","color":"red"}]

# Load the selected map
function mgs:v5.0.0/zombies/load_map_from_storage with storage mgs:zombies game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.map_not_found_select_a_valid_zombies_map","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:zombies game.map set from storage mgs:temp map_load.result

# Set state to preparing
data modify storage mgs:zombies game.state set value "preparing"

# Reset scores
scoreboard players set @a mgs.zb.in_game 0
scoreboard players set @a mgs.zb.points 500
scoreboard players set @a mgs.zb.kills 0
scoreboard players set @a mgs.zb.downs 0
scoreboard players set @a mgs.zb.passive 0
scoreboard players set @a mgs.zb.ability 0
scoreboard players set @a mgs.zb.ability_cd 0

# Tag all players as in-game
scoreboard players set @a mgs.zb.in_game 1

# Reset death counters and spectate timers to prevent false triggers
scoreboard players set @a mgs.mp.death_count 0
scoreboard players set @a mgs.mp.spectate_timer 0

# Set gamerules
gamemode spectator @a[scores={mgs.zb.in_game=1}]
gamerule immediate_respawn true
gamerule keep_inventory true

# Initialize round to 0 (first round will be 1)
data modify storage mgs:zombies game.round set value 0

# Store base coordinates for offset
execute store result score #gm_base_x mgs.data run data get storage mgs:zombies game.map.base_coordinates[0]
execute store result score #gm_base_y mgs.data run data get storage mgs:zombies game.map.base_coordinates[1]
execute store result score #gm_base_z mgs.data run data get storage mgs:zombies game.map.base_coordinates[2]

# Check if map has boundaries defined
scoreboard players set #zb_has_bounds mgs.data 0
execute if data storage mgs:zombies game.map.boundaries[0] run scoreboard players set #zb_has_bounds mgs.data 1

# Normalize and store boundaries (only if defined)
execute if score #zb_has_bounds mgs.data matches 1 store result score #bound_x1 mgs.data run data get storage mgs:zombies game.map.boundaries[0][0]
execute if score #zb_has_bounds mgs.data matches 1 store result score #bound_y1 mgs.data run data get storage mgs:zombies game.map.boundaries[0][1]
execute if score #zb_has_bounds mgs.data matches 1 store result score #bound_z1 mgs.data run data get storage mgs:zombies game.map.boundaries[0][2]
execute if score #zb_has_bounds mgs.data matches 1 store result score #bound_x2 mgs.data run data get storage mgs:zombies game.map.boundaries[1][0]
execute if score #zb_has_bounds mgs.data matches 1 store result score #bound_y2 mgs.data run data get storage mgs:zombies game.map.boundaries[1][1]
execute if score #zb_has_bounds mgs.data matches 1 store result score #bound_z2 mgs.data run data get storage mgs:zombies game.map.boundaries[1][2]
execute if score #zb_has_bounds mgs.data matches 1 run scoreboard players operation #bound_x1 mgs.data += #gm_base_x mgs.data
execute if score #zb_has_bounds mgs.data matches 1 run scoreboard players operation #bound_y1 mgs.data += #gm_base_y mgs.data
execute if score #zb_has_bounds mgs.data matches 1 run scoreboard players operation #bound_z1 mgs.data += #gm_base_z mgs.data
execute if score #zb_has_bounds mgs.data matches 1 run scoreboard players operation #bound_x2 mgs.data += #gm_base_x mgs.data
execute if score #zb_has_bounds mgs.data matches 1 run scoreboard players operation #bound_y2 mgs.data += #gm_base_y mgs.data
execute if score #zb_has_bounds mgs.data matches 1 run scoreboard players operation #bound_z2 mgs.data += #gm_base_z mgs.data
execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.0.0/zombies/normalize_bounds

# Forceload the area (only if bounds defined)
execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.0.0/zombies/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #gm_base_z mgs.data
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.0.0/zombies/tp_to_base with storage mgs:temp _tp

# Register custom maps and mystery box items (extension points)
function #mgs:zombies/register_maps
function #mgs:zombies/register_mystery_box_item

# Schedule preload completion after 1 second
schedule function mgs:v5.0.0/zombies/preload_complete 20t

# Announce
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate": "mgs.loading_zombies_map","color":"yellow"}]

