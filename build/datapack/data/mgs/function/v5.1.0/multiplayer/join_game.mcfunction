
#> mgs:v5.1.0/multiplayer/join_game
#
# @within	mgs:v5.1.0/players/mp_to_red
#			mgs:v5.1.0/players/mp_to_blue
#			mgs:v5.1.0/dialogs/multiplayer/setup {"label": ["", "\ud83c\udfc6 ", {"translate": "mgs.score_limit"}], "tooltip": {"translate": "mgs.set_the_score_needed_to_win"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}}, {"label": ["", "\u23f1 ", {"translate": "mgs.time_limit"}], "tooltip": {"translate": "mgs.set_the_match_time_limit"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}}, {"label": ["", "\ud83d\uddfa ", {"translate": "mgs.select_map", "color": "aqua"}], "tooltip": {"translate": "mgs.browse_and_select_a_map"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/map_select"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_game"}}, {"label": {"translate": "mgs.red_team", "color": "red"}, "tooltip": {"translate": "mgs.join_red_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_red"}}, {"label": {"translate": "mgs.blue_team", "color": "blue"}, "tooltip": {"translate": "mgs.join_blue_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_blue"}}, {"label": {"translate": "mgs.auto_team", "color": "yellow"}, "tooltip": {"translate": "mgs.auto_balance_across_red_blue_in_ffa_seats_everyone_on_the_single"}, "action": {"type": "run_command", "command": "/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.assign_players_to_red_blue_teams"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_multiplayer"}}], "columns": 2, "exit_action": {"label": ["", "\u25c0 ", {"translate": "mgs.back", "color": "gray"}], "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

# Require an active game
execute unless data storage mgs:multiplayer game{state:"active"} unless data storage mgs:multiplayer game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_game_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.mp.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_game","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.mp.in_game 1
scoreboard players set @s mgs.mp.kills 0
scoreboard players set @s mgs.mp.deaths 0
scoreboard players set @s mgs.mp.death_count 0
scoreboard players set @s mgs.mp.spectate_timer 0
scoreboard players set @s mgs.last_hit 0
execute store result score @s mgs.hp_prev run data get entity @s Health 1

# Assign to FFA team for ffa mode, otherwise auto-assign to team
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run team join mgs.ffa @s
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} unless score @s mgs.mp.team matches 1.. run function mgs:v5.1.0/multiplayer/auto_assign_team

# Setup player
gamemode adventure @s

attribute @s minecraft:waypoint_receive_range base set 0.0

# Reset stamina so the stamina system re-inits this player at full (it owns the hunger bar)
scoreboard players set @s mgs.stam_seen 0

# Enable class menu and show class selection
tag @s add mgs.give_class_menu
function mgs:v5.1.0/multiplayer/select_class

# Apply class if already chosen
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

# Teleport to spawn
function mgs:v5.1.0/multiplayer/respawn_tp

# Call map join script (executed as the joining player)
function mgs:v5.1.0/shared/maps/call_join_script_at_base

# Announce
tellraw @a ["",{"selector":"@s","color":"yellow"},[{"text":" ","color":"yellow"}, {"translate":"mgs.joined_the_game"}]]

