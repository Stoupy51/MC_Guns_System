
#> mgs:v5.0.0/missions/start
#
# @within	mgs:v5.0.0/missions/setup "hover_event": {"action": "show_text", "value": "Start the mission"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/missions/stop"}, "hover_event": {"action": "show_text", "value": "Stop the mission"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/select_class"}, "hover_event": {"action": "show_text", "value": "Select your class"}}, "\u2694 Classes", "]"]]
#

# Prevent starting if already active or preparing
execute if data storage mgs:missions game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_already_in_progress","color":"red"}]
execute if data storage mgs:missions game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_already_preparing","color":"red"}]

# Check that a map is selected
execute if data storage mgs:missions game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_use_the_setup_menu_to_select_a_mission_map","color":"red"}]

# Load the selected map
function mgs:v5.0.0/missions/load_map_from_storage with storage mgs:missions game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_not_found_select_a_valid_mission_map","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:missions game.map set from storage mgs:temp map_load.result

# Legacy compatibility: normalize respawn command keys
execute unless data storage mgs:missions game.map.respawn_commands if data storage mgs:missions game.map.respawn_command[0] run data modify storage mgs:missions game.map.respawn_commands set from storage mgs:missions game.map.respawn_command
execute unless data storage mgs:missions game.map.respawn_commands if data storage mgs:missions game.map.respawn_command.command run data modify storage mgs:missions game.map.respawn_commands set value []
execute unless data storage mgs:missions game.map.respawn_commands[0] if data storage mgs:missions game.map.respawn_command.command run data modify storage mgs:missions game.map.respawn_commands append from storage mgs:missions game.map.respawn_command
execute unless data storage mgs:missions game.map.respawn_commands run data modify storage mgs:missions game.map.respawn_commands set value []
execute unless data storage mgs:missions game.map.start_commands run data modify storage mgs:missions game.map.start_commands set value []

# Set state to preparing
data modify storage mgs:missions game.state set value "preparing"

# Reset scores
scoreboard players set @a mgs.mi.in_game 0
scoreboard players set #mi_timer mgs.data 0
scoreboard players set #mi_total_enemies mgs.data 0
scoreboard players set #mi_has_boundary mgs.data 0
scoreboard players set @a mgs.mi.kills 0
scoreboard players set @a mgs.mi.deaths 0

# Tag all team 1 players as in-game (multiplayer support)
execute if entity @a[scores={mgs.mp.team=1}] as @a[scores={mgs.mp.team=1}] run scoreboard players set @s mgs.mi.in_game 1
# Fallback: if no team system, tag all players
execute unless entity @a[scores={mgs.mi.in_game=1}] run scoreboard players set @a mgs.mi.in_game 1

# Missions are fully cooperative: force all mission players to one shared team id
scoreboard players set @a[scores={mgs.mi.in_game=1}] mgs.mp.team 1

# Enable class menu for mission players
tag @a[scores={mgs.mi.in_game=1}] add mgs.give_class_menu

# Snapshot player total kills at mission start for per-mission kill delta
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mi.kill_base = @s mgs.mi.kill_total

# Set gamerules
gamemode spectator @a[scores={mgs.mi.in_game=1}]
gamerule immediate_respawn true
gamerule keep_inventory true

# Store base coordinates for offset
execute store result score #gm_base_x mgs.data run data get storage mgs:missions game.map.base_coordinates[0]
execute store result score #gm_base_y mgs.data run data get storage mgs:missions game.map.base_coordinates[1]
execute store result score #gm_base_z mgs.data run data get storage mgs:missions game.map.base_coordinates[2]

# Detect whether this map defines a boundary (needs 2 points)
execute if data storage mgs:missions game.map.boundaries[0] if data storage mgs:missions game.map.boundaries[1] run scoreboard players set #mi_has_boundary mgs.data 1

# Normalize and store boundaries only when they exist
execute if score #mi_has_boundary mgs.data matches 1 run function mgs:v5.0.0/missions/load_bounds

# Forceload the mission area to ensure chunks are loaded
execute if score #mi_has_boundary mgs.data matches 1 run function mgs:v5.0.0/missions/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #gm_base_z mgs.data
execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.0.0/missions/tp_to_base with storage mgs:temp _tp

# Schedule preload completion after 1 second
schedule function mgs:v5.0.0/missions/preload_complete 20t

# Announce
tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate":"mgs.loading_mission_area","color":"yellow"}]

