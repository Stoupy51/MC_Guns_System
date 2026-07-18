
#> mgs:v5.1.0/multiplayer/start
#
# @executed	"","\ud83c\udfc6 ",{"translate":"mgs.score_limit"}],"tooltip":{"translate":"mgs.set_the_score_needed_to_win"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}},{"label":["","\u23f1 ",{"translate":"mgs.time_limit"}],"tooltip":{"translate":"mgs.set_the_match_time_limit"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}},{"label":["","\ud83d\uddfa ",{"translate":"mgs.select_map","color":"aqua"}],"tooltip":{"translate":"mgs.browse_and_select_a_map"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/map_select"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/stop"}},{"label":["","\u2694 ",{"translate":"mgs.classes","color":"aqua"}],"tooltip":{"translate":"mgs.select_your_class"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/select_class"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_game"}},{"label":{"translate":"mgs.red_team","color":"red"},"tooltip":{"translate":"mgs.join_red_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_red"}},{"label":{"translate":"mgs.blue_team","color":"blue"},"tooltip":{"translate":"mgs.join_blue_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_blue"}},{"label":{"translate":"mgs.auto_team","color":"yellow"},"tooltip":{"translate":"mgs.auto_balance_across_red_blue_in_ffa_seats_everyone_on_the_single"},"action":{"type":"run_command","command":"/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.assign_players_to_red_blue_teams"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_multiplayer"}}
#
# @within	mgs:v5.1.0/dialogs/multiplayer/setup {"label": ["", "\ud83c\udfc6 ", {"translate": "mgs.score_limit"}], "tooltip": {"translate": "mgs.set_the_score_needed_to_win"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}}, {"label": ["", "\u23f1 ", {"translate": "mgs.time_limit"}], "tooltip": {"translate": "mgs.set_the_match_time_limit"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}}, {"label": ["", "\ud83d\uddfa ", {"translate": "mgs.select_map", "color": "aqua"}], "tooltip": {"translate": "mgs.browse_and_select_a_map"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/map_select"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_game"}}, {"label": {"translate": "mgs.red_team", "color": "red"}, "tooltip": {"translate": "mgs.join_red_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_red"}}, {"label": {"translate": "mgs.blue_team", "color": "blue"}, "tooltip": {"translate": "mgs.join_blue_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_blue"}}, {"label": {"translate": "mgs.auto_team", "color": "yellow"}, "tooltip": {"translate": "mgs.auto_balance_across_red_blue_in_ffa_seats_everyone_on_the_single"}, "action": {"type": "run_command", "command": "/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.assign_players_to_red_blue_teams"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_multiplayer"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

# Prevent starting if already active or preparing
execute if data storage mgs:multiplayer game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.game_already_in_progress","color":"red"}]
execute if data storage mgs:multiplayer game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.game_already_preparing","color":"red"}]

# Require at least one opted-in player (players are independent until assigned via Manage Players / + Join)
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

# Teams setup
team add mgs.red
team modify mgs.red color red
team modify mgs.red friendlyFire false
team modify mgs.red nametagVisibility hideForOtherTeams
team add mgs.blue
team modify mgs.blue color blue
team modify mgs.blue friendlyFire false
team modify mgs.blue nametagVisibility hideForOtherTeams
team add mgs.ffa
team modify mgs.ffa color yellow
team modify mgs.ffa friendlyFire true
team modify mgs.ffa nametagVisibility never

# Reset scores
scoreboard players set #red mgs.mp.team 0
scoreboard players set #blue mgs.mp.team 0
scoreboard players set #mp_has_boundary mgs.data 0
scoreboard players set @a mgs.mp.kills 0
scoreboard players set @a mgs.mp.deaths 0
scoreboard players set @a mgs.mp.death_count 0

# Set timer from time_limit
execute store result score #mp_timer mgs.data run data get storage mgs:multiplayer game.time_limit

# Assign vanilla teams to opted-in players only: FFA joins everyone; otherwise honor each player's
# chosen side (set via Manage Players), auto-assigning anyone who opted in without picking a team.
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run team join mgs.ffa @a[scores={mgs.mp.in_game=1}]
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1}] if score @s mgs.mp.team matches 1 run team join mgs.red @s
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1}] if score @s mgs.mp.team matches 2 run team join mgs.blue @s
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} as @a[scores={mgs.mp.in_game=1}] unless score @s mgs.mp.team matches 1.. run function mgs:v5.1.0/multiplayer/auto_assign_team

# Enable class menu for multiplayer players
tag @a[scores={mgs.mp.in_game=1}] add mgs.give_class_menu

# Set all in-game players to adventure and enable instant respawn
gamemode adventure @a[scores={mgs.mp.in_game=1}]
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:waypoint_receive_range base set 0.0
gamerule immediate_respawn true
gamerule keep_inventory true

# Reset spectate timers
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

# Store base coordinates for offset
function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

# Detect whether this map defines a boundary (needs 2 points)
execute if data storage mgs:multiplayer game.map.boundaries[0] if data storage mgs:multiplayer game.map.boundaries[1] run scoreboard players set #mp_has_boundary mgs.data 1

# Normalize and store boundaries only when they exist
execute if score #mp_has_boundary mgs.data matches 1 run function mgs:v5.1.0/shared/load_bounds {mode:"multiplayer"}

# Summon out-of-bounds markers
function mgs:v5.1.0/shared/summon_oob {mode:"multiplayer"}

# Summon spawn point markers (for smart spawn selection)
function mgs:v5.1.0/multiplayer/summon_spawns

# Call register hooks (external datapacks can set up maps/classes)
function #mgs:multiplayer/register_maps
function #mgs:multiplayer/register_classes

# Signal game start
function #mgs:multiplayer/on_game_start

# Run gamemode-specific setup
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.1.0/multiplayer/gamemodes/ffa/setup
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.1.0/multiplayer/gamemodes/tdm/setup
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.1.0/multiplayer/gamemodes/dom/setup
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.1.0/multiplayer/gamemodes/hp/setup
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.1.0/multiplayer/gamemodes/snd/setup

# Run map-defined start commands after entity/setup summons
execute if data storage mgs:multiplayer game.map.start_commands[0] run function mgs:v5.1.0/shared/run_start_commands {mode:"multiplayer"}

# Store score limit and compute initial timer values for sidebar
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

# Create sidebar HUD
scoreboard objectives add mgs.sidebar dummy
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.1.0/multiplayer/create_sidebar_ffa
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.1.0/multiplayer/create_sidebar_team {title:"Team Deathmatch"}
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.1.0/multiplayer/create_sidebar_dom
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.1.0/multiplayer/create_sidebar_hp
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.1.0/multiplayer/create_sidebar_team {title:"Search & Destroy"}

# Show kills in player list (tab)
scoreboard objectives setdisplay list mgs.mp.kills

# Teleport players to spawn points
function mgs:v5.1.0/multiplayer/tp_all_to_spawns

# Freeze all players (no movement during prep)
effect give @a[scores={mgs.mp.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.mp.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.mp.in_game=1}] night_vision 25 255 true
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base set 0

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a[scores={mgs.mp.in_game=1}] at @s unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set
# (add 0 initializes unset scores so the 'matches 0' check below can succeed)
scoreboard players add @a mgs.mp.class 0
execute as @a[scores={mgs.mp.in_game=1}] at @s if score @s mgs.mp.class matches 0 if score @s mgs.mp.default matches 1.. run function mgs:v5.1.0/multiplayer/auto_apply_default

# Show class selection dialog to EVERYONE (so they can change during prep)
execute as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.1.0/multiplayer/select_class

# Store current class for change detection during prep
execute as @a[scores={mgs.mp.in_game=1}] run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

# Schedule end of prep (10 seconds = 200 ticks)
schedule function mgs:v5.1.0/multiplayer/end_prep 200t

# Announce
tellraw @a ["","⚔ ",[{"text":"","color":"gold","bold":true},{"translate":"mgs.preparing"},"! "],{"translate":"mgs.choose_your_class_game_starts_in_10_seconds","color":"yellow"}]

