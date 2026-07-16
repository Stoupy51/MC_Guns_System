
#> mgs:v5.1.0/multiplayer/auto_assign_team
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/start [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/join_game
#			mgs:v5.1.0/multiplayer/gamemodes/tdm/setup [ as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}] ]
#			mgs:v5.1.0/dialogs/multiplayer/setup {"label": ["", "\ud83c\udfc6 ", {"translate": "mgs.score_limit"}], "tooltip": {"translate": "mgs.set_the_score_needed_to_win"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}}, {"label": ["", "\u23f1 ", {"translate": "mgs.time_limit"}], "tooltip": {"translate": "mgs.set_the_match_time_limit"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}}, {"label": ["", "\ud83d\uddfa ", {"translate": "mgs.select_map", "color": "aqua"}], "tooltip": {"translate": "mgs.browse_and_select_a_map"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/map_select"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_game"}}, {"label": {"translate": "mgs.red_team", "color": "red"}, "tooltip": {"translate": "mgs.join_red_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_red"}}, {"label": {"translate": "mgs.blue_team", "color": "blue"}, "tooltip": {"translate": "mgs.join_blue_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_blue"}}, {"label": {"translate": "mgs.auto_team", "color": "yellow"}, "tooltip": {"translate": "mgs.auto_balance_assign"}, "action": {"type": "run_command", "command": "/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.assign_players_to_red_blue_teams"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_multiplayer"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_game_modes_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config/modes"}}}
#

# Count players on each team
execute store result score #red_count mgs.data if entity @a[scores={mgs.mp.team=1}]
execute store result score #blue_count mgs.data if entity @a[scores={mgs.mp.team=2}]

# Exclude self from the count so a player never tips the balance toward their own current team
# (otherwise re-running auto-assign on already-assigned players is unstable and clumps onto one side)
execute if score @s mgs.mp.team matches 1 run scoreboard players remove #red_count mgs.data 1
execute if score @s mgs.mp.team matches 2 run scoreboard players remove #blue_count mgs.data 1

# Assign to team with fewer players (red if tied)
execute if score #red_count mgs.data <= #blue_count mgs.data run function mgs:v5.1.0/multiplayer/join_red
execute if score #red_count mgs.data > #blue_count mgs.data run function mgs:v5.1.0/multiplayer/join_blue

