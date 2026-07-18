
#> mgs:v5.1.0/zombies/map_select
#
# @executed	"","\ud83e\uddec ",{"translate":"mgs.variant"}],"tooltip":{"translate":"mgs.choose_the_zombies_experience"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/zombies/setup/variant"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/stop"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.add_or_remove_players_from_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_zombies"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.all_players_join","color":"green"}],"tooltip":{"translate":"mgs.add_every_online_player_to_the_zombies_game"},"action":{"type":"run_command","command":"/execute as @a run function mgs:v5.1.0/players/zb_join"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_zombies_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/join_game"}}
#
# @within	mgs:v5.1.0/dialogs/zombies/setup {"label": ["", "\ud83e\uddec ", {"translate": "mgs.variant"}], "tooltip": {"translate": "mgs.choose_the_zombies_experience"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/zombies/setup/variant"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/stop"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_zombies"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.all_players_join", "color": "green"}], "tooltip": {"translate": "mgs.add_every_online_player_to_the_zombies_game"}, "action": {"type": "run_command", "command": "/execute as @a run function mgs:v5.1.0/players/zb_join"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_zombies_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/join_game"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

# Build the base map-select dialog (empty actions), then append one button per map
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","🗺 ",{translate:"mgs.select_zombies_map",color:"dark_green",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_map_to_select_it",color:"gray"}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"run_command",command:"/function mgs:v5.1.0/zombies/setup"}}}

# Copy maps list and iterate (select_entry appends one button per map)
data modify storage mgs:temp _map_iter set from storage mgs:maps zombies
scoreboard players set #map_idx mgs.data 0
data modify storage mgs:temp _map_select_mode set value "zombies"
execute if data storage mgs:temp _map_iter[0] run function mgs:v5.1.0/shared/maps/select_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_zombies_maps",color:"red"},tooltip:{translate:"mgs.create_one_in_the_map_editor_first"},action:{type:"run_command",command:"/function mgs:v5.1.0/zombies/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

