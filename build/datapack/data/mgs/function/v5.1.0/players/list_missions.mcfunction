
#> mgs:v5.1.0/players/list_missions
#
# @within	mgs:v5.1.0/players/missions_menu as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mi_remove"}}],exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.back_to_player_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_missions"}}}
#

# Materialize the online players into a fresh list (mode is set first so append_self can color by status)
data modify storage mgs:temp _plr_mode set value "missions"
data modify storage mgs:temp _plr_iter set value []
execute as @a run function mgs:v5.1.0/players/append_self

# Base dialog (3-column grid, stays open after a pick, Back returns to setup)
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:[{text:"👥 ",color:"aqua",bold:true}, {translate:"mgs.manage_players"}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.click_a_player_to_assign_them_a_team",color:"gray"}}],actions:[],columns:3,pause:false,after_action:"none",exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.return_to_setup"},action:{type:"show_dialog",dialog:"mgs:missions/setup"}}}

# Append one button per player
execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.1.0/players/list_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage mgs:temp dialog.actions[0] run data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.no_players_online",color:"red"},tooltip:{translate:"mgs.nobody_to_manage"},action:{type:"show_dialog",dialog:"mgs:missions/setup"}}

# Show the completed dialog
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

