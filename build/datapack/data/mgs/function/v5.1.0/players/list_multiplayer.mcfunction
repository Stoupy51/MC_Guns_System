
#> mgs:v5.1.0/players/list_multiplayer
#
# @within	mgs:v5.1.0/players/row_multiplayer
#			mgs:v5.1.0/dialogs/multiplayer/setup {"label": ["", "\ud83c\udfc6 ", {"translate": "mgs.score_limit"}], "tooltip": {"translate": "mgs.set_the_score_needed_to_win"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}}, {"label": ["", "\u23f1 ", {"translate": "mgs.time_limit"}], "tooltip": {"translate": "mgs.set_the_match_time_limit"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}}, {"label": ["", "\ud83d\uddfa ", {"translate": "mgs.select_map", "color": "aqua"}], "tooltip": {"translate": "mgs.browse_and_select_a_map"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/map_select"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_game"}}, {"label": {"translate": "mgs.red_team", "color": "red"}, "tooltip": {"translate": "mgs.join_red_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_red"}}, {"label": {"translate": "mgs.blue_team", "color": "blue"}, "tooltip": {"translate": "mgs.join_blue_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_blue"}}, {"label": {"translate": "mgs.auto_team", "color": "yellow"}, "tooltip": {"translate": "mgs.auto_balance_across_red_blue_in_ffa_seats_everyone_on_the_single"}, "action": {"type": "run_command", "command": "/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.assign_players_to_red_blue_teams"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_multiplayer"}}], "columns": 2, "exit_action": {"label": ["", "\u25c0 ", {"translate": "mgs.back", "color": "gray"}], "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

# Materialize the online players into a fresh list (mode is set first so append_self can color by status)
data modify storage mgs:temp _plr_mode set value "multiplayer"
data modify storage mgs:temp _plr_iter set value []
execute as @a run function mgs:v5.1.0/players/append_self

# Base dialog (one row per player, stays open after a pick, Back returns to setup)
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{translate:"mgs.manage_players",color:"gold",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.one_row_per_player_click_a_name_to_refresh",color:"gray"}}],actions:[],columns:4,pause:false,after_action:"none",exit_action:{label:["","◀ ",{translate:"mgs.back",color:"gray"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"run_command",command:"/function mgs:v5.1.0/multiplayer/setup"}}}

# Append one button per player
execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.1.0/players/list_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_players_online",color:"red"},tooltip:{translate:"mgs.nobody_to_manage"},action:{type:"run_command",command:"/function mgs:v5.1.0/multiplayer/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

