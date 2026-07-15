
#> mgs:v5.1.0/missions/start
#
# @within	???
#

# Prevent starting if already active or preparing
execute if data storage mgs:missions game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_already_in_progress","color":"red"}]
execute if data storage mgs:missions game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_already_preparing","color":"red"}]

# Require at least one opted-in player (players are independent until added via Manage Players / + Join)
execute unless entity @a[scores={mgs.mi.in_game=1}] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_players_have_joined_the_mission_use_manage_players_first","color":"red"}]

# Check that a map is selected
execute if data storage mgs:missions game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_use_the_setup_menu_to_select_a_map","color":"red"}]

# Load the selected map
function mgs:v5.1.0/missions/load_map_from_storage with storage mgs:missions game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_not_found_select_a_valid_map","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:missions game.map set from storage mgs:temp map_load.result

execute unless data storage mgs:missions game.map.respawn_commands if data storage mgs:missions game.map.respawn_command[0] run data modify storage mgs:missions game.map.respawn_commands set from storage mgs:missions game.map.respawn_command
execute unless data storage mgs:missions game.map.respawn_commands if data storage mgs:missions game.map.respawn_command.command run data modify storage mgs:missions game.map.respawn_commands set value []
execute unless data storage mgs:missions game.map.respawn_commands[0] if data storage mgs:missions game.map.respawn_command.command run data modify storage mgs:missions game.map.respawn_commands append from storage mgs:missions game.map.respawn_command
execute unless data storage mgs:missions game.map.respawn_commands run data modify storage mgs:missions game.map.respawn_commands set value []
execute unless data storage mgs:missions game.map.start_commands run data modify storage mgs:missions game.map.start_commands set value []

# Set state to preparing
data modify storage mgs:missions game.state set value "preparing"

# Blue team for missions
team add mgs.blue
team modify mgs.blue color blue
team modify mgs.blue friendlyFire false
team modify mgs.blue nametagVisibility hideForOtherTeams

# Mission mob team (created once)
team add mgs.mi_mobs
team modify mgs.mi_mobs color dark_red
team modify mgs.mi_mobs friendlyFire true

# Reset scores (in_game is left untouched: it's the opt-in flag, set via Manage Players / + Join)
scoreboard players set #mi_timer mgs.data 0
scoreboard players set #mi_total_enemies mgs.data 0
scoreboard players set #mi_has_boundary mgs.data 0
scoreboard players set @a mgs.mi.kills 0
scoreboard players set @a mgs.mi.deaths 0

# Missions are fully cooperative: all opted-in players join the blue team
scoreboard players set @a[scores={mgs.mi.in_game=1}] mgs.mp.team 1
team join mgs.blue @a[scores={mgs.mi.in_game=1}]

# Enable class menu for mission players
tag @a[scores={mgs.mi.in_game=1}] add mgs.give_class_menu

# Snapshot player total kills at mission start for per-mission kill delta
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mi.kill_base = @s mgs.mi.kill_total

# Set gamerules
gamemode spectator @a[scores={mgs.mi.in_game=1}]
gamerule immediate_respawn true
gamerule keep_inventory true

# Disable natural regeneration, enable custom regen system
gamerule natural_health_regeneration false
scoreboard players set #any_game_active mgs.data 1

# Reset per-player regen state
scoreboard players set @a mgs.last_hit 0
execute as @a run execute store result score @s mgs.hp_prev run data get entity @s Health 1

# Reset stamina state so every player re-inits to full on their next stamina tick (also covers late-joiners)
scoreboard players set @a mgs.stam_seen 0

# Store base coordinates for offset
function mgs:v5.1.0/shared/load_base_coordinates {mode:"missions"}

# Detect whether this map defines a boundary (needs 2 points)
execute if data storage mgs:missions game.map.boundaries[0] if data storage mgs:missions game.map.boundaries[1] run scoreboard players set #mi_has_boundary mgs.data 1

# Normalize and store boundaries only when they exist
execute if score #mi_has_boundary mgs.data matches 1 run function mgs:v5.1.0/shared/load_bounds {mode:"missions"}

# Forceload the mission area to ensure chunks are loaded
execute if score #mi_has_boundary mgs.data matches 1 run function mgs:v5.1.0/shared/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #gm_base_z mgs.data
execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.1.0/shared/tp_to_position with storage mgs:temp _tp

# Schedule preload completion after 1 second
schedule function mgs:v5.1.0/missions/preload_complete 20t

# Announce
tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate":"mgs.loading_mission_area","color":"yellow"}]

