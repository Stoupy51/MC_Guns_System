
#> mgs:v5.1.0/missions/map_select
#
# @executed	"","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_mission"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/missions/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_mission"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/missions/stop"}},{"label":["","\u2694 ",{"translate":"mgs.classes","color":"aqua"}],"tooltip":{"translate":"mgs.select_your_class"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/select_class"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.add_or_remove_players_from_the_mission"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_missions"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.all_players_join","color":"green"}],"tooltip":{"translate":"mgs.add_every_online_player_to_the_mission"},"action":{"type":"run_command","command":"/execute as @a run function mgs:v5.1.0/players/mi_join"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_mission_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/missions/join_game"}}
#
# @within	mgs:v5.1.0/dialogs/missions/setup {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_missions"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.all_players_join", "color": "green"}], "tooltip": {"translate": "mgs.add_every_online_player_to_the_mission"}, "action": {"type": "run_command", "command": "/execute as @a run function mgs:v5.1.0/players/mi_join"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_mission_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/join_game"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

# Build the base map-select dialog (empty actions), then append one button per map
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🗺 ",{translate:"mgs.select_mission_map",color:"aqua",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_map_to_select_it",color:"gray"}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"run_command",command:"/function mgs:v5.1.0/missions/setup"}}}

# Copy maps list and iterate (select_entry appends one button per map)
data modify storage mgs:temp _map_iter set from storage mgs:maps missions
scoreboard players set #map_idx mgs.data 0
data modify storage mgs:temp _map_select_mode set value "missions"
execute if data storage mgs:temp _map_iter[0] run function mgs:v5.1.0/shared/maps/select_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_mission_maps",color:"red"},tooltip:{translate:"mgs.create_one_in_the_map_editor_first"},action:{type:"run_command",command:"/function mgs:v5.1.0/missions/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

