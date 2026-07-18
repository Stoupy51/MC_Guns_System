
#> mgs:v5.1.0/players/list_zombies
#
# @within	mgs:v5.1.0/players/row_zombies
#			mgs:v5.1.0/dialogs/zombies/setup {"label": ["", "\ud83e\uddec ", {"translate": "mgs.variant"}], "tooltip": {"translate": "mgs.choose_the_zombies_experience"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/zombies/setup/variant"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/stop"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_zombies"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.all_players_join", "color": "green"}], "tooltip": {"translate": "mgs.add_every_online_player_to_the_zombies_game"}, "action": {"type": "run_command", "command": "/execute as @a run function mgs:v5.1.0/players/zb_join"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_zombies_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/join_game"}}], "columns": 2, "exit_action": {"label": ["", "\u25c0 ", {"translate": "mgs.back", "color": "gray"}], "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

# Materialize the online players into a fresh list (mode is set first so append_self can color by status)
data modify storage mgs:temp _plr_mode set value "zombies"
data modify storage mgs:temp _plr_iter set value []
execute as @a run function mgs:v5.1.0/players/append_self

# Base dialog (one row per player, stays open after a pick, Back returns to setup)
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{translate:"mgs.manage_players",color:"dark_green",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.one_row_per_player_click_a_name_to_refresh",color:"gray"}}],actions:[],columns:3,pause:false,after_action:"none",exit_action:{label:["","◀ ",{translate:"mgs.back",color:"gray"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"run_command",command:"/function mgs:v5.1.0/zombies/setup"}}}

# Append one button per player
execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.1.0/players/list_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_players_online",color:"red"},tooltip:{translate:"mgs.nobody_to_manage"},action:{type:"run_command",command:"/function mgs:v5.1.0/zombies/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

