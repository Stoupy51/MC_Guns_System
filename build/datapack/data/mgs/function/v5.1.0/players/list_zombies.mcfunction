
#> mgs:v5.1.0/players/list_zombies
#
# @within	mgs:v5.1.0/dialogs/config/players {"label": ["", "\ud83e\udddf ", {"translate": "mgs.zombies_players", "color": "green"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_zombies"}}, {"label": ["", "\ud83c\udfaf ", {"translate": "mgs.mission_players", "color": "gold"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_missions"}}], "columns": 1, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_configuration"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#			mgs:v5.1.0/players/zombies_menu as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/zb_remove"}}],exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.back_to_player_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_zombies"}}}
#			mgs:v5.1.0/dialogs/zombies/setup {"label": ["", "\ud83e\uddec ", {"translate": "mgs.variant"}], "tooltip": {"translate": "mgs.choose_the_zombies_experience"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/zombies/setup/variant"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/stop"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_zombies"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_zombies_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/join_game"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_game_modes_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config/modes"}}}
#

# Materialize the online players into a fresh list (mode is set first so append_self can color by status)
data modify storage mgs:temp _plr_mode set value "zombies"
data modify storage mgs:temp _plr_iter set value []
execute as @a run function mgs:v5.1.0/players/append_self

# Base dialog (3-column grid, stays open after a pick, Back returns to setup)
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{translate:"mgs.manage_players",color:"dark_green",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_player_to_assign_them_a_team",color:"gray"}}],actions:[],columns:3,pause:false,after_action:"none",exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"run_command",command:"/function mgs:v5.1.0/zombies/setup"}}}

# Append one button per player
execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.1.0/players/list_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_players_online",color:"red"},tooltip:{translate:"mgs.nobody_to_manage"},action:{type:"run_command",command:"/function mgs:v5.1.0/zombies/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

