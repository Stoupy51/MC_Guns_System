
#> mgs:v5.1.0/missions/start
#
# @executed	as the player & at current position
#
# @within	dialog mgs:v5.1.0/missions/setup
#

execute if data storage mgs:missions game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_already_in_progress","color":"red"}]
execute if data storage mgs:missions game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_already_preparing","color":"red"}]

# Players join through Manage Players or + Join.
execute unless entity @a[scores={mgs.mi.in_game=1}] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_players_have_joined_the_mission_use_manage_players_first","color":"red"}]

execute if data storage mgs:missions game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_use_the_setup_menu_to_select_a_map","color":"red"}]

function mgs:v5.1.0/missions/load_map_from_storage with storage mgs:missions game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_not_found_select_a_valid_map","color":"red"}]

data modify storage mgs:missions game.map set from storage mgs:temp map_load.result

execute unless data storage mgs:missions game.map.respawn_commands if data storage mgs:missions game.map.respawn_command[0] run data modify storage mgs:missions game.map.respawn_commands set from storage mgs:missions game.map.respawn_command
execute unless data storage mgs:missions game.map.respawn_commands if data storage mgs:missions game.map.respawn_command.command run data modify storage mgs:missions game.map.respawn_commands set value []
execute unless data storage mgs:missions game.map.respawn_commands[0] if data storage mgs:missions game.map.respawn_command.command run data modify storage mgs:missions game.map.respawn_commands append from storage mgs:missions game.map.respawn_command
execute unless data storage mgs:missions game.map.respawn_commands run data modify storage mgs:missions game.map.respawn_commands set value []
execute unless data storage mgs:missions game.map.start_commands run data modify storage mgs:missions game.map.start_commands set value []

# Set state to preparing
data modify storage mgs:missions game.state set value "preparing"

# in_game is the opt-in flag, so it stays.
scoreboard players set #mi_timer mgs.data 0
scoreboard players set #mi_total_enemies mgs.data 0
scoreboard players set #mi_has_boundary mgs.data 0
scoreboard players set @a mgs.mi.kills 0
scoreboard players set @a mgs.mi.deaths 0
scoreboard players set @a mgs.mp.spectate_timer 0

# deathCount keeps counting outside games: a lobby death would fire missions/on_respawn the moment the state turns active.
scoreboard players set @a mgs.mp.death_count 0

scoreboard players set @a[scores={mgs.mi.in_game=1}] mgs.mp.team 1
team join mgs.blue @a[scores={mgs.mi.in_game=1}]

tag @a[scores={mgs.mi.in_game=1}] add mgs.give_class_menu

# Baseline for the per-mission kill count.
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mi.kill_base = @s mgs.mi.kill_total

gamemode spectator @a[scores={mgs.mi.in_game=1}]
gamerule immediate_respawn true
gamerule keep_inventory true

gamerule natural_health_regeneration false
scoreboard players set #any_game_active mgs.data 1

# hp_prev comes from the `health` criterion; a player whose score is unset syncs on their first health change.
scoreboard players set @a mgs.last_hit 0
scoreboard players set @a mgs.hp_prev 0
execute as @a run scoreboard players operation @s mgs.hp_prev = @s mgs.health

# Everyone, late joiners included, re-inits at full stamina on their next tick.
scoreboard players set @a mgs.stam_seen 0

# Post effects live in player NBT, so a round that ended badly could still apply them.
execute as @a run function mgs:v5.1.0/player/fx_reset

function mgs:v5.1.0/shared/load_base_coordinates {mode:"missions"}

# Needs 2 points.
execute if data storage mgs:missions game.map.boundaries[0] if data storage mgs:missions game.map.boundaries[1] run scoreboard players set #mi_has_boundary mgs.data 1

execute if score #mi_has_boundary mgs.data matches 1 run function mgs:v5.1.0/shared/load_bounds {mode:"missions"}

execute if score #mi_has_boundary mgs.data matches 1 run function mgs:v5.1.0/shared/forceload_area

# Spectators at the base coordinates while chunks preload.
execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #gm_base_z mgs.data
execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.1.0/shared/tp_to_position with storage mgs:temp _tp

schedule function mgs:v5.1.0/missions/preload_complete 20t

tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate":"mgs.loading_mission_area","color":"yellow"}]

