
#> mgs:v5.1.0/players/list_missions
#
# @within	mgs:v5.1.0/players/row_missions
#			mgs:v5.1.0/dialogs/missions/setup {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_missions"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.all_players_join", "color": "green"}], "tooltip": {"translate": "mgs.add_every_online_player_to_the_mission"}, "action": {"type": "run_command", "command": "/execute as @a run function mgs:v5.1.0/players/mi_join"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_mission_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/join_game"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

# Materialize the online players into a fresh list (mode is set first so append_self can color by status)
data modify storage mgs:temp _plr_mode set value "missions"
data modify storage mgs:temp _plr_iter set value []
execute as @a run function mgs:v5.1.0/players/append_self

# Base dialog (one row per player, stays open after a pick, Back returns to setup)
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{translate:"mgs.manage_players",color:"aqua",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.one_row_per_player_click_a_name_to_refresh",color:"gray"}}],actions:[],columns:3,pause:false,after_action:"none",exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"run_command",command:"/function mgs:v5.1.0/missions/setup"}}}

# Append one button per player
execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.1.0/players/list_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_players_online",color:"red"},tooltip:{translate:"mgs.nobody_to_manage"},action:{type:"run_command",command:"/function mgs:v5.1.0/missions/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

