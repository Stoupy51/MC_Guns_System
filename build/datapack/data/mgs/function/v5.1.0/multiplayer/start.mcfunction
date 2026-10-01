
#> mgs:v5.1.0/multiplayer/start
#
# @executed	as the player & at current position
#
# @within	dialog mgs:v5.1.0/multiplayer/setup
#

execute if data storage mgs:multiplayer game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.game_already_in_progress","color":"red"}]
execute if data storage mgs:multiplayer game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.game_already_preparing","color":"red"}]

# Players join a side through Manage Players or + Join.
execute unless entity @a[scores={mgs.mp.in_game=1}] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_players_have_joined_a_team_use_manage_players_first","color":"red"}]

# Check that a map is selected
execute if data storage mgs:multiplayer game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_use_the_setup_menu_to_select_a_map","color":"red"}]

# Load the selected map
function mgs:v5.1.0/multiplayer/load_map_from_storage with storage mgs:multiplayer game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_not_found_select_a_valid_map","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:multiplayer game.map set from storage mgs:temp map_load.result

execute unless data storage mgs:multiplayer game.map.respawn_commands if data storage mgs:multiplayer game.map.respawn_command[0] run data modify storage mgs:multiplayer game.map.respawn_commands set from storage mgs:multiplayer game.map.respawn_command
execute unless data storage mgs:multiplayer game.map.respawn_commands if data storage mgs:multiplayer game.map.respawn_command.command run data modify storage mgs:multiplayer game.map.respawn_commands set value []
execute unless data storage mgs:multiplayer game.map.respawn_commands[0] if data storage mgs:multiplayer game.map.respawn_command.command run data modify storage mgs:multiplayer game.map.respawn_commands append from storage mgs:multiplayer game.map.respawn_command
execute unless data storage mgs:multiplayer game.map.respawn_commands run data modify storage mgs:multiplayer game.map.respawn_commands set value []
execute unless data storage mgs:multiplayer game.map.start_commands run data modify storage mgs:multiplayer game.map.start_commands set value []

# Set state to preparing
data modify storage mgs:multiplayer game.state set value "preparing"

scoreboard players set #red mgs.mp.team 0
scoreboard players set #blue mgs.mp.team 0
scoreboard players set #mp_has_boundary mgs.data 0
scoreboard players set @a mgs.mp.kills 0
scoreboard players set @a mgs.mp.deaths 0
scoreboard players set @a mgs.mp.death_count 0

# Per-match XP for the after-action line; lifetime totals stay.
scoreboard players set @a mgs.mp.xp_session 0

# Cleared here and re-claimed by the gamemode's setup, so S&D or Demolition never inherit a stale claim.
execute store result score #mp_timer mgs.data run data get storage mgs:multiplayer game.time_limit
scoreboard players set #mp_mode_owns_timer mgs.data 0

# FFA joins everyone; otherwise each player's chosen side, auto-assigning those who opted in without one.
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run team join mgs.ffa @a[scores={mgs.mp.in_game=1}]
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1}] if score @s mgs.mp.team matches 1 run team join mgs.red @s
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1}] if score @s mgs.mp.team matches 2 run team join mgs.blue @s
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1}] unless score @s mgs.mp.team matches 1.. run function mgs:v5.1.0/multiplayer/auto_assign_team

tag @a[scores={mgs.mp.in_game=1}] add mgs.give_class_menu

gamemode adventure @a[scores={mgs.mp.in_game=1}]
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:waypoint_receive_range base set 0.0
gamerule immediate_respawn true
gamerule keep_inventory true

scoreboard players set @a mgs.mp.spectate_timer 0

# Disable natural regeneration, enable custom regen system
gamerule natural_health_regeneration false
scoreboard players set #any_game_active mgs.data 1

# Reset per-player regen state (hp_prev seeded from the auto-updated health criterion; a player
# whose criterion score is still unset just misses this seed and syncs on their first health change)
scoreboard players set @a mgs.last_hit 0
scoreboard players set @a mgs.hp_prev 0
execute as @a run scoreboard players operation @s mgs.hp_prev = @s mgs.health

# Reset stamina state so every player re-inits to full on their next stamina tick (also covers late-joiners)
scoreboard players set @a mgs.stam_seen 0

# Post effects are stored in player NBT, so a previous round that ended badly would still be
# applied. Clearing here means nobody starts a game scoped or with a red screen.
execute as @a run function mgs:v5.1.0/player/fx_reset

function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

# Needs 2 points.
execute if data storage mgs:multiplayer game.map.boundaries[0] if data storage mgs:multiplayer game.map.boundaries[1] run scoreboard players set #mp_has_boundary mgs.data 1

execute if score #mp_has_boundary mgs.data matches 1 run function mgs:v5.1.0/shared/load_bounds {mode:"multiplayer"}

function mgs:v5.1.0/shared/summon_oob {mode:"multiplayer"}

function mgs:v5.1.0/multiplayer/summon_spawns

# External datapacks can register maps and classes.
function #mgs:multiplayer/register_maps
function #mgs:multiplayer/register_classes

function #mgs:multiplayer/on_game_start

execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.1.0/multiplayer/gamemodes/ffa/setup
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.1.0/multiplayer/gamemodes/tdm/setup
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.1.0/multiplayer/gamemodes/dom/setup
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.1.0/multiplayer/gamemodes/hp/setup
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.1.0/multiplayer/gamemodes/snd/setup
execute if data storage mgs:multiplayer game{gamemode:"demo"} run function mgs:v5.1.0/multiplayer/gamemodes/demo/setup

# After the entity and setup summons.
execute if data storage mgs:multiplayer game.map.start_commands[0] run function mgs:v5.1.0/shared/run_start_commands {mode:"multiplayer"}

# Score limit and initial timer values for the sidebar.
execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute store result score #timer_sec mgs.data run scoreboard players get #mp_timer mgs.data
scoreboard players operation #timer_sec mgs.data /= #20 mgs.data
execute store result score #timer_min mgs.data run scoreboard players get #timer_sec mgs.data
scoreboard players operation #timer_min mgs.data /= #60 mgs.data
scoreboard players operation #timer_mod mgs.data = #timer_sec mgs.data
scoreboard players operation #timer_mod mgs.data %= #60 mgs.data
scoreboard players operation #timer_tens mgs.data = #timer_mod mgs.data
scoreboard players operation #timer_tens mgs.data /= #10 mgs.data
scoreboard players operation #timer_ones mgs.data = #timer_mod mgs.data
scoreboard players operation #timer_ones mgs.data %= #10 mgs.data

scoreboard objectives add mgs.sidebar dummy
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.1.0/multiplayer/refresh_sidebar_ffa
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.1.0/multiplayer/create_sidebar_team {title:"Team Deathmatch"}
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.1.0/multiplayer/create_sidebar_dom
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.1.0/multiplayer/create_sidebar_hp
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.1.0/multiplayer/create_sidebar_snd
execute if data storage mgs:multiplayer game{gamemode:"demo"} run function mgs:v5.1.0/multiplayer/create_sidebar_demo

# Kills in the tab list.
scoreboard objectives setdisplay list mgs.mp.kills

function mgs:v5.1.0/multiplayer/tp_all_to_spawns

effect give @a[scores={mgs.mp.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.mp.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.mp.in_game=1}] night_vision 25 255 true
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base set 0

# Positive: standard class, negative: custom loadout.
execute as @a[scores={mgs.mp.in_game=1}] at @s unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

# `add 0` initializes unset scores, so the `matches 0` test below can succeed.
scoreboard players add @a mgs.mp.class 0
execute as @a[scores={mgs.mp.in_game=1}] at @s if score @s mgs.mp.class matches 0 if score @s mgs.mp.default matches 1.. run function mgs:v5.1.0/multiplayer/auto_apply_default

# Everyone, so classes can change during prep.
execute as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.1.0/multiplayer/select_class

# For change detection during prep.
execute as @a[scores={mgs.mp.in_game=1}] run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

# Prep lasts 10 s.
schedule function mgs:v5.1.0/multiplayer/end_prep 200t

tellraw @a ["","⚔ ",[{"text":"","color":"gold","bold":true},{"translate":"mgs.preparing"},"! "],{"translate":"mgs.choose_your_class_game_starts_in_10_seconds","color":"yellow"}]

